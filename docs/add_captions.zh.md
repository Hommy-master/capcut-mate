# ADD_CAPTIONS API 接口文档

## 🌐 语言切换
[中文版](./add_audios.zh.md) | [English](./add_audios.md)

## 接口信息

```
POST /openapi/capcut-mate/v1/add_captions
```

## 功能描述

向现有草稿中批量添加字幕。该接口用于在指定的时间段内添加字幕到剪映草稿中，支持丰富的字幕样式设置，包括文本颜色、边框颜色、对齐方式、透明度、字体、字体大小、字间距、行间距、缩放和位置调整等。

## 更多文档

📖 更多详细文档和教程请访问：[https://docs.jcaigc.cn](https://docs.jcaigc.cn)

## 请求参数

```json
{
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
  "captions": "[{\"start\":0,\"end\":10000000,\"text\":\"你好，剪映\",\"keyword\":\"好\",\"keyword_color\":\"#457616\",\"keyword_font_size\":15,\"font_size\":15}]",
  "text_color": "#ffffff",
  "border_color": null,
  "alignment": 1,
  "alpha": 1.0,
  "font": null,
  "font_size": 15,
  "letter_spacing": null,
  "line_spacing": null,
  "scale_x": 1.0,
  "scale_y": 1.0,
  "transform_x": 0.0,
  "transform_y": 0.0,
  "style_text": false
}
```

### 参数说明

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| draft_url | string | ✅ | - | 目标草稿的完整URL |
| captions | string | ✅ | - | 字幕信息列表的JSON字符串 |
| text_color | string | ❌ | "#ffffff" | 文本颜色（十六进制） |
| border_color | string | ❌ | null | 边框颜色（十六进制） |
| alignment | integer | ❌ | 1 | 文本对齐方式（0-5） |
| alpha | number | ❌ | 1.0 | 文本透明度（0.0-1.0） |
| font | string | ❌ | null | 字体名称 |
| font_size | integer | ❌ | 15 | 字体大小 |
| letter_spacing | number | ❌ | null | 字间距 |
| line_spacing | number | ❌ | null | 行间距 |
| scale_x | number | ❌ | 1.0 | 水平缩放比例 |
| scale_y | number | ❌ | 1.0 | 垂直缩放比例 |
| transform_x | number | ❌ | 0.0 | X轴位置偏移（像素） |
| transform_y | number | ❌ | 0.0 | Y轴位置偏移（像素） |
| style_text | boolean | ❌ | false | 是否使用样式文本 |
| has_shadow | boolean | ❌ | false | 是否启用文本阴影 |
| shadow_info | object | ❌ | null | 文本阴影参数 |

### captions字段详细说明

captions是一个JSON字符串，包含字幕数组，每个字幕对象包含以下字段：

| 字段名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| start | integer | ✅ | - | 字幕开始时间（微秒） |
| end | integer | ✅ | - | 字幕结束时间（微秒） |
| text | string | ✅ | - | 字幕文本内容 |
| keyword | string | ❌ | null | 关键词（用\|分隔多个关键词） |
| keyword_color | string | ❌ | "#ff7100" | 关键词颜色 |
| keyword_font_size | integer | ❌ | 15 | 关键词字体大小 |
| keyword_border_color | string | ❌ | null | 关键词边框颜色 |
| keyword_has_shadow | boolean | ❌ | false | 是否启用关键词阴影 |
| keyword_shadow_info | object | ❌ | null | 关键词阴影参数（字段同 shadow_info） |
| font_size | integer | ❌ | 15 | 文本字体大小 |
| in_animation | string | ❌ | null | 入场动画 |
| out_animation | string | ❌ | null | 出场动画 |
| loop_animation | string | ❌ | null | 循环动画 |
| in_animation_duration | integer | ❌ | null | 入场动画时长 |
| out_animation_duration | integer | ❌ | null | 出场动画时长 |
| loop_animation_duration | integer | ❌ | null | 循环动画时长 |

### 参数详解

#### 时间参数

- **start**: 字幕在时间轴上的开始时间，单位为微秒（1秒 = 1,000,000微秒）
- **end**: 字幕在时间轴上的结束时间，单位为微秒
- **duration**: 字幕显示时长 = end - start

#### 对齐方式说明

| 值 | 说明 |
|---|------|
| 0 | 左对齐 |
| 1 | 居中对齐 |
| 2 | 右对齐 |
| 3 | 垂直居中 |
| 4 | 垂直左对齐 |
| 5 | 垂直右对齐 |

#### 字体大小参数

- **font_size**: 普通文本（非关键词）的字体大小
  - 默认值：15（仅在caption项中未指定font_size时生效）
  - 建议范围：8-72
  - 注意：如果在caption项中明确指定了font_size，则使用caption项中的值；如果未指定，则使用接口级别的font_size参数值

#### 缩放参数

- **scale_x**: 字幕的水平缩放比例
  - 1.0 = 原始大小
  - 0.5 = 水平缩小到一半
  - 2.0 = 水平放大到两倍

- **scale_y**: 字幕的垂直缩放比例
  - 1.0 = 原始大小
  - 0.5 = 垂直缩小到一半
  - 2.0 = 垂直放大到两倍

#### 位置参数

- **transform_x**: 字幕在X轴方向的位置偏移，单位为像素
  - 正值向右移动
  - 负值向左移动
  - 以画布中心为原点
  - 实际存储时会转换为半画布宽单位（假设画布宽度1920，即除以960）

- **transform_y**: 字幕在Y轴方向的位置偏移，单位为像素
  - 正值向下移动
  - 负值向上移动
  - 以画布中心为原点
  - 实际存储时会转换为半画布高单位（假设画布高度1080，即除以540）

#### 文本阴影参数

`shadow_info` 是一个对象，包含以下字段：

| 字段名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| shadow_alpha | number | ❌ | 1.0 | 阴影不透明度，取值范围为[0, 1] |
| shadow_color | string | ❌ | "#000000" | 阴影颜色（十六进制） |
| shadow_diffuse | number | ❌ | 15.0 | 阴影扩散程度，取值范围为[0, 100] |
| shadow_distance | number | ❌ | 5.0 | 阴影距离，取值范围为[0, 100] |
| shadow_angle | number | ❌ | -45.0 | 阴影角度，取值范围为[-180, 180] |

当 `has_shadow` 设置为 `true` 但未提供 `shadow_info` 时，系统将使用以下默认阴影配置：

```json
{
  "shadow_color": "#000000",
  "shadow_alpha": 0.9,
  "shadow_diffuse": 15,
  "shadow_distance": 5,
  "shadow_angle": -45
}
```

#### 关键词阴影参数

`keyword_has_shadow` / `keyword_shadow_info` 作用于 captions 单项中的关键词高亮范围，字段与接口级 `shadow_info` 完全一致。当 `keyword_has_shadow` 为 `true` 且未提供 `keyword_shadow_info` 时，使用与上文相同的默认阴影配置。有效花字效果启用时，关键词阴影会被禁用（与整段 `has_shadow` 行为一致）。

## 响应格式

### 成功响应 (200)

```json
{
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
  "track_id": "text_track_123",
  "text_ids": ["text_001", "text_002"],
  "segment_ids": ["seg_001", "seg_002"],
  "segment_infos": [
    {
      "id": "seg_001",
      "start": 0,
      "end": 5000000
    },
    {
      "id": "seg_002",
      "start": 5000000,
      "end": 10000000
    }
  ]
}
```

### 响应字段说明

| 字段名 | 类型 | 说明 |
|--------|------|------|
| draft_url | string | 更新后的草稿URL |
| track_id | string | 字幕轨道ID |
| text_ids | array | 字幕ID列表 |
| segment_ids | array | 字幕片段ID列表 |
| segment_infos | array | 片段信息列表 |

### 错误响应 (4xx/5xx)

```json
{
  "detail": "错误信息描述"
}
```

## 使用示例

### cURL 示例

#### 1. 基本字幕添加

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_captions \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "captions": "[{\"start\":0,\"end\":5000000,\"text\":\"你好，剪映\"}]",
    "text_color": "#ffffff",
    "alignment": 1,
    "alpha": 1.0,
    "font_size": 20
  }'
