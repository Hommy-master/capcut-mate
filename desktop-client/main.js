const { app, BrowserWindow, dialog } = require('electron');
const path = require('path');
const logger = require('./nodeapi/logger');

// 引入IPC处理程序模块
const { setupIpcHandlers } = require('./nodeapi/ipcHandlers');

let mainWindow;
let ipcHandlersInitialized = false;

function createWindow() {
  // 避免重复创建窗口
  if (mainWindow) {
    mainWindow.show();
    return mainWindow;
  }

  // 根据平台选择合适的图标格式
  let iconPath;
  if (process.platform === 'darwin') {
    iconPath = path.join(__dirname, './assets/icons/logo.icns');
  } else if (process.platform === 'win32') {
    iconPath = path.join(__dirname, './assets/icons/logo.ico');
  } else {
    iconPath = path.join(__dirname, './assets/icons/logo.png');
  }

  mainWindow = new BrowserWindow({
    width: 1366,
    height: 868,
    icon: iconPath,
    show: false, // 创建窗口但先隐藏，等页面加载完成后再显示
    webPreferences: {
      nodeIntegration: false, // 禁用 Node.js 集成（出于安全考虑，强烈推荐）
      contextIsolation: true, // 启用上下文隔离（Electron 12 后默认 true，推荐开启）
      preload: path.join(__dirname, 'preload.js'), // 指定预加载脚本的绝对路径
      // webSecurity: false, // 禁用web安全策略（可选，根据需求调整）
      disableBlinkFeatures: 'OutOfBlinkCors', // 禁用某些Blink特性以提高性能
      hardwareAcceleration: true // 启用硬件加速
    }
  });

  // 在 macOS 上设置 Dock 图标
  if (process.platform === 'darwin') {
    app.dock.setIcon(path.join(__dirname, './assets/icons/logo.png'));
  }

  // 判断是否为开发模式
  const isDev = process.env.NODE_ENV === 'development' || !app.isPackaged;
  
  // 加载React应用
  if (isDev) {
    // 开发模式下加载本地web服务
    mainWindow.loadURL('http://localhost:9000');
    // 开发模式下打开开发者工具
    mainWindow.webContents.openDevTools();
  } else {
    // 生产模式下加载构建后的文件
    mainWindow.loadFile(path.join(__dirname, 'ui', 'index.html'));
  }

  // 当页面加载完成后显示窗口
  mainWindow.webContents.on('ready-to-show', () => {
    mainWindow.show();
  });

  // 只初始化一次IPC处理程序
  if (!ipcHandlersInitialized) {
    setupIpcHandlers(mainWindow);
    ipcHandlersInitialized = true;
  }

  mainWindow.on('closed', function () {
    mainWindow = null;
  });

  return mainWindow;
}

// 处理未捕获的异常，特别是与文件权限相关的错误
process.on('uncaughtException', (error) => {
  logger.error('未捕获的异常:', error);
  
  // 在 macOS 沙箱环境下，某些权限错误可能在这里捕获
  if (process.platform === 'darwin' && error.message && 
      (error.message.includes('Operation not permitted') || error.message.includes('EPERM'))) {
    dialog.showMessageBoxSync({
      type: 'error',
      title: '权限错误',
      message: '应用缺少必要的文件访问权限，请检查系统偏好设置中的隐私与安全性设置。',
      detail: '请在 系统偏好设置 > 安全性与隐私 > 隐私 > 文件夹访问 中允许本应用访问相关文件夹。',
      buttons: ['确定']
    });
  }
});

// 当Electron完成初始化并准备创建浏览器窗口时调用此方法
app.whenReady().then(() => {
  createWindow();
});

// 当所有窗口都关闭时退出应用
app.on('window-all-closed', () => {
  // 在macOS上，应用及其菜单栏通常保持活动状态，直到用户使用Cmd + Q明确退出
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  // 在macOS上，当单击dock图标时，如果没有任何窗口打开则创建一个，
  // 否则显示已存在的窗口
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  } else {
    // 如果已有窗口，确保它被显示和聚焦
    if (mainWindow) {
      if (mainWindow.isMinimized()) mainWindow.restore();
      mainWindow.focus();
    }
  }
});