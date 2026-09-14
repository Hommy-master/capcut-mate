/**
 * macOS 公证（带重试）
 * 解决 Apple notarytool 偶发返回非 JSON 的 HTTP 错误导致 CI 失败。
 */
const path = require("path");
const { execFileSync } = require("child_process");

module.exports = async function notarizeAfterSign(context) {
  const { electronPlatformName, appOutDir } = context;
  if (electronPlatformName !== "darwin") return;

  const appleId = process.env.APPLE_ID;
  const appleIdPassword = process.env.APPLE_APP_SPECIFIC_PASSWORD;
  const teamId = process.env.APPLE_TEAM_ID;
  if (!appleId || !appleIdPassword || !teamId) {
    console.log("skip notarize: APPLE_ID / APPLE_APP_SPECIFIC_PASSWORD / APPLE_TEAM_ID not set");
    return;
  }

  // 长时间打包后钥匙串可能再次上锁，公证前先解锁
  const keychainPath = process.env.KEYCHAIN_PATH;
  const keychainPassword = process.env.KEYCHAIN_PASSWORD;
  if (keychainPath && keychainPassword) {
    try {
      execFileSync("security", ["unlock-keychain", "-p", keychainPassword, keychainPath], {
        stdio: "inherit"
      });
    } catch (err) {
      console.warn("unlock-keychain failed:", err && err.message ? err.message : err);
    }
  }

  const { notarize } = require("@electron/notarize");
  const appName = context.packager.appInfo.productFilename;
  const appPath = path.join(appOutDir, `${appName}.app`);

  const maxAttempts = 5;
  let lastError;

  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    const started = Date.now();
    try {
      console.log(`notarizing ${appPath} (attempt ${attempt}/${maxAttempts})`);
      // @electron/notarize v3：提交公证并自动 staple
      await notarize({
        appPath,
        appleId,
        appleIdPassword,
        teamId
      });
      console.log(`notarization successful in ${Math.round((Date.now() - started) / 1000)}s`);
      return;
    } catch (err) {
      lastError = err;
      const message = err && err.message ? err.message : String(err);
      console.warn(`notarize attempt ${attempt} failed after ${Math.round((Date.now() - started) / 1000)}s: ${message}`);
      if (attempt < maxAttempts) {
        const waitSec = attempt * 60;
        console.log(`waiting ${waitSec}s before retry...`);
        await new Promise((resolve) => setTimeout(resolve, waitSec * 1000));
      }
    }
  }

  throw lastError;
};
