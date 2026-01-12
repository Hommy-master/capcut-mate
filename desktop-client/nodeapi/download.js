const path = require("path");
const axios = require("axios");
const { app, dialog, shell } = require("electron");
const { createWriteStream } = require("fs");
const fs = require("fs").promises; // 使用 fs.promises 进行异步文件操作
const logger = require("./logger");
const { v4: uuidv4 } = require('uuid');

const RECORD_MAX = 500;

const LOG_MAX = 2000;

const axiosConfig = {
  method: "GET",
  timeout: 30000, // 30秒超时
  headers: {
    // 添加常见的浏览器User-Agent
    "User-Agent":
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
  },
};

function getConfigPath() {
  return path.join(app.getPath("userData"), "app-config.json");
}

async function readConfig() {
  const configPath = getConfigPath();
  logger.info("[log] Config path:", configPath);
  try {
    const data = await fs.readFile(configPath, "utf8");
    return JSON.parse(data) || {};
  } catch (error) {
    return {};
  }
}

async function writeConfig(config) {
  const configPath = getConfigPath();
  try {
    await fs.writeFile(configPath, JSON.stringify(config, null, 2), "utf8");
    return true;
  } catch (error) {
    logger.error("写入配置文件失败:", error);
    return false;
  }
}

function getDownloadLogPath() {
  return path.join(app.getPath("userData"), "download-log.json");
}

async function readDownloadLog() {
  const logPath = getDownloadLogPath();
  logger.info("[log] Log path:", logPath);
  try {
    const data = await fs.readFile(logPath, "utf8");
    return JSON.parse(data);
  } catch (error) {
    return [];
  }
}

/**
 *
 * @param {*} entry {time: Date, level: 'error', message: '日志内容' }
 */
async function appendDownloadLog(entry, parentWindow) {
  const logPath = getDownloadLogPath();
  let logs = [];
  try {
    logs = await readDownloadLog();
  } catch (error) {
    // 如果文件不存在或无法读取，初始化为空数组
    logs = [];
  }

  entry.time = new Date();
  console.log(`appendDownloadLog: ${JSON.stringify(entry)}`);
  await parentWindow.webContents.send("file-operation-log", entry);
  logs.push(entry);
  if (logs.length > LOG_MAX) {
    logs.shift();
  }
  try {
    await fs.writeFile(logPath, JSON.stringify(logs, null, 2), "utf8");
  } catch (writeErr) {
    logger.error("写入日志文件失败:", writeErr);
  }
}

async function clearDownloadLog() {
  const logPath = getDownloadLogPath();
  try {
    await fs.writeFile(logPath, JSON.stringify([], null, 2), "utf8");
    return true;
  } catch (error) {
    logger.error("清空日志文件失败:", error);
    return false;
  }
}

function getHistoryRecordPath() {
  return path.join(app.getPath("userData"), "history-record.json");
}

async function readHistoryRecord() {
  const recordPath = getHistoryRecordPath();
  console.info("[History] Record path:", recordPath);
  try {
    const data = await fs.readFile(recordPath, "utf8");
    return JSON.parse(data);
  } catch (error) {
    return [];
  }
}

/**
 *
 * @param {*} entry {id: 'uuid', time: Date, draft_id: 'draft_id' draft_url: 'draft_url' }
 */
async function appendHistoryRecord(entry) {
  const recordPath = getHistoryRecordPath();
  let records = [];
  try {
    records = await readHistoryRecord();
  } catch (error) {
    // 如果文件不存在或无法读取，初始化为空数组
    records = [];
  }

  console.log(`appendHistoryRecord: ${JSON.stringify(entry)}`);
  records.push(entry);
  if (records.length > RECORD_MAX) {
    records.shift();
  }
  try {
    await fs.writeFile(recordPath, JSON.stringify(records, null, 2), "utf8");
  } catch (writeErr) {
    console.error("写入草稿历史记录文件失败:", writeErr);
  }
}

// 更精确的错误处理
function errorHandler(error = {}, url = "") {
  if (error.code === "ECONNREFUSED") {
    throw new Error(`[error] not connect to server: ${url}`);
  } else if (error.code === "ENOTFOUND") {
    throw new Error(`[error] domain not found: ${url}`);
  } else if (error.response) {
    // 服务器返回了错误状态码（如4xx, 5xx）
    throw new Error(`[error] server error (${error.response.status}): ${url}`);
  } else {
    throw error; // 重新抛出其他未知错误
  }
}

