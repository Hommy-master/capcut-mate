const path = require("path");
const axios = require("axios");
const { app, dialog, shell } = require("electron");
const { createWriteStream } = require("fs");
const fs = require("fs").promises; // 使用 fs.promises 进行异步文件操作
const logger = require("./logger");
const { detectJianyingDraftRoot } = require("./draftPathDetect");
const { v4: uuidv4 } = require('uuid');

const RECORD_MAX = 500;

const LOG_MAX = 2000;

const axiosConfig = {
  method: "GET",
  timeout: 30000, // 30秒超时
  headers: {
    // 添加常见的浏览器User-Agent
    "User-Agent":
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
  },
};

function isHttpUrl(value) {
  if (!value || typeof value !== "string") return false;
  try {
    const parsed = new URL(value);
    return parsed.protocol === "http:" || parsed.protocol === "https:";
  } catch {
    return false;
  }
}

function inferMaterialSubDir(materialType, material) {
  if (materialType === "audios") return "audios";
  if (materialType === "videos") {
    return material?.type === "photo" ? "images" : "videos";
  }
  return "misc";
}

const MIME_TO_EXT = {
  "image/jpeg": ".jpg",
  "image/jpg": ".jpg",
  "image/png": ".png",
  "image/gif": ".gif",
  "image/webp": ".webp",
  "image/bmp": ".bmp",
  "video/mp4": ".mp4",
  "video/quicktime": ".mov",
  "audio/mpeg": ".mp3",
  "audio/mp3": ".mp3",
  "audio/wav": ".wav",
  "audio/x-wav": ".wav",
};

function inferExtFromContentType(contentType, fallbackExt = ".bin") {
  if (!contentType || typeof contentType !== "string") {
    return fallbackExt;
  }
  const mime = contentType.split(";")[0].trim().toLowerCase();
  const ext = MIME_TO_EXT[mime];
  return ext || fallbackExt;
}

function buildMaterialFilename(baseName, ext) {
  return baseName.toLowerCase().endsWith(ext.toLowerCase()) ? baseName : `${baseName}${ext}`;
}

const IMAGE_EXTENSIONS = new Set([
  ".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".heic", ".jpe",
]);
const VIDEO_EXTENSIONS = new Set([
  ".mp4", ".mov", ".avi", ".mkv", ".webm", ".m4v", ".flv",
]);
const AUDIO_EXTENSIONS = new Set([
  ".mp3", ".wav", ".aac", ".m4a", ".flac", ".ogg", ".wma",
]);

/** 除图片/视频/音频外均视为配置文件 */
function classifyDraftFile(filePath) {
  const normalized = String(filePath).replace(/\\/g, "/").toLowerCase();
  if (normalized.includes("/assets/images/")) return "image";
  if (normalized.includes("/assets/videos/")) return "video";
  if (normalized.includes("/assets/audios/")) return "audio";

  const ext = path.extname(filePath).toLowerCase();
  if (IMAGE_EXTENSIONS.has(ext)) return "image";
  if (VIDEO_EXTENSIONS.has(ext)) return "video";
  if (AUDIO_EXTENSIONS.has(ext)) return "audio";
  return "config";
}

function materialSubDirToCategory(subDir) {
  if (subDir === "images") return "image";
  if (subDir === "videos") return "video";
  if (subDir === "audios") return "audio";
  return "config";
}

function buildFileLogMessage(phase, category, sourceUrl) {
  const kind = category === "config" ? "配置" : "资源";
  if (phase === "loading") {
    return `${kind} ${sourceUrl} 下载中...`;
  }
  if (phase === "success") {
    return `${kind} ${sourceUrl} 下载完成`;
  }
  return `${kind} ${sourceUrl} 下载失败`;
}

function createDownloadProgressTracker(targetId) {
  let seq = 0;
  const stats = {
    image: 0,
    video: 0,
    audio: 0,
    config: 0,
    success: 0,
    failure: 0,
  };

  return {
    beginFile(sourceUrl, category) {
      stats[category] += 1;
      return {
        id: `file-${targetId}-${++seq}-${sourceUrl}`,
        category,
        sourceUrl,
      };
    },
    recordSuccess() {
      stats.success += 1;
    },
    recordFailure() {
      stats.failure += 1;
    },
    buildSummaryMessage() {
      const total = stats.image + stats.video + stats.audio + stats.config;
      return `下载完成：共${total}个文件，图片：${stats.image}个，视频：${stats.video}个，音频：${stats.audio}个，配置：${stats.config}个，成功${stats.success}个，失败${stats.failure}个`;
    },
    get failureCount() {
      return stats.failure;
    },
    get totalCount() {
      return stats.image + stats.video + stats.audio + stats.config;
    },
  };
}

async function logFileDownloadStatus(parentWindow, logMeta, phase) {
  const level =
    phase === "loading" ? "loading" : phase === "success" ? "success" : "error";
  await upsertDownloadLog(
    {
      id: logMeta.id,
      level,
      message: buildFileLogMessage(phase, logMeta.category, logMeta.sourceUrl),
    },
    parentWindow
  );
}

function extractFileNameFromUrl(fileUrl) {
  try {
    return path.basename(new URL(fileUrl).pathname) || "未知文件";
  } catch {
    return "未知文件";
  }
}

async function markFileDownloadFailed(parentWindow, tracker, sourceUrl) {
  const category = classifyDraftFile(extractFileNameFromUrl(sourceUrl));
  const logMeta = tracker.beginFile(sourceUrl, category);
  await logFileDownloadStatus(parentWindow, logMeta, "error");
  tracker.recordFailure();
}

