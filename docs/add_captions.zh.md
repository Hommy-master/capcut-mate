# ADD_CAPTIONS API 接口文档

## 🌐 语言切换
[中文版](./add_captions.zh.md) | [English](./add_captions.md)

## 接口信息

```
POST /openapi/capcut-mate/v1/add_captions
```

## 功能描述

向现有草稿中批量添加字幕。该接口用于在指定的时间段内添加字幕到剪映草稿中，支持丰富的字幕样式设置，包括文本颜色、边框颜色、对齐方式、透明度、字体、字体大小、字间距、行间距、缩放、位置、下划线/斜体/加粗、文本阴影、关键词高亮与关键词阴影、文字动画、花字效果等。

## 更多文档

📖 更多详细文档和教程请访问：[https://docs.jcaigc.cn](https://docs.jcaigc.cn)

## 请求参数

### 接口级参数说明

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| draft_url | string | ✅ | - | 目标草稿的完整 URL，需包含 `draft_id` 查询参数 |
| captions | string | ✅ | - | 字幕信息列表的 **JSON 字符串**（不是 JSON 数组本身） |
| text_color | string | ❌ | `"#ffffff"` | 普通字幕文本颜色，十六进制，如 `#ffffff` |
| border_color | string | ❌ | `null` | 普通字幕描边颜色，十六进制；`null` 表示无描边 |
| alignment | integer | ❌ | `1` | 文本对齐方式：`0` 左对齐，`1` 居中，`2` 右对齐（`3`-`5` 为预留） |
| alpha | number | ❌ | `1.0` | 文本透明度，取值范围 `[0.0, 1.0]`，`1.0` 为不透明 |
| font | string | ❌ | `null` | 字体名称（枚举名、展示名或别名）；`null` 使用默认字体 |
| font_size | integer | ❌ | `15` | 接口级默认字号；当 caption 项未指定 `font_size` 时生效，须 `>= 1` |
| letter_spacing | number | ❌ | `null` | 字间距；`null` 表示使用默认值 `0` |
| line_spacing | number | ❌ | `null` | 行间距；`null` 表示使用默认值 `0` |
| scale_x | number | ❌ | `1.0` | 水平缩放，`1.0` 为原始大小 |
| scale_y | number | ❌ | `1.0` | 垂直缩放，`1.0` 为原始大小 |
| transform_x | number | ❌ | `0.0` | 水平位移（像素），正值向右，负值向左，以画布中心为原点 |
| transform_y | number | ❌ | `0.0` | 垂直位移（像素），正值向下，负值向上，以画布中心为原点 |
| style_text | boolean | ❌ | `false` | 是否使用样式文本（预留开关） |
| underline | boolean | ❌ | `false` | 是否开启文字下划线 |
| italic | boolean | ❌ | `false` | 是否开启文字斜体 |
| bold | boolean | ❌ | `false` | 是否开启文字加粗 |
| has_shadow | boolean | ❌ | `false` | 是否启用**整段字幕**文本阴影 |
| shadow_info | object | ❌ | `null` | 整段字幕阴影参数；`has_shadow=true` 且本字段为 `null` 时使用默认阴影 |
| text_effect | string | ❌ | `null` | 花字效果名称或 `effect_id`；有效花字会重置颜色/描边/阴影相关效果 |

### captions 字段详细说明

`captions` 是一个 JSON 字符串，解析后为字幕对象数组。每个对象字段如下：

| 字段名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| start | integer | ✅ | - | 字幕开始时间（微秒），`1 秒 = 1_000_000 微秒`，须 `>= 0` |
| end | integer | ✅ | - | 字幕结束时间（微秒），必须大于 `start` |
| text | string | ✅ | - | 字幕文本内容，不能为空 |
| keyword | string | ❌ | `null` | 关键词，多个用 `\|` 分隔，如 `"剪映\|字幕"` |
| keyword_color | string | ❌ | `"#ff7100"` | 关键词填充颜色（十六进制） |
| keyword_border_color | string | ❌ | `null` | 关键词描边颜色；未指定时回退使用接口级 `border_color` |
| keyword_font_size | integer | ❌ | `15` | 关键词字号，须 `> 0` |
| keyword_has_shadow | boolean | ❌ | `false` | 是否启用**关键词范围**阴影 |
| keyword_shadow_info | object | ❌ | `null` | 关键词阴影参数，字段同 `shadow_info`；未提供时用默认阴影 |
| font_size | integer | ❌ | `null` | 本条字幕普通文本字号；未指定则使用接口级 `font_size` |
| in_animation | string | ❌ | `null` | 入场动画名称，需与 `get_text_animations` 返回的名称一致，如 `"向上滑动"` |
| out_animation | string | ❌ | `null` | 出场动画名称，如 `"向下滑动"` |
| loop_animation | string | ❌ | `null` | 循环动画名称，如 `"弹幕滚动"` |
| in_animation_duration | integer | ❌ | `null` | 入场动画时长（微秒）；不填则用动画默认时长 |
| out_animation_duration | integer | ❌ | `null` | 出场动画时长（微秒）；不填则用动画默认时长 |
| loop_animation_duration | integer | ❌ | `null` | 循环动画**单次循环**时长（微秒）；不填则用动画默认时长 |

### shadow_info / keyword_shadow_info 字段说明

| 字段名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| shadow_alpha | number | ❌ | `1.0` | 阴影不透明度，取值范围 `[0, 1]` |
| shadow_color | string | ❌ | `"#000000"` | 阴影颜色（十六进制） |
| shadow_diffuse | number | ❌ | `15.0` | 阴影扩散程度，取值范围 `[0, 100]` |
| shadow_distance | number | ❌ | `5.0` | 阴影距离，取值范围 `[0, 100]` |
| shadow_angle | number | ❌ | `-45.0` | 阴影角度，取值范围 `[-180, 180]` |

当 `has_shadow=true`（或 `keyword_has_shadow=true`）且未提供对应 `*_shadow_info` 时，默认阴影为：

```json
{
  "shadow_color": "#000000",
  "shadow_alpha": 0.9,
  "shadow_diffuse": 15,
  "shadow_distance": 5,
  "shadow_angle": -45
}
```

### 参数详解

#### 对齐方式

| 值 | 说明 |
|---|------|
| 0 | 左对齐 |
| 1 | 居中对齐 |
| 2 | 右对齐 |
| 3 | 垂直居中（预留） |
| 4 | 垂直左对齐（预留） |
| 5 | 垂直右对齐（预留） |

#### 花字与阴影的关系

当 `text_effect` 能解析到有效花字时，系统会将 `text_color` 重置为 `#ffffff`、`border_color` 重置为 `null`、`has_shadow` 重置为 `false`，并禁用关键词阴影（`keyword_has_shadow` 不生效）。若需要自定义颜色/阴影，请不要同时传有效花字。

#### 关键词阴影如何生效

`keyword_has_shadow` / `keyword_shadow_info` 与 `keyword_color` / `keyword_border_color` 一样，都作用在**同一条字幕**内，不会新建额外字幕行。

实现上会把字幕拆成互不重叠的 `styles` 分区：普通文字分区 `shadows: []`，关键词分区写入阴影参数，从而尽量只让关键词带阴影。不传阴影相关字段时，仍走原来的「base + 关键词叠加样式」路径，行为与增加阴影功能前一致。

## 完整参数请求示例（含注释）

下列为**全部接口级参数 + captions 全部字段**的示意；`//` 注释仅用于说明，不能直接作为请求体。

```js
{
  // 【必填】目标草稿 URL，必须带 draft_id
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",

  // 【必填】字幕列表 JSON 字符串（下方用数组展示结构，实际请求需序列化为字符串）
  "captions": [
    {
      "start": 0,                              // 【必填】开始时间（微秒）
      "end": 3000000,                          // 【必填】结束时间（微秒），须 > start
      "text": "你好，剪映字幕",                 // 【必填】字幕文本
      "keyword": "剪映|字幕",                   // 【可选】关键词，多个用 | 分隔
      "keyword_color": "#ff7100",              // 【可选】关键词颜色
      "keyword_border_color": "#000000",       // 【可选】关键词描边颜色
      "keyword_font_size": 22,                 // 【可选】关键词字号
      "keyword_has_shadow": true,              // 【可选】是否启用关键词阴影
      "keyword_shadow_info": {                 // 【可选】关键词阴影参数
        "shadow_alpha": 0.85,                  // 阴影不透明度 [0,1]
        "shadow_color": "#000000",             // 阴影颜色
        "shadow_diffuse": 18.0,                // 阴影扩散 [0,100]
        "shadow_distance": 6.0,                // 阴影距离 [0,100]
        "shadow_angle": -45.0                  // 阴影角度 [-180,180]
      },
      "font_size": 18,                         // 【可选】本条普通文本字号
      "in_animation": "向上滑动",               // 【可选】入场动画名称
      "out_animation": "向下滑动",              // 【可选】出场动画名称
      "loop_animation": "弹幕滚动",             // 【可选】循环动画名称
      "in_animation_duration": 500000,         // 【可选】入场动画时长（微秒）
      "out_animation_duration": 500000,        // 【可选】出场动画时长（微秒）
      "loop_animation_duration": 1000000       // 【可选】循环动画单次时长（微秒）
    }
  ],

  "text_color": "#ffffff",                     // 【可选】普通文本颜色
  "border_color": "#333333",                   // 【可选】普通文本描边颜色
  "alignment": 1,                              // 【可选】对齐：0左/1中/2右
  "alpha": 1.0,                                // 【可选】透明度 [0,1]
  "font": "思源黑体",                           // 【可选】字体名称
  "font_size": 15,                             // 【可选】接口级默认字号
  "letter_spacing": 0,                         // 【可选】字间距
  "line_spacing": 0,                           // 【可选】行间距
  "scale_x": 1.0,                              // 【可选】水平缩放
  "scale_y": 1.0,                              // 【可选】垂直缩放
  "transform_x": 0.0,                          // 【可选】水平位移（像素）
  "transform_y": -200.0,                       // 【可选】垂直位移（像素）
  "style_text": false,                         // 【可选】样式文本开关
  "underline": false,                          // 【可选】下划线
  "italic": false,                             // 【可选】斜体
  "bold": true,                                // 【可选】加粗
  "has_shadow": true,                          // 【可选】整段文本阴影开关
  "shadow_info": {                             // 【可选】整段文本阴影参数
    "shadow_alpha": 0.9,
    "shadow_color": "#000000",
    "shadow_diffuse": 15.0,
    "shadow_distance": 5.0,
    "shadow_angle": -45.0
  },
  // 【可选】花字；与自定义颜色/阴影冲突，完整示例中置为 null 以保留阴影效果
  "text_effect": null
}
```

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
      "end": 3000000
    },
    {
      "id": "seg_002",
      "start": 3000000,
      "end": 6000000
    }
  ]
}
```

### 响应字段说明

| 字段名 | 类型 | 说明 |
|--------|------|------|
| draft_url | string | 更新后的草稿 URL |
| track_id | string | 字幕轨道 ID |
| text_ids | array | 字幕素材 ID 列表 |
| segment_ids | array | 字幕片段 ID 列表 |
| segment_infos | array | 片段信息列表（含 `id`/`start`/`end`） |

### 错误响应 (4xx/5xx)

```json
{
  "detail": "错误信息描述"
}
```

## 使用示例

### cURL 示例

#### 1. 完整参数请求（全部必填 + 可选参数）

> 下列 curl 可直接执行：每个参数都给出了合法值。`captions` 必须是 JSON 字符串。本示例将 `text_effect` 设为 `null`，以便整段阴影与关键词阴影生效。

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_captions \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
    "captions": "[{\"start\":0,\"end\":3000000,\"text\":\"你好，剪映字幕\",\"keyword\":\"剪映|字幕\",\"keyword_color\":\"#ff7100\",\"keyword_border_color\":\"#000000\",\"keyword_font_size\":22,\"keyword_has_shadow\":true,\"keyword_shadow_info\":{\"shadow_alpha\":0.85,\"shadow_color\":\"#000000\",\"shadow_diffuse\":18.0,\"shadow_distance\":6.0,\"shadow_angle\":-45.0},\"font_size\":18,\"in_animation\":\"向上滑动\",\"out_animation\":\"向下滑动\",\"loop_animation\":\"弹幕滚动\",\"in_animation_duration\":500000,\"out_animation_duration\":500000,\"loop_animation_duration\":1000000},{\"start\":3000000,\"end\":6000000,\"text\":\"欢迎使用字幕功能\",\"keyword\":\"字幕\",\"keyword_color\":\"#457616\",\"keyword_border_color\":\"#111111\",\"keyword_font_size\":20,\"keyword_has_shadow\":true,\"keyword_shadow_info\":{\"shadow_alpha\":0.9,\"shadow_color\":\"#000000\",\"shadow_diffuse\":15.0,\"shadow_distance\":5.0,\"shadow_angle\":-45.0},\"font_size\":16,\"in_animation\":\"右上弹入\",\"out_animation\":\"右上弹出\",\"loop_animation\":\"VHS\",\"in_animation_duration\":400000,\"out_animation_duration\":400000,\"loop_animation_duration\":800000}]",
    "text_color": "#ffffff",
    "border_color": "#333333",
    "alignment": 1,
    "alpha": 1.0,
    "font": "思源黑体",
    "font_size": 15,
    "letter_spacing": 0,
    "line_spacing": 0,
    "scale_x": 1.0,
    "scale_y": 1.0,
    "transform_x": 0.0,
    "transform_y": -200.0,
    "style_text": false,
    "underline": false,
    "italic": false,
    "bold": true,
    "has_shadow": true,
    "shadow_info": {
      "shadow_alpha": 0.9,
      "shadow_color": "#000000",
      "shadow_diffuse": 15.0,
      "shadow_distance": 5.0,
      "shadow_angle": -45.0
    },
    "text_effect": null
  }'
```

