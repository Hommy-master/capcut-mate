import { useCallback, useEffect, useRef, useState } from "react";
import electronService from "../services/electronService";

import "./PermissionGuide.less";

const POLL_INTERVAL_MS = 2000;

/**
 * 草稿目录写入权限引导。
 *
 * macOS 一旦在系统弹窗里点过「不允许」，应用自身无法再次触发系统授权弹窗，
 * 只能引导用户去「系统设置 → 隐私与安全性」里打开开关；本组件会持续用真实写入
 * 探针检测，授权完成后直接允许用户继续下载，无需重启应用。
 */
function PermissionGuide({
  open,
  targetDirectory,
  protectedFolder,
  platform,
  onClose,
  onContinue,
}) {
  const isMac = platform === "darwin";
  const [granted, setGranted] = useState(false);
  const [checking, setChecking] = useState(false);
  const [openedSettings, setOpenedSettings] = useState(false);
  const [showFullDisk, setShowFullDisk] = useState(false);
  const [continuing, setContinuing] = useState(false);
  const [copied, setCopied] = useState(false);
  const [settingsError, setSettingsError] = useState("");
  const primaryButtonRef = useRef(null);
  const copyTimerRef = useRef(null);
  const grantedRef = useRef(false);

  const checkPermission = useCallback(
    async ({ silent = false } = {}) => {
      if (!silent) setChecking(true);
      try {
        // 路径为空时主进程会回退到当前配置的草稿目录
        const result = await electronService.checkDraftPermission(targetDirectory);
        const ok = Boolean(result?.ok);
        grantedRef.current = ok;
        setGranted(ok);
        return ok;
      } catch (error) {
        console.error("检测草稿目录权限失败:", error);
        return false;
      } finally {
        if (!silent) setChecking(false);
      }
    },
    [targetDirectory]
  );

  // 打开期间自动轮询 + 窗口重新聚焦时立即检测
  useEffect(() => {
    if (!open) {
      grantedRef.current = false;
      setGranted(false);
      setChecking(false);
      setOpenedSettings(false);
      setShowFullDisk(false);
      setContinuing(false);
      setCopied(false);
      setSettingsError("");
      return undefined;
    }

    grantedRef.current = false;
    setGranted(false);
    setOpenedSettings(false);
    setShowFullDisk(false);
    setContinuing(false);
    setSettingsError("");
    checkPermission({ silent: true });

    // 已授权后停止轮询，避免持续在草稿目录里创建探针
    const timer = setInterval(() => {
      if (!grantedRef.current) checkPermission({ silent: true });
    }, POLL_INTERVAL_MS);
    const handleFocus = () => {
      if (!grantedRef.current) checkPermission({ silent: true });
    };
    window.addEventListener("focus", handleFocus);
    return () => {
      clearInterval(timer);
      window.removeEventListener("focus", handleFocus);
    };
  }, [open, checkPermission]);

  useEffect(() => {
    if (open) primaryButtonRef.current?.focus();
  }, [open]);

  useEffect(() => {
    if (!open) return undefined;
    const handleKeyDown = (event) => {
      if (event.key === "Escape" && !continuing) onClose?.();
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [open, continuing, onClose]);

  useEffect(
    () => () => {
      if (copyTimerRef.current) clearTimeout(copyTimerRef.current);
    },
    []
  );

  if (!open) return null;

  const folderLabel = protectedFolder
    ? `「${protectedFolder}」文件夹`
    : "草稿目录";
  const handleOpenSettings = async (panel = "files") => {
    try {
      const result = await electronService.openPrivacySettings(panel);
      if (result?.success !== false) {
        setSettingsError("");
        setOpenedSettings(true);
        if (panel === "full-disk") setShowFullDisk(true);
      } else {
        setSettingsError(
          "无法自动打开系统设置，请手动前往「系统设置 → 隐私与安全性 → 文件与文件夹」。"
        );
      }
    } catch (error) {
      console.error("打开系统设置失败:", error);
      setSettingsError(
        "无法自动打开系统设置，请手动前往「系统设置 → 隐私与安全性 → 文件与文件夹」。"
      );
    }
  };

  const handleCopyPath = async () => {
    try {
      await electronService.clipboardWriteText(targetDirectory);
      setCopied(true);
      if (copyTimerRef.current) clearTimeout(copyTimerRef.current);
      copyTimerRef.current = setTimeout(() => setCopied(false), 1600);
    } catch (error) {
      console.error("复制路径失败:", error);
    }
  };

  const handleContinue = async () => {
    if (continuing) return;
    setContinuing(true);
    try {
      await onContinue?.();
    } catch (error) {
      console.error("继续下载失败:", error);
    } finally {
      setContinuing(false);
    }
  };

  return (
    <div className="permission-guide-overlay">
      <div
        className="permission-guide"
        role="dialog"
        aria-modal="true"
        aria-labelledby="permission-guide-title"
        aria-describedby="permission-guide-desc"
      >
        <header className="permission-guide-header">
          <div className="permission-guide-icon" aria-hidden="true">
            <i className="fas fa-folder-open"></i>
            <span className="permission-guide-icon-badge">
              <i className="fas fa-lock"></i>
            </span>
          </div>
          <div className="permission-guide-heading">
            <h2 id="permission-guide-title">
              {isMac ? "无法保存到剪映草稿目录" : "无法写入草稿目录"}
            </h2>
            <p id="permission-guide-desc">
              {isMac
                ? `macOS 出于隐私保护，阻止了「剪映小助手」访问${folderLabel}。这不是草稿的问题，完成一次授权即可恢复正常下载。`
                : "目标目录当前不可写，草稿无法保存。请检查目录权限后重试。"}
            </p>
          </div>
          <button
            type="button"
            className="permission-guide-close"
            aria-label="关闭"
            onClick={onClose}
            disabled={continuing}
          >
            <i className="fas fa-times"></i>
          </button>
        </header>

        {targetDirectory && (
          <div className="permission-guide-path">
            <span className="permission-guide-path-label">目标目录</span>
            <code className="permission-guide-path-value" title={targetDirectory}>
              {targetDirectory}
            </code>
            <button
              type="button"
              className="permission-guide-copy"
              onClick={handleCopyPath}
            >
              <i className={`fas ${copied ? "fa-check" : "fa-copy"}`}></i>
              {copied ? "已复制" : "复制"}
            </button>
          </div>
        )}

        <ol className="permission-guide-steps">
          {isMac ? (
            <>
              <li>
                <span className="permission-guide-step-index">1</span>
                <div className="permission-guide-step-body">
                  <strong>打开系统设置</strong>
                  <p>
                    点击「打开系统设置」，我们会直接定位到「隐私与安全性 →
                    文件与文件夹」。
                  </p>
                </div>
              </li>
              <li>
                <span className="permission-guide-step-index">2</span>
                <div className="permission-guide-step-body">
                  <strong>允许「剪映小助手」访问{folderLabel}</strong>
                  <p>
                    在列表中找到「剪映小助手」，打开右侧开关。若列表中找不到它，
                    请使用下方的「完全磁盘访问权限」。
                  </p>
                </div>
              </li>
              <li>
                <span className="permission-guide-step-index">3</span>
                <div className="permission-guide-step-body">
                  <strong>返回这里继续下载</strong>
                  <p>
                    授权后无需重启，本窗口会自动检测；显示「已获得权限」后点击
                    「继续下载」。
                  </p>
                </div>
              </li>
            </>
          ) : (
            <>
              <li>
                <span className="permission-guide-step-index">1</span>
                <div className="permission-guide-step-body">
                  <strong>检查目录权限</strong>
                  <p>确认当前用户对目标目录拥有读写权限。</p>
                </div>
              </li>
              <li>
                <span className="permission-guide-step-index">2</span>
                <div className="permission-guide-step-body">
                  <strong>排除占用</strong>
                  <p>如果目录或文件正被其他程序占用，请关闭后重试。</p>
                </div>
              </li>
              <li>
                <span className="permission-guide-step-index">3</span>
                <div className="permission-guide-step-body">
                  <strong>重新检测</strong>
                  <p>处理完成后点击「重新检测」。</p>
                </div>
              </li>
            </>
          )}
        </ol>

        {isMac && (
          <div className="permission-guide-alt">
            <button
              type="button"
              className="permission-guide-alt-toggle"
              onClick={() => setShowFullDisk((value) => !value)}
              aria-expanded={showFullDisk}
            >
              <i className={`fas fa-chevron-${showFullDisk ? "down" : "right"}`}></i>
              在列表里找不到「剪映小助手」？
            </button>
            {showFullDisk && (
              <div className="permission-guide-alt-body">
                <p>
                  改用「完全磁盘访问权限」：点击「+」添加应用，或在访达中把
                  「剪映小助手」拖入列表。
                </p>
                <div className="permission-guide-alt-actions">
                  <button
                    type="button"
                    className="permission-guide-link-btn"
                    onClick={() => handleOpenSettings("full-disk")}
                  >
                    <i className="fas fa-arrow-up-right-from-square"></i>
                    打开完全磁盘访问权限
                  </button>
                  <button
                    type="button"
                    className="permission-guide-link-btn"
                    onClick={() => electronService.revealAppInFinder()}
                  >
                    <i className="fas fa-folder-open"></i>
                    在访达中显示应用
                  </button>
                </div>
                <p className="permission-guide-alt-note">
                  提示：完全磁盘访问权限的变更通常需要退出并重新打开应用后生效。
                </p>
              </div>
            )}
          </div>
        )}

        {settingsError && (
          <p className="permission-guide-error" role="alert">
            <i className="fas fa-circle-exclamation"></i>
            {settingsError}
          </p>
        )}

        <div
          className={`permission-guide-status ${granted ? "is-granted" : "is-waiting"}`}
          role="status"
          aria-live="polite"
        >
          <span className="permission-guide-status-dot" aria-hidden="true"></span>
          <span>
            {granted
              ? "已获得文件夹访问权限"
              : checking
                ? "正在检测权限…"
                : openedSettings
                  ? "等待授权中，授权后会自动检测"
                  : "尚未获得访问权限"}
          </span>
        </div>

        <footer className="permission-guide-footer">
          <button
            type="button"
            className="permission-guide-btn is-ghost"
            onClick={onClose}
            disabled={continuing}
          >
            稍后设置
          </button>
          <div className="permission-guide-footer-right">
            <button
              type="button"
              className="permission-guide-btn is-secondary"
              onClick={() => checkPermission()}
              disabled={checking || continuing}
            >
              <i className={`fas ${checking ? "fa-spinner fa-spin" : "fa-rotate-right"}`}></i>
              重新检测
            </button>
            {granted ? (
              <button
                type="button"
                className="permission-guide-btn is-primary"
                onClick={handleContinue}
                disabled={continuing}
                ref={primaryButtonRef}
              >
                <i className={`fas ${continuing ? "fa-spinner fa-spin" : "fa-download"}`}></i>
                {continuing ? "正在继续下载…" : "继续下载"}
              </button>
            ) : isMac ? (
              <button
                type="button"
                className="permission-guide-btn is-primary"
                onClick={() => handleOpenSettings("files")}
                ref={primaryButtonRef}
              >
                <i className="fas fa-arrow-up-right-from-square"></i>
                打开系统设置
              </button>
            ) : null}
          </div>
        </footer>
      </div>
    </div>
  );
}

/**
 * 关闭引导后保留的轻量提示，点击可重新打开授权引导。
 */
export function PermissionBanner({ visible, message, onOpen }) {
  if (!visible) return null;
  return (
    <div className="permission-banner" role="alert">
      <span className="permission-banner-icon" aria-hidden="true">
        <i className="fas fa-lock"></i>
      </span>
      <div className="permission-banner-text">
        <strong>无法写入剪映草稿目录</strong>
        <span>{message || "macOS 尚未授予文件夹访问权限，草稿无法保存。"}</span>
      </div>
      <button type="button" className="permission-banner-action" onClick={onOpen}>
        去授权
        <i className="fas fa-chevron-right"></i>
      </button>
    </div>
  );
}

export default PermissionGuide;
