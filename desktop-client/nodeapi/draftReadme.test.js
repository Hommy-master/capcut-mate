const { test } = require("node:test");
const assert = require("node:assert/strict");
const os = require("os");
const path = require("path");
const fs = require("fs").promises;

const {
  DRAFT_README_FILENAME,
  DRAFT_README_TEXT,
  draftReadmeData,
  writeDraftReadmeFile,
} = require("./draftReadme");

test("readme carries a UTF-8 BOM for Windows Notepad", () => {
  const data = draftReadmeData();
  assert.deepEqual([...data.subarray(0, 3)], [0xef, 0xbb, 0xbf]);
  assert.equal(data.subarray(3).toString("utf8"), DRAFT_README_TEXT);
});

test("filename says this is a JianYing draft", () => {
  assert.equal(DRAFT_README_FILENAME, "【剪映草稿】请用剪映打开查看成片.txt");
  assert.match(DRAFT_README_TEXT, /剪映草稿/);
  assert.match(DRAFT_README_TEXT, /不是可直接播放的视频文件/);
});

test("writes readme into the draft directory", async () => {
  const dir = await fs.mkdtemp(path.join(os.tmpdir(), "capcut-mate-readme-"));
  try {
    const target = await writeDraftReadmeFile(dir);
    assert.equal(target, path.join(dir, DRAFT_README_FILENAME));
    const content = await fs.readFile(target);
    assert.deepEqual(content, Buffer.concat([Buffer.from([0xef, 0xbb, 0xbf]), Buffer.from(DRAFT_README_TEXT, "utf8")]));
  } finally {
    await fs.rm(dir, { recursive: true, force: true });
  }
});

test("rejects when the draft directory does not exist", async () => {
  const dir = path.join(os.tmpdir(), `capcut-mate-missing-${Date.now()}`);
  await assert.rejects(() => writeDraftReadmeFile(dir));
});