**上述完整请求参数含义速查：**

| 参数 | 示例值 | 含义 |
|------|--------|------|
| draft_url | `...draft_id=2025092811473036584258` | 【必填】目标草稿地址 |
| captions | JSON 字符串（含 2 条字幕） | 【必填】字幕内容与每条字幕的样式/动画/关键词配置 |
| text_color | `#ffffff` | 【可选】普通文本白色 |
| border_color | `#333333` | 【可选】普通文本深灰描边 |
| alignment | `1` | 【可选】居中对齐 |
| alpha | `1.0` | 【可选】完全不透明 |
| font | `思源黑体` | 【可选】字体名称 |
| font_size | `15` | 【可选】接口级默认字号 |
| letter_spacing | `0` | 【可选】字间距 |
| line_spacing | `0` | 【可选】行间距 |
| scale_x / scale_y | `1.0` | 【可选】不缩放 |
| transform_x | `0.0` | 【可选】水平不偏移 |
| transform_y | `-200.0` | 【可选】向上偏移 200 像素 |
| style_text | `false` | 【可选】不启用样式文本开关 |
| underline / italic | `false` | 【可选】无下划线、无斜体 |
| bold | `true` | 【可选】加粗 |
| has_shadow | `true` | 【可选】启用整段阴影 |
| shadow_info.* | 见上 | 【可选】整段阴影详细参数 |
| text_effect | `null` | 【可选】不使用花字，避免覆盖颜色/阴影 |

