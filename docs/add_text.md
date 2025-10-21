# add_text 接口文档

## 接口概述

添加文字到剪映草稿中，支持丰富的文字样式、动画效果、阴影、背景、边框等功能。

---

## 接口信息

### RESTful API 端点

```
POST /add_text
```

### Content-Type

```
application/json
```

---

## 请求参数

### 基础参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| **text** | string | **是** | - | 文字内容（必需参数） |
| **start** | number | **是** | - | 文字开始时间（秒） |
| **end** | number | **是** | - | 文字结束时间（秒） |
| draft_id | string | 否 | null | 草稿 ID |
| width | integer | 否 | 1080 | 画布宽度 |
| height | integer | 否 | 1920 | 画布高度 |

### 文字样式参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| font | string | 否 | "文轩体" | 字体名称 |
| font_color/color | string | 否 | "#FF0000" | 文字颜色（16进制） |
| font_size/size | number | 否 | 8.0 | 文字大小 |
| font_alpha/alpha | number | 否 | 1.0 | 文字透明度（0.0-1.0） |
| vertical | boolean | 否 | false | 是否竖排文字 |
| track_name | string | 否 | "text_main" | 文字轨道名称 |

### 位置和尺寸参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| transform_x | number | 否 | 0 | X 轴位移（-1.0 到 1.0） |
| transform_y | number | 否 | 0 | Y 轴位移（-1.0 到 1.0） |
| fixed_width | number | 否 | -1 | 固定宽度（-1 表示自动） |
| fixed_height | number | 否 | -1 | 固定高度（-1 表示自动） |

### 边框参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| border_alpha | number | 否 | 1.0 | 边框透明度 |
| border_color | string | 否 | "#000000" | 边框颜色 |
| border_width | number | 否 | 0.0 | 边框宽度 |

### 背景参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| background_color | string | 否 | "#000000" | 背景颜色 |
| background_style | integer | 否 | 0 | 背景样式 |
| background_alpha | number | 否 | 0.0 | 背景透明度 |
| background_round_radius | number | 否 | 0.0 | 背景圆角半径 |
| background_height | number | 否 | 0.14 | 背景高度（0.0-1.0） |
| background_width | number | 否 | 0.14 | 背景宽度（0.0-1.0） |
| background_horizontal_offset | number | 否 | 0.5 | 背景水平偏移 |
| background_vertical_offset | number | 否 | 0.5 | 背景垂直偏移 |

### 阴影参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| shadow_enabled | boolean | 否 | false | 是否启用阴影 |
| shadow_alpha | number | 否 | 0.9 | 阴影透明度 |
| shadow_angle | number | 否 | -45.0 | 阴影角度（-180 到 180） |
| shadow_color | string | 否 | "#000000" | 阴影颜色 |
| shadow_distance | number | 否 | 5.0 | 阴影距离 |
| shadow_smoothing | number | 否 | 0.15 | 阴影平滑度 |

### 特效参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| bubble_effect_id | string | 否 | null | 气泡特效 ID |
| bubble_resource_id | string | 否 | null | 气泡资源 ID |
| effect_effect_id | string | 否 | null | 装饰特效 ID |

### 动画参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| intro_animation | string | 否 | null | 入场动画类型 |
| intro_duration | number | 否 | 0.5 | 入场动画时长（秒） |
| outro_animation | string | 否 | null | 出场动画类型 |
| outro_duration | number | 否 | 0.5 | 出场动画时长（秒） |

### 多样式文本参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| text_styles | array | 否 | [] | 多样式文本配置数组 |

**text_styles 数组元素结构:**

```json
{
  "start": 0,
  "end": 5,
  "font": "字体名称",
  "style": {
    "size": 10.0,
    "color": "#FF0000",
    "alpha": 1.0,
    "bold": false,
    "italic": false,
    "underline": false
  },
  "border": {
    "width": 0.0,
    "color": "#000000",
    "alpha": 1.0
  }
}
```

---

## 响应参数

### 响应体 (JSON)

| 参数名 | 类型 | 说明 |
|--------|------|------|
| success | boolean | 请求是否成功 |
| output | object/string | 成功时返回草稿结果信息 |
| error | string | 失败时的错误信息 |

---

## 请求示例

### 示例 1: 基础文字添加

```bash
curl -X POST http://localhost:9001/add_text \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello World",
    "start": 0,
    "end": 5
  }'
```

### 示例 2: 带样式的文字

```json
{
  "text": "标题文字",
  "start": 0,
  "end": 3,
  "draft_id": "dfd_12345",
  "font": "思源黑体",
  "font_color": "#FFD700",
  "font_size": 12.0,
  "transform_y": -0.7,
  "shadow_enabled": true,
  "shadow_color": "#000000",
  "shadow_alpha": 0.8
}
```

