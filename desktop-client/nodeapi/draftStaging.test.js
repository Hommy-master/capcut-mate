const { test } = require("node:test");
const assert = require("node:assert/strict");
const os = require("os");
const path = require("path");
const fs = require("fs").promises;

const {
  STAGING_DIR_NAME,
  getStagingRootDir,
  getStagingDraftDir,
  publishStagedDraft,
} = require("./draftStaging");

const DRAFT_ID = "20260927202001abcd";

async function makeWorkspace(t) {
  const root = await fs.mkdtemp(path.join(os.tmpdir(), "draft-staging-"));
  t.after(() => fs.rm(root, { recursive: true, force: true }));

  const stagingDir = getStagingDraftDir(root, DRAFT_ID);
  const finalDir = path.join(root, DRAFT_ID);
  await fs.mkdir(path.join(stagingDir, "assets", "videos"), { recursive: true });
  await fs.writeFile(path.join(stagingDir, "draft_content.json"), "{}", "utf8");
  await fs.writeFile(
    path.join(stagingDir, "assets", "videos", "clip.mp4"),
    "binary",
    "utf8"
  );

  return { root, stagingDir, finalDir };
}

test("staging paths live under the hidden staging dir in the draft root", () => {
  const root = "/drafts";
  assert.equal(getStagingRootDir(root), path.join(root, STAGING_DIR_NAME));
  assert.equal(
    getStagingDraftDir(root, DRAFT_ID),
    path.join(root, STAGING_DIR_NAME, DRAFT_ID)
  );
});

test("publishes a complete draft with a single rename", async (t) => {
  const { root, stagingDir, finalDir } = await makeWorkspace(t);

  const result = await publishStagedDraft(stagingDir, finalDir);

  assert.deepEqual(result, { replacedExisting: false, leftoverBackupDir: null });
  assert.equal(
    await fs.readFile(path.join(finalDir, "draft_content.json"), "utf8"),
    "{}"
  );
  assert.equal(
    await fs.readFile(path.join(finalDir, "assets", "videos", "clip.mp4"), "utf8"),
    "binary"
  );
  await assert.rejects(fs.access(stagingDir));
  // 暂存根目录清空后一并移除
  await assert.rejects(fs.access(getStagingRootDir(root)));
});

test("replaces an existing draft and removes the backup", async (t) => {
  const { root, stagingDir, finalDir } = await makeWorkspace(t);
  await fs.mkdir(finalDir, { recursive: true });
  await fs.writeFile(path.join(finalDir, "stale.json"), "old", "utf8");

  const result = await publishStagedDraft(stagingDir, finalDir);

  assert.equal(result.replacedExisting, true);
  assert.equal(result.leftoverBackupDir, null);
  assert.equal(
    await fs.readFile(path.join(finalDir, "draft_content.json"), "utf8"),
    "{}"
  );
  await assert.rejects(fs.access(path.join(finalDir, "stale.json")));
  await assert.rejects(fs.access(getStagingRootDir(root)));
});

test("restores the previous draft when publishing fails", async (t) => {
  const root = await fs.mkdtemp(path.join(os.tmpdir(), "draft-staging-"));
  t.after(() => fs.rm(root, { recursive: true, force: true }));

  const finalDir = path.join(root, DRAFT_ID);
  await fs.mkdir(finalDir, { recursive: true });
  await fs.writeFile(path.join(finalDir, "draft_content.json"), "old", "utf8");

  // 暂存根目录存在、暂存草稿目录不存在：正式目录让位后改名必然失败
  const missingStagingDir = getStagingDraftDir(root, DRAFT_ID);
  await fs.mkdir(getStagingRootDir(root), { recursive: true });
  await assert.rejects(publishStagedDraft(missingStagingDir, finalDir));

  assert.equal(
    await fs.readFile(path.join(finalDir, "draft_content.json"), "utf8"),
    "old"
  );
  await assert.rejects(fs.access(getStagingRootDir(root)));
});