async function downloadRemoteMaterial(fileUrl, draftRootDir, subDir, baseName, fallbackExt) {
  const response = await axios({
    ...axiosConfig,
    url: fileUrl,
    responseType: "stream",
  });
  if (response.status !== 200) {
    throw new Error(`[error] [material] request failed, status code: ${response.status}`);
  }

  const ext = inferExtFromContentType(response.headers["content-type"], fallbackExt);
  const fileName = buildMaterialFilename(baseName, ext);
  const localPath = path.join(draftRootDir, "assets", subDir, fileName);

  await fs.mkdir(path.dirname(localPath), { recursive: true });
  const writer = response.data.pipe(createWriteStream(localPath, { flags: "w", mode: 0o666 }));
  await new Promise((resolve, reject) => {
    writer.on("close", resolve);
    writer.on("error", (err) => {
      fs.unlink(localPath).catch(() => { });
      reject(err);
    });
    response.data.on("error", (err) => {
      writer.destroy();
      fs.unlink(localPath).catch(() => { });
      reject(err);
    });
  });
  return localPath;
}

function sanitizeFilename(value) {
  if (!value || typeof value !== "string") return "";
  return value.replace(/[\\/:*?"<>|]/g, "_").trim();
}

/**
 * Windows 上“权限异常”多与只读属性有关；Node 对文件的 fs.chmod(0o666) 会清除只读位。
 * 下载完成后统一处理，避免 copyFile / 外部软件间歇性带上只读导致剪映无法改写素材。
 */
async function ensureWindowsDraftFilesWritable(rootDir) {
  if (process.platform !== "win32" || !rootDir) return;
  const stack = [rootDir];
  while (stack.length) {
    const current = stack.pop();
    let entries;
    try {
      entries = await fs.readdir(current, { withFileTypes: true });
    } catch {
      continue;
    }
    for (const ent of entries) {
      const full = path.join(current, ent.name);
      if (ent.isSymbolicLink()) continue;
      try {
        if (ent.isDirectory()) {
          stack.push(full);
        } else if (ent.isFile()) {
          await fs.chmod(full, 0o666);
        }
      } catch (e) {
        logger.warn(`[perm] 无法调整文件权限（已跳过）: ${full} — ${e.message}`);
      }
    }
  }
}

const MAX_DOWNLOAD_ATTEMPTS = 6;

/** 拉取 get_draft：首次请求 + 2 次重试（共 3 次），自开始起硬截止 3000ms 内必须结束 */
const GET_DRAFT_FETCH_MAX_ATTEMPTS = 3;
const GET_DRAFT_FETCH_DEADLINE_MS = 3000;
const GET_DRAFT_FETCH_PER_ATTEMPT_MAX_MS = 800;
const GET_DRAFT_FETCH_BACKOFF_MS = [120, 200];

/** 网关/限流等暂时不可用，退避重试有效（不含 500 等通常表示持久故障的状态） */
const RETRYABLE_TRANSIENT_HTTP_STATUSES = new Set([408, 429, 502, 503, 504]);

/** 限流/网关错误退避：1s 起指数增长，上限 30s */
const TRANSIENT_HTTP_BACKOFF_MS = [1000, 2000, 4000, 8000, 16000];
const TRANSIENT_HTTP_BACKOFF_MAX_MS = 30000;

/** 网络/流错误默认固定退避 */
const DEFAULT_RETRY_DELAY_MS = 1000;

/** 从 axios 错误或手动抛出的 Error 消息中解析 HTTP 状态码 */
function getHttpStatusFromError(error) {
  if (error?.response?.status != null) {
    return error.response.status;
  }
  const match = /status code:\s*(\d+)/i.exec(String(error?.message || ""));
  return match ? Number.parseInt(match[1], 10) : null;
}

function isTransientHttpError(error) {
  const status = getHttpStatusFromError(error);
  return status !== null && RETRYABLE_TRANSIENT_HTTP_STATUSES.has(status);
}

/** 解析 Retry-After（秒或 HTTP 日期），返回毫秒；无法解析时返回 null */
function parseRetryAfterMs(headers) {
  if (!headers) return null;
  const raw = headers["retry-after"] ?? headers["Retry-After"];
  if (raw == null || raw === "") return null;

  const asSeconds = Number(raw);
  if (Number.isFinite(asSeconds) && asSeconds >= 0) {
    return Math.min(asSeconds * 1000, TRANSIENT_HTTP_BACKOFF_MAX_MS);
  }

  const retryAt = Date.parse(String(raw));
  if (Number.isFinite(retryAt)) {
    return Math.min(Math.max(0, retryAt - Date.now()), TRANSIENT_HTTP_BACKOFF_MAX_MS);
  }
  return null;
}

/**
 * 计算下次重试前的等待时间。
 * @param {unknown} error 本次失败错误
 * @param {number} failedAttempt 已失败的尝试序号（1-based）
 */
function getRetryDelayMs(error, failedAttempt) {
  const retryAfterMs = parseRetryAfterMs(error?.response?.headers);
  if (retryAfterMs != null) {
    return retryAfterMs;
  }

  if (isTransientHttpError(error)) {
    const idx = Math.min(Math.max(failedAttempt - 1, 0), TRANSIENT_HTTP_BACKOFF_MS.length - 1);
    return Math.min(
      TRANSIENT_HTTP_BACKOFF_MS[idx] ?? TRANSIENT_HTTP_BACKOFF_MS.at(-1),
      TRANSIENT_HTTP_BACKOFF_MAX_MS
    );
  }

  return DEFAULT_RETRY_DELAY_MS;
}

/**
 * 判断下载错误是否值得重试。
 * - HTTP：408 / 429 / 502 / 503 / 504 可重试（限流/网关暂时不可用）；404 等 4xx 及 500 等不重试
 * - 网络：DNS 失败、连接拒绝不重试；超时、连接重置等可重试
 * - 流写入/读取中断可重试
 */
function isRetryableDownloadError(error) {
  if (!error) return false;

  const status = getHttpStatusFromError(error);
  if (status !== null) {
    return RETRYABLE_TRANSIENT_HTTP_STATUSES.has(status);
  }

  const code = error.code;
  if (code === "ENOTFOUND" || code === "ECONNREFUSED") return false;
  if (
    code === "ECONNABORTED" ||
    code === "ETIMEDOUT" ||
    code === "ECONNRESET" ||
    code === "EAI_AGAIN"
  ) {
    return true;
  }

  const message = String(error.message || "");
  if (/write file failed|download stream error/i.test(message)) {
    return true;
  }

  if (!error.response && code) return true;

  return false;
}

async function requestGetDraftOnce(remoteUrl, timeoutMs) {
  return axios({
    ...axiosConfig,
    url: remoteUrl,
    responseType: "json",
    timeout: timeoutMs,
  });
}

async function fetchGetDraftWithRetry(remoteUrl) {
  const deadline = Date.now() + GET_DRAFT_FETCH_DEADLINE_MS;
  const timeLeftMs = () => deadline - Date.now();
  let lastError = null;

  for (let attempt = 1; attempt <= GET_DRAFT_FETCH_MAX_ATTEMPTS; attempt++) {
    if (timeLeftMs() <= 0) break;

    if (attempt > 1) {
      const baseBackoff = GET_DRAFT_FETCH_BACKOFF_MS[attempt - 2] ?? 100;
      const planned = isTransientHttpError(lastError)
        ? Math.max(baseBackoff, getRetryDelayMs(lastError, attempt - 1))
        : baseBackoff;
      const wait = Math.min(planned, Math.max(0, timeLeftMs() - 1));
      if (wait > 0) {
        await new Promise((resolve) => setTimeout(resolve, wait));
      }
      if (timeLeftMs() <= 0) break;
    }

    const timeout = Math.min(
      GET_DRAFT_FETCH_PER_ATTEMPT_MAX_MS,
      Math.max(1, timeLeftMs())
    );

    try {
      return await requestGetDraftOnce(remoteUrl, timeout);
    } catch (error) {
      lastError = error;
      const willRetry =
        attempt < GET_DRAFT_FETCH_MAX_ATTEMPTS &&
        timeLeftMs() > 0 &&
        isRetryableDownloadError(error);
      if (willRetry) {
        logger.warn(
          `[warn] get draft url attempt ${attempt}/${GET_DRAFT_FETCH_MAX_ATTEMPTS} failed: ${error.message}`
        );
        continue;
      }
      throw error;
    }
  }

  throw lastError;
}

async function retryDownloadTask(task, options = {}) {
  const {
    maxAttempts = MAX_DOWNLOAD_ATTEMPTS,
    retryDelayMs = null,
    isRetryableError = isRetryableDownloadError,
    onAttempt = null,
    onRetry = null,
    onExhausted = null,
  } = options;

  let lastError = null;
  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      if (typeof onAttempt === "function") {
        await onAttempt(attempt, maxAttempts);
      }
      return await task(attempt, maxAttempts);
    } catch (error) {
      lastError = error;
      const hasNextAttempt = attempt < maxAttempts;
      const canRetry = hasNextAttempt && isRetryableError(error);

      if (!canRetry) {
        if (hasNextAttempt) {
          logger.warn(
            `[warn] download error is not retryable (attempt ${attempt}/${maxAttempts}): ${error?.message || error}`
          );
        } else if (typeof onExhausted === "function") {
          await onExhausted(error, attempt, maxAttempts);
        }
        throw error;
      }

      const delayMs =
        retryDelayMs != null ? retryDelayMs : getRetryDelayMs(error, attempt);

      if (typeof onRetry === "function") {
        await onRetry(error, attempt, maxAttempts, delayMs);
      }
      if (delayMs > 0) {
        if (isTransientHttpError(error)) {
          logger.warn(
            `[warn] transient HTTP ${getHttpStatusFromError(error)}, retry in ${delayMs}ms (attempt ${attempt}/${maxAttempts})`
          );
        }
        await new Promise((resolve) => setTimeout(resolve, delayMs));
      }
    }
  }

  throw lastError || new Error("retryDownloadTask failed without explicit error");
}

