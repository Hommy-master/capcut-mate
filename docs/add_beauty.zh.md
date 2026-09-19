# ADD_BEAUTY API 接口文档

## 🌐 语言切换
[中文版](./add_beauty.zh.md) | [English](./add_beauty.md)

## 接口信息

```
POST /openapi/capcut-mate/v1/add_beauty
```

## 功能描述

给已有草稿中的视频片段添加美颜。美颜挂在视频片段上，写入 `materials.effects`（`type=figure`），不是独立特效轨道。

当前支持从剪映草稿核对过的三个滑杆：美白、磨皮、白牙。任一滑杆生效时，会自动为该片段补一条 `makeup-root`。同一片段再次设置同名滑杆时只更新强度，不重复追加素材。

## 更多文档

📖 更多详细文档和教程请访问：[https://docs.jcaigc.cn](https://docs.jcaigc.cn)

## 请求参数

```json
{
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
  "segment_ids": ["d62994b4-25fe-422a-a123-87ef05038558"],
  "beauty_infos": [
    {"name": "美白", "intensity": 60},
    {"name": "磨皮", "intensity": 20},
    {"name": "白牙", "intensity": 17}
  ]
}
```

### 参数说明

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| draft_url | string | ✅ | "" | 目标草稿的完整 URL |
| segment_ids | array | ✅ | [] | 要应用美颜的视频片段 ID |
| beauty_infos | array | ✅ | [] | 美颜滑杆列表 |

### beauty_infos

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| name | string | ✅ | 美颜名称：`美白`、`磨皮`、`白牙` |
| intensity | number | ✅ | 强度，0-100，与剪映滑杆一致 |

写入草稿时强度会除以 100。美白、磨皮写在素材的 `value`；白牙写在 `adjust_params`（`name` 为 `"1"`），顶层 `value` 保持 0。

## 响应参数

```json
{
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
  "affected_segments": ["d62994b4-25fe-422a-a123-87ef05038558"],
  "figure_ids": ["figure-id-1", "makeup-root-id"]
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| draft_url | string | 草稿 URL |
| affected_segments | array | 成功应用美颜的片段 ID |
| figure_ids | array | 美颜素材 ID，包含自动补上的 makeup-root |

## 说明

- 只支持视频轨道上的片段（视频或图片）。字幕、音频等片段会失败。
- 瘦脸、大眼等未在草稿中核对过的滑杆暂不支持，传入会返回美颜类型未找到。
- 美颜资源按 `resource_id` 写入，不写本机特效缓存路径。剪映打开草稿时自行下载资源。
