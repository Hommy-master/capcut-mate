import electronService from "@/services/electronService";

import "./index.css";

// 顶部导航组件
function TopHeader({ onTabChange, selectedTab }) {
  const handleTabClick = (tab) => {
    onTabChange(tab);
  };
  return (
    <div className="top-header">
      <div className="top-nav">
        <div
          className={`top-nav-item logo`}
          onClick={() => handleTabClick("download")}
        >
          剪映小助手(免费客户端)
        </div>
        <div className="top-nav-group">
          <div
            className={`top-nav-item`}
            onClick={() => {
              handleTabClick("download");
              electronService.openExternalUrl("https://ai.luffycity.com/");
            }}
          >
            前往官网
          </div>
          <div
            className={`top-nav-item ${selectedTab === "history" ? "active" : ""}`}
            onClick={() => handleTabClick("history")}
          >
            草稿历史
          </div>
          <div
            className={`top-nav-item ${selectedTab === "config" ? "active" : ""}`}
            onClick={() => handleTabClick("config")}
          >
            配置中心
          </div>
        </div>
      </div>
    </div>
  );
}
export default TopHeader;
