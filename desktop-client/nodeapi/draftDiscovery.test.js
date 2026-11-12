const { test } = require("node:test");
const assert = require("node:assert/strict");
const os = require("os");
const path = require("path");
const fs = require("fs").promises;

const {
  ROOT_META_INFO_FILENAME,
  findDraftEntry,
  waitForDraftDiscovery,
} = require("./draftDiscovery");

const DRAFT_DIR = path.join("C:", "Users", "me", "drafts", "20260927202001abcd");
const DRAFT_ID = "20260927202001abcd";

function makeMeta(entries) {
  return { all_draft_store: entries, draft_ids: entries.length, root_path: "" };
}

test("matches draft_fold_path despite separators and trailing slash", () => {
  const meta = makeMeta([
    {
      draft_name: "renamed-in-jianying",
      draft_fold_path: "C:\\Users\\me\\drafts\\20260927202001abcd\\",
    },
  ]);
  const entry = findDraftEntry(meta, { draftDir: DRAFT_DIR, draftId: DRAFT_ID });
  assert.equal(entry?.draft_name, "renamed-in-jianying");
});

test("falls back to draft_name when the path form differs", () => {
  const meta = makeMeta([
    {
      draft_name: DRAFT_ID,
      draft_fold_path: "/Users/me/Movies/CapCut/User Data/Projects/com.lveditor.draft/20260927202001abcd",
    },
  ]);
  assert.ok(findDraftEntry(meta, { draftDir: DRAFT_DIR, draftId: DRAFT_ID }));
});

test("ignores unrelated and malformed entries", () => {
  const meta = makeMeta([
    null,
    "not-an-object",
    { draft_name: "other-draft", draft_fold_path: "/tmp/other-draft" },
  ]);
  assert.equal(findDraftEntry(meta, { draftDir: DRAFT_DIR, draftId: DRAFT_ID }), null);
  assert.equal(findDraftEntry({ all_draft_store: "nope" }, { draftDir: DRAFT_DIR }), null);
  assert.equal(findDraftEntry(null, { draftDir: DRAFT_DIR }), null);
});

test("waitForDraftDiscovery sees the entry added by JianYing after a delay", async (t) => {
  const root = await fs.mkdtemp(path.join(os.tmpdir(), "draft-discovery-"));
  t.after(() => fs.rm(root, { recursive: true, force: true }));

  const draftDir = path.join(root, DRAFT_ID);
  await fs.mkdir(draftDir);
  const metaPath = path.join(root, ROOT_META_INFO_FILENAME);
  await fs.writeFile(metaPath, JSON.stringify(makeMeta([])), "utf8");

  setTimeout(() => {
    const entry = { draft_name: DRAFT_ID, draft_fold_path: draftDir };
    fs.writeFile(metaPath, JSON.stringify(makeMeta([entry])), "utf8").catch(() => {});
  }, 120);

  const result = await waitForDraftDiscovery(draftDir, {
    timeoutMs: 2000,
    pollIntervalMs: 40,
  });
  assert.equal(result.discovered, true);
  assert.equal(result.reason, "found");
  assert.equal(result.entry.draft_name, DRAFT_ID);
});

test("waitForDraftDiscovery retries while the meta file is mid-write", async (t) => {
  const root = await fs.mkdtemp(path.join(os.tmpdir(), "draft-discovery-"));
  t.after(() => fs.rm(root, { recursive: true, force: true }));

  const draftDir = path.join(root, DRAFT_ID);
  await fs.mkdir(draftDir);
  const metaPath = path.join(root, ROOT_META_INFO_FILENAME);
  await fs.writeFile(metaPath, '{"all_draft_store": [', "utf8");
  setTimeout(() => {
    fs.writeFile(
      metaPath,
      JSON.stringify(makeMeta([{ draft_name: DRAFT_ID }])),
      "utf8"
    ).catch(() => {});
  }, 100);

  const result = await waitForDraftDiscovery(draftDir, {
    timeoutMs: 2000,
    pollIntervalMs: 40,
  });
  assert.equal(result.discovered, true);
});

test("waitForDraftDiscovery returns immediately when root meta is missing", async (t) => {
  const root = await fs.mkdtemp(path.join(os.tmpdir(), "draft-discovery-"));
  t.after(() => fs.rm(root, { recursive: true, force: true }));

  const draftDir = path.join(root, DRAFT_ID);
  await fs.mkdir(draftDir);

  const startedAt = Date.now();
  const result = await waitForDraftDiscovery(draftDir, { timeoutMs: 5000 });
  assert.equal(result.discovered, false);
  assert.equal(result.reason, "root_meta_missing");
  assert.ok(Date.now() - startedAt < 1000);
});

test("waitForDraftDiscovery times out when the draft is never listed", async (t) => {
  const root = await fs.mkdtemp(path.join(os.tmpdir(), "draft-discovery-"));
  t.after(() => fs.rm(root, { recursive: true, force: true }));

  const draftDir = path.join(root, DRAFT_ID);
  await fs.mkdir(draftDir);
  await fs.writeFile(
    path.join(root, ROOT_META_INFO_FILENAME),
    JSON.stringify(makeMeta([{ draft_name: "other", draft_fold_path: "/tmp/other" }])),
    "utf8"
  );

  const result = await waitForDraftDiscovery(draftDir, {
    timeoutMs: 250,
    pollIntervalMs: 40,
  });
  assert.equal(result.discovered, false);
  assert.equal(result.reason, "not_listed");
});

test("waitForDraftDiscovery treats a BOM-prefixed meta file as valid JSON", async (t) => {
  const root = await fs.mkdtemp(path.join(os.tmpdir(), "draft-discovery-"));
  t.after(() => fs.rm(root, { recursive: true, force: true }));

  const draftDir = path.join(root, DRAFT_ID);
  await fs.mkdir(draftDir);
  await fs.writeFile(
    path.join(root, ROOT_META_INFO_FILENAME),
    "\uFEFF" + JSON.stringify(makeMeta([{ draft_name: DRAFT_ID }])),
    "utf8"
  );

  const result = await waitForDraftDiscovery(draftDir, {
    timeoutMs: 500,
    pollIntervalMs: 40,
  });
  assert.equal(result.discovered, true);
});
