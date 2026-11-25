import { useEffect, useState } from "react";
import electronService from "../../services/electronService";
import DraftPathGuide from "../../components/DraftPathGuide";

import "./index.less";

const ConfigCenter = () => {
  const [status, setStatus] = useState(null);
  const [guideOpen, setGuideOpen] = useState(false);

  const loadStatus = async () => {
    try {
      const next = await electronService.getDraftDirectoryStatus();
      setStatus(next || null);
    } catch (error) {
      console.error("加载草稿目录状态失败:", error);
    }
  };

  // 加载草稿目录状态
  useEffect(() => {
    loadStatus();
  }, []);

  const ready = Boolean(status?.ready);
  const needsPermission = status?.reason === "needs_permission";
  const configured = Boolean(status?.targetDirectory);

  const badgeText = ready
    ? needsPermission
      ? "待授权"
      : "已就绪"
    : configured
      ? "目录不可用"
      : "未设置";

  const description = ready
    ? needsPermission
      ? "路径已保存，但 macOS 尚未允许本应用访问该文件夹，首次下载时会引导完成授权。"
      : "目录有效，下载的草稿会被剪映自动识别。"
    : status?.reason === "missing"
      ? "之前设置的草稿目录已不存在，请重新选择。"
      : status?.reason === "not_draft_root"
        ? "当前路径不是剪映草稿目录，剪映将无法看到下载的草稿。"
        : "尚未设置剪映草稿目录，下载前需要先完成设置。";

  return (
    <div className="set-page">
      <div className="container">
        <div className="card config-card">
          <div className="card-body">
            <div className="section-title">剪映草稿目录</div>

            <div
              className={`config-status ${
                ready && !needsPermission ? "is-ready" : "is-warning"
              }`}
            >
              <span className="config-status-icon" aria-hidden="true">
                <i
                  className={`fas ${
                    ready
                      ? needsPermission
                        ? "fa-lock"
                        : "fa-circle-check"
                      : "fa-circle-exclamation"
                  }`}
                ></i>
              </span>
              <div className="config-status-text">
                <strong>草稿目录状态</strong>
                <span>{description}</span>
              </div>
              <span className="config-status-badge">{badgeText}</span>
            </div>

            <div className="config-path-row">
              <span className="config-path-label">当前目录</span>
              <code
                className={`config-path-value ${configured ? "" : "is-empty"}`}
                title={status?.targetDirectory || ""}
              >
                {status?.targetDirectory || "尚未设置"}
              </code>
              <button
                type="button"
                className="btn btn-small config-path-action"
                onClick={() => setGuideOpen(true)}
              >
                <i className="fas fa-folder-open"></i>
                {configured ? "更换目录" : "去设置"}
              </button>
            </div>

            <p className="config-hint">
              下载的草稿会写入此目录。只有指向剪映的草稿根目录
              （com.lveditor.draft），剪映才能自动识别新草稿。
            </p>

            {!ready && status?.defaultPath && (
              <div className="config-tip">
                <i className="fas fa-circle-info" aria-hidden="true"></i>
                <div className="config-tip-body">
                  <strong>不知道目录在哪？</strong>
                  <p>剪映默认草稿位置：</p>
                  <code title={status.defaultPath}>{status.defaultPath}</code>
                  <p>
                    若该文件夹不存在，请先打开一次剪映，让剪映自动创建草稿目录。
                  </p>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      <DraftPathGuide
        open={guideOpen}
        status={status}
        hasPendingDownloads={false}
        onClose={() => {
          setGuideOpen(false);
          loadStatus();
        }}
        onStatusChange={setStatus}
      />
    </div>
  );
};

export default ConfigCenter;
