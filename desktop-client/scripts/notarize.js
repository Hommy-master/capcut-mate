/**
 * macOS 公证（带重试）
 * 优先使用 App Store Connect API Key；未配置时回退 Apple ID + App 专用密码。
 */
const fs = require("fs");
const path = require("path");
const { execFileSync } = require("child_process");

function buildNotarizeAuth() {
  const appleApiKey = process.env.APPLE_API_KEY;
  const appleApiKeyId = process.env.APPLE_API_KEY_ID;
  const appleApiIssuer = process.env.APPLE_API_ISSUER;

  if (appleApiKey && appleApiKeyId) {
    if (!fs.existsSync(appleApiKey)) {
      throw new Error(`APPLE_API_KEY file not found: ${appleApiKey}`);
    }
    const pem = fs.readFileSync(appleApiKey, "utf8");
    if (!pem.includes("BEGIN PRIVATE KEY")) {
      throw new Error(
        "APPLE_API_KEY does not look like a valid .p8 private key (missing BEGIN PRIVATE KEY)"
      );
    }
    const auth = {
      appleApiKey,
      appleApiKeyId
    };
    // Team Key 需要 Issuer ID；个人账号开通 API 后一般也是 Team Key
    if (appleApiIssuer) {
      auth.appleApiIssuer = appleApiIssuer;
    } else {
      console.warn(
        "APPLE_API_ISSUER is empty; Team API Key normally requires Issuer ID"
      );
    }
    return { mode: "apiKey", auth };
  }

  const appleId = process.env.APPLE_ID;
  const appleIdPassword = process.env.APPLE_APP_SPECIFIC_PASSWORD;
  const teamId = process.env.APPLE_TEAM_ID;
  if (appleId && appleIdPassword && teamId) {
    return {
      mode: "appleId",
      auth: { appleId, appleIdPassword, teamId }
    };
  }

  return null;
}

function unlockKeychainIfNeeded() {
  const keychainPath = process.env.KEYCHAIN_PATH;
  const keychainPassword = process.env.KEYCHAIN_PASSWORD;
  if (!keychainPath || !keychainPassword) return;
  try {
    execFileSync("security", ["unlock-keychain", "-p", keychainPassword, keychainPath], {
      stdio: "inherit"
    });
  } catch (err) {
    console.warn("unlock-keychain failed:", err && err.message ? err.message : err);
  }
}

function isTransientNotarizeError(message) {
  const text = String(message || "").toLowerCase();
  return (
    text.includes("timed out") ||
    text.includes("timeout") ||
    text.includes("offline") ||
    text.includes("no network route") ||
    text.includes("connection") ||
    text.includes("httperror") ||
    text.includes("socket") ||
    text.includes("econnreset") ||
    text.includes("enotfound") ||
    text.includes("unexpected result")
  );
}

module.exports = async function notarizeAfterSign(context) {
  const { electronPlatformName, appOutDir } = context;
  if (electronPlatformName !== "darwin") return;

  const requireApiKey = process.env.NOTARIZE_REQUIRE_API_KEY === "1";
  const creds = buildNotarizeAuth();
  if (!creds) {
    const msg =
      "notarize credentials missing: set App Store Connect API Key " +
      "(APPLE_API_KEY + APPLE_API_KEY_ID + APPLE_API_ISSUER) " +
      "or Apple ID (APPLE_ID + APPLE_APP_SPECIFIC_PASSWORD + APPLE_TEAM_ID)";
    if (requireApiKey) {
      throw new Error(msg);
    }
    console.log(`skip notarize: ${msg}`);
    return;
  }
  if (requireApiKey && creds.mode !== "apiKey") {
    throw new Error(
      "NOTARIZE_REQUIRE_API_KEY=1 but API Key is not configured; refusing Apple ID fallback"
    );
  }

  unlockKeychainIfNeeded();

  const { notarize } = require("@electron/notarize");
  const appName = context.packager.appInfo.productFilename;
  const appPath = path.join(appOutDir, `${appName}.app`);

  const maxAttempts = 6;
  let lastError;

  console.log(`notarize auth mode: ${creds.mode}`);
  if (creds.mode === "apiKey") {
    console.log(`notarize api key id: ${creds.auth.appleApiKeyId}`);
    console.log(`notarize api issuer set: ${Boolean(creds.auth.appleApiIssuer)}`);
  }

  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    const started = Date.now();
    try {
      unlockKeychainIfNeeded();
      console.log(`notarizing ${appPath} (attempt ${attempt}/${maxAttempts})`);
      await notarize({
        appPath,
        ...creds.auth
      });
      console.log(`notarization successful in ${Math.round((Date.now() - started) / 1000)}s`);
      return;
    } catch (err) {
      lastError = err;
      const message = err && err.message ? err.message : String(err);
      console.warn(
        `notarize attempt ${attempt} failed after ${Math.round((Date.now() - started) / 1000)}s: ${message}`
      );
      if (attempt >= maxAttempts) break;
      if (!isTransientNotarizeError(message)) {
        console.warn("non-transient notarize error, stop retrying");
        break;
      }
      const waitSec = Math.min(180, attempt * 45);
      console.log(`waiting ${waitSec}s before retry...`);
      await new Promise((resolve) => setTimeout(resolve, waitSec * 1000));
    }
  }

  throw lastError;
};
