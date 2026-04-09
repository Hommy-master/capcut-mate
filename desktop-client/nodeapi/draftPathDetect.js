const path = require("path");
const fs = require("fs").promises;
const os = require("os");
const logger = require("./logger");

/** Windows 下相对用户主目录的剪映草稿根路径后缀 */
const DRAFT_REL_WIN = path.join(
  "AppData",
  "Local",
  "JianyingPro",
  "User Data",
  "Projects",
  "com.lveditor.draft"
);

/**
 * 目录下存在 root_meta_info.json 或 .recycle_bin 子目录时，认为是剪映草稿根目录。
 */
async function isConfirmedJianyingDraftDir(dir) {
  try {
    await fs.access(dir, fs.constants.R_OK | fs.constants.W_OK);
  } catch {
    return false;
  }
  const metaPath = path.join(dir, "root_meta_info.json");
  try {
    const st = await fs.stat(metaPath);
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
    logger.warn("[draft-detect] Windows Users 目录扫描失败:", e.message);
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
  const candidates = [
    path.join(home, "Movies", "CapCut", "User Data", "Projects", "com.lveditor.draft"),
    path.join(home, "Movies", "JianyingPro", "User Data", "Projects", "com.lveditor.draft"),
  ];
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

module.exports = {
  detectJianyingDraftRoot,
};
