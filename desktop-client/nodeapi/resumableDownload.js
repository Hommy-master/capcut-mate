const path = require("path");
const axios = require("axios");
const { createWriteStream } = require("fs");
const fs = require("fs").promises;
const logger = require("./logger");

/** 等待响应头的时间，与原 axios timeout 对齐 */
const HEADER_TIMEOUT_MS = 30000;
/** 传输过程中无数据则中断，便于上层重试续传；不限制总下载时长 */
const STREAM_IDLE_TIMEOUT_MS = 60000;
/** 小于该尺寸的半成品不值得发 Range，按整文件重下 */
const MIN_PARTIAL_SIZE = 1024;

const DEFAULT_HEADERS = {
  "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
  Accept: "*/*",
  "Accept-Encoding": "identity",
  "Cache-Control": "no-cache",
};

async function getLocalFileSize(filePath) {
  if (!filePath) return 0;
  try {
    const st = await fs.stat(filePath);
    return st.isFile() ? st.size : 0;
  } catch {
    return 0;
  }
}

function parseContentRange(contentRange) {
  if (!contentRange) return { start: null, end: null, total: null };
  const match = /^bytes\s+(?:(\d+)-(\d+)|\*)\/(\d+|\*)$/i.exec(
    String(contentRange).trim()
  );
  if (!match) return { start: null, end: null, total: null };
  return {
    start: match[1] != null ? Number(match[1]) : null,
    end: match[2] != null ? Number(match[2]) : null,
    total: match[3] === "*" ? null : Number(match[3]),
  };
}

function parseContentLength(headers) {
  const raw = headers?.["content-length"];
  if (raw == null || raw === "") return null;
  const n = Number(raw);
  return Number.isFinite(n) ? n : null;
}

function destroyStream(stream) {
  if (!stream) return;
  try {
    stream.destroy();
  } catch {
    // ignore
  }
}

async function requestDownloadStream(fileUrl, headers) {
  const controller = new AbortController();
  const headerTimer = setTimeout(() => controller.abort(), HEADER_TIMEOUT_MS);
  try {
    return await axios({
      method: "GET",
      url: fileUrl,
      responseType: "stream",
      timeout: 0,
      maxContentLength: Infinity,
      maxBodyLength: Infinity,
      maxRedirects: 5,
      decompress: false,
      signal: controller.signal,
      headers,
      validateStatus: (status) =>
        status === 200 || status === 206 || status === 416,
    });
  } catch (error) {
    if (error.code === "ERR_CANCELED" || error.name === "CanceledError" || error.name === "AbortError") {
      throw new Error("[error] download stream error: header timeout");
    }
    throw error;
  } finally {
    clearTimeout(headerTimer);
  }
}

function writeStreamToFile(readable, filePath, { flags, startSize, expectedSize }) {
  return new Promise((resolve, reject) => {
    const writer = createWriteStream(filePath, { flags, mode: 0o666 });
    let received = startSize;
    let settled = false;
    let idleTimer;

    const cleanup = () => {
      clearTimeout(idleTimer);
    };

    const fail = (err) => {
      if (settled) return;
      settled = true;
      cleanup();
      destroyStream(readable);
      writer.destroy();
      reject(err);
    };

    const resetIdle = () => {
      clearTimeout(idleTimer);
      idleTimer = setTimeout(() => {
        fail(new Error("[error] download stream error: idle timeout"));
      }, STREAM_IDLE_TIMEOUT_MS);
    };

    resetIdle();

    readable.on("data", (chunk) => {
      received += chunk.length;
      resetIdle();
    });

    writer.on("close", () => {
      if (settled) return;
      cleanup();
      if (expectedSize != null && received !== expectedSize) {
        settled = true;
        reject(
          new Error(
            `[error] download stream error: incomplete file ${received}/${expectedSize}`
          )
        );
        return;
      }
      settled = true;
      resolve(received);
    });

    writer.on("error", (err) => {
      fail(new Error(`[error] write file failed: ${err.message}`));
    });

    readable.on("error", (err) => {
      fail(new Error(`[error] download stream error: ${err.message}`));
    });

    readable.pipe(writer);
  });
}

