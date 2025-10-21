# add_image 接口文档

## 接口概述

添加图片到剪映草稿中，支持位置调整、缩放、动画、转场、蒙版、背景模糊等功能。

---

## 接口信息

### RESTful API 端点

```
POST /add_image
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
| **image_url** | string | **是** | - | 图片文件的 URL 地址（必需参数） |
| draft_folder | string | 否 | null | 草稿文件夹路径 |
| draft_id | string | 否 | null | 草稿 ID |
| width | integer | 否 | 1080 | 画布宽度 |
| height | integer | 否 | 1920 | 画布高度 |
| start | number | 否 | 0 | 图片开始时间（秒） |
| end | number | 否 | 3.0 | 图片结束时间（秒） |

### 位置和缩放参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| transform_x | number | 否 | 0 | X 轴位移（-1.0 到 1.0） |
| transform_y | number | 否 | 0 | Y 轴位移（-1.0 到 1.0） |
| scale_x | number | 否 | 1 | X 轴缩放比例 |
| scale_y | number | 否 | 1 | Y 轴缩放比例 |

### 轨道参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| track_name | string | 否 | "image_main" | 图片轨道名称 |
| relative_index | integer | 否 | 0 | 轨道渲染顺序索引 |

### 动画参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| animation | string | 否 | null | 入场动画（向后兼容） |
| animation_duration | number | 否 | 0.5 | 入场动画时长 |
| intro_animation | string | 否 | null | 入场动画（优先级高） |
| intro_animation_duration | number | 否 | 0.5 | 入场动画时长 |
| outro_animation | string | 否 | null | 出场动画 |
| outro_animation_duration | number | 否 | 0.5 | 出场动画时长 |
| combo_animation | string | 否 | null | 组合动画 |
| combo_animation_duration | number | 否 | 0.5 | 组合动画时长 |

### 转场参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| transition | string | 否 | null | 转场效果类型 |
| transition_duration | number | 否 | 0.5 | 转场时长（秒） |

### 蒙版参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| mask_type | string | 否 | null | 蒙版类型 |
| mask_center_x | number | 否 | 0.0 | 蒙版中心 X 坐标 |
| mask_center_y | number | 否 | 0.0 | 蒙版中心 Y 坐标 |
| mask_size | number | 否 | 0.5 | 蒙版大小 |
| mask_rotation | number | 否 | 0.0 | 蒙版旋转角度 |
| mask_feather | number | 否 | 0.0 | 蒙版羽化程度 |
| mask_invert | boolean | 否 | false | 是否反转蒙版 |
| mask_rect_width | number | 否 | null | 矩形蒙版宽度 |
| mask_round_corner | number | 否 | null | 矩形蒙版圆角 |

### 背景模糊参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| background_blur | integer | 否 | null | 背景模糊级别（1-4） |

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

### 示例 1: 基础图片添加

```bash
curl -X POST http://localhost:9001/add_image \
  -H "Content-Type: application/json" \
  -d '{
    "image_url": "https://example.com/photo.jpg"
  }'
```

### 示例 2: 带入场动画的图片

```json
{
  "image_url": "https://example.com/photo.jpg",
  "draft_id": "dfd_12345",
  "start": 0,
  "end": 5,
  "intro_animation": "fade_in",
  "intro_animation_duration": 1.0,
  "outro_animation": "zoom_out",
  "outro_animation_duration": 0.8
}
```

### 示例 3: 画中画效果

```json
{
  "image_url": "https://example.com/pip.png",
  "draft_id": "dfd_12345",
  "track_name": "image_pip",
  "transform_x": 0.6,
  "transform_y": -0.6,
  "scale_x": 0.3,
  "scale_y": 0.3,
  "relative_index": 1
}
```

### 示例 4: 圆形蒙版效果

```json
{
  "image_url": "https://example.com/portrait.jpg",
  "draft_id": "dfd_12345",
  "mask_type": "circle",
  "mask_center_x": 0.5,
  "mask_center_y": 0.5,
  "mask_size": 0.8,
  "mask_feather": 0.1
}
```

### 示例 5: 带转场和背景模糊

```json
{
  "image_url": "https://example.com/landscape.jpg",
  "draft_id": "dfd_12345",
  "start": 3,
  "end": 8,
  "transition": "dissolve",
  "transition_duration": 1.0,
  "background_blur": 3,
  "scale_x": 0.9,
  "scale_y": 0.9
}
```

### 示例 6: Python 完整示例

```python
import requests

