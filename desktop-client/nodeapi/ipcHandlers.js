const { ipcMain, dialog } = require('electron');

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
  readConfig,
  checkUrlAccessRight,
  readHistoryRecord,
} = require('./download');

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
      return {};
    }
  });

  ipcMain.handle('save-file', async (event, config) => {
    await downloadFiles(config, mainWindow);
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
    return await readConfig();
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
}

module.exports = { setupIpcHandlers };