**captions 内每条字幕字段含义速查：**

| 字段 | 示例值 | 含义 |
|------|--------|------|
| start / end | `0` / `3000000` | 【必填】起止时间（微秒） |
| text | `你好，剪映字幕` | 【必填】字幕文本 |
| keyword | `剪映\|字幕` | 【可选】高亮关键词 |
| keyword_color | `#ff7100` | 【可选】关键词颜色 |
| keyword_border_color | `#000000` | 【可选】关键词描边 |
| keyword_font_size | `22` | 【可选】关键词字号 |
| keyword_has_shadow | `true` | 【可选】启用关键词阴影 |
| keyword_shadow_info.* | 见上 | 【可选】关键词阴影参数 |
| font_size | `18` | 【可选】本条普通文本字号 |
| in_animation | `向上滑动` | 【可选】入场动画 |
| out_animation | `向下滑动` | 【可选】出场动画 |
| loop_animation | `弹幕滚动` | 【可选】循环动画 |
| *_animation_duration | `500000` 等 | 【可选】对应动画时长（微秒） |

#### 2. 仅必填参数

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_captions \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
    "captions": "[{\"start\":0,\"end\":5000000,\"text\":\"你好，剪映\"}]"
  }'
```

#### 3. 关键词高亮 + 关键词阴影

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_captions \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
    "captions": "[{\"start\":0,\"end\":5000000,\"text\":\"你好，剪映\",\"keyword\":\"剪映\",\"keyword_color\":\"#ff0000\",\"keyword_font_size\":22,\"keyword_has_shadow\":true,\"keyword_shadow_info\":{\"shadow_alpha\":0.8,\"shadow_color\":\"#000000\",\"shadow_diffuse\":20.0,\"shadow_distance\":8.0,\"shadow_angle\":-45.0}}]",
    "text_color": "#ffffff",
    "font_size": 16,
    "alignment": 1
  }'
```

