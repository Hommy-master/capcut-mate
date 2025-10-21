# add_video 接口文档

## 接口概述

添加视频到剪映草稿中，支持视频裁剪、位置调整、缩放、变速、转场、蒙版、背景模糊等功能。

---

## 接口信息

### RESTful API 端点

```
POST /add_video
```

### Content-Type

```
application/json
```

---

## 请求参数

### 请求体 (JSON)

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| **video_url** | string | **是** | - | 视频文件的 URL 地址（必需参数） |
| draft_folder | string | 否 | null | 草稿文件夹路径 |
| draft_id | string | 否 | null | 草稿 ID，不提供则创建新草稿 |
| width | integer | 否 | 1080 | 画布宽度（像素） |
| height | integer | 否 | 1920 | 画布高度（像素） |
| start | number | 否 | 0 | 视频起始时间（秒） |
| end | number | 否 | 0 | 视频结束时间（秒），0 表示到视频末尾 |
| target_start | number | 否 | 0 | 视频在时间轴上的起始位置（秒） |
| duration | number | 否 | null | 视频显示时长（秒），优先级高于 end |

### 位置和缩放参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| transform_x | number | 否 | 0 | X 轴位移，范围 -1.0 到 1.0（相对画布） |
| transform_y | number | 否 | 0 | Y 轴位移，范围 -1.0 到 1.0（相对画布） |
| scale_x | number | 否 | 1 | X 轴缩放比例 |
| scale_y | number | 否 | 1 | Y 轴缩放比例 |

### 播放控制参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| speed | number | 否 | 1.0 | 播放速度，1.0 为正常速度 |
| volume | number | 否 | 1.0 | 音量大小，范围 0.0 到 1.0 |

### 轨道参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| track_name | string | 否 | "video_main" | 视频轨道名称 |
| relative_index | integer | 否 | 0 | 轨道渲染顺序索引 |

### 转场参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| transition | string | 否 | null | 转场效果类型（如 "fade_in", "dissolve" 等） |
| transition_duration | number | 否 | 0.5 | 转场效果持续时间（秒） |

### 蒙版参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| mask_type | string | 否 | null | 蒙版类型 |
| mask_center_x | number | 否 | 0.5 | 蒙版中心 X 坐标（0.0-1.0） |
| mask_center_y | number | 否 | 0.5 | 蒙版中心 Y 坐标（0.0-1.0） |
| mask_size | number | 否 | 1.0 | 蒙版大小（相对屏幕高度） |
| mask_rotation | number | 否 | 0.0 | 蒙版旋转角度（度） |
| mask_feather | number | 否 | 0.0 | 蒙版羽化程度（0.0-1.0） |
| mask_invert | boolean | 否 | false | 是否反转蒙版 |
| mask_rect_width | number | 否 | null | 矩形蒙版宽度 |
| mask_round_corner | number | 否 | null | 矩形蒙版圆角半径 |

### 背景模糊参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| background_blur | integer | 否 | null | 背景模糊级别：1（轻度）、2（中度）、3（强度）、4（最大） |

---

## 响应参数

### 响应体 (JSON)

| 参数名 | 类型 | 说明 |
|--------|------|------|
| success | boolean | 请求是否成功 |
| output | object/string | 成功时返回草稿结果信息 |
| error | string | 失败时的错误信息 |

### 成功响应的 output 字段

| 参数名 | 类型 | 说明 |
|--------|------|------|
| draft_id | string | 草稿唯一标识符 |
| draft_url | string | 草稿预览 URL |

---

## 请求示例

### 示例 1: 基础视频添加

```bash
curl -X POST http://localhost:9001/add_video \
  -H "Content-Type: application/json" \
  -d '{
    "video_url": "https://example.com/video.mp4",
    "start": 0,
    "end": 10
  }'
```

**请求体 (JSON):**

```json
{
  "video_url": "https://example.com/video.mp4",
  "start": 0,
  "end": 10
}
```

### 示例 2: 完整参数视频添加

```bash
curl -X POST http://localhost:9001/add_video \
  -H "Content-Type: application/json" \
  -d '{
    "video_url": "https://example.com/background.mp4",
    "draft_id": "dfd_12345",
    "width": 1920,
    "height": 1080,
    "start": 5,
    "end": 15,
    "target_start": 0,
    "transform_x": 0.2,
    "transform_y": -0.1,
    "scale_x": 1.2,
    "scale_y": 1.2,
    "speed": 1.5,
    "volume": 0.8,
    "track_name": "video_main",
    "transition": "fade_in",
    "transition_duration": 1.0
  }'
```

**请求体 (JSON):**

```json
{
  "video_url": "https://example.com/background.mp4",
  "draft_id": "dfd_12345",
  "width": 1920,
  "height": 1080,
  "start": 5,
  "end": 15,
  "target_start": 0,
  "transform_x": 0.2,
  "transform_y": -0.1,
  "scale_x": 1.2,
  "scale_y": 1.2,
  "speed": 1.5,
  "volume": 0.8,
  "track_name": "video_main",
  "transition": "fade_in",
  "transition_duration": 1.0
}
```