async function moveIfNeeded(fromPath, toPath) {
  if (!toPath || path.normalize(fromPath) === path.normalize(toPath)) {
    return fromPath;
  }
  await fs.mkdir(path.dirname(toPath), { recursive: true });
  await fs.unlink(toPath).catch(() => {});
  await fs.rename(fromPath, toPath);
  return toPath;
}

async function finalizeDestPath(filePath, responseHeaders, resolveDestPath) {
  if (typeof resolveDestPath !== "function") return filePath;
  const finalPath = resolveDestPath(responseHeaders);
  if (!finalPath) return filePath;
  return moveIfNeeded(filePath, finalPath);
}

/**
 * 下载二进制资源：有半成品且服务端返回 206 时断点续传；
 * 服务端忽略 Range 返回 200 时回退为整文件覆盖（原下载模式）。
 * 中断时保留半成品，供上层重试接着下。
 *
 * @param {string} fileUrl
 * @param {{ destPath: string, resolveDestPath?: (headers: object) => string, requestHeaders?: object }} options
 * @returns {Promise<string>} 最终文件路径
 */
async function downloadBinaryToFile(fileUrl, options = {}) {
  const { destPath, resolveDestPath = null, requestHeaders = {} } = options;
  if (!destPath) {
    throw new Error("[error] download dest path is required");
  }

  const targetPath = destPath;
  const existingSize = await getLocalFileSize(targetPath);
  const canResume = existingSize >= MIN_PARTIAL_SIZE;

  const headers = {
    ...DEFAULT_HEADERS,
    ...requestHeaders,
    Accept: "*/*",
    "Accept-Encoding": "identity",
    "Cache-Control": "no-cache",
  };

  if (canResume) {
    headers.Range = `bytes=${existingSize}-`;
    logger.info(`[log] resume download from byte ${existingSize}: ${fileUrl}`);
  }

  const response = await requestDownloadStream(fileUrl, headers);

  await fs.mkdir(path.dirname(targetPath), { recursive: true });

  if (response.status === 416) {
    const total = parseContentRange(response.headers["content-range"]).total;
    destroyStream(response.data);
    const size = await getLocalFileSize(targetPath);
    if (total != null && size === total) {
      logger.info(`[log] local file already complete: ${targetPath}`);
      return finalizeDestPath(targetPath, response.headers, resolveDestPath);
    }
    await fs.unlink(targetPath).catch(() => {});
    throw new Error(
      "[error] download stream error: range not satisfiable, will restart"
    );
  }

  if (response.status !== 200 && response.status !== 206) {
    destroyStream(response.data);
    throw new Error(
      `[error] [stream] request failed, status code: ${response.status}`
    );
  }

  const contentRange = parseContentRange(response.headers["content-range"]);
  const contentLength = parseContentLength(response.headers);
  const rangeStart = contentRange.start;
  const rangeMatches =
    rangeStart == null || rangeStart === existingSize;

  let flags = "w";
  let startSize = 0;
  let expectedSize = contentLength;

  if (response.status === 206 && canResume && rangeMatches) {
    flags = "a";
    startSize = existingSize;
    expectedSize = contentRange.total;
    logger.info(
      `[log] server supports resume (HTTP 206), append to ${targetPath}`
    );
  } else if (response.status === 206 && !canResume && (rangeStart == null || rangeStart === 0)) {
    expectedSize = contentRange.total ?? contentLength;
    logger.info(`[log] received HTTP 206 from byte 0, write full file: ${targetPath}`);
  } else if (response.status === 206) {
    destroyStream(response.data);
    await fs.unlink(targetPath).catch(() => {});
    throw new Error(
      "[error] download stream error: resume offset mismatch, will restart"
    );
  } else {
    expectedSize = contentLength;
    if (canResume) {
      logger.warn(
        `[warn] server does not support resume (HTTP 200), fallback to full download: ${fileUrl}`
      );
    }
  }

  logger.info(`[log] start create writable stream: ${targetPath}`);
  await writeStreamToFile(response.data, targetPath, {
    flags,
    startSize,
    expectedSize,
  });
  return finalizeDestPath(targetPath, response.headers, resolveDestPath);
}

module.exports = {
  downloadBinaryToFile,
};
