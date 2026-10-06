# ADD_BEAUTY API 接口文档

## 🌐 语言切换
[中文版](./add_beauty.zh.md) | [English](./add_beauty.md)

## 接口信息

```
POST /openapi/capcut-mate/v1/add_beauty
```

## 功能描述

给已有草稿中的视频片段添加人像美化，覆盖剪映「美颜 / 美型 / 美妆 / 美体」四个面板，
对应请求体中的 `skin` / `shape` / `makeup` / `body` 四个分组。
美化素材挂在视频片段上，写入 `materials.effects`（`type=figure`），不是独立特效轨道。

**字段名全部为英文**（取自剪映草稿中的英文标识与海外版剪映文案）；
预设的**取值**沿用剪映预设名，仍为中文（如 `skin_tone: "冷白"`、`look: "淡人妆"`）。
每个分组都可选，滑杆为 0 或预设为空时**不写入**（与剪映「关闭」= 素材缺失一致）；
任一滑杆生效时会自动为该片段补一条 `makeup-root`。
同一片段再次设置同一滑杆时只原地更新强度（保留素材 id），不会重复追加素材。

> ⚠️ **破坏性变更**：v1 起改为分组对象，旧的扁平字段（匀肤…肤色强度）与 `beauty_infos` 已移除。
> 分组名原先为中文（`美颜`/`美型`/`美妆`/`美体`），组内滑杆名也全是中文，现均已改为英文。

## 更多文档

