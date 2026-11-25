const { ipcMain, BrowserWindow, dialog, app, clipboard, shell } = require('electron');
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
  getDraftDirectoryStatus,
  autoDetectDraftPath,
  checkDraftDirectoryPermission,
  checkUrlAccessRight,
  readHistoryRecord,
  readConfig,
} = require('./download');
const { getMacPrivacySettingsUrl } = require('./filePermission');

/**
 * 每次 IPC 调用时解析当前可用窗口。
 *
 * macOS 关闭窗口不会退出应用，重新打开会创建新的 BrowserWindow。
 * 不能在注册 IPC 时把窗口捕获进闭包，否则后续调用会继续使用已销毁的窗口，
 * 导致 Electron 抛出 "Object has been destroyed"。
 */
function getActiveWindow() {
  const focused = BrowserWindow.getFocusedWindow();
  if (focused && !focused.isDestroyed()) return focused;

  return (
    BrowserWindow.getAllWindows().find((win) => win && !win.isDestroyed()) || null
  );
}

/** 优先返回发起本次 IPC 的窗口，取不到时回退到当前活动窗口。 */
function getInvokingWindow(event) {
  try {
    const invoking = BrowserWindow.fromWebContents(event?.sender);
    if (invoking && !invoking.isDestroyed()) return invoking;
  } catch {
    // 发送方 webContents 已销毁时回退到活动窗口
  }
  return getActiveWindow();
}

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

// 注册一次 IPC 处理器；窗口在每次调用时动态解析，避免窗口重建后引用失效
function setupIpcHandlers() {

  ipcMain.handle('get-download-log', async (event) => {
    return await readDownloadLog();
  });

  ipcMain.handle('clear-download-log', async (event) => {
    return await clearDownloadLog();
  });

  ipcMain.handle('get-url-json-data', async (event, remoteUrl) => {
    try {
      return await getDraftUrls(remoteUrl, getInvokingWindow(event));
    } catch (error) {
      logger.error(`[error] get draft url:`, error);
      return { code: -1, message: error.message || "获取草稿地址失败" };
    }
  });

  ipcMain.handle('save-file', async (event, config) => {
    // 必须把结果回传给渲染层：保存失败（尤其是权限问题）需要据此弹出引导
    return await downloadFiles(config, getInvokingWindow(event));
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
    const messageBoxOptions = {
      type: options.type || 'info',
      title: options.title || '提示',
      message: options.message || '',
      buttons: ['确定'],
      noLink: true, // 防止按钮以链接样式显示，这通常会使按钮更小更紧凑
      normalizeAccessKeys: true // 标准化访问键，确保按钮文本格式一致
    };
    const parentWindow = getInvokingWindow(event);
    return parentWindow
      ? await dialog.showMessageBox(parentWindow, messageBoxOptions)
      : await dialog.showMessageBox(messageBoxOptions);
  });

  ipcMain.handle('get-config-data', async (event) => {
    return await ensureAutoDetectedDraftPathInConfig();
  });

  // 草稿目录状态：渲染层据此展示设置引导
  ipcMain.handle('get-draft-directory-status', async () => {
    try {
      return await getDraftDirectoryStatus();
    } catch (error) {
      logger.error('获取草稿目录状态失败:', error);
      return {
        configured: false,
        ready: false,
        reason: 'error',
        targetDirectory: '',
        platform: process.platform,
        defaultPath: '',
        message: error.message || '获取草稿目录状态失败',
      };
    }
  });

  // 用户主动触发自动检测
  ipcMain.handle('auto-detect-draft-path', async () => {
    try {
      return await autoDetectDraftPath();
    } catch (error) {
      logger.error('自动检测草稿目录失败:', error);
      return { success: false, code: 'DETECT_FAILED', message: error.message };
    }
  });

  // 设置默认草稿路径（选择后校验是否为剪映草稿目录）
  ipcMain.handle('update-draft-path', async (event) => {
    return await updateDraftPath(getInvokingWindow(event));
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