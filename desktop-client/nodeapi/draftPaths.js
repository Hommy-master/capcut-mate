/**
 * 草稿内资源路径的相对化工具（`src/pyJianYingDraft/draft_paths.py` 的 JS 镜像）。
 *
 * 剪映保存草稿时不写绝对路径，而是使用「草稿目录占位符」：
 *
 *     ##_draftpath_placeholder_<UUID>_##/<草稿内相对路径>
 *
 * 该 UUID 是编译进剪映二进制的常量，因此两端硬编码同一个默认值；
 * 可用环境变量 `DRAFT_PATH_PLACEHOLDER_ID` 覆盖。
 *
 * 仅依赖 `path`，保持纯函数以便单测。
 */

const path = require("path");

const DEFAULT_PLACEHOLDER_ID = "0E685133-18CE-45ED-8CB8-2904A212EC80";

const PLACEHOLDER_RE = /^##_draftpath_placeholder_[^#]+_##/;

const DRIVE_ABS_RE = /^[A-Za-z]:[\\/]/;
const DRIVE_REF_RE = /^[A-Za-z]:/;

/** 需要改写的素材字段：[materials 下的列表名, 素材内路径键]。 */
const MATERIAL_PATH_KEYS = [
  ["videos", "path"],
  ["audios", "path"],
  ["images", "path"],
];

/**
 * 草稿内素材的根目录名，与 Python 侧 `draft_paths.DRAFT_MEDIA_ROOT` 保持一致。
 * 剪映原生用 `Resources/local`；本项目沿用 `assets/{videos,audios,images}`，
 * 集中成常量是为了将来切换布局时只需改这一处。
 */
const DRAFT_MEDIA_ROOT = "assets";

function materialLocalDir(draftDir, subDir) {
  return path.join(draftDir, DRAFT_MEDIA_ROOT, subDir);
}

function placeholderId() {
  return process.env.DRAFT_PATH_PLACEHOLDER_ID || DEFAULT_PLACEHOLDER_ID;
}

function placeholderPrefix() {
  return `##_draftpath_placeholder_${placeholderId()}_##`;
}

function isHttpUrl(value) {
  if (!value || typeof value !== "string") return false;
  try {
    const parsed = new URL(value);
    return parsed.protocol === "http:" || parsed.protocol === "https:";
  } catch {
    return false;
  }
}

function isDraftRelative(value) {
  return typeof value === "string" && PLACEHOLDER_RE.test(value);
}

function isAbsLike(value) {
  if (!value || typeof value !== "string") return false;
  if (value.startsWith("\\\\") || value.startsWith("//")) return true;
  if (DRIVE_ABS_RE.test(value)) return true;
  // 两套实现都试：客户端可能在任何平台运行，而草稿路径常为 Windows 形式
  return path.posix.isAbsolute(value) || path.win32.isAbsolute(value);
}

/**
 * 归一化到可比较形式（分隔符统一为 `/`，Windows 下忽略大小写）。
 * 仅做等长替换，因此可以按同一偏移量切回原字符串。
 */
function normalizeForCompare(value) {
  const posix = value.replace(/\\/g, "/").replace(/\/+$/, "");
  return process.platform === "win32" ? posix.toLowerCase() : posix;
}

/**
 * 若 `value` 位于 `directory` 内，返回 posix 相对路径，否则返回 null。
 */
function relativeUnder(value, directory) {
  if (!value || typeof value !== "string") return null;
  if (!directory || typeof directory !== "string") return null;

  const target = normalizeForCompare(value);
  const base = normalizeForCompare(directory);
  if (!target || !base || target === base) return null;

  const prefix = `${base}/`;
  if (!target.startsWith(prefix)) return null;

  const posixValue = value.replace(/\\/g, "/");
  // normalizeForCompare 只在去除末尾斜杠时会改变长度，此时无法按同一偏移量切分
  if (target.length !== posixValue.length) return null;
  return posixValue.slice(prefix.length);
}

/**
 * 把草稿目录内的绝对路径改写为占位符相对路径，其余原样返回。
 *
 * 原样返回：非字符串 / 空串、http(s) URL、已是占位符形式、非绝对路径
 * （含 `"D:"` 这类剪映字体哨兵值）、以及位于 `draftDir` 之外的绝对路径。
 */
function toDraftRelative(value, draftDir) {
  if (!value || typeof value !== "string") return value;
  if (isHttpUrl(value) || isDraftRelative(value) || !isAbsLike(value)) return value;

  const rel = draftDir ? relativeUnder(value, draftDir) : null;
  if (rel === null) return value;
  return `${placeholderPrefix()}/${rel}`;
}

/**
 * 转换为 `draft_meta_info.json` 中 `file_Path` 的形式（`./<相对路径>`）。
 */