async function downloadOneRemoteMaterial(
  item,
  materialType,
  draftRootDir,
  cache,
  parentWindow,
  tracker
) {
  const subDir = inferMaterialSubDir(materialType, item);
  const category = materialSubDirToCategory(subDir);
  const fallbackExt = materialType === "audios" ? ".mp3" : ".mp4";
  const baseName = sanitizeFilename(item.material_name || item.name || item.id || uuidv4());
  const sourceUrl = item.path;

  const logMeta = tracker.beginFile(sourceUrl, category);

  try {
    await logFileDownloadStatus(parentWindow, logMeta, "loading");
    let localPath;
    await retryDownloadTask(
      async () => {
        localPath = await downloadRemoteMaterial(
          sourceUrl,
          draftRootDir,
          subDir,
          baseName,
          fallbackExt
        );
      },
      {
        onRetry: async (err, attempt) => {
          logger.warn(
            `[warn] 下载URL素材失败，准备重试(${attempt}/${MAX_DOWNLOAD_ATTEMPTS}): ${sourceUrl}`,
            err?.message || err
          );
        },
      }
    );
    cache.set(sourceUrl, localPath);
    item.path = localPath;
    await logFileDownloadStatus(parentWindow, logMeta, "success");
    tracker.recordSuccess();
  } catch (err) {
    await logFileDownloadStatus(parentWindow, logMeta, "error");
    tracker.recordFailure();
    logger.error(`[error] 下载URL素材失败，已达到重试上限: ${sourceUrl}`, err);
    item.path = cache.get(sourceUrl) || item.path;
  }
}

