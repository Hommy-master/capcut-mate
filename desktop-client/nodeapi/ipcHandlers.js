const { ipcMain, dialog, app, clipboard, shell } = require('electron');
const path = require('path');

// 引入logger模块
const logger = require('./logger');

// 引入axios
const axios = require('axios');

// 引入download.js模块
const {
  readDownloadLog,
  clearDownloadLog,
  getDraftUrls,
  updateDraftPath,
  downloadFiles,
  ensureAutoDetectedDraftPathInConfig,
  checkDraftDirectoryPermission,
  checkUrlAccessRight,
  readHistoryRecord,
  readConfig,
} = require('./download');
const { getMacPrivacySettingsUrl } = require('./filePermission');

/** macOS 上 .app 包路径（用于引导用户拖入「完全磁盘访问权限」列表） */
function getMacAppBundlePath() {
  const exePath = app.getPath('exe');
  if (exePath.includes('.app/Contents/MacOS/')) {
    return path.resolve(exePath, '../../..');
  }
  return path.dirname(exePath);
}

console.log(process.versions.electron);
console.log(process.versions.chrome);

// 接收mainWindow作为参数
function setupIpcHandlers(mainWindow) {

  ipcMain.handle('get-download-log', async (event) => {
    return await readDownloadLog();
  });

  ipcMain.handle('clear-download-log', async (event) => {
    return await clearDownloadLog();
  });

  ipcMain.handle('get-url-json-data', async (event, remoteUrl) => {
    try {
      return await getDraftUrls(remoteUrl, mainWindow);
    } catch (error) {
      logger.error(`[error] get draft url:`, error);
      return { code: -1, message: error.message || "获取草稿地址失败" };
    }
  });

  ipcMain.handle('save-file', async (event, config) => {
    // 必须把结果回传给渲染层：保存失败（尤其是权限问题）需要据此弹出引导
    return await downloadFiles(config, mainWindow);
  });

  // 真实写入探针，供授权引导弹窗轮询/手动重试
  ipcMain.handle('check-draft-permission', async (event, targetDirectory) => {
    try {
      let dir = typeof targetDirectory === 'string' ? targetDirectory : '';
      if (!dir) {
        const config = await readConfig();
        dir = config.targetDirectory || '';
      }
      return await checkDraftDirectoryPermission(dir);
    } catch (error) {
      logger.error('检测草稿目录权限失败:', error);
      return {
        ok: false,
        permissionDenied: false,
        code: 'CHECK_FAILED',
        platform: process.platform,
        targetDirectory: targetDirectory || '',
        message: error.message,
      };
    }
  });

  // 打开 macOS「文件与文件夹」/「完全磁盘访问权限」设置页
  ipcMain.handle('open-privacy-settings', async (event, panel) => {
    if (process.platform !== 'darwin') {
      return { success: false, error: '仅 macOS 支持打开隐私设置' };
    }
    const target = panel === 'full-disk' ? 'full-disk' : 'files';
    const url = getMacPrivacySettingsUrl(target);
    try {
      await shell.openExternal(url);
      logger.info(`已打开系统隐私设置: ${url}`);
      return { success: true, url };
    } catch (error) {
      logger.error('打开系统设置失败:', error);
      return { success: false, error: error.message };
    }
  });

  // 在访达中定位应用，方便用户拖入「完全磁盘访问权限」列表
  ipcMain.handle('reveal-app-in-finder', async () => {
    if (process.platform !== 'darwin') {
      return { success: false, error: '仅 macOS 支持' };
    }
    try {
      const appBundlePath = getMacAppBundlePath();
      shell.showItemInFolder(appBundlePath);
      return { success: true, path: appBundlePath };
    } catch (error) {
      logger.error('在访达中显示应用失败:', error);
      return { success: false, error: error.message };
    }
  });

  ipcMain.handle('show-message-box', async (event, options) => {
    return await dialog.showMessageBox(mainWindow, {
      type: options.type || 'info',
      title: options.title || '提示',
      message: options.message || '',
      buttons: ['确定'],
      noLink: true, // 防止按钮以链接样式显示，这通常会使按钮更小更紧凑
      normalizeAccessKeys: true // 标准化访问键，确保按钮文本格式一致
    });
  });

  ipcMain.handle('get-config-data', async (event) => {
    return await ensureAutoDetectedDraftPathInConfig();
  });

  // 设置默认草稿路径
  ipcMain.handle('update-draft-path', async (event) => {
    return await updateDraftPath(mainWindow);
  });

  // 在默认浏览器中打开URL
  ipcMain.handle('open-external-url', async (event, url) => {
    try {
      const { shell } = require('electron');
      await shell.openExternal(url);
      logger.info(`已在默认浏览器中打开URL: ${url}`);
      return { success: true };
    } catch (error) {
      logger.error(`打开URL失败: ${url}`, error);
      return { success: false, error: error.message };
    }
  });
  
  // 检测URL是否可访问
  ipcMain.handle('check-url-access', async (event, url) => {
    return await checkUrlAccessRight(url);
  });

  ipcMain.handle('get-history-record', async (event) => {
    return await readHistoryRecord();
  });

  ipcMain.handle('get-app-version', async () => {
    return app.getVersion();
  });

  ipcMain.handle('clipboard-read-text', () => clipboard.readText());

  ipcMain.handle('clipboard-write-text', (event, text) => {
    clipboard.writeText(String(text || ''));
    return true;
  });
}

module.exports = { setupIpcHandlers };