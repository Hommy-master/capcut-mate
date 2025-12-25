const { app, BrowserWindow } = require('electron');
const path = require('path');
const logger = require('./nodeapi/logger');

// 引入IPC处理程序模块
const { setupIpcHandlers } = require('./nodeapi/ipcHandlers');

let mainWindow;

function createWindow() {
  mainWindow = null;

  mainWindow = new BrowserWindow({
    width: 1366,
    height: 868,
    icon: path.join(__dirname, './assets/icons/logo.ico'),
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

  
  if (process.platform==='darwin') {
    app.dock.setIcon(path.join(__dirname, './assets/icons/logo.png'))
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

  // 调用IPC处理程序，传递mainWindow参数
  setupIpcHandlers(mainWindow);

  mainWindow.on('closed', function () {
    mainWindow = null;
  });
}

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
  // 在macOS上，当单击dock图标并且没有其他窗口打开时，
  // 通常在应用程序中重新创建一个窗口
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});