async function localizeRemoteMaterialPaths(
  materials,
  draftRootDir,
  parentWindow,
  sharedCache = null,
  tracker = null
) {
  if (!materials || typeof materials !== "object") return;
  const supportedTypes = ["videos", "audios"];
  const cache = sharedCache instanceof Map ? sharedCache : new Map();
  const pendingDownloads = [];
  const inFlightByUrl = new Map();

  for (const materialType of supportedTypes) {
    const list = materials[materialType];
    if (!Array.isArray(list)) continue;
    for (let i = 0; i < list.length; i++) {
      const item = list[i];
      if (!item || typeof item !== "object") continue;
      if (!isHttpUrl(item.path)) continue;

      const sourceUrl = item.path;

      if (cache.has(sourceUrl)) {
        item.path = cache.get(sourceUrl);
        continue;
      }

      if (inFlightByUrl.has(sourceUrl)) {
        pendingDownloads.push(
          inFlightByUrl.get(sourceUrl).then((localPath) => {
            item.path = localPath;
          })
        );
        continue;
      }

      let downloadTask;
      if (!tracker) {
        downloadTask = (async () => {
          try {
            const subDir = inferMaterialSubDir(materialType, item);
            const fallbackExt = materialType === "audios" ? ".mp3" : ".mp4";
            const baseName = sanitizeFilename(
              item.material_name || item.name || item.id || uuidv4()
            );
            const localPath = await downloadRemoteMaterial(
              sourceUrl,
              draftRootDir,
              subDir,
              baseName,
              fallbackExt
            );
            cache.set(sourceUrl, localPath);
            return localPath;
          } catch (err) {
            logger.error(`[error] 下载URL素材失败: ${sourceUrl}`, err);
            return cache.get(sourceUrl) || sourceUrl;
          }
        })();
      } else {
        downloadTask = downloadOneRemoteMaterial(
          item,
          materialType,
          draftRootDir,
          cache,
          parentWindow,
          tracker
        ).then(() => cache.get(sourceUrl) || item.path);
      }

      inFlightByUrl.set(sourceUrl, downloadTask);
      pendingDownloads.push(
        downloadTask.then((localPath) => {
          item.path = localPath;
        })
      );
    }
  }

  if (pendingDownloads.length > 0) {
    await Promise.all(pendingDownloads);
  }
}

function getConfigPath() {
  return path.join(app.getPath("userData"), "app-config.json");
}

async function readConfig() {
  const configPath = getConfigPath();
  logger.info("[log] Config path:", configPath);
  try {
    const data = await fs.readFile(configPath, "utf8");
    return JSON.parse(data) || {};
  } catch (error) {
    return {};
  }
}

async function writeConfig(config) {
  const configPath = getConfigPath();
  try {
    await fs.writeFile(configPath, JSON.stringify(config, null, 2), "utf8");
    return true;
  } catch (error) {
    logger.error("写入配置文件失败:", error);
    return false;
  }
}

/**
 * 未配置草稿路径时，按平台规则自动探测并写入配置。
 */
async function ensureAutoDetectedDraftPathInConfig() {
  let config = await readConfig();
  if (config.targetDirectory) {
    return config;
  }
  const detected = await detectJianyingDraftRoot();
  if (detected) {
    config.targetDirectory = detected;
    await writeConfig(config);
    logger.info("[draft-detect] 已自动识别剪映草稿目录:", detected);
  }
  return config;
}

function getDownloadLogPath() {
  return path.join(app.getPath("userData"), "download-log.json");
}

async function readDownloadLog() {
  const logPath = getDownloadLogPath();
  logger.info("[log] Log path:", logPath);
  try {
    const data = await fs.readFile(logPath, "utf8");
    return JSON.parse(data);
  } catch (error) {
    return [];
  }
}

/**
 *
 * @param {*} entry {time: Date, level: 'error', message: '日志内容' }
 */
async function appendDownloadLog(entry, parentWindow) {
  const logPath = getDownloadLogPath();
  let logs = [];
  try {
    logs = await readDownloadLog();
  } catch (error) {
    // 如果文件不存在或无法读取，初始化为空数组
    logs = [];
  }

  entry.time = new Date();
  console.log(`appendDownloadLog: ${JSON.stringify(entry)}`);
  await parentWindow.webContents.send("file-operation-log", {
    ...entry,
    action: "append",
  });
  logs.push(entry);
  if (logs.length > LOG_MAX) {
    logs.shift();
  }
  try {
    await fs.writeFile(logPath, JSON.stringify(logs, null, 2), "utf8");
  } catch (writeErr) {
    logger.error("写入日志文件失败:", writeErr);
  }
}

/**
 * 按 id 追加或更新日志（用于草稿下载状态：正在下载 → 下载完成）
 * @param {*} entry { id, level, message }
 */
async function upsertDownloadLog(entry, parentWindow) {
  if (!entry?.id) {
    return appendDownloadLog(entry, parentWindow);
  }

  const logPath = getDownloadLogPath();
  let logs = [];
  try {
    logs = await readDownloadLog();
  } catch {
    logs = [];
  }

  const now = new Date();
  const existingIndex = logs.findIndex((item) => item.id === entry.id);
  const storedEntry =
    existingIndex >= 0
      ? { ...logs[existingIndex], ...entry, time: now }
      : { ...entry, time: now };

  if (existingIndex >= 0) {
    logs[existingIndex] = storedEntry;
  } else {
    logs.push(storedEntry);
  }

  if (logs.length > LOG_MAX) {
    logs.shift();
  }

  console.log(`upsertDownloadLog: ${JSON.stringify(storedEntry)}`);
  await parentWindow.webContents.send("file-operation-log", {
    ...storedEntry,
    action: existingIndex >= 0 ? "update" : "append",
  });

  try {
    await fs.writeFile(logPath, JSON.stringify(logs, null, 2), "utf8");
  } catch (writeErr) {
    logger.error("写入日志文件失败:", writeErr);
  }
}

