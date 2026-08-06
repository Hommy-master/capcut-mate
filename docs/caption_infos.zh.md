# CAPTION_INFOS API 接口文档

## 🌐 语言切换
[中文版](./caption_infos.zh.md) | [English](./caption_infos.md)

## 接口信息

```
POST /openapi/capcut-mate/v1/caption_infos
```

## 功能描述

根据文本列表与时间线生成字幕信息 JSON 字符串，可直接作为 `add_captions` 的 `captions` 参数使用。支持字体大小、关键词高亮（颜色/描边/字号/阴影）、入场/循环/出场动画及转场配置。

## 更多文档

📖 更多详细文档和教程请访问：[https://docs.jcaigc.cn](https://docs.jcaigc.cn)

## 请求参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| texts | array[string] | ✅ | - | 字幕文本列表，每一项对应一条字幕 |
| timelines | array[object] | ✅ | - | 时间线列表，与 `texts` 按索引一一对应 |
| timelines[].start | integer | ✅ | - | 该条字幕开始时间（微秒），须 `>= 0` |
| timelines[].end | integer | ✅ | - | 该条字幕结束时间（微秒），须大于 `start` |
| font_size | integer | ❌ | `null` | 写入每条字幕的普通文本字号；不传则生成结果中不含该字段 |
| keyword_color | string | ❌ | `null` | 关键词颜色（十六进制），写入每条字幕 |
| keyword_border_color | string | ❌ | `null` | 关键词描边颜色（十六进制），写入每条字幕 |
| keyword_font | string | ❌ | `null` | 关键词字体名称，写入每条字幕 |
| keyword_font_size | integer | ❌ | `null` | 关键词字号，写入每条字幕 |
| keyword_has_shadow | boolean | ❌ | `null` | 是否启用关键词阴影，写入每条字幕 |
| keyword_shadow_info | object | ❌ | `null` | 关键词阴影参数，字段同 `add_captions` 的 `shadow_info` |
| keywords | array[string] | ❌ | `null` | 重点词列表，按索引分配到对应 `texts[i]`；不足时后续文本 `keyword` 为空字符串 |
| in_animation | string | ❌ | `null` | 入场动画名称，如 `"向上滑动"` |
| in_animation_duration | integer | ❌ | `null` | 入场动画时长（微秒） |
| loop_animation | string | ❌ | `null` | 循环动画名称，如 `"弹幕滚动"` |
| loop_animation_duration | integer | ❌ | `null` | 循环动画**单次循环**时长（微秒） |
| out_animation | string | ❌ | `null` | 出场动画名称，如 `"向下滑动"` |
| out_animation_duration | integer | ❌ | `null` | 出场动画时长（微秒） |
| transition | string | ❌ | `null` | 转场名称（写入生成的字幕信息，供后续流程使用） |
| transition_duration | integer | ❌ | `null` | 转场时长（微秒） |

### keyword_shadow_info 字段说明

| 字段名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| shadow_alpha | number | ❌ | `1.0` | 阴影不透明度，取值范围 `[0, 1]` |
| shadow_color | string | ❌ | `"#000000"` | 阴影颜色（十六进制） |
| shadow_diffuse | number | ❌ | `15.0` | 阴影扩散程度，取值范围 `[0, 100]` |
| shadow_distance | number | ❌ | `5.0` | 阴影距离，取值范围 `[0, 100]` |
| shadow_angle | number | ❌ | `-45.0` | 阴影角度，取值范围 `[-180, 180]` |

### 说明

1. `texts` 与 `timelines` 长度不一致时，按**较短长度**截断后继续生成（不会直接报错）。
2. `keywords[i]` 会写入第 `i` 条字幕的 `keyword` 字段；若 `keywords` 比 `texts` 短，后续条目的 `keyword` 为空字符串。
3. 可选参数仅在非 `null` 时写入生成结果。

## 完整参数请求示例（含注释）

下列为**全部必填 + 可选参数**示意；`//` 注释仅用于说明，不能直接作为请求体。

```js
{
  // 【必填】字幕文本列表，每项对应一条字幕
  "texts": [
    "欢迎观看剪映教程",
    "这是一个字幕示例"
  ],

  // 【必填】时间线列表，与 texts 按索引一一对应
  "timelines": [
    {
      "start": 0,                 // 【必填】第 1 条开始时间（微秒）
      "end": 3000000              // 【必填】第 1 条结束时间（微秒）
    },
    {
      "start": 3000000,           // 【必填】第 2 条开始时间（微秒）
      "end": 6000000              // 【必填】第 2 条结束时间（微秒）
    }
  ],

  "font_size": 24,                // 【可选】普通文本字号
  "keyword_color": "#FF5500",     // 【可选】关键词颜色
  "keyword_border_color": "#000000", // 【可选】关键词描边颜色
  "keyword_font": "思源中宋",          // 【可选】关键词字体
  "keyword_font_size": 28,        // 【可选】关键词字号
  "keyword_has_shadow": true,     // 【可选】启用关键词阴影
  "keyword_shadow_info": {        // 【可选】关键词阴影详细参数
    "shadow_alpha": 0.85,         // 阴影不透明度 [0,1]
    "shadow_color": "#000000",    // 阴影颜色
    "shadow_diffuse": 18.0,       // 阴影扩散 [0,100]
    "shadow_distance": 6.0,       // 阴影距离 [0,100]
    "shadow_angle": -45.0         // 阴影角度 [-180,180]
  },
  "keywords": [                   // 【可选】重点词，按索引分配到 texts
    "剪映",
    "字幕"
  ],
  "in_animation": "向上滑动",      // 【可选】入场动画名称
  "in_animation_duration": 500000, // 【可选】入场动画时长（微秒）
  "loop_animation": "弹幕滚动",    // 【可选】循环动画名称
  "loop_animation_duration": 1000000, // 【可选】循环单次时长（微秒）
  "out_animation": "向下滑动",     // 【可选】出场动画名称
  "out_animation_duration": 500000, // 【可选】出场动画时长（微秒）
  "transition": "淡入淡出",        // 【可选】转场名称
  "transition_duration": 300000   // 【可选】转场时长（微秒）
}
```

## 响应格式

### 成功响应 (200)

```json
{
  "infos": "[{\"start\":0,\"end\":3000000,\"text\":\"欢迎观看剪映教程\",\"keyword\":\"剪映\",\"keyword_color\":\"#FF5500\",\"keyword_border_color\":\"#000000\",\"keyword_font\":\"思源中宋\",\"keyword_font_size\":28,\"keyword_has_shadow\":true,\"keyword_shadow_info\":{\"shadow_alpha\":0.85,\"shadow_color\":\"#000000\",\"shadow_diffuse\":18.0,\"shadow_distance\":6.0,\"shadow_angle\":-45.0},\"font_size\":24,\"in_animation\":\"向上滑动\",\"in_animation_duration\":500000,\"loop_animation\":\"弹幕滚动\",\"loop_animation_duration\":1000000,\"out_animation\":\"向下滑动\",\"out_animation_duration\":500000,\"transition\":\"淡入淡出\",\"transition_duration\":300000},{\"start\":3000000,\"end\":6000000,\"text\":\"这是一个字幕示例\",\"keyword\":\"字幕\",\"keyword_color\":\"#FF5500\",\"keyword_border_color\":\"#000000\",\"keyword_font\":\"思源中宋\",\"keyword_font_size\":28,\"keyword_has_shadow\":true,\"keyword_shadow_info\":{\"shadow_alpha\":0.85,\"shadow_color\":\"#000000\",\"shadow_diffuse\":18.0,\"shadow_distance\":6.0,\"shadow_angle\":-45.0},\"font_size\":24,\"in_animation\":\"向上滑动\",\"in_animation_duration\":500000,\"loop_animation\":\"弹幕滚动\",\"loop_animation_duration\":1000000,\"out_animation\":\"向下滑动\",\"out_animation_duration\":500000,\"transition\":\"淡入淡出\",\"transition_duration\":300000}]"
}
```

### 响应字段说明

| 字段名 | 类型 | 说明 |
|--------|------|------|
| infos | string | 字幕信息 JSON 字符串，可直接作为 `add_captions.captions` 使用 |

### 错误响应 (4xx/5xx)

```json
{
  "detail": "错误信息描述"
}
```

## 使用示例

### cURL 示例

#### 1. 完整参数请求（全部必填 + 可选参数）

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/caption_infos \
  -H "Content-Type: application/json" \
  -d '{
    "texts": ["欢迎观看剪映教程", "这是一个字幕示例"],
    "timelines": [
      {"start": 0, "end": 3000000},
      {"start": 3000000, "end": 6000000}
    ],
    "font_size": 24,
    "keyword_color": "#FF5500",
    "keyword_border_color": "#000000",
    "keyword_font": "思源中宋",
    "keyword_font_size": 28,
    "keyword_has_shadow": true,
    "keyword_shadow_info": {
      "shadow_alpha": 0.85,
      "shadow_color": "#000000",
      "shadow_diffuse": 18.0,
      "shadow_distance": 6.0,
      "shadow_angle": -45.0
    },
    "keywords": ["剪映", "字幕"],
    "in_animation": "向上滑动",
    "in_animation_duration": 500000,
    "loop_animation": "弹幕滚动",
    "loop_animation_duration": 1000000,
    "out_animation": "向下滑动",
    "out_animation_duration": 500000,
    "transition": "淡入淡出",
    "transition_duration": 300000
  }'
