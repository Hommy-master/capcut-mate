import electronService from "../services/electronService";

import { version } from "../../package.json";

export const THEME_COLOR = "#5c89ff"; // --primary-l

export const G_EmptyStr = "-";

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