#### 4. 整段文本阴影（使用默认 shadow_info）

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_captions \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
    "captions": "[{\"start\":0,\"end\":5000000,\"text\":\"你好，剪映\"}]",
    "text_color": "#ffffff",
    "font_size": 20,
    "has_shadow": true
  }'
```

#### 5. 使用花字效果

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_captions \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
    "captions": "[{\"start\":0,\"end\":5000000,\"text\":\"花字演示\"}]",
    "text_effect": "白字橘色发光花字"
  }'
```

## 错误码说明

| 错误码 | 错误信息 | 说明 | 解决方案 |
|--------|----------|------|----------|
| 400 | draft_url是必填项 | 缺少草稿 URL | 提供有效的 `draft_url` |
| 400 | captions是必填项 | 缺少字幕信息 | 提供有效的 `captions` |
| 400 | 无效的字幕信息 | captions 校验失败 | 检查 JSON 与必填字段 |
| 400 | 时间范围无效 | end 必须大于 start | 修正起止时间 |
| 404 | 草稿不存在 | draft_id 无效或不在缓存中 | 检查草稿 URL |
| 500 | 字幕添加失败 | 内部处理错误 | 联系技术支持 |

## 注意事项

1. **时间单位**：所有时间参数使用微秒（`1 秒 = 1_000_000 微秒`）
2. **captions 格式**：必须是合法 JSON **字符串**，外层再包一层请求 JSON
3. **颜色格式**：十六进制，如 `#ffffff`、`#ff0000`
4. **动画名称**：请通过 `get_text_animations` 获取可用名称
5. **花字名称**：请通过 `get_text_effects` 获取可用名称或 `effect_id`
6. **坐标系统**：`transform_x` / `transform_y` 使用像素，内部会按画布尺寸换算
7. **关键词阴影**：与关键词颜色/描边一样写在同一字幕的 styles 分区内，不另建字幕行；整段阴影仍由 `has_shadow` / `shadow_info` 控制

## 工作流程

1. 验证必填参数（`draft_url`, `captions`）
2. 解析并校验每条字幕
3. 从缓存获取草稿
4. 创建字幕轨道
5. 创建文本片段并应用样式/关键词/动画/花字
6. 保存草稿并返回结果

## 相关接口

- [创建草稿](./create_draft.md)
- [生成字幕信息](./caption_infos.md)
- [获取文字动画](./get_text_animations.md)
- [获取花字效果](./get_text_effects.md)
- [保存草稿](./save_draft.md)
- [生成视频](./gen_video.md)

---
<div align="right">

📚 **项目资源**  
**GitHub**: [https://github.com/Hommy-master/capcut-mate](https://github.com/Hommy-master/capcut-mate)  
**Gitee**: [https://gitee.com/taohongmin-gitee/capcut-mate](https://gitee.com/taohongmin-gitee/capcut-mate)

</div>