```

#### 2. 多字幕添加

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_captions \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "captions": "[{\"start\":0,\"end\":5000000,\"text\":\"你好，剪映\"},{\"start\":5000000,\"end\":10000000,\"text\":\"欢迎使用字幕功能\"}]",
    "text_color": "#ffffff",
    "alignment": 1,
    "alpha": 1.0,
    "font_size": 16
  }'
```

#### 3. 带样式和位置的字幕

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_captions \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "captions": "[{\"start\":0,\"end\":5000000,\"text\":\"你好，剪映\",\"keyword\":\"好\",\"keyword_color\":\"#ff0000\"]",
    "text_color": "#ffffff",
    "alignment": 1,
    "alpha": 1.0,
    "font_size": 20,
    "scale_x": 1.2,
    "scale_y": 1.2,
    "transform_x": 100.0,
    "transform_y": -50.0
  }'
```

#### 4. 带文本阴影的字幕

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_captions \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "captions": "[{\"start\":0,\"end\":5000000,\"text\":\"你好，剪映\"}]",
    "text_color": "#ffffff",
    "alignment": 1,
    "alpha": 1.0,
    "font_size": 20,
    "has_shadow": true,
    "shadow_info": {
      "shadow_alpha": 0.8,
      "shadow_color": "#000000",
      "shadow_diffuse": 20.0,
      "shadow_distance": 10.0,
      "shadow_angle": -45.0
    }
  }'
```

