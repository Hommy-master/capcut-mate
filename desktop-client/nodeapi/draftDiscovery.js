/**
 * 剪映草稿发现确认。
 *
 * 草稿下载到剪映草稿根目录后，download.js 会触发一次目录扫描，让剪映感知新草稿。
 * 剪映发现草稿后会把草稿登记到草稿根目录下的 root_meta_info.json
 * （all_draft_store 列表）。这里轮询该文件，确认本次下载的草稿确实已被收录；
 * 未收录时用户打开剪映会看不到刚下载的草稿。
 *
 * 只依赖 path/fs，保持可单测；日志由调用方负责。
 */

const path = require("path");
const fs = require("fs").promises;

const ROOT_META_INFO_FILENAME = "root_meta_info.json";

/**
 * 剪映收到目录变更后通常 1~2s 内完成登记，这里留出富余。
 * 超时只表示本次未能确认，不代表剪映之后不会发现（例如剪映尚未启动）。
 */
const DRAFT_DISCOVERY_TIMEOUT_MS = 8000;
const DRAFT_DISCOVERY_POLL_INTERVAL_MS = 500;

/** 统一分隔符并去掉末尾斜杠，便于比较不同来源的同一路径。 */
function normalizePathForCompare(value) {
  if (typeof value !== "string" || !value) return "";
  const posix = value.replace(/\\/g, "/").replace(/\/+$/, "");
  return process.platform === "win32" ? posix.toLowerCase() : posix;
}

function entryMatches(entry, draftDir, realDraftDir, draftId) {
  if (!entry || typeof entry !== "object") return false;

  const foldPath = normalizePathForCompare(entry.draft_fold_path);
  if (foldPath) {
    if (foldPath === normalizePathForCompare(draftDir)) return true;
    if (realDraftDir && foldPath === normalizePathForCompare(realDraftDir)) {
      return true;
    }
  }

  // 路径写法可能不同（软链接/容器路径/相对形式）；下载后 draft_name
  // 与文件夹名一致，可作为兜底。
  return Boolean(draftId) && entry.draft_name === draftId;
}

/**
 * 在 root_meta_info.json 内容中查找已登记的草稿。
 * @param {object} rootMetaInfo root_meta_info.json 解析结果
 * @param {{draftDir?: string, draftId?: string, realDraftDir?: string}} target
 * @returns {object|null} 匹配到的登记项
 */
function findDraftEntry(rootMetaInfo, target = {}) {
  const entries = rootMetaInfo?.all_draft_store;
  if (!Array.isArray(entries)) return null;

  const { draftDir, draftId, realDraftDir } = target;
  for (const entry of entries) {
    if (entryMatches(entry, draftDir, realDraftDir, draftId)) return entry;
  }
  return null;
}

function stripBom(text) {
  return text.charCodeAt(0) === 0xfeff ? text.slice(1) : text;
}

/**
 * 读取根目录下的 root_meta_info.json。
 * @returns {Promise<{ok: true, path: string, data: object}|{ok: false, path: string, reason: 'missing'|'unreadable', error?: Error}>}
 */
async function readRootMetaInfo(draftRootDir) {
  const metaPath = path.join(draftRootDir, ROOT_META_INFO_FILENAME);
  try {
    const raw = await fs.readFile(metaPath, "utf8");
    return { ok: true, path: metaPath, data: JSON.parse(stripBom(raw)) };
  } catch (error) {
    if (error?.code === "ENOENT") {
      return { ok: false, path: metaPath, reason: "missing" };
    }
    // 剪映写入期间可能读到半截 JSON，交由轮询继续重试
    return { ok: false, path: metaPath, reason: "unreadable", error };
  }
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

/**
 * 轮询 root_meta_info.json，确认草稿已被剪映登记。
 *
 * @param {string} draftDir 草稿目录（<草稿根目录>/<draft_id>）
 * @param {object} [options]
 * @param {string} [options.draftRootDir] 草稿根目录，默认取 draftDir 的父目录
 * @param {string} [options.draftId] 草稿 ID，默认取目录名
 * @param {number} [options.timeoutMs]
 * @param {number} [options.pollIntervalMs]
 * @returns {Promise<{
 *   discovered: boolean,
 *   reason: 'found'|'not_listed'|'root_meta_missing'|'root_meta_unreadable',
 *   entry: object|null,
 *   metaPath: string,
 *   elapsedMs: number,
 *   error?: Error
 * }>}
 */
async function waitForDraftDiscovery(draftDir, options = {}) {
  const draftRootDir = options.draftRootDir || path.dirname(draftDir);
  const draftId = options.draftId || path.basename(draftDir);
  const timeoutMs = options.timeoutMs ?? DRAFT_DISCOVERY_TIMEOUT_MS;
  const pollIntervalMs = options.pollIntervalMs ?? DRAFT_DISCOVERY_POLL_INTERVAL_MS;

  const startedAt = Date.now();
  let realDraftDir = null;
  try {
    realDraftDir = await fs.realpath(draftDir);
  } catch {
    // realpath 只用于兼容软链接差异，失败时退回原始路径比较
  }

  let lastRead = null;
  for (;;) {
    lastRead = await readRootMetaInfo(draftRootDir);
    const elapsedMs = Date.now() - startedAt;

    if (lastRead.ok) {
      const entry = findDraftEntry(lastRead.data, {
        draftDir,
        draftId,
        realDraftDir,
      });
      if (entry) {
        return {
          discovered: true,
          reason: "found",
          entry,
          metaPath: lastRead.path,
          elapsedMs,
        };
      }
    } else if (lastRead.reason === "missing") {
      // 没有索引文件说明剪映尚未初始化草稿发现，再等也不会出现登记项
      return {
        discovered: false,
        reason: "root_meta_missing",
        entry: null,
        metaPath: lastRead.path,
        elapsedMs,
      };
    }

    if (elapsedMs >= timeoutMs) {
      return {
        discovered: false,
        reason: lastRead.ok ? "not_listed" : "root_meta_unreadable",
        entry: null,
        metaPath: lastRead.path,
        elapsedMs,
        error: lastRead.error,
      };
    }

    await sleep(Math.min(pollIntervalMs, timeoutMs - elapsedMs));
  }
}

module.exports = {
  ROOT_META_INFO_FILENAME,
  DRAFT_DISCOVERY_TIMEOUT_MS,
  DRAFT_DISCOVERY_POLL_INTERVAL_MS,
  normalizePathForCompare,
  findDraftEntry,
  readRootMetaInfo,
  waitForDraftDiscovery,
};
