const fs = require('fs');
const path = require('path');

/**
 * electron-builder 在 signAndEditExecutable=false 时不会把 .ico 写入 exe。
 * 用 resedit（Node 实现，不依赖 winCodeSign）补回桌面 / 任务栏图标。
 */
module.exports = async function afterPackWinIcon(context) {
  if (context.electronPlatformName !== 'win32') {
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

  const { resedit } = require('@electron/packager/dist/resedit');
  await resedit(exePath, { iconPath });
  console.log(`Embedded Windows icon into ${exeName}`);
};