async function getDraftUrls(remoteUrl, parentWindow) {
  logger.info("[info] get draft url");
  try {
    const response = await axios({
      ...axiosConfig,
      url: remoteUrl,
      responseType: "json",
    });

    // 检查HTTP状态码
    if (response.status !== 200) {
      await appendDownloadLog(
        { level: "error", message: `获取草稿地址信息失败` },
        parentWindow
      );
      throw new Error(
        `[error] [draft url] request failed, status code: ${response.status}`
      );
    }
    logger.info("[success] get draft url");
    return response.data;
  } catch (error) {
    errorHandler(error, remoteUrl);
  }
}

async function updateDraftPath(parentWindow) {
  const targetDir = await getTargetDirectory(parentWindow, true);
  if (!targetDir) {
    return { success: false, error: "用户取消了目录选择" };
  }
  try {
    // 验证目录权限
    try {
      await fs.access(targetDir, fs.constants.R_OK | fs.constants.W_OK);
    } catch (accessError) {
      logger.error('所选目录无读写权限:', accessError);
      // 尝试使用 dialog 显示错误消息
      if (parentWindow) {
        const { dialog } = require('electron');
        await dialog.showMessageBox(parentWindow, {
          type: 'error',
          title: '权限不足',
          message: '所选目录没有足够的读写权限，请选择其他目录。',
          buttons: ['确定']
        });
      }
      return { success: false, error: '所选目录没有足够的读写权限' };
    }

    const configPath = getConfigPath();
    let config = {};

    // 尝试读取现有配置
    try {
      const data = await fs.readFile(configPath, "utf8");
      config = JSON.parse(data);
    } catch (error) {
      // 如果文件不存在，保持config为空对象
    }

    config.targetDirectory = targetDir;

    // 写回配置文件
    await fs.writeFile(configPath, JSON.stringify(config, null, 2), 'utf8');
    logger.info('默认草稿路径已更新为:', targetDir);
    return { success: true, targetDir };
  } catch (error) {
    logger.error('更新默认草稿路径失败:', error);
    return { success: false, error: error.message };
  }
}

// 提取出来的函数，可选参数parentWindow用于显示对话框时附加到对话框
async function getTargetDirectory(parentWindow = null, isUpdate = false) {
  let config = await readConfig();
  if (!isUpdate && config.targetDirectory) {
    try {
      await fs.access(config.targetDirectory, fs.constants.R_OK | fs.constants.W_OK);
      return config.targetDirectory;
    } catch (accessErr) {
      logger.warn("配置的目录已不存在或无访问权限，将重新选择。", accessErr.message);
    }
  }

  const dialogOptions = {
    properties: ["openDirectory", "createDirectory"], // 允许创建新目录
    title: "请选择目标目录",
    buttonLabel: "选择此目录",
    defaultPath: isUpdate ? config.targetDirectory : undefined
  };

  // 如果有父窗口，则附加到父窗口
  if (parentWindow) {
    dialogOptions.window = parentWindow;
  }

  const result = await dialog.showOpenDialog(dialogOptions);

  if (!result.canceled && result.filePaths.length > 0) {
    const selectedDir = result.filePaths[0];
    
    // 再次验证目录权限
    try {
      await fs.access(selectedDir, fs.constants.R_OK | fs.constants.W_OK);
    } catch (accessErr) {
      logger.error('所选目录无读写权限:', accessErr);
      if (parentWindow) {
        const { dialog } = require('electron');
        await dialog.showMessageBox(parentWindow, {
          type: 'error',
          title: '权限不足',
          message: '所选目录没有足够的读写权限，请重新选择。',
          buttons: ['确定']
        });
      }
      return ''; // 返回空字符串表示失败
    }
    
    config.targetDirectory = selectedDir;
    await writeConfig(config);
    return selectedDir;
  } else {
    return '';
  }
}

function updateValue(current, finalKey, targetDir, oldVal, targetId) {
  if (oldVal) {
    // 找到ID在路径中的位置
    const idIndex = oldVal.indexOf(targetId);
    if (idIndex === -1) return;

    // 提取ID及之后的部分作为将要下载的路径
    const relativePath = oldVal.substring(idIndex).replaceAll("/", path.sep); // 替换为系统路径分隔符
    // targetDir 已包含 targetId 目录，所以relativePath中的targetId要去重
    const newRelativePath = relativePath.replace(`${targetId}${path.sep}`, "");
    const newValue = path.join(targetDir, newRelativePath);
    current[finalKey] = newValue;

    logger.info(`✅ newValue to:`, newValue);
  }
}