async function clearDownloadLog() {
  const logPath = getDownloadLogPath();
  try {
    await fs.writeFile(logPath, JSON.stringify([], null, 2), "utf8");
    return true;
  } catch (error) {
    logger.error("清空日志文件失败:", error);
    return false;
  }
}

function getHistoryRecordPath() {
  return path.join(app.getPath("userData"), "history-record.json");
}

async function readHistoryRecord() {
  const recordPath = getHistoryRecordPath();
  console.info("[History] Record path:", recordPath);
  try {
    const data = await fs.readFile(recordPath, "utf8");
    return JSON.parse(data);
  } catch (error) {
    return [];
  }
}

/**
 *
 * @param {*} entry {id: 'uuid', time: Date, draft_id: 'draft_id' draft_url: 'draft_url' }
 */
async function appendHistoryRecord(entry) {
  const recordPath = getHistoryRecordPath();
  let records = [];
  try {
    records = await readHistoryRecord();
  } catch (error) {
    // 如果文件不存在或无法读取，初始化为空数组
    records = [];
  }

  console.log(`appendHistoryRecord: ${JSON.stringify(entry)}`);
  records.push(entry);
  if (records.length > RECORD_MAX) {
    records.shift();
  }
  try {
    await fs.writeFile(recordPath, JSON.stringify(records, null, 2), "utf8");
  } catch (writeErr) {
    console.error("写入草稿历史记录文件失败:", writeErr);
  }
}

// 更精确的错误处理
function errorHandler(error = {}, url = "") {
  if (error.code === "ECONNREFUSED") {
    throw new Error(`[error] not connect to server: ${url}`);
  } else if (error.code === "ENOTFOUND") {
    throw new Error(`[error] domain not found: ${url}`);
  } else if (error.response) {
    // 服务器返回了错误状态码（如4xx, 5xx）
    throw new Error(`[error] server error (${error.response.status}): ${url}`);
  } else {
    throw error; // 重新抛出其他未知错误
  }
}

async function getDraftUrls(remoteUrl, parentWindow) {
  logger.info("[info] get draft url");
  try {
    const response = await fetchGetDraftWithRetry(remoteUrl);

    // 检查HTTP状态码
    if (response.status !== 200) {
      await appendDownloadLog(
        { level: "error", message: `获取草稿地址信息失败` },
        parentWindow
      );
      throw new Error(
        `[error] [draft url] request failed, status code: ${response.status}`
      );
    }
    logger.info("[success] get draft url");
    return response.data;
  } catch (error) {
    errorHandler(error, remoteUrl);
  }
}

async function updateDraftPath(parentWindow) {
  const targetDir = await getTargetDirectory(parentWindow, true);
  if (!targetDir) {
    return { success: false, error: "用户取消了目录选择" };
  }
  try {
    // 验证目录权限
    try {
      await fs.access(targetDir, fs.constants.R_OK | fs.constants.W_OK);
    } catch (accessError) {
      logger.error('所选目录无读写权限:', accessError);
      // 尝试使用 dialog 显示错误消息
      if (parentWindow) {
        const { dialog } = require('electron');
        await dialog.showMessageBox(parentWindow, {
          type: 'error',
          title: '权限不足',
          message: '所选目录没有足够的读写权限，请选择其他目录。',
          buttons: ['确定']
        });
      }
      return { success: false, error: '所选目录没有足够的读写权限' };
    }

    const configPath = getConfigPath();
    let config = {};

    // 尝试读取现有配置
    try {
      const data = await fs.readFile(configPath, "utf8");
      config = JSON.parse(data);
    } catch (error) {
      // 如果文件不存在，保持config为空对象
    }

    config.targetDirectory = targetDir;

    // 写回配置文件
    await fs.writeFile(configPath, JSON.stringify(config, null, 2), 'utf8');
    logger.info('默认草稿路径已更新为:', targetDir);
    return { success: true, targetDir };
  } catch (error) {
    logger.error('更新默认草稿路径失败:', error);
    return { success: false, error: error.message };
  }
}

// 提取出来的函数，可选参数parentWindow用于显示对话框时附加到对话框
async function getTargetDirectory(parentWindow = null, isUpdate = false) {
  let config = await readConfig();
  if (!isUpdate && config.targetDirectory) {
    try {
      await fs.access(config.targetDirectory, fs.constants.R_OK | fs.constants.W_OK);
      return config.targetDirectory;
    } catch (accessErr) {
      logger.warn(
        "配置的目录已不存在或无访问权限，将清除并尝试自动识别或手动选择。",
        accessErr.message
      );
      delete config.targetDirectory;
      await writeConfig(config);
    }
  }

  if (!isUpdate) {
    config = await ensureAutoDetectedDraftPathInConfig();
    if (config.targetDirectory) {
      try {
        await fs.access(config.targetDirectory, fs.constants.R_OK | fs.constants.W_OK);
        return config.targetDirectory;
      } catch (e) {
        logger.warn("自动识别的草稿目录不可读写，将打开目录选择:", e.message);
        delete config.targetDirectory;
        await writeConfig(config);
      }
    }
  }

  const dialogOptions = {
    properties: ["openDirectory", "createDirectory"], // 允许创建新目录
    title: "请选择目标目录",
    buttonLabel: "选择此目录",
    defaultPath: isUpdate ? config.targetDirectory : undefined
  };

  // 如果有父窗口，则附加到父窗口
  if (parentWindow) {
    dialogOptions.window = parentWindow;
  }

  const result = await dialog.showOpenDialog(dialogOptions);

  if (!result.canceled && result.filePaths.length > 0) {
    const selectedDir = result.filePaths[0];
    
    // 再次验证目录权限
    try {
      await fs.access(selectedDir, fs.constants.R_OK | fs.constants.W_OK);
    } catch (accessErr) {
      logger.error('所选目录无读写权限:', accessErr);
      if (parentWindow) {
        const { dialog } = require('electron');
        await dialog.showMessageBox(parentWindow, {
          type: 'error',
          title: '权限不足',
          message: '所选目录没有足够的读写权限，请重新选择。',
          buttons: ['确定']
        });
      }
      return ''; // 返回空字符串表示失败
    }
    
    config.targetDirectory = selectedDir;
    await writeConfig(config);
    return selectedDir;
  } else {
    return '';
  }
}