📖 更多详细文档和教程请访问：[https://docs.jcaigc.cn](https://docs.jcaigc.cn)

## 请求参数

```json
{
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
  "segment_ids": ["d62994b4-25fe-422a-a123-87ef05038558"],
  "skin": { "smooth": 52, "whitening": 67, "skin_tone": "冷白", "temperature": 11, "intensity": 60 },
  "shape": { "small_face": 19, "slim": 33 },
  "makeup": { "look": "淡人妆", "intensity": 80 },
  "body": { "small_head": 33, "slim_waist": 60, "smooth": 19, "whitening": 26 }
}
```

### 公共参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| draft_url | string | ✅ | - | 草稿 URL |
| segment_ids | array | ✅ | - | 要应用美化的视频片段 ID 数组 |
| skin | object | ❌ | - | 美颜参数组（剪映「美颜」面板），见下表 |
| shape | object | ❌ | - | 美型参数组（剪映「美型 - 面部」），见下表 |
| makeup | object | ❌ | - | 美妆参数组（剪映「美妆」），见下表 |
| body | object | ❌ | - | 美体参数组（剪映「美体」），见下表 |

### skin（美颜）

| 字段 | 剪映面板名 | 类型 | 默认 | 说明 |
|------|-----------|------|------|------|
| even | 匀肤 | number | 0 | 强度 0-100 |
| plump | 丰盈 | number | 0 | 强度 0-100 |
| smooth | 磨皮 | number | 0 | 强度 0-100（与 `body.smooth` 是两个素材） |
| dewrinkle | 祛法令纹 | number | 0 | 强度 0-100 |
| bright_eye | 亮眼 | number | 0 | 强度 0-100 |
| dark_circle | 祛黑眼圈 | number | 0 | 强度 0-100 |
| whitening | 美白 | number | 0 | 强度 0-100（与 `body.whitening` 是两个素材） |
| white_teeth | 白牙 | number | 0 | 强度 0-100 |
| skin_tone | 肤色 | string | "" | 肤色预设：`冷白` / `暖白`，空字符串表示不应用 |
| temperature | 冷暖 | number | 0 | 肤色冷暖 0-99，仅设置 `skin_tone` 时生效 |
| intensity | 程度 | number | 60 | 肤色程度 0-100，仅设置 `skin_tone` 时生效 |

### shape（美型）—— 剪映「美型 - 面部」

| 字段 | 剪映面板名 | 类型 | 默认 | 说明 |
|------|-----------|------|------|------|
| small_face | 小脸 | number | 0 | 强度 0-100 |
| slim | 瘦脸 | number | 0 | 强度 0-100 |
| v_shape | V脸 | number | 0 | 强度 0-100 |
| jaw | 下颌骨 | number | 0 | 强度 0-100 |
| cheekbone | 颧骨 | number | 0 | 强度 0-100 |
| shorten | 短脸 | number | 0 | 强度 0-100 |
| contour_smooth | 流畅脸 | number | 0 | 强度 0-100 |
| lower | 下庭 | number | 0 | 强度 0-100 |
| middle | 中庭 | number | 0 | 强度 0-100 |
| upper | 上庭 | number | 0 | 强度 0-100 |
| hairline | 发际线 | number | 0 | 强度 0-100 |
| width | 窄脸 | number | 0 | **预留字段，暂不支持**，仅允许 0 |
| chin_length | 下巴长短 | number | 0 | **预留字段，暂不支持**，仅允许 0 |

### makeup（美妆）

| 字段 | 剪映面板名 | 类型 | 默认 | 说明 |
|------|-----------|------|------|------|
| look | 套装 | string | "" | 美妆预设：`淡人妆` / `氧气感`，空字符串表示不应用 |
| intensity | 程度 | number | 80 | 套装程度 0-100，仅设置 `look` 时生效 |

### body（美体）

| 字段 | 剪映面板名 | 类型 | 默认 | 说明 |
|------|-----------|------|------|------|
| small_head | 小头 | number | 0 | 强度 0-100 |
| swan_neck | 天鹅颈 | number | 0 | 强度 0-100 |
| slim_arm | 瘦手臂 | number | 0 | 强度 0-100 |
| straight_shoulder | 直角肩 | number | 0 | 强度 0-100 |
| slim_body | 瘦身 | number | 0 | 强度 0-100 |
| slim_waist | 瘦腰 | number | 0 | 强度 0-100 |
| long_leg | 长腿 | number | 0 | 强度 0-100 |
| plump_breast | 丰胸 | number | 0 | 强度 0-100 |
| slim_hip | 美胯 | number | 0 | 强度 0-100 |
| smooth | 磨皮 | number | 0 | 美体磨皮 0-100（与 `skin.smooth` 是两个素材） |
| whitening | 美白 | number | 0 | 美体美白 0-100（与 `skin.whitening` 是两个素材） |
| wide_shoulder | 宽肩 | number | 0 | **预留字段，暂不支持**，仅允许 0 |

## 写入草稿的映射

| 分组 | category_id | 强度落点 | 归一 |
|------|-------------|----------|------|
| skin 滑杆 | auto-beauty2 | `smooth`/`whitening` 写顶层 `value`，其余写 `adjust_params` | ÷100 |
| skin 肤色 | auto-beauty2 | `face_adjust_params`（ColdWarm + Intensity） | 冷暖 ÷99，程度 ÷100 |
| shape | auto-beauty | `adjust_params`（name 恒为 "0"） | ÷100 |
| makeup | makeup | `face_adjust_params`（face_adjust_whole） | ÷100 |
| body | auto-beauty3 | 顶层 `value` | ÷100 |

- skin、shape、makeup 的滑杆需要算法路径 `algorithm_artifact_path`；`whitening`、全部 body 滑杆、肤色不需要。
- makeup 会写入固定的 11 项 `exclusion_group`，避免与其它妆容部件叠加。
- 所有素材按 `resource_id` 写入，不写本机特效缓存路径；剪映打开草稿时自行下载资源。
- 草稿里效果条的 `name` 字段仍写剪映面板的中文名（如 `"name": "磨皮"`），与接口字段名无关。

### 预设对照

| 预设 | resource_id | 备注 |
|------|-------------|------|
| `skin_tone: 冷白` | 7148720872105185800 | 冷暖 ÷99、程度 ÷100 |
| `skin_tone: 暖白` | 7148720647714116132 | 冷暖默认 0 |
| `look: 淡人妆` | 7376172391774294554 | 槽位 face_id "1" |
| `look: 氧气感` | 7154258998315717150 | 槽位 face_id "0" |

## 响应格式

### 成功响应 (200)

```json
{
  "code": 0,
  "message": "success",
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
  "affected_segments": ["d62994b4-25fe-422a-a123-87ef05038558"],
  "figure_ids": ["figure-id-1", "makeup-root-id"]
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| draft_url | string | 草稿 URL |
| affected_segments | array | 成功应用美化的片段 ID |
| figure_ids | array | 人像美化素材 ID，包含自动补上的 makeup-root |

## 使用示例

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_beauty \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
    "segment_ids": ["d62994b4-25fe-422a-a123-87ef05038558"],
    "skin": { "smooth": 52, "whitening": 67, "skin_tone": "冷白", "temperature": 11, "intensity": 60 },
    "shape": { "small_face": 19, "slim": 33 },
    "makeup": { "look": "淡人妆", "intensity": 80 },
    "body": { "small_head": 33, "slim_waist": 60, "smooth": 19, "whitening": 26 }
  }'
```

## 错误码说明

| 错误码 | 错误信息 | 说明 | 解决方案 |
|--------|----------|------|----------|
| 1001 | 参数校验失败 | 滑杆越界（0-100，冷暖 0-99）、组内出现未知字段（含已废弃的中文键） | 检查请求参数 |
| 2043 | 无效的美颜信息 | 未提供任何有效参数，或参数类型非法 | 至少提供一个非 0 滑杆或有效预设 |
| 2044 | 美颜类型未找到 | 预留字段传了非 0 值、肤色/美妆预设不支持、直接调用时出现未知字段 | 按错误详情改用受支持的名称，或把预留字段传 0 |
| 2045 | 美颜添加失败 | 写入草稿过程出错 | 重试或检查草稿状态 |
| 2001 | 无效的草稿URL | draft_url 无效或草稿不在缓存 | 先创建或下载草稿 |
| 2015 | 片段未找到 | segment_id 不存在 | 检查片段 ID |
| 2016 | 无效的片段类型 | 目标片段不是视频/图片片段 | 只对视频轨道片段应用 |
| 2042 | 草稿锁获取超时 | 同一草稿并发操作 | 稍后重试 |

## 注意事项

1. **只支持视频轨道上的片段**（视频或图片），字幕、音频等片段会失败。
2. **0 表示不写入**：与剪映「关闭」= 素材缺失一致；已写入的滑杆只能改值，暂不支持删除/关闭。
3. **预留字段**：`width`（窄脸）、`chin_length`（下巴长短）、`wide_shoulder`（宽肩）在剪映草稿中没有对应素材资源，传非 0 会返回 2044，请传 0。
4. **skin 与 body 重名**：`smooth`、`whitening` 在两个分组下是不同的素材（resource_id 不同），需按分组设置。
5. **重复调用**：同一片段同一滑杆只更新强度，素材 id 不变。
6. **资源下载**：草稿只写 resource_id，不写本机缓存路径；首次用剪映打开时需联网下载素材。
7. **手绘小脸**（`manual_deformations`）不在本接口范围内。

## 工作流程

1. 按分组收集并校验全部滑杆（0 跳过、预留字段拦截、预设查表）
2. 校验草稿与片段
3. 逐片段写入 `materials.effects` 并挂到 `extra_material_refs`
4. 为每个片段补一条 `makeup-root`
5. 保存草稿并返回素材 ID 列表

## 相关接口

- [创建草稿](./create_draft.zh.md)
- [添加视频](./add_videos.zh.md)

---

<div align="right">

📚 **项目资源**  
**GitHub**: [https://github.com/Hommy-master/capcut-mate](https://github.com/Hommy-master/capcut-mate)  
**Gitee**: [https://gitee.com/taohongmin-gitee/capcut-mate](https://gitee.com/taohongmin-gitee/capcut-mate)

</div>