// 递归遍历对象，更新所有名为path的属性
function recursivelyUpdatePaths(obj, targetDir, targetId) {
  // 处理数组
  if (Array.isArray(obj)) {
    obj.forEach((item) => {
      recursivelyUpdatePaths(item, targetDir, targetId);
    });
    return;
  }

  // 处理对象
  if (obj && typeof obj === "object") {
    // 检查是否有path属性
    if (obj.path && typeof obj.path === "string") {
      updateValue(obj, "path", targetDir, obj.path, targetId);
    }

    // 递归处理所有属性
    for (const key in obj) {
      if (obj.hasOwnProperty(key)) {
        recursivelyUpdatePaths(obj[key], targetDir, targetId);
      }
    }
  }
}

async function downloadJsonFile(
  { fileUrl, filePath, targetDir, targetId },
  parentWindow
) {
  // 1. 使用 Axios 下载 JSON 文件
  try {
    const response = await axios({
      method: "GET",
      url: fileUrl,
      responseType: "json", // 直接告诉 Axios 解析 JSON
    });

    // 检查HTTP状态码
    if (response.status !== 200) {
      await appendDownloadLog(
        { level: "error", message: `下载草稿内容文件失败` },
        parentWindow
      );
      throw new Error(
        `[error] [json] request failed, status code: ${response.status}`
      );
    }

    // 2. 解析获取到的数据（Axios 会根据 responseType: 'json' 自动解析）
    const jsonData = response.data;

    // 3. 修改 JSON 数据中指定键的值
    if (jsonData?.materials) {
      logger.info(`[log] start modifyJsonValue: materials`);
      recursivelyUpdatePaths(jsonData.materials, targetDir, targetId);
    }

    await appendDownloadLog(
      {
        level: "loading",
        message: `正在将草稿内容文件写入本地草稿目录 ${targetDir}`,
      },
      parentWindow
    );

    // 4. 将修改后的 JSON 对象转换为格式化的字符串并写入本地文件
    const jsonString = JSON.stringify(jsonData, null, 2); // 使用 2 个空格进行缩进，美化输出
    await fs.writeFile(filePath, jsonString, "utf8"); // 指定编码为 utf8
  } catch (error) {
    errorHandler(error, fileUrl);
  }
}

async function downloadNotJsonFile(
  { fileUrl, filePath, targetDir },
  parentWindow
) {
  try {
    // 1. 使用 Axios 下载非 JSON 文件
    const response = await axios({
      ...axiosConfig,
      url: fileUrl,
      responseType: "stream", // 设置响应类型为 'stream' 以处理大文件
    });

    // 检查HTTP状态码
    if (response.status !== 200) {
      await appendDownloadLog(
        { level: "error", message: `下载草稿内容文件失败` },
        parentWindow
      );
      throw new Error(
        `[error] [stream] request failed, status code: ${response.status}`
      );
    }

    logger.info(`[log] start create writable stream: ${filePath}`);

    await appendDownloadLog(
      {
        level: "loading",
        message: `正在将草稿内容文件写入本地草稿目录 ${targetDir}`,
      },
      parentWindow
    );

    // 创建可写流
    const writer = response.data.pipe(createWriteStream(filePath));

    return new Promise((resolve, reject) => {
      writer.on("finish", resolve);
      writer.on("error", (err) => {
        // 尝试删除可能不完整的文件
        fs.unlink(filePath).catch(() => { });
        reject(new Error(`[error] write file failed: ${err.message}`));
      });
      response.data.on("error", (err) => {
        reject(new Error(`[error] download stream error: ${err.message}`));
      });
    });
  } catch (error) {
    errorHandler(error, fileUrl);
  }
}

/**
 * 下载单个文件并保存到指定路径的辅助函数
 * @param {string} url 远程文件的URL
 * @param {string} filePath 要保存到的本地文件路径
 */
async function downloadSingleFile(config, parentWindow) {
  const filePath = config.filePath;
  const fileUrl = config.fileUrl;

  if (fileUrl.endsWith(".json")) {
    logger.info(`[log] start download json file : ${filePath}`);
    await downloadJsonFile(config, parentWindow);
  } else {
    logger.info(`[log] start download non-json file : ${filePath}`);
    await downloadNotJsonFile(config, parentWindow);
  }
}

// 打开目录
async function openDraftDirectory(dirPath) {
  try {
    const errorMsg = await shell.openPath(dirPath);
    if (errorMsg) {
      logger.error(`[error] Failed to open path: ${errorMsg}`);
      return { success: false, error: errorMsg };
    }
    return { success: true };
  } catch (error) {
    logger.error(`[error] Error opening path: ${error}`);
    return { success: false, error: error.message };
  }
}

