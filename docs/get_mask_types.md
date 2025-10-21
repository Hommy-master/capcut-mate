# get_mask_types 接口文档

## 接口概述

获取所有支持的蒙版类型列表，用于视频和图片的蒙版效果。

---

## 接口信息

### RESTful API 端点

```
GET /get_mask_types
```

### Content-Type

```
application/json
```

---

## 请求参数

### 无需请求参数

此接口不需要任何请求参数。

---

## 响应参数

### 响应体 (JSON)

| 参数名 | 类型 | 说明 |
|--------|------|------|
| success | boolean | 请求是否成功 |
| output | array | 蒙版类型列表 |
| error | string | 失败时的错误信息 |

### output 数组中每个元素的结构

| 参数名 | 类型 | 说明 |
|--------|------|------|
| name | string | 蒙版类型名称 |

---

## 请求示例

### 示例 1: 获取蒙版类型列表

```bash
curl -X GET http://localhost:9001/get_mask_types
```

### 示例 2: Python 请求示例

```python
import requests

url = "http://localhost:9001/get_mask_types"
response = requests.get(url)
result = response.json()

print(f"Success: {result['success']}")
if result['success']:
    print(f"Total mask types: {len(result['output'])}")
    for mask in result['output']:
        print(f"  - {mask['name']}")
else:
    print(f"Error: {result['error']}")
```

### 示例 3: JavaScript 请求示例

```javascript
fetch('http://localhost:9001/get_mask_types')
  .then(response => response.json())
  .then(result => {
    if (result.success) {
      console.log('Mask types:', result.output);
      result.output.forEach(type => {
        console.log(`- ${type.name}`);
      });
    } else {
      console.error('Error:', result.error);
    }
  });
```

---

## 响应示例

### 成功响应

**状态码:** 200 OK

```json
{
  "success": true,
  "output": [
    { "name": "circle" },
    { "name": "rectangle" },
    { "name": "heart" },
    { "name": "star" },
    { "name": "diamond" },
    { "name": "hexagon" },
    { "name": "oval" },
    { "name": "rounded_rectangle" },
    { "name": "triangle" },
    { "name": "mirror_split" },
    { "name": "horizontal_split" },
    { "name": "vertical_split" }
  ],
  "error": ""
}
```

### 失败响应

**状态码:** 200 OK

```json
{
  "success": false,
  "output": "",
  "error": "Error occurred while getting mask types: Internal error."
}
```

---

## 常见蒙版类型说明

| 蒙版名称 | 形状 | 说明 | 适用场景 |
|---------|------|------|---------|
| circle | 圆形 | 标准圆形蒙版 | 人物特写、聚焦效果 |
| rectangle | 矩形 | 标准矩形蒙版 | 画框效果、窗口视图 |
| heart | 心形 | 爱心形状蒙版 | 浪漫场景、情感表达 |
| star | 星形 | 五角星形蒙版 | 重点突出、装饰效果 |
| diamond | 菱形 | 菱形蒙版 | 时尚设计、几何美感 |
| hexagon | 六边形 | 正六边形蒙版 | 科技感、蜂窝效果 |
| oval | 椭圆形 | 椭圆形蒙版 | 柔和过渡、人物肖像 |
| rounded_rectangle | 圆角矩形 | 带圆角的矩形蒙版 | 现代设计、柔和边框 |
| triangle | 三角形 | 三角形蒙版 | 方向指示、动态设计 |
| mirror_split | 镜像分割 | 镜像对称分割 | 创意效果、对比展示 |
| horizontal_split | 水平分割 | 水平方向分割 | 上下对比、分屏效果 |
| vertical_split | 垂直分割 | 垂直方向分割 | 左右对比、双画面 |

---

## 使用场景

### 场景 1: 在添加视频时使用圆形蒙版

```python
import requests

# 首先获取蒙版类型
mask_types = requests.get('http://localhost:9001/get_mask_types').json()
print('Available masks:', [m['name'] for m in mask_types['output']])

# 然后在添加视频时使用圆形蒙版
requests.post('http://localhost:9001/add_video', json={
    "video_url": "https://example.com/video.mp4",
    "mask_type": "circle",
    "mask_center_x": 0.5,
    "mask_center_y": 0.5,
    "mask_size": 0.8,
    "mask_feather": 0.1
})
```

### 场景 2: 创建画中画效果

```python
import requests

# 添加背景视频（带模糊）
requests.post('http://localhost:9001/add_video', json={
    "video_url": "https://example.com/background.mp4",
    "track_name": "video_main",
    "background_blur": 3
})

# 添加前景视频（圆形蒙版）
requests.post('http://localhost:9001/add_video', json={
    "video_url": "https://example.com/foreground.mp4",
    "track_name": "video_pip",
    "mask_type": "circle",
    "mask_size": 0.6,
    "transform_x": 0.6,
    "transform_y": -0.6,
    "scale_x": 0.4,
    "scale_y": 0.4,
    "relative_index": 1
})
```

### 场景 3: 心形蒙版浪漫效果

```python
import requests

requests.post('http://localhost:9001/add_video', json={
    "video_url": "https://example.com/romantic.mp4",
    "mask_type": "heart",
    "mask_center_x": 0.5,
    "mask_center_y": 0.5,
    "mask_size": 1.0,
    "mask_feather": 0.05
})
```

---

## 蒙版参数配合使用

在 `add_video` 或 `add_image` 接口中使用蒙版时，可配合以下参数：

| 参数名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| mask_type | string | null | 蒙版类型（从此接口获取） |
| mask_center_x | number | 0.5 | 蒙版中心 X 坐标（0.0-1.0） |
| mask_center_y | number | 0.5 | 蒙版中心 Y 坐标（0.0-1.0） |
| mask_size | number | 1.0 | 蒙版大小（相对屏幕高度） |
| mask_rotation | number | 0.0 | 蒙版旋转角度（度） |
| mask_feather | number | 0.0 | 蒙版羽化程度（0.0-1.0） |
| mask_invert | boolean | false | 是否反转蒙版 |
| mask_rect_width | number | null | 矩形蒙版宽度 |
| mask_round_corner | number | null | 圆角半径 |

---

## 注意事项

1. **环境差异**: 返回的蒙版类型根据环境（剪映/CapCut）可能不同
2. **形状适配**: 某些蒙版可能需要额外的参数（如矩形需要 mask_rect_width）
3. **羽化效果**: mask_feather 参数可以创建柔和的边缘
4. **性能影响**: 使用蒙版会增加渲染时间
5. **反转效果**: mask_invert 可以反转蒙版区域
6. **旋转角度**: 某些非对称蒙版支持旋转

---

## 环境变量

接口返回的蒙版类型取决于以下环境配置：

- **IS_CAPCUT_ENV = True**: 返回 CapCut 国际版的蒙版类型
- **IS_CAPCUT_ENV = False**: 返回剪映的蒙版类型

---

## 相关接口

- `POST /add_video` - 添加视频（支持蒙版参数）
- `POST /add_image` - 添加图片（支持蒙版参数）
- `GET /get_transition_types` - 获取转场类型
- `GET /get_intro_animation_types` - 获取入场动画类型

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