function updateValue(current, finalKey, targetDir, oldVal, targetId) {
  if (oldVal) {
    // 找到ID在路径中的位置
    const idIndex = oldVal.indexOf(targetId);
    if (idIndex === -1) return;

    // 提取ID及之后的部分作为将要下载的路径
    const relativePath = oldVal.substring(idIndex).replaceAll("/", path.sep); // 替换为系统路径分隔符
    // targetDir 已包含 targetId 目录，所以relativePath中的targetId要去重
    const newRelativePath = relativePath.replace(`${targetId}${path.sep}`, "");
    const newValue = path.join(targetDir, newRelativePath);
    current[finalKey] = newValue;

    logger.info(`✅ newValue to:`, newValue);
  }
}

// 递归遍历对象，更新所有名为path的属性
function recursivelyUpdatePaths(obj, targetDir, targetId) {
  // 处理数组
  if (Array.isArray(obj)) {
    obj.forEach((item) => {
      recursivelyUpdatePaths(item, targetDir, targetId);
    });
    return;
  }

  // 处理对象
  if (obj && typeof obj === "object") {
    // 检查是否有path属性
    if (obj.path && typeof obj.path === "string") {
      updateValue(obj, "path", targetDir, obj.path, targetId);
    }

    // 递归处理所有属性
    for (const key in obj) {
      if (obj.hasOwnProperty(key)) {
        recursivelyUpdatePaths(obj[key], targetDir, targetId);
      }
    }
  }
}

// 带错误处理的JSON文件下载
async function downloadJsonFile(
  { fileUrl, filePath, targetDir, targetId, materialDownloadCache, tracker },
  parentWindow
) {
  // 1. 使用 Axios 下载 JSON 文件
  try {
    const response = await axios({
      method: "GET",
      url: fileUrl,
      responseType: "json", // 直接告诉 Axios 解析 JSON
    });

    // 检查HTTP状态码
    if (response.status !== 200) {
      throw new Error(
        `[error] [json] request failed, status code: ${response.status}`
      );
    }

    // 2. 解析获取到的数据（Axios 会根据 responseType: 'json' 自动解析）
    const jsonData = response.data;

    // 3. 修改 JSON 数据中指定键的值
    if (jsonData?.materials) {
      logger.info(`[log] start modifyJsonValue: materials`);
      recursivelyUpdatePaths(jsonData.materials, targetDir, targetId);
      // 当素材 path 为 URL 时，下载到本地并回写为本地路径。
      await localizeRemoteMaterialPaths(
        jsonData.materials,
        targetDir,
        parentWindow,
        materialDownloadCache,
        tracker
      );
    }

    // 4. 将修改后的 JSON 对象转换为格式化的字符串并写入本地文件
    const jsonString = JSON.stringify(jsonData, null, 2); // 使用 2 个空格进行缩进，美化输出
    await fs.writeFile(filePath, jsonString, { encoding: "utf8", mode: 0o666 });
  } catch (error) {
    logger.error(`下载JSON文件失败: ${fileUrl}`, error);
    throw error;
  }
}

async function downloadNotJsonFile(
  { fileUrl, filePath, targetDir },
  parentWindow
) {
  try {
    // 1. 使用 Axios 下载非 JSON 文件
    const response = await axios({
      ...axiosConfig,
      url: fileUrl,
      responseType: "stream", // 设置响应类型为 'stream' 以处理大文件
    });

    // 检查HTTP状态码
    if (response.status !== 200) {
      throw new Error(
        `[error] [stream] request failed, status code: ${response.status}`
      );
    }

    logger.info(`[log] start create writable stream: ${filePath}`);

    // 创建可写流
    // 显式指定 flags 和 mode，避免 Windows 下文件句柄共享模式异常
    const writer = response.data.pipe(createWriteStream(filePath, { flags: "w", mode: 0o666 }));

    return new Promise((resolve, reject) => {
      // 监听 close 而非 finish：finish 仅表示数据写完，close 才表示文件句柄已释放
      // 在 Windows 上，句柄未释放时其他进程访问该文件会出现权限异常（EACCES）
      writer.on("close", resolve);
      writer.on("error", (err) => {
        // 尝试删除可能不完整的文件
        fs.unlink(filePath).catch(() => { });
        reject(new Error(`[error] write file failed: ${err.message}`));
      });
      response.data.on("error", (err) => {
        reject(new Error(`[error] download stream error: ${err.message}`));
      });
    });
  } catch (error) {
    logger.error(`下载非JSON文件失败: ${fileUrl}`, error);
    // 不使用errorHandler，直接抛出错误以便上层进行重试
    throw error;
  }
}

/**
 * 下载单个文件并保存到指定路径的辅助函数
 * @param {string} url 远程文件的URL
 * @param {string} filePath 要保存到的本地文件路径
 */
