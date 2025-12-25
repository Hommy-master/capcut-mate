const { contextBridge, ipcRenderer } = require('electron');

console.log('Preload script is loaded!');

// 通过 contextBridge 安全地将 API 暴露给渲染进程
contextBridge.exposeInMainWorld('electronAPI', {
    // 保存文件
    saveFile: (data) => ipcRenderer.invoke('save-file', data),

    getUrlJsonData: (url) => ipcRenderer.invoke('get-url-json-data', url),

    getDownloadLog: () => ipcRenderer.invoke('get-download-log'),

    clearDownloadLog: () => ipcRenderer.invoke('clear-download-log'),

    // 监听来自主进程的日志消息
    onFileOperationLog: (callback) => {
        ipcRenderer.on('file-operation-log', (event, logEntry) => {
            // 调用渲染进程提供的回调函数，并传递日志数据
            callback(logEntry);
        });
    },

    // 清理监听器，避免内存泄漏
    removeAllFileOperationLogListeners: () => {
        ipcRenderer.removeAllListeners('file-operation-log');
    },
    
    // 显示消息框
    showMessageBox: (options) => ipcRenderer.invoke('show-message-box', options),
    
    // 清空默认草稿路径
    clearDefaultDraftPath: () => ipcRenderer.invoke('clear-default-draft-path'),
    
    // 在默认浏览器中打开URL
    openExternalUrl: (url) => ipcRenderer.invoke('open-external-url', url),
    
    // 获取草稿保存路径
    getConfigData: () => ipcRenderer.invoke('get-config-data'),
    
    // 设置草稿保存路径
    updateDraftPath: () => ipcRenderer.invoke('update-draft-path'),
    
    // 检测URL是否可访问
    checkUrlAccess: (url) => ipcRenderer.invoke('check-url-access', url),
    
    getHistoryRecord: () => ipcRenderer.invoke('get-history-record'),
});