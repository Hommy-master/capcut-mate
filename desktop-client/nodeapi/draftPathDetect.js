const path = require("path");
const fs = require("fs").promises;
const os = require("os");

/**
 * 延迟加载 logger：logger 依赖 Electron 的 app，纯 Node 单测里无法初始化。
 * 探测逻辑本身与 Electron 无关，这里退化到 console 以保证可单测。
 */
function warnLog(...args) {
  try {
    require("./logger").warn(...args);
  } catch {
    console.warn(...args);
  }
}

/** Windows 下相对用户主目录的剪映草稿根路径后缀 */
const DRAFT_REL_WIN = path.join(
  "AppData",
  "Local",
  "JianyingPro",
  "User Data",
  "Projects",
  "com.lveditor.draft"
);

/** macOS 下相对用户主目录的剪映草稿根路径后缀 */
const DRAFT_REL_MAC = path.join(
  "Movies",
  "JianyingPro",
  "User Data",
  "Projects",
  "com.lveditor.draft"
);

/** 剪映草稿根目录的文件夹名（UUID 风格的固定包名） */
const DRAFT_ROOT_DIR_NAME = "com.lveditor.draft";

/**
 * 目录下存在 root_meta_info.json 或 .recycle_bin 子目录时，
 * 说明它具备剪映草稿根目录的结构特征（不检查读写权限）。
 */
async function hasJianyingDraftMarkers(dir) {
  if (!dir || typeof dir !== "string") return false;
  try {
    const st = await fs.stat(path.join(dir, "root_meta_info.json"));
    if (st.isFile()) return true;
  } catch {
    // ignore
  }
  try {
    const st = await fs.stat(path.join(dir, ".recycle_bin"));
    if (st.isDirectory()) return true;
  } catch {
    // ignore
  }
  return false;
}

/**
 * 目录可读写且存在剪映草稿根目录特征时，认为是剪映草稿根目录。
 */
async function isConfirmedJianyingDraftDir(dir) {
  try {
    await fs.access(dir, fs.constants.R_OK | fs.constants.W_OK);
  } catch {
    return false;
  }
  return hasJianyingDraftMarkers(dir);
}

/**
 * 当前平台的剪映默认草稿根目录（仅用于界面提示，不保证存在）。
 */
function getDefaultDraftRootHint() {
  if (process.platform === "win32") {
    return path.join(os.homedir(), DRAFT_REL_WIN);
  }
  if (process.platform === "darwin") {
    return path.join(os.homedir(), DRAFT_REL_MAC);
  }
  return "";
}

async function detectWindowsDraftPath() {
  const usersDir = path.join(process.env.SystemDrive || "C:", "Users");
  const ordered = [];
  const seen = new Set();
  const push = (p) => {
    const norm = path.normalize(p);
    if (seen.has(norm)) return;
    seen.add(norm);
    ordered.push(norm);
  };

  push(path.join(os.homedir(), DRAFT_REL_WIN));

  try {
    const names = await fs.readdir(usersDir);
    for (const name of names) {
      const userRoot = path.join(usersDir, name);
      try {
        const st = await fs.stat(userRoot);
        if (!st.isDirectory()) continue;
      } catch {
        continue;
      }
      push(path.join(userRoot, DRAFT_REL_WIN));
    }
  } catch (e) {
    warnLog("[draft-detect] Windows Users 目录扫描失败:", e.message);
  }

  for (const dir of ordered) {
    if (await isConfirmedJianyingDraftDir(dir)) {
      return dir;
    }
  }
  return null;
}

async function detectMacDraftPath() {
  const home = os.homedir();
  const candidates = [path.join(home, DRAFT_REL_MAC)];
  for (const dir of candidates) {
    if (await isConfirmedJianyingDraftDir(dir)) return dir;
  }
  return null;
}

/**
 * 按平台自动探测剪映草稿根目录（com.lveditor.draft）。
 * @returns {Promise<string|null>}
 */
async function detectJianyingDraftRoot() {
  if (process.platform === "win32") {
    return detectWindowsDraftPath();
  }
  if (process.platform === "darwin") {
    return detectMacDraftPath();
  }
  return null;
}

/**
 * 从用户选择的目录解析出真正的剪映草稿根目录。
 *
 * 用户经常选中草稿根目录的上级（如 ~/Movies）或某份草稿的子目录，
 * 这里按常见层级向下/向上各找几层，命中则返回：
 *   { path: '<草稿根目录>', corrected: boolean }
 * corrected 为 true 表示选中的不是根目录本身。
 *
 * @param {string} selectedDir
 * @returns {Promise<{path: string, corrected: boolean}|null>}
 */
async function resolveDraftRootFromSelection(selectedDir) {
  if (!selectedDir || typeof selectedDir !== "string") return null;

  if (await hasJianyingDraftMarkers(selectedDir)) {
    return { path: selectedDir, corrected: false };
  }

  // 选中的是草稿根目录的某一级上级
  const nestedCandidates = [
    path.join(selectedDir, DRAFT_ROOT_DIR_NAME),
    path.join(selectedDir, "Projects", DRAFT_ROOT_DIR_NAME),
    path.join(selectedDir, "User Data", "Projects", DRAFT_ROOT_DIR_NAME),
    path.join(selectedDir, "JianyingPro", "User Data", "Projects", DRAFT_ROOT_DIR_NAME),
    path.join(selectedDir, DRAFT_REL_MAC),
    path.join(selectedDir, DRAFT_REL_WIN),
  ];
  for (const dir of nestedCandidates) {
    if (await hasJianyingDraftMarkers(dir)) {
      return { path: dir, corrected: true };
    }
  }

  // 选中的是草稿根目录内部（例如某份草稿文件夹）
  let current = path.dirname(selectedDir);
  for (let depth = 0; depth < 4; depth += 1) {
    const parent = path.dirname(current);
    if (parent === current) break; // 已到文件系统根
    if (await hasJianyingDraftMarkers(current)) {
      return { path: current, corrected: true };
    }
    current = parent;
  }

  return null;
}

module.exports = {
  DRAFT_ROOT_DIR_NAME,
  DRAFT_REL_WIN,
  DRAFT_REL_MAC,
  hasJianyingDraftMarkers,
  isConfirmedJianyingDraftDir,
  getDefaultDraftRootHint,
  detectJianyingDraftRoot,
  resolveDraftRootFromSelection,
};