### 示例 3: 带背景的文字

```json
{
  "text": "重要提示",
  "start": 2,
  "end": 8,
  "draft_id": "dfd_12345",
  "font_size": 10.0,
  "font_color": "#FFFFFF",
  "background_color": "#FF0000",
  "background_alpha": 0.8,
  "background_round_radius": 10.0,
  "transform_y": 0.8
}
```

### 示例 4: 多样式彩色文字

```json
{
  "text": "彩色文字效果展示",
  "start": 0,
  "end": 5,
  "draft_id": "dfd_12345",
  "text_styles": [
    {
      "start": 0,
      "end": 2,
      "style": {"color": "#FF0000", "size": 10.0}
    },
    {
      "start": 2,
      "end": 4,
      "style": {"color": "#00FF00", "size": 10.0}
    },
    {
      "start": 4,
      "end": 6,
      "style": {"color": "#0000FF", "size": 10.0}
    }
  ]
}
```

### 示例 5: 带入场动画的文字

```json
{
  "text": "欢迎观看",
  "start": 0,
  "end": 3,
  "draft_id": "dfd_12345",
  "font_size": 15.0,
  "intro_animation": "fade_in",
  "intro_duration": 1.0,
  "outro_animation": "fade_out",
  "outro_duration": 0.5
}
```

### 示例 6: Python 完整示例

```python
import requests

url = "http://localhost:9001/add_text"
data = {
    "text": "精彩内容",
    "start": 1,
    "end": 6,
    "draft_id": "dfd_abc123",
    "font": "思源黑体",
    "font_color": "#FFFFFF",
    "font_size": 12.0,
    "transform_y": -0.6,
    "shadow_enabled": True,
    "shadow_alpha": 0.9,
    "shadow_color": "#000000",
    "shadow_distance": 5.0,
    "background_alpha": 0.6,
    "background_color": "#000000",
    "background_round_radius": 8.0,
    "intro_animation": "slide_in",
    "intro_duration": 0.8
}

response = requests.post(url, json=data)
result = response.json()
print(f"Success: {result['success']}")
```

---

## 响应示例

### 成功响应

```json
{
  "success": true,
  "output": {
    "draft_id": "dfd_1234567890abcdef",
    "draft_url": "http://example.com/preview?draft_id=dfd_1234567890abcdef"
  },
  "error": ""
}
```

### 失败响应

```json
{
  "success": false,
  "output": "",
  "error": "Hi, the required parameters 'text', 'start' or 'end' are missing."
}
```

---

## 使用场景

### 场景 1: 视频标题

```json
{
  "text": "旅行VLOG第1集",
  "start": 0,
  "end": 3,
  "font_size": 15.0,
  "font_color": "#FFFFFF",
  "transform_y": -0.7,
  "shadow_enabled": true,
  "intro_animation": "zoom_in"
}
```

### 场景 2: 字幕

```json
{
  "text": "这是一段字幕文字",
  "start": 5,
  "end": 10,
  "font_size": 6.0,
  "font_color": "#FFFFFF",
  "transform_y": 0.8,
  "background_alpha": 0.7,
  "background_color": "#000000"
}
```

### 场景 3: 水印

```json
{
  "text": "© 2025",
  "start": 0,
  "end": 30,
  "font_size": 4.0,
  "font_alpha": 0.5,
  "transform_x": 0.8,
  "transform_y": 0.85
}
```

---

## 注意事项

1. **必需参数**: text, start, end 是必需的
2. **坐标系统**: transform_x/y 使用相对坐标（-1.0 到 1.0）
3. **颜色格式**: 使用 16 进制颜色码，如 "#FF0000"
4. **透明度**: alpha 值范围 0.0（完全透明）到 1.0（完全不透明）
5. **动画类型**: 需先通过 `/get_text_intro_types` 等接口获取可用类型
6. **多样式文本**: text_styles 的 start/end 是字符索引，不是时间
7. **字体支持**: 不同环境支持的字体可能不同

---

## 相关接口

- `GET /get_text_intro_types` - 获取文字入场动画类型
- `GET /get_text_outro_types` - 获取文字出场动画类型
- `GET /get_text_loop_anim_types` - 获取文字循环动画类型
- `GET /get_font_types` - 获取可用字体列表
- `POST /add_subtitle` - 添加字幕（SRT格式）

---

## 更新日志

| 版本 | 日期 | 说明 |
|------|------|------|
| 1.0 | 2025-10-21 | 初始版本 |

---

## 技术支持

如有问题，请联系：
- Email: sguann2023@gmail.com
- GitHub Issues: https://github.com/sun-guannan/CapCutAPI/issues
