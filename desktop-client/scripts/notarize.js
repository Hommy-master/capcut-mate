/**
 * macOS 公证（带重试）
 * 解决 Apple notarytool 偶发返回非 JSON 的 HTTP 错误导致 CI 失败。
 */
const path = require("path");
const { execFileSync } = require("child_process");

function loadNotarize() {
  try {
    return require("@electron/notarize");
  } catch (_) {
    // electron-builder 自带的嵌套依赖
    return require("app-builder-lib/node_modules/@electron/notarize");
  }
}

exports.default = async function notarizeAfterSign(context) {
  const { electronPlatformName, appOutDir } = context;
  if (electronPlatformName !== "darwin") return;

  const appleId = process.env.APPLE_ID;
  const appleIdPassword = process.env.APPLE_APP_SPECIFIC_PASSWORD;
  const teamId = process.env.APPLE_TEAM_ID;
  if (!appleId || !appleIdPassword || !teamId) {
    console.log("skip notarize: APPLE_ID / APPLE_APP_SPECIFIC_PASSWORD / APPLE_TEAM_ID not set");
    return;
  }

  const { notarize } = loadNotarize();
  const appName = context.packager.appInfo.productFilename;
  const appPath = path.join(appOutDir, `${appName}.app`);

  const maxAttempts = 5;
  let lastError;

  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      console.log(`notarizing ${appPath} (attempt ${attempt}/${maxAttempts})`);
      await notarize({
        tool: "notarytool",
        appPath,
        appleId,
        appleIdPassword,
        teamId
      });
      console.log("notarization successful, stapling...");
      execFileSync("xcrun", ["stapler", "staple", "-v", appPath], { stdio: "inherit" });
      console.log("staple successful");
      return;
    } catch (err) {
      lastError = err;
      const message = err && err.message ? err.message : String(err);
      console.warn(`notarize attempt ${attempt} failed: ${message}`);
      if (attempt < maxAttempts) {
        const waitSec = attempt * 45;
        console.log(`waiting ${waitSec}s before retry...`);
        await new Promise((resolve) => setTimeout(resolve, waitSec * 1000));
      }
    }
  }

  throw lastError;
};