#### 5. 使用默认文本阴影的字幕

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_captions \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "captions": "[{\"start\":0,\"end\":5000000,\"text\":\"你好，剪映\"}]",
    "text_color": "#ffffff",
    "alignment": 1,
    "alpha": 1.0,
    "font_size": 20,
    "has_shadow": true
  }'
```

## 错误码说明

| 错误码 | 错误信息 | 说明 | 解决方案 |
|--------|----------|------|----------|
| 400 | draft_url是必填项 | 缺少草稿URL参数 | 提供有效的draft_url |
| 400 | captions是必填项 | 缺少字幕信息参数 | 提供有效的captions |
| 400 | 无效的字幕信息，请检查captions字段值是否正确 | 字幕参数校验失败 | 检查字幕参数是否符合要求 |
| 400 | 时间范围无效 | end必须大于start | 确保结束时间大于开始时间 |
| 404 | 草稿不存在 | 指定的草稿URL无效 | 检查草稿URL是否正确 |
| 500 | 字幕添加失败 | 内部处理错误 | 联系技术支持 |

## 注意事项

1. **时间单位**: 所有时间参数使用微秒（1秒 = 1,000,000微秒）
2. **字幕时长**: end 时间必须大于 start 时间
3. **颜色格式**: 颜色值使用十六进制格式，如 "#ffffff"、"#ff0000"
4. **关键词高亮**: 暂未完全实现，目前为预留功能
5. **动画效果**: 暂未完全实现，目前为预留功能
6. **字体支持**: 字体名称需要系统支持或使用默认字体
7. **对齐方式**: 目前仅支持基础对齐方式（0-2），高级对齐方式（3-5）为预留功能
8. **坐标系统**: transform_x 和 transform_y 使用像素值，会自动转换为草稿相对坐标
9. **缩放参数**: scale_x 和 scale_y 建议在合理范围内使用

## 工作流程

1. 验证必填参数（draft_url, captions）
2. 检查时间范围的有效性
3. 从缓存中获取草稿
4. 创建字幕轨道（如果不存在）
5. 遍历字幕信息，创建字幕片段
6. 添加片段到轨道
7. 保存草稿
8. 返回字幕信息

## 相关接口

- [创建草稿](./create_draft.md)
- [添加视频](./add_videos.md)
- [添加音频](./add_audios.md)
- [添加图片](./add_images.md)
- [保存草稿](./save_draft.md)
- [生成视频](./gen_video.md)

---
<div align="right">

📚 **项目资源**  
**GitHub**: [https://github.com/Hommy-master/capcut-mate](https://github.com/Hommy-master/capcut-mate)  
**Gitee**: [https://gitee.com/taohongmin-gitee/capcut-mate](https://gitee.com/taohongmin-gitee/capcut-mate)

</div>