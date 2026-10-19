import { useState, useEffect, useRef, useCallback } from "react";
import { toast } from "react-toastify";
import electronService from "../../services/electronService";
import ExternalWebpage from "../../components/ExternalWebpage";
import Textarea from "../../components/Textarea";
import Tabs from "../../components/Tabs";
import DownloadControls from "../../components/DownloadControls";
import DownloadButton from "../../components/DownloadButton";
import LogModule from "../../components/LogModule";
import PermissionGuide, {
  PermissionBanner,
} from "../../components/PermissionGuide";
import { applyLogBatch } from "../../utils/downloadLog";

import "./index.less";

const PERMISSION_DENIED = "DRAFT_PERMISSION_DENIED";

function MainPage() {
  const [textareaValue, setTextareaValue] = useState("");
  const [isDownloadOpen, setIsDownloadOpen] = useState(true);
  const [logs, setLogs] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  // 权限问题：issue 用于保留提示条，open 用于控制引导弹窗
  const [permissionIssue, setPermissionIssue] = useState(null);
  const [permissionOpen, setPermissionOpen] = useState(false);
  // 每次新的权限失败都重建引导组件，避免沿用上一次的「已授权」状态
  const [permissionGuideKey, setPermissionGuideKey] = useState(0);
  // 授权完成后需要继续下载的草稿地址
  const pendingDownloadsRef = useRef([]);

  // 外层容器的ref，用于实现自动滚动
  const downloadPageRef = useRef(null);
  const pendingLogsRef = useRef([]);
  const flushScheduledRef = useRef(false);

  const flushLogQueue = useCallback(() => {
    flushScheduledRef.current = false;
    if (pendingLogsRef.current.length === 0) {
      return;
    }
    const batch = pendingLogsRef.current.splice(0);
    setLogs((prevLogs) => applyLogBatch(prevLogs, batch));
    if (pendingLogsRef.current.length > 0) {
      flushScheduledRef.current = true;
      queueMicrotask(flushLogQueue);
    }
  }, []);

  const enqueueLogEntry = useCallback(
    (logEntry) => {
      pendingLogsRef.current.push(logEntry);
      if (!flushScheduledRef.current) {
        flushScheduledRef.current = true;
        queueMicrotask(flushLogQueue);
      }
    },
    [flushLogQueue]
  );

  // 加载配置
  useEffect(() => {
    // 监听日志更新（支持按 id 更新草稿下载状态）
    electronService.onFileOperationLog((logEntry) => {
      enqueueLogEntry(logEntry);
    });

    return () => {
      try {
        electronService.removeAllFileOperationLogListeners();
      } catch (error) {
        console.error("取消订阅日志失败:", error);
      }
    };
  }, [enqueueLogEntry]);

  // 当日志更新时，将外层容器滚动到底部
  useEffect(() => {
    if (downloadPageRef.current) {
      downloadPageRef.current.scrollTop = downloadPageRef.current.scrollHeight;
    }
  }, [logs]);

  const openPermissionGuide = (result) => {
    pendingDownloadsRef.current = result?._pendingUrls || [];
    setPermissionGuideKey((key) => key + 1);
    setPermissionIssue({
      targetDirectory: result?.targetDirectory || "",
      protectedFolder: result?.protectedFolder || "",
      platform: result?.platform || "darwin",
      message: result?.message || "",
    });
    setPermissionOpen(true);
  };

  // 顺序下载；遇到权限问题时停下，把剩余地址留到授权后继续
  const runDownloads = async (urls) => {
    const list = urls.filter(Boolean);
    for (let i = 0; i < list.length; i++) {
      const result = await saveFile(list[i]);
      if (result?.code === PERMISSION_DENIED) {
        openPermissionGuide({
          ...result,
          _pendingUrls: list.slice(i),
        });
        return false;
      }
    }
    setPermissionIssue(null);
    return true;
  };

  const handleDownload = async () => {
    const trimmedValue = textareaValue.trim();
    if (!trimmedValue) {
      toast.warn("请输入草稿地址，多个使用回车换行分隔");
      return;
    }

    const valArray = trimmedValue
      .split("\n")
      .map((line) => line.trim())
      .filter(Boolean);
    setLogs([]);
    setPermissionIssue(null);
    setPermissionOpen(false);
    pendingDownloadsRef.current = [];
    await runDownloads(valArray);
  };

  const saveFile = async (value) => {
    // 从URL中提取draft_id
    const urlParams = new URLSearchParams(
      value.includes("?") ? value.split("?")[1] : ""
    );
    const targetId = urlParams.get("draft_id");

    if (!targetId) {
      toast.warn(`${value} 中缺少 draft_id 参数`);
      return { success: false, code: "MISSING_DRAFT_ID" };
    }

    try {
      const jsonData = await electronService.getUrlJsonData(value);
      if (jsonData?.code !== 0 || !jsonData?.files) {
        const message = jsonData?.message
          ? `获取文件列表失败：${jsonData.message}`
          : "获取文件列表失败，请确保您输入的地址可正常访问";
        toast.error(message);
        return { success: false, code: "GET_DRAFT_FAILED", message };
      }

      const matchedFiles = jsonData.files.filter((fileUrl) =>
        fileUrl.includes(targetId)
      );

      if (matchedFiles.length === 0) {
        const message = "未找到包含 draft_id 的文件";
        toast.error(message);
        return { success: false, code: "NO_MATCHED_FILES", message };
      }

      const result = await electronService.saveFile({
        sourceUrl: value,
        remoteFileUrls: matchedFiles,
        targetId,
        isOpenDir: isDownloadOpen,
      });

      // 权限问题由引导弹窗接管，不再弹普通 toast
      if (result?.code === PERMISSION_DENIED) {
        return result;
      }

      if (result?.success === false) {
        toast.error(
          result.message || `获取草稿 ${targetId} 失败，请查看下载日志`
        );
        return result;
      }

      toast.success(`获取草稿 ${targetId} 成功`);
      return result || { success: true };
    } catch (error) {
      toast.error(
        error?.message ? `保存文件失败：${error.message}` : "保存文件失败，请重试"
      );
      return {
        success: false,
        code: "SAVE_FAILED",
        message: error?.message || "",
      };
    }
  };

  const handlePermissionContinue = async () => {
    const urls = pendingDownloadsRef.current;
    pendingDownloadsRef.current = [];
    setPermissionOpen(false);
    if (urls.length === 0) return;
    setIsLoading(true);
    try {
      await runDownloads(urls);
    } finally {
      setIsLoading(false);
    }
  };

  const handleClearLogs = () => setLogs([]);

  return (
    <div className="download-page" ref={downloadPageRef}>
      <div className="container">
        <ExternalWebpage />

        <PermissionBanner
          visible={Boolean(permissionIssue) && !permissionOpen}
          message={
            permissionIssue?.protectedFolder
              ? `需要允许「剪映小助手」访问「${permissionIssue.protectedFolder}」文件夹`
              : permissionIssue?.message
          }
          onOpen={() => setPermissionOpen(true)}
        />

        <Textarea
          value={textareaValue}
          onChange={(val) => setTextareaValue(val)}
        />

        <Tabs
          onTabChange={(content) => setTextareaValue(content)}
          initialContent={textareaValue}
        />

        <DownloadControls
          isOpen={isDownloadOpen}
          isLoading={isLoading}
          onToggle={setIsDownloadOpen}
        />

        <DownloadButton
          onClick={handleDownload}
          isLoading={isLoading}
          setIsLoading={setIsLoading}
          textValue={textareaValue}
        />

        <LogModule logs={logs} onClear={handleClearLogs} />
      </div>

      <PermissionGuide
        key={permissionGuideKey}
        open={permissionOpen}
        targetDirectory={permissionIssue?.targetDirectory || ""}
        protectedFolder={permissionIssue?.protectedFolder || ""}
        platform={permissionIssue?.platform || "darwin"}
        onClose={() => setPermissionOpen(false)}
        onContinue={handlePermissionContinue}
      />
    </div>
  );
}

export default MainPage;