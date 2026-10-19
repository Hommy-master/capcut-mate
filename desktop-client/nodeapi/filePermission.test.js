const { test } = require("node:test");
const assert = require("node:assert/strict");
const fs = require("fs").promises;
const os = require("os");
const path = require("path");

const {
  isPermissionError,
  getMacProtectedFolderName,
  probeWriteAccess,
  probeReadAccess,
  buildMacPrivacySettingsUrl,
} = require("./filePermission");

test("isPermissionError recognizes TCC and filesystem permission errors", () => {
  assert.equal(isPermissionError({ code: "EPERM" }), true);
  assert.equal(isPermissionError({ code: "EACCES" }), true);
  assert.equal(
    isPermissionError(new Error("EPERM: operation not permitted, open '/x'")),
    true
  );
  assert.equal(
    isPermissionError(new Error("EACCES: permission denied, mkdir '/x'")),
    true
  );
  assert.equal(isPermissionError(new Error("ENOENT: no such file or directory")), false);
  assert.equal(
    isPermissionError({ message: "permission denied", response: { status: 403 } }),
    false,
    "HTTP errors must not be treated as filesystem permission errors"
  );
  assert.equal(isPermissionError(null), false);
});

test("macOS 13+ uses the ExtensionKit privacy settings URL", () => {
  assert.equal(
    buildMacPrivacySettingsUrl("files", 22),
    "x-apple.systempreferences:com.apple.settings.PrivacySecurity.extension?Privacy_FilesAndFolders"
  );
  assert.equal(
    buildMacPrivacySettingsUrl("full-disk", 25),
    "x-apple.systempreferences:com.apple.settings.PrivacySecurity.extension?Privacy_AllFiles"
  );
});

test("older macOS keeps the legacy privacy pane identifier", () => {
  assert.equal(
    buildMacPrivacySettingsUrl("files", 21),
    "x-apple.systempreferences:com.apple.preference.security?Privacy_FilesAndFolders"
  );
});

test("unknown panels fall back to Files and Folders", () => {
  assert.equal(
    buildMacPrivacySettingsUrl("unknown", 23),
    "x-apple.systempreferences:com.apple.settings.PrivacySecurity.extension?Privacy_FilesAndFolders"
  );
});

test("getMacProtectedFolderName maps the top-level user folder", { skip: process.platform !== "darwin" }, () => {
  const home = path.join("/Users", "tester");
  assert.equal(
    getMacProtectedFolderName(
      path.join(home, "Movies", "CapCut", "User Data", "Projects"),
      home
    ),
    "影片"
  );
  assert.equal(
    getMacProtectedFolderName(path.join(home, "Documents", "CapCut"), home),
    "文稿"
  );
  assert.equal(getMacProtectedFolderName(path.join(home, "Projects"), home), "");
  assert.equal(getMacProtectedFolderName("/Volumes/Disk/Movies", home), "");
  assert.equal(getMacProtectedFolderName(home, home), "");
});

test("probeWriteAccess succeeds for a writable directory", async () => {
  const dir = await fs.mkdtemp(path.join(os.tmpdir(), "capcut-mate-perm-test-"));
  try {
    const result = await probeWriteAccess(dir);
    assert.equal(result.ok, true);
    assert.equal(result.permissionDenied, false);

    const entries = await fs.readdir(dir);
    assert.deepEqual(entries, [], "probe directory should be cleaned up");
  } finally {
    await fs.rm(dir, { recursive: true, force: true });
  }
});

test("probeReadAccess checks readability and write permission without writing", async () => {
  const dir = await fs.mkdtemp(path.join(os.tmpdir(), "capcut-mate-perm-test-"));
  try {
    const result = await probeReadAccess(dir);
    assert.equal(result.ok, true);
    assert.deepEqual(await fs.readdir(dir), []);
  } finally {
    await fs.rm(dir, { recursive: true, force: true });
  }
});

test("probeReadAccess reports a missing directory as non-permission error", async () => {
  const missing = path.join(os.tmpdir(), `capcut-mate-missing-${Date.now()}`);
  const result = await probeReadAccess(missing);
  assert.equal(result.ok, false);
  assert.equal(result.permissionDenied, false);
  assert.equal(result.code, "ENOENT");
});

test("probeWriteAccess reports permission errors for a read-only directory", async (t) => {
  if (process.platform === "win32" || process.getuid?.() === 0) {
    t.skip("POSIX permissions are not enforced for this test user");
    return;
  }

  const dir = await fs.mkdtemp(path.join(os.tmpdir(), "capcut-mate-perm-test-"));
  try {
    await fs.chmod(dir, 0o500);
    const result = await probeWriteAccess(dir);
    assert.equal(result.ok, false);
    assert.equal(result.permissionDenied, true);
    assert.match(String(result.code), /EACCES|EPERM/);

    // 轮询用的只读探测也要能发现「可读但不可写」
    const readResult = await probeReadAccess(dir);
    assert.equal(readResult.ok, false);
    assert.equal(readResult.permissionDenied, true);
  } finally {
    await fs.chmod(dir, 0o700).catch(() => {});
    await fs.rm(dir, { recursive: true, force: true });
  }
});