async function downloadSingleFile(config, parentWindow) {
  const filePath = config.filePath;
  const fileUrl = config.fileUrl;
  const fileName = path.basename(filePath);

  // 已知 draft_content.json 与 draft_info.json 内容一致时，直接复用，避免重复构建与重复下载 URL 素材。
  if (fileName === "draft_info.json") {
    const contentFilePath = path.join(path.dirname(filePath), "draft_content.json");
    try {
      await fs.access(contentFilePath, fs.constants.R_OK);
      await fs.copyFile(contentFilePath, filePath);
      logger.info(`[log] draft_info.json 直接复用 draft_content.json: ${filePath}`);
      return;
    } catch {
      // draft_content.json 不存在时回退到原逻辑，保证兼容。
    }
  }

  if (fileUrl.endsWith(".json")) {
    logger.info(`[log] start download json file : ${filePath}`);
    await downloadJsonFile(config, parentWindow);
  } else {
    logger.info(`[log] start download non-json file : ${filePath}`);
    await downloadNotJsonFile(config, parentWindow);
  }
}

/**
 * 触发目录扫描，激活剪映的目录发现机制
 * 原理：将草稿目录复制到临时目录，触发文件系统变更通知，让剪映无需重启即可感知到新草稿
 * - Windows：使用 robocopy（内置工具，返回码 0-7 均为成功）
 * - macOS：使用 rsync（触发 FSEvents 变更通知）
 * @param {string} targetDir 草稿目录路径
 */
async function triggerDirectoryScan(targetDir) {
  if (!targetDir) return;

  try {
    await fs.access(targetDir);
  } catch {
    // 目录不存在则跳过
    return;
  }

  const tmpDir = targetDir + ".tmp";
  const { execFile } = require("child_process");
  const platform = process.platform;

  await new Promise((resolve) => {
    if (platform === "win32") {
      // Windows：使用 robocopy 触发 ReadDirectoryChangesW 通知
      const args = [
        targetDir,
        tmpDir,
        "/E",        // 递归复制所有子目录
        "/COPY:DAT", // 复制数据、属性和时间戳（无需管理员权限）
        "/R:1",      // 失败重试1次
        "/W:1",      // 重试等待1秒
        "/NP",       // 不显示进度百分比
        "/NJH",      // 不显示作业头
        "/NJS",      // 不显示作业摘要
      ];
      execFile("robocopy", args, { windowsHide: true }, (err) => {
        // robocopy 返回码 0-7 均表示成功或正常状态，8+ 才是错误
        const code = err ? err.code : 0;
        if (typeof code === "number" && code >= 8) {
          logger.warn(`[scan] Windows 触发目录扫描失败，robocopy 返回码: ${code}`);
        } else {
          logger.info(`[scan] Windows 触发目录扫描完成，robocopy 返回码: ${code}`);
        }
        resolve();
      });
    } else if (platform === "darwin") {
      // macOS：使用 rsync 触发 FSEvents 变更通知
      // -a: 归档模式（递归+保留属性），触发目录写入事件
      execFile("rsync", ["-a", targetDir + "/", tmpDir], (err) => {
        if (err) {
          logger.warn(`[scan] macOS 触发目录扫描失败: ${err.message}`);
        } else {
          logger.info(`[scan] macOS 触发目录扫描完成`);
        }
        resolve();
      });
    } else {
      logger.info(`[scan] 当前平台 ${platform} 不支持触发目录扫描，跳过`);
      resolve();
    }
  });

  // 清理临时目录
  try {
    await fs.rm(tmpDir, { recursive: true, force: true });
  } catch (e) {
    logger.warn(`[scan] 清理临时目录失败 ${tmpDir}: ${e.message}`);
  }
}

// 打开目录
async function openDraftDirectory(dirPath) {
  try {
    const errorMsg = await shell.openPath(dirPath);
    if (errorMsg) {
      logger.error(`[error] Failed to open path: ${errorMsg}`);
      return { success: false, error: errorMsg };
    }
    return { success: true };
  } catch (error) {
    logger.error(`[error] Error opening path: ${error}`);
    return { success: false, error: error.message };
  }
}

// 获取目标文件路径
// 解析URL并创建必要的目录结构
async function getTargetFilePath(fileUrl, baseTargetDir, targetId) {
  const urlObj = new URL(fileUrl);
  let fullPath = urlObj.pathname;

  // 找到ID在路径中的位置
  const idIndex = fullPath.indexOf(targetId);
  if (idIndex === -1) return null;

  // 提取ID及之后的部分作为将要下载的路径
  const relativePath = fullPath.substring(idIndex).replaceAll("/", path.sep); // 替换为系统路径分隔符
  const fullTargetPath = path.join(baseTargetDir, relativePath);
  const targetDir = path.dirname(fullTargetPath);

  logger.info("[log] fullTargetPath: " + fullTargetPath);
  logger.info("[log] targetDir: " + targetDir);

  // 确保目标目录存在
  try {
    await fs.mkdir(targetDir, { recursive: true }); // recursive: true 可以创建多级目录
  } catch (mkdirError) {
    logger.error(`创建目录失败: ${targetDir}`, mkdirError);
    throw mkdirError;
  }

  return { fullTargetPath, targetDir };
}

// 带重试机制的单个文件下载
async function downloadFileWithRetry(config, parentWindow, tracker) {
  const category = classifyDraftFile(config.filePath);
  const logMeta = tracker.beginFile(config.fileUrl, category);

  try {
    await logFileDownloadStatus(parentWindow, logMeta, "loading");
    await retryDownloadTask(
      async () => {
        await downloadSingleFile(config, parentWindow);
      },
      {
        onAttempt: async (attempt, maxAttempts) => {
          logger.info(
            `[log] start get file context : ${config.fileUrl}, attempt: ${attempt}/${maxAttempts}`
          );
        },
        onRetry: async (error, attempt, maxAttempts) => {
          logger.error(
            `[error] download file ${config.fileUrl} failed (attempt ${attempt}/${maxAttempts}):`,
            error
          );
        },
        onExhausted: async (error, attempt, maxAttempts) => {
          logger.error(
            `[error] download file ${config.fileUrl} exhausted retries (attempt ${attempt}/${maxAttempts}):`,
            error
          );
        },
      }
    );

    await logFileDownloadStatus(parentWindow, logMeta, "success");
    tracker.recordSuccess();
    logger.info(`[log] file saved to : ${config.filePath}`);
    return true;
  } catch {
    await logFileDownloadStatus(parentWindow, logMeta, "error");
    tracker.recordFailure();
    return false;
  }
}

