const fs = require('fs');
const path = require('path');

/**
 * electron-builder 在 signAndEditExecutable=false 时不会把 .ico 写入 exe。
 * 若已设置 signExecutable=false（仅跳过签名、仍写图标），通常无需此钩子。
 * 此处保留兜底：用 @electron/packager/resedit 补回桌面 / 任务栏图标。
 */
module.exports = async function afterPackWinIcon(context) {
  if (context.electronPlatformName !== 'win32') {
    return;
  }

  // electron-builder 26：signExecutable=false 时会自行写入图标，无需再补
  if (context.packager.platformSpecificBuildOptions.signExecutable === false) {
    return;
  }

  const exeName = `${context.packager.appInfo.productFilename}.exe`;
  const exePath = path.join(context.appOutDir, exeName);
  const iconPath = path.resolve(__dirname, '../assets/icons/logo.ico');

  if (!fs.existsSync(exePath)) {
    throw new Error(`Windows executable not found: ${exePath}`);
  }
  if (!fs.existsSync(iconPath)) {
    throw new Error(`Windows icon not found: ${iconPath}`);
  }

  const { resedit } = await import('@electron/packager/resedit');
  await resedit(exePath, { iconPath });
  console.log(`Embedded Windows icon into ${exeName}`);
};
