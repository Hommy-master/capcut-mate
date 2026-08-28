import electronService from "../services/electronService";

import { version } from "../../package.json";

export const THEME_COLOR = "#5c89ff"; // --primary-l

export const G_EmptyStr = "-";

export const PROJECT_LINKS = {
  discussions: "https://github.com/Hommy-master/capcut-mate/discussions",
  docs: "https://docs.jcaigc.cn",
  github: "https://github.com/Hommy-master/capcut-mate",
  gitee: "https://gitee.com/taohongmin-gitee/capcut-mate",
};

export const fetchAppVersion = async () => {
    let appVersion = version;
  try {
    const realVersion = await electronService.getAppVersion();
    if (realVersion) {
      return realVersion;
    }
  } catch (error) {
    console.error("获取应用版本号失败:", error);
  }
  return appVersion;
};