function toDraftFilePath(value) {
  if (!value || typeof value !== "string") return value;
  // `"D:"` / `"C:"` 是字体哨兵值而非路径
  if (isHttpUrl(value) || isAbsLike(value) || DRIVE_REF_RE.test(value)) return value;

  let rel = value;
  const match = value.match(PLACEHOLDER_RE);
  if (match) rel = value.slice(match[0].length);
  rel = rel.replace(/^\/+/, "");
  if (!rel) return value;
  return `./${rel}`;
}

/**
 * 就地把 `materials` 中位于草稿目录内的绝对素材路径改写为占位符形式。
 * @returns {boolean} 是否发生了改写
 */
function normalizeMaterialPaths(materials, draftDir) {
  if (!materials || typeof materials !== "object" || !draftDir) return false;

  let changed = false;
  for (const [listKey, pathKey] of MATERIAL_PATH_KEYS) {
    const items = materials[listKey];
    if (!Array.isArray(items)) continue;
    for (const item of items) {
      if (!item || typeof item !== "object") continue;
      const oldValue = item[pathKey];
      const newValue = toDraftRelative(oldValue, draftDir);
      if (newValue !== oldValue) {
        item[pathKey] = newValue;
        changed = true;
      }
    }
  }
  return changed;
}

/**
 * 按素材路径的实际形态推断 `config.material_save_mode`。
 * 1 = 素材已收纳进草稿目录；0 = 仍引用草稿目录之外的资源。
 */
function computeMaterialSaveMode(materials, draftDir) {
  if (!materials || typeof materials !== "object") return 1;
  for (const [listKey, pathKey] of MATERIAL_PATH_KEYS) {
    const items = materials[listKey];
    if (!Array.isArray(items)) continue;
    for (const item of items) {
      if (!item || typeof item !== "object") continue;
      const value = item[pathKey];
      if (isHttpUrl(value)) return 0;
      if (isAbsLike(value) && relativeUnder(value, draftDir) === null) return 0;
    }
  }
  return 1;
}

/**
 * 推断并写入 `jsonData.config.material_save_mode`。
 *
 * 远程素材本地化之后必须重新推断：URL 直写模式下服务端声明的是 0，
 * 客户端把素材下载进草稿目录后若仍写 0，剪映会认为素材在草稿之外。
 */
function ensureMaterialSaveMode(jsonData, draftDir) {
  if (!jsonData || typeof jsonData !== "object") return 1;
  const mode = computeMaterialSaveMode(jsonData.materials, draftDir);
  if (!jsonData.config || typeof jsonData.config !== "object") {
    jsonData.config = {};
  }
  jsonData.config.material_save_mode = mode;
  return mode;
}

/**
 * 归一化整个 `draft_content.json` / `draft_info.json`。
 * @returns {number} 最终写入的 material_save_mode
 */
function normalizeDraftContent(jsonData, draftDir) {
  if (!jsonData || typeof jsonData !== "object") return 1;
  normalizeMaterialPaths(jsonData.materials, draftDir);
  return ensureMaterialSaveMode(jsonData, draftDir);
}

/**
 * 把 `draft_meta_info.json` 的名称与路径改写为本地草稿目录。
 *
 * 服务端写的是**服务端自己的**草稿目录绝对路径，直接下发会把服务端路径
 * 带进用户机器；`draft_name` 也必须与本地文件夹名一致，否则剪映首页标题
 * 对不上、导出阶段会 DraftNotFound。
 */
function localizeDraftMeta(meta, targetDir, targetId) {
  if (!meta || typeof meta !== "object") return meta;
  const toPosix = (value) =>
    typeof value === "string" ? value.replace(/\\/g, "/") : value;

  if (targetId) meta.draft_name = targetId;
  if (targetDir) {
    meta.draft_fold_path = toPosix(targetDir);
    meta.draft_root_path = toPosix(path.dirname(targetDir));
  }

  // 素材登记表里的 file_Path 同样只保留相对形式
  if (Array.isArray(meta.draft_materials)) {
    for (const group of meta.draft_materials) {
      if (!group || !Array.isArray(group.value)) continue;
      for (const entry of group.value) {
        if (entry && typeof entry === "object" && entry.file_Path) {
          entry.file_Path = toDraftFilePath(entry.file_Path);
        }
      }
    }
  }
  return meta;
}

module.exports = {
  DEFAULT_PLACEHOLDER_ID,
  MATERIAL_PATH_KEYS,
  DRAFT_MEDIA_ROOT,
  materialLocalDir,
  placeholderId,
  placeholderPrefix,
  isHttpUrl,
  isDraftRelative,
  isAbsLike,
  relativeUnder,
  toDraftRelative,
  toDraftFilePath,
  normalizeMaterialPaths,
  computeMaterialSaveMode,
  ensureMaterialSaveMode,
  normalizeDraftContent,
  localizeDraftMeta,
};