### 示例 3: 带蒙版和背景模糊

```bash
curl -X POST http://localhost:9001/add_video \
  -H "Content-Type: application/json" \
  -d '{
    "video_url": "https://example.com/portrait.mp4",
    "width": 1080,
    "height": 1920,
    "mask_type": "circle",
    "mask_center_x": 0.5,
    "mask_center_y": 0.5,
    "mask_size": 0.8,
    "mask_feather": 0.1,
    "background_blur": 3
  }'
```

**请求体 (JSON):**

```json
{
  "video_url": "https://example.com/portrait.mp4",
  "width": 1080,
  "height": 1920,
  "mask_type": "circle",
  "mask_center_x": 0.5,
  "mask_center_y": 0.5,
  "mask_size": 0.8,
  "mask_feather": 0.1,
  "background_blur": 3
}
```

### 示例 4: Python 请求示例

```python
import requests

url = "http://localhost:9001/add_video"
headers = {
    "Content-Type": "application/json"
}
data = {
    "video_url": "https://example.com/video.mp4",
    "draft_id": "dfd_abc123",
    "start": 0,
    "end": 10,
    "transform_y": -0.5,
    "scale_x": 1.5,
    "scale_y": 1.5,
    "speed": 2.0,
    "volume": 0.6,
    "transition": "dissolve",
    "transition_duration": 0.8
}

response = requests.post(url, json=data, headers=headers)
result = response.json()

print(f"Success: {result['success']}")
if result['success']:
    print(f"Draft ID: {result['output']['draft_id']}")
    print(f"Draft URL: {result['output']['draft_url']}")
else:
    print(f"Error: {result['error']}")
```

---

## 响应示例

### 成功响应

**状态码:** 200 OK

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

### 失败响应 - 缺少必需参数

**状态码:** 200 OK

```json
{
  "success": false,
  "output": "",
  "error": "Hi, the required parameters 'video_url' are missing."
}
```

### 失败响应 - 处理错误

**状态码:** 200 OK

```json
{
  "success": false,
  "output": "",
  "error": "Error occurred while processing video: Invalid video format."
}
```

---

## 错误码说明

| 错误信息 | 说明 | 解决方案 |
|---------|------|---------|
| "Hi, the required parameters 'video_url' are missing." | 缺少必需的 video_url 参数 | 请在请求体中提供 video_url 参数 |
| "Error occurred while processing video: ..." | 视频处理过程中出错 | 检查视频 URL 是否有效，格式是否支持 |

---

## 使用场景

### 场景 1: 添加背景视频

```json
{
  "video_url": "https://example.com/background.mp4",
  "start": 0,
  "end": 30,
  "volume": 0.5
}
```

### 场景 2: 添加画中画视频

```json
{
  "video_url": "https://example.com/pip.mp4",
  "track_name": "video_pip",
  "transform_x": 0.6,
  "transform_y": -0.6,
  "scale_x": 0.3,
  "scale_y": 0.3,
  "relative_index": 1
}
```

### 场景 3: 快进视频片段

```json
{
  "video_url": "https://example.com/timelapse.mp4",
  "start": 10,
  "end": 40,
  "speed": 3.0,
  "volume": 0
}
```

### 场景 4: 视频慢动作效果

```json
{
  "video_url": "https://example.com/action.mp4",
  "start": 5,
  "duration": 10,
  "speed": 0.5,
  "transition": "fade_in",
  "transition_duration": 1.0
}
```

### 场景 5: 竖屏视频添加模糊背景

```json
{
  "video_url": "https://example.com/portrait.mp4",
  "width": 1080,
  "height": 1920,
  "background_blur": 4,
  "scale_x": 0.8,
  "scale_y": 0.8
}
```

---

## 注意事项

1. **必需参数**: `video_url` 是唯一的必需参数，其他参数都有默认值
2. **时间参数**: `start` 和 `end` 的单位都是秒，支持小数
3. **坐标系统**: `transform_x` 和 `transform_y` 使用相对坐标系，范围通常在 -1.0 到 1.0 之间
4. **优先级**: 如果同时提供 `end` 和 `duration`，`duration` 优先级更高
5. **视频格式**: 支持常见视频格式（MP4, MOV, AVI 等）
6. **URL 要求**: video_url 必须是可访问的完整 URL
7. **draft_id**: 如果不提供 draft_id，系统会自动创建新草稿
8. **转场效果**: 需要先查询可用的转场类型，使用 `/get_transition_types` 接口
9. **蒙版类型**: 需要先查询可用的蒙版类型，使用 `/get_mask_types` 接口

---

## 相关接口

- `POST /create_draft` - 创建新草稿
- `POST /save_draft` - 保存草稿
- `GET /get_transition_types` - 获取可用转场类型
- `GET /get_mask_types` - 获取可用蒙版类型
- `POST /add_audio` - 添加音频
- `POST /add_text` - 添加文字
- `POST /add_image` - 添加图片

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
