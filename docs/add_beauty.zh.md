# ADD_BEAUTY API 接口文档

## 🌐 语言切换
[中文版](./add_beauty.zh.md) | [English](./add_beauty.md)

## 接口信息

```
POST /openapi/capcut-mate/v1/add_beauty
```

## 功能描述

给已有草稿中的视频片段添加美颜。美颜挂在视频片段上，写入 `materials.effects`（`type=figure`），不是独立特效轨道。

支持剪映「美颜」面板中已核对的 10 个参数：匀肤、丰盈、磨皮、祛法令纹、亮眼、祛黑眼圈、美白、白牙、肤色、肤色强度。每个参数都有默认值；滑杆为 0、肤色为空时不写入。任一滑杆生效时，会自动为该片段补一条 `makeup-root`。同一片段再次设置同名滑杆时只更新强度，不重复追加素材。

## 更多文档

📖 更多详细文档和教程请访问：[https://docs.jcaigc.cn](https://docs.jcaigc.cn)

## 请求参数

```json
{
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
  "segment_ids": ["d62994b4-25fe-422a-a123-87ef05038558"],
  "匀肤": 100,
  "丰盈": 100,
  "磨皮": 100,
  "祛法令纹": 100,
  "亮眼": 100,
  "祛黑眼圈": 100,
  "美白": 60,
  "白牙": 100,
  "肤色": "暖白",
  "肤色强度": 60
}
```

### 参数说明

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| draft_url | string | ✅ | "" | 目标草稿的完整 URL |
| segment_ids | array | ✅ | [] | 要应用美颜的视频片段 ID |
| 匀肤 | number | ❌ | 0 | 匀肤强度，0–100 |
| 丰盈 | number | ❌ | 0 | 丰盈强度，0–100 |
| 磨皮 | number | ❌ | 0 | 磨皮强度，0–100 |
| 祛法令纹 | number | ❌ | 0 | 祛法令纹强度，0–100 |
| 亮眼 | number | ❌ | 0 | 亮眼强度，0–100 |
| 祛黑眼圈 | number | ❌ | 0 | 祛黑眼圈强度，0–100 |
| 美白 | number | ❌ | 0 | 美白强度，0–100 |
| 白牙 | number | ❌ | 0 | 白牙强度，0–100 |
| 肤色 | string | ❌ | "" | 肤色预设，空字符串表示不应用；当前支持 `暖白` |
| 肤色强度 | number | ❌ | 60 | 肤色强度，0–100，仅在设置 `肤色` 时生效 |
| beauty_infos | array | ❌ | [] | 兼容旧写法的滑杆列表，可与具名参数同时使用 |

### beauty_infos

| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| name | string | ✅ | - | 美颜名称：`匀肤`、`丰盈`、`磨皮`、`祛法令纹`、`亮眼`、`祛黑眼圈`、`美白`、`白牙`、`肤色`/`暖白` |
| intensity | number | ❌ | 0 | 强度，0–100，与剪映滑杆一致 |

写入草稿时强度会除以 100。美白、磨皮写在素材的 `value`；匀肤、丰盈、祛法令纹、亮眼、祛黑眼圈写在 `adjust_params`（`name` 为 `"0"`）；白牙写在 `adjust_params`（`name` 为 `"1"`）；肤色写在 `face_adjust_params`，导出名称为 `暖白`。

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
- 具名参数为 0 或肤色为空时不会写入对应素材；至少需要提供一个非默认美颜参数或 `beauty_infos`。