async function downloadFiles(
  { sourceUrl, remoteFileUrls, targetId, isOpenDir },
  parentWindow
) {
  try {
    let baseTargetDir = "";
    // 然后获取目标目录，将主窗口作为父窗口传递
    try {
      baseTargetDir = await getTargetDirectory(parentWindow);
    } catch (error) {
      logger.error("[log] get target dir fail:", error);
      baseTargetDir = '';
    }

    if (!baseTargetDir) {
      await appendDownloadLog(
        { level: "error", message: `获取目录失败：${error}` },
        parentWindow
      );
      return;
    }

    logger.info("[log] get target dir:", baseTargetDir);

    await appendDownloadLog(
      { level: "info", message: `创建剪映草稿目录：${targetId}` },
      parentWindow
    );

    let i = 0;
    let relativePath = "";
    // 2. 遍历远程文件URL数组
    for (const fileUrl of remoteFileUrls) {
      try {
        // 从URL中提取相对路径部分
        // 假设你的URL结构固定，可以从特定部分之后开始提取
        const urlObj = new URL(fileUrl);
        // 提取路径名中可能包含的部分路径（根据你的URL结构调整）
        let fullPath = urlObj.pathname;

        // 找到ID在路径中的位置
        const idIndex = fullPath.indexOf(targetId);
        if (idIndex === -1) continue;

        // 提取ID及之后的部分作为将要下载的路径
        relativePath = fullPath.substring(idIndex).replaceAll("/", path.sep); // 替换为系统路径分隔符

        const fullTargetPath = path.join(baseTargetDir, relativePath);
        const targetDir = path.dirname(fullTargetPath);

        logger.info("[log] fullTargetPath: " + fullTargetPath);

        logger.info("[log] targetDir: " + targetDir);

        // 3. 确保目标目录存在
        try {
          await fs.mkdir(targetDir, { recursive: true }); // recursive: true 可以创建多级目录
        } catch (mkdirError) {
          logger.error(`创建目录失败: ${targetDir}`, mkdirError);
          await appendDownloadLog(
            { level: "error", message: `创建目录失败: ${targetDir} - ${mkdirError.message}` },
            parentWindow
          );
          throw mkdirError;
        }
        // return { success: true, message: targetDir };

        // 4. 下载文件

        logger.info(`[log] start get file context : ${fileUrl}`);
        await appendDownloadLog(
          {
            level: "loading",
            message: `正在下载草稿内容文件: ${relativePath}`,
          },
          parentWindow
        );

        await downloadSingleFile(
          { fileUrl, filePath: fullTargetPath, targetDir, targetId },
          parentWindow
        );

        logger.info(`[log] file saved to : ${fullTargetPath}`);
        await appendDownloadLog(
          { level: "success", message: `第 ${++i} 个草稿信息文件保存成功` },
          parentWindow
        );
      } catch (error) {
        logger.error(`[error] download file ${fileUrl} failed:`, error);

        await appendDownloadLog(
          { level: "error", message: `第 ${++i} 个草稿信息文件保存失败` },
          parentWindow
        );
        // 你可以决定是继续下载其他文件还是直接抛出错误
        // 这里记录错误但继续尝试下载下一个文件
      }
    }
    await appendDownloadLog(
      {
        level: "all",
        message: `下载完成：所有 ${targetId} 中的剪映草稿已下载！`,
      },
      parentWindow
    );

    // {id: 'uuid', time: Date, draft_id: 'draft_id', draft_url: 'draft_url' }
    await appendHistoryRecord({
      id: uuidv4(),
      time: new Date(),
      draft_id: targetId,
      draft_url: sourceUrl,
    });
    const jointPath = path.join(baseTargetDir, targetId);
    logger.info(`[finish] all download: ${jointPath}`);
    if (isOpenDir) await openDraftDirectory(jointPath);
    return {
      success: true,
      message: `文件批量保存完成，保存至目录: ${jointPath}`,
    };
  } catch (error) {
    logger.error(`[error] 批量保存过程发生错误:`, error);

    await appendDownloadLog(
      {
        level: "error",
        message: `下载失败：批量保存 ${targetId} 中的剪映草稿过程发生错误！`,
      },
      parentWindow
    );
    return { success: false, message: `保存失败: ${error.message} ` };
  }
}

async function checkUrlAccessRight(url) {
  try {
    const response = await axios({
      ...axiosConfig,
      method: 'HEAD',
      url: url,
      timeout: 5000
    });
    logger.info(`URL Accessibility Check Result: ${url} - ${response.status}`);
    return { accessible: response.status < 400 };
  } catch (error) {
    logger.error(`URL Accessibility Check Failed: ${url}`, error);
    return { accessible: false, error: error.message };
  }
}

module.exports = {
  readDownloadLog,
  clearDownloadLog,

  updateDraftPath,

  readConfig,

  getDraftUrls,

  downloadFiles,

  checkUrlAccessRight,

  readHistoryRecord
};
