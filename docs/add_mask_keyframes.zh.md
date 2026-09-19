# ADD_MASK_KEYFRAMES API 接口文档

## 🌐 语言切换
[中文版](./add_mask_keyframes.zh.md) | [English](./add_mask_keyframes.md)

## 接口信息

```
POST /openapi/capcut-mate/v1/add_mask_keyframes
```

## 功能描述

给已有蒙版的视频片段添加蒙版关键帧。关键帧写在片段的 `common_keyframes` 上，支持位置（X/Y）、大小（width/height）、羽化、旋转角度。单位与 `add_masks` 一致：位置和大小用像素，羽化用 0–100，旋转用角度。

片段必须已经通过 `add_masks` 添加过蒙版，本接口不会自动创建蒙版，也不会改写蒙版素材的静态 `config`。

## 更多文档

📖 更多详细文档和教程请访问：[https://docs.jcaigc.cn](https://docs.jcaigc.cn)

## 请求参数

```json
{
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
  "keyframes": [
    {"segment_id": "d62994b4-25fe-422a-a123-87ef05038558", "offset": 0, "X": 0, "Y": 0, "width": 540, "height": 540, "feather": 0, "rotation": 0},
    {"segment_id": "d62994b4-25fe-422a-a123-87ef05038558", "offset": 5000000, "X": -360, "Y": -200, "width": 1076, "height": 1071, "feather": 100, "rotation": 180}
  ]
}
```

### 参数说明

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| draft_url | string | ✅ | "" | 目标草稿的完整 URL |
| keyframes | array | ✅ | [] | 蒙版关键帧列表 |

### keyframes

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| segment_id | string | ✅ | 目标视频片段 ID |
| offset | integer | ✅ | 相对片段起点的时间偏移，单位微秒 |
| X | number | ❌ | 蒙版中心 X，像素，相对素材中心，右为正 |
| Y | number | ❌ | 蒙版中心 Y，像素，相对素材中心，下为正 |
| width | number | ❌ | 蒙版宽度，像素 |
| height | number | ❌ | 蒙版高度，像素 |
| feather | number | ❌ | 羽化程度，0–100 |
| rotation | number | ❌ | 旋转角度，单位度 |

`X` / `Y` / `width` / `height` / `feather` / `rotation` 均为可选，但每一项至少提供其中一个。`0` 是有效值。位置或大小动画建议同一 `offset` 同时传两个轴。只传 `X` 则只写入 X 轴位置关键帧；只传 `width` 则只写入 `KFTypeMaskSizeX`。

同一片段、同一属性、同一时间点再次写入会覆盖旧值，不会重复追加。

## 响应参数

```json
{
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
  "keyframes_added": 12,
  "affected_segments": ["d62994b4-25fe-422a-a123-87ef05038558"]
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| draft_url | string | 草稿 URL |
| keyframes_added | integer | 实际写入的草稿属性条数（X/Y、width/height 分别计 1） |
| affected_segments | array | 成功写入关键帧的片段 ID |

## 使用示例

### cURL 示例

#### 1. 位置关键帧

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_mask_keyframes \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "keyframes": [
      {"segment_id": "segment-id", "offset": 0, "X": 0, "Y": 0},
      {"segment_id": "segment-id", "offset": 5000000, "X": -360, "Y": -200}
    ]
  }'
```

#### 2. 大小关键帧

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_mask_keyframes \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "keyframes": [
      {"segment_id": "segment-id", "offset": 0, "width": 540, "height": 540},
      {"segment_id": "segment-id", "offset": 5000000, "width": 1076, "height": 1071}
    ]
  }'
```

#### 3. 羽化 + 旋转

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_mask_keyframes \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "keyframes": [
      {"segment_id": "segment-id", "offset": 0, "feather": 0, "rotation": 0},
      {"segment_id": "segment-id", "offset": 5000000, "feather": 100, "rotation": 180}
    ]
  }'
```

## 错误码说明

| 错误码 | 错误信息 | 说明 | 解决方案 |
|--------|----------|------|----------|
| 2001 | 无效的草稿URL | 草稿不存在或不在缓存中 | 检查 draft_url |
| 2015 | 片段未找到 | segment_id 不存在 | 确认片段 ID |
| 2016 | 无效的片段类型 | 非视频片段 | 只对视频/图片片段调用 |
| 2046 | 无效的蒙版关键帧信息 | 缺少属性、羽化越界或格式错误 | 检查 keyframes |
| 2047 | 片段上未找到遮罩 | 该片段还没有蒙版 | 先调用 add_masks |
| 2048 | 蒙版关键帧添加失败 | 保存草稿失败 | 重试或联系技术支持 |

## 说明

- 必须先调用 [添加遮罩](./add_masks.zh.md)，再添加蒙版关键帧。
- 位置换算使用素材宽高（像素 / 半素材尺寸），不是画布尺寸。
- 大小换算使用素材宽高（`width / 素材宽度`、`height / 素材高度`），与蒙版静态 config 一致。
- 超出片段时长的 `offset` 会被截断到片段末尾。
- 不支持圆角关键帧。

## 相关接口

- [添加遮罩](./add_masks.zh.md)
- [添加关键帧](./add_keyframes.zh.md)
- [保存草稿](./save_draft.zh.md)

---

<div align="right">

📚 **项目资源**  
**GitHub**: [https://github.com/Hommy-master/capcut-mate](https://github.com/Hommy-master/capcut-mate)  
**Gitee**: [https://gitee.com/taohongmin-gitee/capcut-mate](https://gitee.com/taohongmin-gitee/capcut-mate)

</div>
