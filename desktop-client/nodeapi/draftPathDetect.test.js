const { test } = require("node:test");
const assert = require("node:assert/strict");
const os = require("os");
const path = require("path");
const fs = require("fs").promises;

const {
  DRAFT_ROOT_DIR_NAME,
  DRAFT_REL_WIN,
  hasJianyingDraftMarkers,
  resolveDraftRootFromSelection,
  getDefaultDraftRootHint,
} = require("./draftPathDetect");

async function makeTempDir() {
  return fs.mkdtemp(path.join(os.tmpdir(), "capcut-mate-detect-"));
}

async function makeDraftRoot(parentDir) {
  const root = path.join(parentDir, DRAFT_ROOT_DIR_NAME);
  await fs.mkdir(root, { recursive: true });
  await fs.writeFile(path.join(root, "root_meta_info.json"), "{}", "utf8");
  return root;
}

test("root_meta_info.json 存在时识别为草稿根目录", async (t) => {
  const base = await makeTempDir();
  t.after(() => fs.rm(base, { recursive: true, force: true }));

  const root = await makeDraftRoot(base);
  assert.equal(await hasJianyingDraftMarkers(root), true);
  assert.equal(await hasJianyingDraftMarkers(base), false);
});

test(".recycle_bin 子目录同样视为草稿根目录特征", async (t) => {
  const base = await makeTempDir();
  t.after(() => fs.rm(base, { recursive: true, force: true }));

  const root = path.join(base, "drafts");
  await fs.mkdir(path.join(root, ".recycle_bin"), { recursive: true });
  assert.equal(await hasJianyingDraftMarkers(root), true);
});

test("选中草稿根目录本身时原样返回", async (t) => {
  const base = await makeTempDir();
  t.after(() => fs.rm(base, { recursive: true, force: true }));

  const root = await makeDraftRoot(base);
  assert.deepEqual(await resolveDraftRootFromSelection(root), {
    path: root,
    corrected: false,
  });
});

test("选中上级目录时向下定位到草稿根目录", async (t) => {
  const base = await makeTempDir();
  t.after(() => fs.rm(base, { recursive: true, force: true }));

  const root = await makeDraftRoot(base);
  assert.deepEqual(await resolveDraftRootFromSelection(base), {
    path: root,
    corrected: true,
  });
});

test("选中 Movies 层级时能向下定位到 JianyingPro 草稿根目录", async (t) => {
  const base = await makeTempDir();
  t.after(() => fs.rm(base, { recursive: true, force: true }));

  const projects = path.join(base, "Movies", "JianyingPro", "User Data", "Projects");
  const root = await makeDraftRoot(projects);

  const resolved = await resolveDraftRootFromSelection(path.join(base, "Movies"));
  assert.deepEqual(resolved, { path: root, corrected: true });
});

test("选中用户主目录时能定位 Windows AppData 下的草稿目录", async (t) => {
  const home = await makeTempDir();
  t.after(() => fs.rm(home, { recursive: true, force: true }));

  const root = path.join(home, DRAFT_REL_WIN);
  await fs.mkdir(root, { recursive: true });
  await fs.writeFile(path.join(root, "root_meta_info.json"), "{}", "utf8");

  assert.deepEqual(await resolveDraftRootFromSelection(home), {
    path: root,
    corrected: true,
  });
});

test("选中草稿根目录内的某份草稿时向上定位", async (t) => {
  const base = await makeTempDir();
  t.after(() => fs.rm(base, { recursive: true, force: true }));

  const root = await makeDraftRoot(base);
  const draftDir = path.join(root, "20260101120000abcd");
  await fs.mkdir(draftDir, { recursive: true });

  assert.deepEqual(await resolveDraftRootFromSelection(draftDir), {
    path: root,
    corrected: true,
  });
});

test("普通目录不会被误判为草稿根目录", async (t) => {
  const base = await makeTempDir();
  t.after(() => fs.rm(base, { recursive: true, force: true }));

  const plain = path.join(base, "plain");
  await fs.mkdir(plain, { recursive: true });
  assert.equal(await resolveDraftRootFromSelection(plain), null);
});

test("默认草稿目录提示以 com.lveditor.draft 结尾", () => {
  const hint = getDefaultDraftRootHint();
  if (process.platform === "darwin" || process.platform === "win32") {
    assert.equal(path.basename(hint), DRAFT_ROOT_DIR_NAME);
  } else {
    assert.equal(hint, "");
  }
});