url = "http://localhost:9001/add_image"
data = {
    "image_url": "https://example.com/photo.jpg",
    "draft_id": "dfd_abc123",
    "start": 0,
    "end": 5,
    "transform_y": -0.2,
    "scale_x": 1.2,
    "scale_y": 1.2,
    "intro_animation": "slide_in",
    "intro_animation_duration": 1.0,
    "transition": "fade",
    "transition_duration": 0.8
}

response = requests.post(url, json=data)
result = response.json()

print(f"Success: {result['success']}")
if result['success']:
    print(f"Draft ID: {result['output']['draft_id']}")
else:
    print(f"Error: {result['error']}")
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
  "error": "Hi, the required parameters 'image_url' are missing."
}
```

---

## 使用场景

### 场景 1: 封面图片

```json
{
  "image_url": "https://example.com/cover.jpg",
  "start": 0,
  "end": 3,
  "intro_animation": "zoom_in",
  "intro_animation_duration": 1.5
}
```

### 场景 2: 照片墙

```json
{
  "image_url": "https://example.com/photo1.jpg",
  "start": 0,
  "end": 2,
  "transform_x": -0.5,
  "transform_y": -0.5,
  "scale_x": 0.4,
  "scale_y": 0.4
}
```

### 场景 3: Logo 水印

```json
{
  "image_url": "https://example.com/logo.png",
  "start": 0,
  "end": 30,
  "transform_x": 0.8,
  "transform_y": -0.8,
  "scale_x": 0.2,
  "scale_y": 0.2,
  "track_name": "image_watermark"
}
```

### 场景 4: 产品展示

```json
{
  "image_url": "https://example.com/product.png",
  "start": 2,
  "end": 8,
  "intro_animation": "fade_in",
  "combo_animation": "float",
  "outro_animation": "fade_out",
  "background_blur": 2
}
```

---

## 图片格式支持

| 格式 | 扩展名 | 说明 |
|------|--------|------|
| JPEG | .jpg, .jpeg | 有损压缩，文件小 |
| PNG | .png | 支持透明通道 |
| GIF | .gif | 支持动画（仅显示第一帧） |
| WebP | .webp | 现代格式，压缩率高 |
| BMP | .bmp | 无压缩，文件大 |

---

## 注意事项

1. **必需参数**: image_url 是唯一的必需参数
2. **默认时长**: 默认显示 3 秒
3. **坐标系统**: transform_x/y 使用相对坐标（-1.0 到 1.0）
4. **动画优先级**: intro_animation 优先于 animation 参数
5. **透明图片**: PNG 格式支持透明背景
6. **图片尺寸**: 建议使用适当大小的图片，过大会影响性能
7. **URL 要求**: image_url 必须是可访问的完整 URL

---

## 动画类型

可通过以下接口获取可用动画类型：

- `/get_intro_animation_types` - 入场动画
- `/get_outro_animation_types` - 出场动画
- `/get_combo_animation_types` - 组合动画

---

## 相关接口

- `POST /create_draft` - 创建新草稿
- `POST /save_draft` - 保存草稿
- `GET /get_intro_animation_types` - 获取入场动画类型
- `GET /get_transition_types` - 获取转场类型
- `GET /get_mask_types` - 获取蒙版类型
- `POST /add_video` - 添加视频
- `POST /add_text` - 添加文字

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