```

**上述完整请求参数含义速查：**

| 参数 | 示例值 | 含义 |
|------|--------|------|
| texts | `["欢迎观看剪映教程", "这是一个字幕示例"]` | 【必填】两条字幕文本 |
| timelines[0].start / end | `0` / `3000000` | 【必填】第 1 条起止时间（微秒） |
| timelines[1].start / end | `3000000` / `6000000` | 【必填】第 2 条起止时间（微秒） |
| font_size | `24` | 【可选】普通文本字号 |
| keyword_color | `#FF5500` | 【可选】关键词颜色 |
| keyword_border_color | `#000000` | 【可选】关键词描边颜色 |
| keyword_font | `思源中宋` | 【可选】关键词字体 |
| keyword_font_size | `28` | 【可选】关键词字号 |
| keyword_has_shadow | `true` | 【可选】启用关键词阴影 |
| keyword_shadow_info.shadow_alpha | `0.85` | 【可选】关键词阴影不透明度 |
| keyword_shadow_info.shadow_color | `#000000` | 【可选】关键词阴影颜色 |
| keyword_shadow_info.shadow_diffuse | `18.0` | 【可选】关键词阴影扩散 |
| keyword_shadow_info.shadow_distance | `6.0` | 【可选】关键词阴影距离 |
| keyword_shadow_info.shadow_angle | `-45.0` | 【可选】关键词阴影角度 |
| keywords | `["剪映", "字幕"]` | 【可选】按索引分配到对应文本的关键词 |
| in_animation | `向上滑动` | 【可选】入场动画 |
| in_animation_duration | `500000` | 【可选】入场动画时长（微秒） |
| loop_animation | `弹幕滚动` | 【可选】循环动画 |
| loop_animation_duration | `1000000` | 【可选】循环单次时长（微秒） |
| out_animation | `向下滑动` | 【可选】出场动画 |
| out_animation_duration | `500000` | 【可选】出场动画时长（微秒） |
| transition | `淡入淡出` | 【可选】转场名称 |
| transition_duration | `300000` | 【可选】转场时长（微秒） |

