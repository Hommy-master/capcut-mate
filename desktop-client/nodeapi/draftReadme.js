/**
 * 草稿目录提示文件。
 *
 * 用户常常直接打开草稿文件夹，容易把素材视频当成成片；文件名与内容都说明
 * 「这是剪映草稿」，用户不看内容也能明白。参考 live-mixer/LiveMix 的
 * CapCutMateClient::writeDraftReadmeFile。
 *
 * 只依赖 fs/path，保持可单测。
 */

const path = require("path");
const fs = require("fs").promises;

/** 提示文件名：不看内容也能知道这是剪映草稿，需要剪映打开才能查看成片。 */
const DRAFT_README_FILENAME = "【剪映草稿】请用剪映打开查看成片.txt";

/** 提示文件正文。 */
const DRAFT_README_TEXT =
  "这是一个剪映草稿，不是可直接播放的视频文件。\n" +
  "\n" +
  "请打开剪映，在「本地草稿」中找到并打开这个草稿，即可查看和导出成片。\n";

/** 带 UTF-8 BOM：Windows 记事本等编辑器才能正确识别中文。 */
const UTF8_BOM = Buffer.from([0xef, 0xbb, 0xbf]);

/** 提示文件的完整字节内容（BOM + UTF-8 正文）。 */
function draftReadmeData() {
  return Buffer.concat([UTF8_BOM, Buffer.from(DRAFT_README_TEXT, "utf8")]);
}

/**
 * 把提示文件写入草稿目录。
 *
 * macOS 写进隐藏暂存目录，随原子改名一起发布；Windows 直接写正式目录。
 * 写入失败会抛错，由调用方决定是否忽略（提示文件不是草稿本体）。
 *
 * @param {string} draftDir 草稿目录（正式目录或暂存目录）
 * @returns {Promise<string>} 写入的提示文件完整路径
 */
async function writeDraftReadmeFile(draftDir) {
  const target = path.join(draftDir, DRAFT_README_FILENAME);
  await fs.writeFile(target, draftReadmeData());
  return target;
}

module.exports = {
  DRAFT_README_FILENAME,
  DRAFT_README_TEXT,
  draftReadmeData,
  writeDraftReadmeFile,
};
