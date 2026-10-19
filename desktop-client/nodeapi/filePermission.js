/**
 * 文件系统权限检测（macOS TCC / 通用 EPERM）。
 *
 * macOS 对「影片」「桌面」「文稿」「下载」等用户目录有 TCC 保护：
 * 未授权时真实写入会返回 EPERM / EACCES，但 `fs.access` 仍可能返回成功，
 * 因此这里用「创建临时目录 + 写探针文件」来判断目录是否真的可写。
 *
 * 本模块只依赖 Node 内置模块，便于单测。
 */

const fs = require("fs").promises;
const os = require("os");
const path = require("path");

const PERMISSION_ERROR_CODES = new Set(["EPERM", "EACCES"]);

/** macOS TCC 保护的用户目录 → 中文名称 */
const MAC_PROTECTED_FOLDERS = {
  Desktop: "桌面",
  Documents: "文稿",
  Downloads: "下载",
  Movies: "影片",
  Music: "音乐",
  Pictures: "图片",
};

/** 系统设置中「隐私与安全性」的锚点 */
const PRIVACY_PANES = {
  files: "Privacy_FilesAndFolders",
  "full-disk": "Privacy_AllFiles",
};

function isPermissionError(error) {
  if (!error) return false;
  // 带 HTTP 响应的网络错误不是文件系统权限问题
  if (error.response) return false;
  const code = String(error.code || "");
  if (PERMISSION_ERROR_CODES.has(code)) return true;
  const message = String(error.message || "");
  return /operation not permitted|permission denied|access is denied/i.test(message);
}

/**
 * 判断目录是否位于 macOS 受保护的用户目录下，返回中文目录名（如「影片」）。
 * 不在受保护目录下时返回空字符串。
 */
function getMacProtectedFolderName(targetDir, homeDir = os.homedir()) {
  if (!targetDir || typeof targetDir !== "string") return "";
  if (process.platform !== "darwin") return "";

  const relative = path.relative(homeDir, targetDir);
  if (!relative || relative.startsWith("..") || path.isAbsolute(relative)) {
    return "";
  }
  const topLevel = relative.split(path.sep)[0];
  return MAC_PROTECTED_FOLDERS[topLevel] || "";
}

/**
 * 通过真实写入验证目录可写。
 * 成功时返回 { ok: true }；失败时附带 permissionDenied / code / message。
 * @param {string} targetDir
 */
async function probeWriteAccess(targetDir) {
  if (!targetDir || typeof targetDir !== "string") {
    return {
      ok: false,
      permissionDenied: false,
      code: "EINVAL",
      message: "目标目录为空",
      targetDirectory: targetDir || "",
    };
  }

  let probeDir = "";
  try {
    await fs.mkdir(targetDir, { recursive: true });
    probeDir = await fs.mkdtemp(path.join(targetDir, ".capcut-mate-perm-"));
    await fs.writeFile(path.join(probeDir, "probe"), "ok", {
      encoding: "utf8",
      mode: 0o600,
    });
    return {
      ok: true,
      permissionDenied: false,
      targetDirectory: targetDir,
    };
  } catch (error) {
    return {
      ok: false,
      permissionDenied: isPermissionError(error),
      code: error?.code || "UNKNOWN",
      message: error?.message || String(error),
      targetDirectory: targetDir,
    };
  } finally {
    if (probeDir) {
      try {
        await fs.rm(probeDir, { recursive: true, force: true });
      } catch {
        // 探针清理失败不影响检测结果
      }
    }
  }
}

/**
 * 只读探测目录权限，用于授权弹窗轮询：
 * `readdir` 会触发/反映 macOS TCC 授权状态，但不往草稿目录写任何东西。
 * @param {string} targetDir
 */
async function probeReadAccess(targetDir) {
  if (!targetDir || typeof targetDir !== "string") {
    return {
      ok: false,
      permissionDenied: false,
      code: "EINVAL",
      message: "目标目录为空",
      targetDirectory: targetDir || "",
    };
  }

  try {
    await fs.readdir(targetDir);
    // 排除「可读但不可写」的 POSIX 权限问题
    await fs.access(targetDir, fs.constants.W_OK);
    return {
      ok: true,
      permissionDenied: false,
      targetDirectory: targetDir,
    };
  } catch (error) {
    return {
      ok: false,
      permissionDenied: isPermissionError(error),
      code: error?.code || "UNKNOWN",
      message: error?.message || String(error),
      targetDirectory: targetDir,
    };
  }
}

/**
 * 按 Darwin 内核主版本生成系统设置深链。
 * macOS 13（Darwin 22）起 System Settings 改用 ExtensionKit 标识。
 * @param {"files"|"full-disk"} panel
 * @param {number} darwinMajor
 */
function buildMacPrivacySettingsUrl(panel = "files", darwinMajor = 0) {
  const anchor = PRIVACY_PANES[panel] || PRIVACY_PANES.files;
  const extension =
    Number.isFinite(darwinMajor) && darwinMajor >= 22
      ? "com.apple.settings.PrivacySecurity.extension"
      : "com.apple.preference.security";
  return `x-apple.systempreferences:${extension}?${anchor}`;
}

/**
 * @param {"files"|"full-disk"} panel
 * @returns {string}
 */
function getMacPrivacySettingsUrl(panel = "files") {
  const darwinMajor = Number.parseInt(String(os.release()).split(".")[0], 10);
  return buildMacPrivacySettingsUrl(panel, darwinMajor);
}

module.exports = {
  isPermissionError,
  getMacProtectedFolderName,
  probeWriteAccess,
  probeReadAccess,
  buildMacPrivacySettingsUrl,
  getMacPrivacySettingsUrl,
};