function yieldToRenderer() {
  return new Promise((resolve) => setImmediate(resolve));
}

// 批量下载文件主函数
async function downloadFiles(
  { sourceUrl, remoteFileUrls, targetId, isOpenDir },
  parentWindow
) {
  try {
    let baseTargetDir = "";
    // 然后获取目标目录，将主窗口作为父窗口传递
    try {
      baseTargetDir = await getTargetDirectory(parentWindow);
    } catch (error) {
      logger.error("[log] get target dir fail:", error);
      baseTargetDir = '';
    }

    if (!baseTargetDir) {
      await appendDownloadLog(
        { level: "error", message: `获取目录失败` },
        parentWindow
      );
      return;
    }

    logger.info("[log] get target dir:", baseTargetDir);

    const draftLogId = `draft-${targetId}`;
    const tracker = createDownloadProgressTracker(targetId);

    await upsertDownloadLog(
      {
        id: draftLogId,
        level: "loading",
        message: `正在下载草稿 ${targetId}`,
      },
      parentWindow
    );

    const materialDownloadCache = new Map();

    // 2. 遍历远程文件URL数组
    for (let i = 0; i < remoteFileUrls.length; i++) {
      const fileUrl = remoteFileUrls[i];

      try {
        // 获取目标文件路径
        const targetPaths = await getTargetFilePath(fileUrl, baseTargetDir, targetId);

        if (!targetPaths) {
          logger.error(`[error] 无法获取文件的目标路径: ${fileUrl}`);
          await markFileDownloadFailed(parentWindow, tracker, fileUrl);
          continue;
        }

        const { fullTargetPath, targetDir } = targetPaths;

        await downloadFileWithRetry(
          {
            fileUrl,
            filePath: fullTargetPath,
            targetDir,
            targetId,
            materialDownloadCache,
            tracker,
          },
          parentWindow,
          tracker
        );
      } catch (error) {
        logger.error(`[error] 处理文件时发生错误:`, error);
        await markFileDownloadFailed(parentWindow, tracker, fileUrl);
      }
    }

    // 等待渲染进程处理已发送的资源日志，再标记草稿完成，避免 UI 仍显示「下载中」
    await yieldToRenderer();

    const failureCount = tracker.failureCount;
    const draftCompleteMessage =
      failureCount === 0
        ? `获取草稿 ${targetId} 成功`
        : failureCount === tracker.totalCount && tracker.totalCount > 0
          ? `获取草稿 ${targetId} 失败`
          : `获取草稿 ${targetId} 成功（${failureCount} 个文件失败）`;
    const draftCompleteLevel =
      failureCount === 0
        ? "success"
        : failureCount === tracker.totalCount && tracker.totalCount > 0
          ? "error"
          : "all";

    await upsertDownloadLog(
      {
        id: draftLogId,
        level: draftCompleteLevel,
        message: draftCompleteMessage,
      },
      parentWindow
    );

    const summaryLogId = `summary-${targetId}`;
    await upsertDownloadLog(
      {
        id: summaryLogId,
        level: failureCount === 0 ? "all" : "info",
        message: tracker.buildSummaryMessage(),
      },
      parentWindow
    );

    // {id: 'uuid', time: Date, draft_id: 'draft_id', draft_url: 'draft_url' }
    await appendHistoryRecord({
      id: uuidv4(),
      time: new Date(),
      draft_id: targetId,
      draft_url: sourceUrl,
    });
    const jointPath = path.join(baseTargetDir, targetId);
    logger.info(`[finish] all download: ${jointPath}`);

    await ensureWindowsDraftFilesWritable(jointPath);

    // 触发剪映目录扫描，使剪映无需重启即可识别新草稿
    await triggerDirectoryScan(jointPath);

    if (isOpenDir) await openDraftDirectory(jointPath);
    
    return {
      success: failureCount === 0,
      message: `文件批量保存完成，保存至目录: ${jointPath}，${tracker.buildSummaryMessage()}`,
    };
  } catch (error) {
    logger.error(`[error] 批量保存过程发生错误:`, error);

    await upsertDownloadLog(
      {
        id: `draft-${targetId}`,
        level: "error",
        message: `获取草稿 ${targetId} 失败`,
      },
      parentWindow
    );

    await appendDownloadLog(
      {
        level: "error",
        message: `下载失败：批量保存 ${targetId} 中的剪映草稿过程发生错误！`,
      },
      parentWindow
    );
    return { success: false, message: `保存失败: ${error.message} ` };
  }
}

async function checkUrlAccessRight(url) {
  try {
    const response = await axios({
      ...axiosConfig,
      method: 'HEAD',
      url: url,
      timeout: 5000
    });
    logger.info(`URL Accessibility Check Result: ${url} - ${response.status}`);
    return { accessible: response.status < 400 };
  } catch (error) {
    logger.error(`URL Accessibility Check Failed: ${url}`, error);
    return { accessible: false, error: error.message };
  }
}

module.exports = {
  readDownloadLog,
  clearDownloadLog,

  updateDraftPath,

  readConfig,
  ensureAutoDetectedDraftPathInConfig,

  getDraftUrls,

  downloadFiles,

  checkUrlAccessRight,

  readHistoryRecord,

  inferExtFromContentType,
};