#### 2. 仅必填参数

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/caption_infos \
  -H "Content-Type: application/json" \
  -d '{
    "texts": ["Hello World"],
    "timelines": [{"start": 0, "end": 3000000}]
  }'
```

#### 3. 关键词高亮 + 关键词阴影

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/caption_infos \
  -H "Content-Type: application/json" \
  -d '{
    "texts": ["欢迎观看我们的视频", "这是一个精彩示例"],
    "timelines": [
      {"start": 0, "end": 3000000},
      {"start": 3000000, "end": 6000000}
    ],
    "font_size": 24,
    "keyword_color": "#FF5500",
    "keyword_border_color": "#111111",
    "keyword_font": "思源中宋",
    "keyword_font_size": 28,
    "keyword_has_shadow": true,
    "keyword_shadow_info": {
      "shadow_alpha": 0.9,
      "shadow_color": "#000000",
      "shadow_diffuse": 15.0,
      "shadow_distance": 5.0,
      "shadow_angle": -45.0
    },
    "keywords": ["视频", "精彩"]
  }'
```

#### 4. 配合 add_captions 使用

1. 先调用 `caption_infos`，从响应中取出 `infos` 字符串。
2. 将该字符串原样作为 `add_captions` 的 `captions` 参数传入。

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_captions \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
    "captions": "[{\"start\":0,\"end\":3000000,\"text\":\"欢迎观看剪映教程\",\"keyword\":\"剪映\",\"keyword_color\":\"#FF5500\",\"keyword_has_shadow\":true,\"font_size\":24}]",
    "text_color": "#ffffff",
    "alignment": 1
  }'
```

## 错误码说明

| 错误码 | 错误信息 | 说明 | 解决方案 |
|--------|----------|------|----------|
| 400 | texts是必填项 | 缺少文本内容 | 提供非空 `texts` |
| 400 | timelines是必填项 | 缺少时间线 | 提供有效 `timelines` |
| 500 | 字幕信息生成失败 | 内部处理错误 | 联系技术支持 |

## 注意事项

1. **时间单位**：微秒（`1 秒 = 1_000_000 微秒`）
2. **颜色格式**：十六进制，如 `#FF0000`
3. **动画名称**：建议通过 `get_text_animations` 获取可用名称
4. **输出用途**：返回的 `infos` 可直接作为 `add_captions` 的 `captions` 参数
5. **关键词阴影**：本接口只负责写入字段；真正渲染由 `add_captions` 完成

## 工作流程

1. 校验 `texts` / `timelines`
2. 按较短长度对齐两个数组
3. 按索引组装每条字幕信息（含关键词与可选样式/动画）
4. 序列化为 JSON 字符串并返回

## 相关接口

- [创建草稿](./create_draft.md)
- [添加字幕](./add_captions.md)
- [获取文字动画](./get_text_animations.md)
- [保存草稿](./save_draft.md)

---

<div align="right">

📚 **项目资源**  
**GitHub**: [https://github.com/Hommy-master/capcut-mate](https://github.com/Hommy-master/capcut-mate)  
**Gitee**: [https://gitee.com/taohongmin-gitee/capcut-mate](https://gitee.com/taohongmin-gitee/capcut-mate)

</div>
