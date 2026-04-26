// import {
//   BrowserRouter as Router,
//   Routes,
//   Route,
//   Navigate,
// } from "react-router-dom";

import "bootstrap/dist/css/bootstrap.min.css";
import "react-toastify/dist/ReactToastify.css";

import "./styles/index.less";

import { ToastContainer } from "react-toastify";

import TopHeader from "./components/Header";
import HistoryPage from "./pages/History";
import MainPage from "./pages/Download";
import ConfigCenter from "./pages/ConfigCenter";
import { useEffect, useState } from "react";
import electronService from "./services/electronService";

import { version } from "../package.json";

function App() {
  const [selectedTab, setSelectedTab] = useState("download");
  const [appVersion, setAppVersion] = useState(version);

  useEffect(() => {
    const fetchAppVersion = async () => {
      try {
        const realVersion = await electronService.getAppVersion();
        if (realVersion) {
          setAppVersion(realVersion);
        }
      } catch (error) {
        console.error("获取应用版本号失败:", error);
      }
    };

    fetchAppVersion();
  }, []);

  const tabMap = {
    download: <MainPage />,
    history: <HistoryPage />,
    config: <ConfigCenter />,
  };
  return (
    <div className="app">
      {/* <Router> */}
        <TopHeader onTabChange={setSelectedTab} selectedTab={selectedTab} />
        <div className="main-content flex-1">
          {tabMap[selectedTab] || <MainPage />}
          {/* <Routes>
            <Route path="*" element={<Navigate replace to="/" />} />
            <Route path="/" element={<MainPage />} />
            <Route path="/history" element={<HistoryPage />} />
            <Route path="/config" element={<ConfigCenter />} />
          </Routes> */}
          <div className="main-content-footer">当前版本号：v{appVersion}</div>
        </div>
        <ToastContainer style={{ top: "55px" }} />
      {/* </Router> */}
    </div>
  );
}

export default App;
