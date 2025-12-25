import { useEffect, useState } from "react";
import electronService from "../../services/electronService";

import "./index.css";
import { toast } from "react-toastify";

const ConfigCenter = () => {
  const [config, setConfig] = useState({ targetDirectory: "" });

  const loadConfig = async () => {
    try {
      const configData = await electronService.getConfigData();
      setConfig(configData || { targetDirectory: "" });
    } catch (error) {
      console.error("加载配置失败:", error);
    }
  };

  // 加载配置
  useEffect(() => {
    loadConfig();
  }, []);

  const handleSelectPath = async () => {
    try {
      const { success, targetDir, error } =
        await electronService.updateDraftPath();
      if (success) {
        setConfig({ targetDirectory: targetDir });
    //   } else if (error) {
    //     toast.info(error);
      }
    } catch (error) {
      toast.error("选择路径失败:", error);
    }
  };

  return (
    <div className="set-page">
      <div className="container">
        <div className="card">
          <div className="card-body">
            <div className="section-title">剪映路径设置</div>
            {/* <div className="setting-item"> */}
            <div className="setting-path-input-group flex item-center">
              <label className="setting-path-label">当前路径：</label>
              <input
                type="text"
                className="setting-draft-path-input"
                placeholder="请选择草稿保存路径"
                value={config.targetDirectory || ""}
                readOnly
                onClick={handleSelectPath}
              />
              <button className="btn btn-small" onClick={handleSelectPath}>
                选择...
              </button>
            </div>
            <p className="settings-hint">
              设置剪映软件的草稿路径以导入草稿至剪映
            </p>
            {/* </div> */}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ConfigCenter;
