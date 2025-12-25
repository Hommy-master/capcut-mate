/**
 * 时间格式化工具函数
 */

import type { ConfigType } from "dayjs";
import dayjs from "dayjs";
import { G_EmptyStr } from "./const";

export const DATE_TIME_FORMAT = "YYYY-MM-DD HH:mm:ss";
export const DATE_TIME_MIN_FORMAT = "YYYY-MM-DD HH:mm";
const DATE_FORMAT = "YYYY-MM-DD";
const TIME_FORMAT = "HH:mm:ss";

export function formatToDateTime(
  date: ConfigType = null,
  format = DATE_TIME_FORMAT
): string {
  return date ? dayjs(date).format(format) : G_EmptyStr;
}

export function formatToDateTimeMin(
  date: ConfigType = null,
  format = DATE_TIME_MIN_FORMAT
): string {
  return formatToDateTime(date, format);
}

export function formatToDate(
  date: ConfigType = null,
  format = DATE_FORMAT
): string {
  return date ? dayjs(date).format(format) : G_EmptyStr;
}

export function formatToTime(
  date: ConfigType = null,
  format = TIME_FORMAT
): string {
  return date ? dayjs(date).format(format) : G_EmptyStr;
}

export function formatToUTCDate(date: ConfigType = null): string {
  return date ? dayjs(date).format() : G_EmptyStr;
}

/** 转Date实例 */
export function toDate(date?: ConfigType) {
  return dayjs(date).toDate();
}

/** 转时间戳 */
export function toTimeStamp(date?: ConfigType) {
  return dayjs(date).valueOf();
}

export const dateUtil = dayjs;
