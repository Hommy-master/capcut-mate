import { useCallback, useEffect, useRef, useState } from "react";
import electronService from "../services/electronService";

import "./DraftPathGuide.less";

/**
 * 剪映草稿目录设置引导。
 *
 * 草稿目录不存在或指向错误时，剪映不会识别下载下来的草稿。这里提供
 * 「自动检测 / 手动选择」两条路径，选择后由主进程校验目录结构；只有
 * 通过校验的目录才会保存，避免用户以为下载成功、剪映里却看不到。
 */
function DraftPathGuide({
  open,
  status,
  hasPendingDownloads,
  onClose,
  onStatusChange,
  onContinue,
}) {
  const [localStatus, setLocalStatus] = useState(status || null);
  const [action, setAction] = useState(null); // 'auto' | 'manual'
  const [error, setError] = useState(null);
  const [note, setNote] = useState("");
  const [copied, setCopied] = useState(false);
  const autoButtonRef = useRef(null);
  const primaryButtonRef = useRef(null);
  const copyTimerRef = useRef(null);

  const busy = Boolean(action);
  const ready = Boolean(localStatus?.ready);
  const needsPermission = localStatus?.reason === "needs_permission";

  // 每次打开都从最新状态开始，清掉上一次的错误/提示
  useEffect(() => {
    if (!open) return;
    setLocalStatus(status || null);
    setError(null);
    setNote("");
    setAction(null);
    setCopied(false);
  }, [open]); // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => {
    if (status) setLocalStatus(status);
  }, [status]);

  useEffect(() => {
    if (open) autoButtonRef.current?.focus();
  }, [open]);

  useEffect(() => {
    if (!open) return undefined;
    const handleKeyDown = (event) => {
      if (event.key === "Escape" && !busy) onClose?.();
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [open, busy, onClose]);

  useEffect(
    () => () => {
      if (copyTimerRef.current) clearTimeout(copyTimerRef.current);
    },
    []
  );

  const refreshStatus = useCallback(async () => {
    const next = await electronService.getDraftDirectoryStatus();
    if (next) {
      setLocalStatus(next);
      onStatusChange?.(next);
    }
    return next;
  }, [onStatusChange]);

  const handleAutoDetect = async () => {
    if (busy) return;
    setAction("auto");
    setError(null);
    setNote("");
    try {
      const result = await electronService.autoDetectDraftPath();
      if (result?.success) {
        const next = await refreshStatus();
        if (result.needsPermission || next?.reason === "needs_permission") {
          setNote("路径已保存。下载时如提示授权，按引导允许访问即可。");
        } else if (next?.ready) {
          setNote("已找到剪映草稿目录，剪映可以识别新下载的草稿了");
        } else {
          setNote("目录已保存，但暂时无法确认它是否是剪映草稿目录");
        }
      } else {
        setError({
          title: "没有找到剪映草稿目录",
          detail:
            "请先打开一次剪映，等首页加载完成后再点「自动检测」；也可以直接手动选择目录。",
        });
      }
    } catch (err) {
      setError({
        title: "自动检测失败",
        detail: err?.message || "请稍后重试，或手动选择草稿目录。",
      });
    } finally {
      setAction(null);
    }
  };

  const handleManualSelect = async () => {
    if (busy) return;
    setAction("manual");
    setError(null);
    setNote("");
    try {
      const result = await electronService.updateDraftPath();
      if (result?.success) {
        const next = await refreshStatus();
        if (result.corrected) {
          setNote(`已自动定位到剪映草稿目录：${result.targetDirectory}`);
        } else if (result.needsPermission || next?.reason === "needs_permission") {
          setNote("路径已保存。下载时如提示授权，按引导允许访问即可。");
        } else {
          setNote("剪映草稿目录设置成功");
        }
      } else if (result?.code !== "CANCELED") {
        setError({
          title:
            result?.code === "NOT_DRAFT_ROOT"
              ? "这不是剪映草稿目录"
              : "目录设置失败",
          detail:
            result?.message ||
            "请选择包含 root_meta_info.json 的 com.lveditor.draft 文件夹。",
          selectedPath: result?.selectedPath || "",
        });
      }
    } catch (err) {
      setError({
        title: "目录设置失败",
        detail: err?.message || "请稍后重试。",
      });
    } finally {
      setAction(null);
    }
  };

  const handleCopyPath = async () => {
    const value = localStatus?.targetDirectory || localStatus?.defaultPath || "";
    if (!value) return;
    try {
      await electronService.clipboardWriteText(value);
      setCopied(true);
      if (copyTimerRef.current) clearTimeout(copyTimerRef.current);
      copyTimerRef.current = setTimeout(() => setCopied(false), 1600);
    } catch (err) {
      console.error("复制路径失败:", err);
    }
  };

  if (!open) return null;

  const statusTone = ready
    ? needsPermission
      ? "is-warning"
      : "is-ready"
    : "is-warning";
  const statusText =
    action === "auto"
      ? "正在查找剪映草稿目录…"
      : action === "manual"
        ? "请在弹出的窗口中完成选择…"
        : ready
          ? needsPermission
            ? "路径已保存，待完成文件夹授权"
            : "目录有效，剪映可以识别新草稿"
          : localStatus?.reason === "missing"
            ? "之前设置的草稿目录已不存在"
            : localStatus?.reason === "not_draft_root"
              ? "当前目录不是剪映草稿目录"
              : "尚未设置剪映草稿目录";

  const platformLabel =
    localStatus?.platform === "darwin"
      ? "macOS 默认位置"
      : localStatus?.platform === "win32"
        ? "Windows 默认位置"
        : "剪映默认草稿位置";
  const defaultPath = localStatus?.defaultPath || "";

  return (
    <div className="draft-guide-overlay">
      <div
        className={`draft-guide ${ready ? "is-ready" : ""}`}
        role="dialog"
        aria-modal="true"
        aria-labelledby="draft-guide-title"
        aria-describedby="draft-guide-desc"
      >
        <header className="draft-guide-header">
          <div className="draft-guide-icon" aria-hidden="true">
            <i className="fas fa-folder-tree"></i>
            <span className="draft-guide-icon-badge">
              <i className={`fas ${ready ? "fa-check" : "fa-location-dot"}`}></i>
            </span>
          </div>
          <div className="draft-guide-heading">
            <h2 id="draft-guide-title">
              {ready ? "剪映草稿目录" : "设置剪映草稿目录"}
            </h2>
            <p id="draft-guide-desc">
              剪映只识别它自己草稿根目录下的草稿。完成设置后，下载的草稿会自动出现在剪映首页。
            </p>
          </div>
          <button
            type="button"
            className="draft-guide-close"
            aria-label="关闭"
            onClick={onClose}
            disabled={busy}
          >
            <i className="fas fa-times"></i>
          </button>
        </header>

        <div
          className={`draft-guide-status ${statusTone}`}
          role="status"
          aria-live="polite"
        >
          <span className="draft-guide-status-icon" aria-hidden="true">
            <i
              className={`fas ${
                busy
                  ? "fa-spinner fa-spin"
                  : ready
                    ? needsPermission
                      ? "fa-lock"
                      : "fa-circle-check"
                    : "fa-circle-exclamation"
              }`}
            ></i>
          </span>
          <span>{statusText}</span>
        </div>

        {localStatus?.targetDirectory && (
          <div className="draft-guide-path">
            <span className="draft-guide-path-label">当前目录</span>
            <code className="draft-guide-path-value" title={localStatus.targetDirectory}>
              {localStatus.targetDirectory}
            </code>
            <button
              type="button"
              className="draft-guide-copy"
              onClick={handleCopyPath}
            >
              <i className={`fas ${copied ? "fa-check" : "fa-copy"}`}></i>
              {copied ? "已复制" : "复制"}
            </button>
          </div>
        )}

        <div className="draft-guide-actions">
          <button
            type="button"
            className="draft-guide-action is-primary"
            onClick={handleAutoDetect}
            disabled={busy}
            ref={autoButtonRef}
          >
            <span className="draft-guide-action-icon" aria-hidden="true">
              <i
                className={`fas ${
                  action === "auto" ? "fa-spinner fa-spin" : "fa-magnifying-glass-location"
                }`}
              ></i>
            </span>
            <span className="draft-guide-action-body">
              <strong>
                自动检测
                <em className="draft-guide-action-badge">推荐</em>
              </strong>
              <span>在本机查找剪映创建的草稿目录</span>
            </span>
            <i className="fas fa-chevron-right draft-guide-action-chevron"></i>
          </button>

          <button
            type="button"
            className="draft-guide-action"
            onClick={handleManualSelect}
            disabled={busy}
          >
            <span className="draft-guide-action-icon is-plain" aria-hidden="true">
              <i
                className={`fas ${
                  action === "manual" ? "fa-spinner fa-spin" : "fa-folder-open"
                }`}
              ></i>
            </span>
            <span className="draft-guide-action-body">
              <strong>手动选择</strong>
              <span>已知位置时，直接指定文件夹</span>
            </span>
            <i className="fas fa-chevron-right draft-guide-action-chevron"></i>
          </button>
        </div>

        {error && (
          <div className="draft-guide-error" role="alert">
            <i className="fas fa-circle-exclamation" aria-hidden="true"></i>
            <div className="draft-guide-error-body">
              <strong>{error.title}</strong>
              <p>{error.detail}</p>
              {error.selectedPath && (
                <code className="draft-guide-error-path" title={error.selectedPath}>
                  {error.selectedPath}
                </code>
              )}
            </div>
          </div>
        )}

        {note && (
          <div className="draft-guide-note" role="status">
            <i className="fas fa-circle-check" aria-hidden="true"></i>
            <span>{note}</span>
          </div>
        )}

        <div className="draft-guide-why">
          <i className="fas fa-circle-info" aria-hidden="true"></i>
          <p>
            <strong>为什么一定要设置？</strong>
            剪映启动时只扫描自己的草稿根目录。目录不正确时，草稿虽然下载成功，剪映首页也不会出现。
          </p>
        </div>

        {defaultPath && (
          <details className="draft-guide-default">
            <summary>
              <i className="fas fa-chevron-right" aria-hidden="true"></i>
              找不到目录？查看 {platformLabel}
            </summary>
            <div className="draft-guide-default-body">
              <code title={defaultPath}>{defaultPath}</code>
              <p>
                如果该文件夹不存在，请先打开一次剪映，让剪映自动创建草稿目录，再回来设置。
              </p>
            </div>
          </details>
        )}

        <footer className="draft-guide-footer">
          <button
            type="button"
            className="draft-guide-btn is-ghost"
            onClick={onClose}
            disabled={busy}
          >
            稍后设置
          </button>
          <div className="draft-guide-footer-right">
            {ready && (
              <button
                type="button"
                className="draft-guide-btn is-primary"
                onClick={hasPendingDownloads ? onContinue : onClose}
                disabled={busy}
                ref={primaryButtonRef}
              >
                <i
                  className={`fas ${hasPendingDownloads ? "fa-download" : "fa-check"}`}
                ></i>
                {hasPendingDownloads ? "继续下载" : "完成"}
              </button>
            )}
          </div>
        </footer>
      </div>
    </div>
  );
}

/**
 * 关闭设置引导后保留在下载页顶部的提示条，点击可重新打开引导。
 */
export function DraftPathBanner({ visible, status, onOpen }) {
  if (!visible) return null;

  const configured = Boolean(status?.configured);
  const title = configured ? "剪映草稿目录不可用" : "还差一步：设置剪映草稿目录";
  const description = configured
    ? status?.reason === "missing"
      ? "之前设置的剪映草稿目录已不存在，请重新选择。"
      : "当前指向的文件夹不是剪映草稿目录，剪映将无法看到下载的草稿。"
    : "下载的草稿会写入剪映的草稿目录。完成设置后，剪映才能自动识别新草稿。";

  return (
    <div className={`draft-path-banner ${configured ? "is-warning" : ""}`} role="alert">
      <span className="draft-path-banner-icon" aria-hidden="true">
        <i className="fas fa-folder-plus"></i>
      </span>
      <div className="draft-path-banner-text">
        <strong>{title}</strong>
        <span>{description}</span>
      </div>
      <button type="button" className="draft-path-banner-action" onClick={onOpen}>
        去设置
        <i className="fas fa-chevron-right" aria-hidden="true"></i>
      </button>
    </div>
  );
}

export default DraftPathGuide;
