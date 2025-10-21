# get_transition_types 接口文档

## 接口概述

获取所有支持的转场动画类型列表，用于视频和图片的转场效果。

---

## 接口信息

### RESTful API 端点

```
GET /get_transition_types
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
| output | array | 转场类型列表 |
| error | string | 失败时的错误信息 |

### output 数组中每个元素的结构

| 参数名 | 类型 | 说明 |
|--------|------|------|
| name | string | 转场类型名称 |

---

## 请求示例

### 示例 1: 获取转场类型列表

```bash
curl -X GET http://localhost:9001/get_transition_types
```

### 示例 2: Python 请求示例

```python
import requests

url = "http://localhost:9001/get_transition_types"
response = requests.get(url)
result = response.json()

print(f"Success: {result['success']}")
if result['success']:
    print(f"Total transition types: {len(result['output'])}")
    for transition in result['output']:
        print(f"  - {transition['name']}")
else:
    print(f"Error: {result['error']}")
```

### 示例 3: JavaScript 请求示例

```javascript
fetch('http://localhost:9001/get_transition_types')
  .then(response => response.json())
  .then(result => {
    if (result.success) {
      console.log('Transition types:', result.output);
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
    { "name": "fade" },
    { "name": "dissolve" },
    { "name": "wipe_left" },
    { "name": "wipe_right" },
    { "name": "wipe_up" },
    { "name": "wipe_down" },
    { "name": "slide_left" },
    { "name": "slide_right" },
    { "name": "zoom_in" },
    { "name": "zoom_out" },
    { "name": "circle_in" },
    { "name": "circle_out" },
    { "name": "blur" },
    { "name": "pixelate" }
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
  "error": "Error occurred while getting transition animation types: Internal error."
}
```

---

## 常见转场类型说明

| 转场名称 | 类型 | 说明 | 适用场景 |
|---------|------|------|---------|
| fade | 淡入淡出 | 前一画面淡出，后一画面淡入 | 温和过渡，适合大部分场景 |
| dissolve | 溶解 | 两个画面交叉溶解 | 时间流逝、场景切换 |
| wipe_left | 左滑擦除 | 从右向左擦除 | 动感场景切换 |
| wipe_right | 右滑擦除 | 从左向右擦除 | 动感场景切换 |
| wipe_up | 上滑擦除 | 从下向上擦除 | 揭示效果 |
| wipe_down | 下滑擦除 | 从上向下擦除 | 覆盖效果 |
| slide_left | 左滑动 | 画面向左滑动切换 | 连续场景切换 |
| slide_right | 右滑动 | 画面向右滑动切换 | 连续场景切换 |
| zoom_in | 放大 | 新画面放大进入 | 强调重点 |
| zoom_out | 缩小 | 旧画面缩小退出 | 视野拉远 |
| circle_in | 圆形收缩 | 圆形区域收缩 | 聚焦效果 |
| circle_out | 圆形扩展 | 圆形区域扩展 | 展开效果 |
| blur | 模糊 | 前画面模糊后切换 | 梦幻效果 |
| pixelate | 像素化 | 像素化过渡 | 数字、科技感 |

---

## 使用场景

### 场景 1: 在添加视频时使用转场

```python
import requests

# 首先获取转场类型
transition_types = requests.get('http://localhost:9001/get_transition_types').json()
print('Available transitions:', [t['name'] for t in transition_types['output']])

# 然后在添加视频时使用
requests.post('http://localhost:9001/add_video', json={
    "video_url": "https://example.com/video.mp4",
    "transition": "fade",
    "transition_duration": 1.0
})
```

### 场景 2: 动态选择转场效果

```python
import requests
import random

# 获取所有转场类型
response = requests.get('http://localhost:9001/get_transition_types')
transitions = response.json()['output']

# 随机选择一个转场效果
random_transition = random.choice(transitions)['name']

# 应用到视频
requests.post('http://localhost:9001/add_video', json={
    "video_url": "https://example.com/video.mp4",
    "transition": random_transition,
    "transition_duration": 0.8
})
```

---

## 注意事项

1. **环境差异**: 返回的转场类型根据环境（剪映/CapCut）可能不同
2. **可用性**: 某些转场效果可能在特定版本中不可用
3. **性能**: 复杂的转场效果（如模糊、像素化）可能影响渲染性能
4. **时长建议**: 转场时长一般在 0.3-1.5 秒之间效果最佳
5. **搭配使用**: 可与 `add_video` 和 `add_image` 接口配合使用

---

## 环境变量

接口返回的转场类型取决于以下环境配置：

- **IS_CAPCUT_ENV = True**: 返回 CapCut 国际版的转场类型
- **IS_CAPCUT_ENV = False**: 返回剪映的转场类型

---

## 相关接口

- `POST /add_video` - 添加视频（支持转场参数）
- `POST /add_image` - 添加图片（支持转场参数）
- `GET /get_intro_animation_types` - 获取入场动画类型
- `GET /get_outro_animation_types` - 获取出场动画类型
- `GET /get_combo_animation_types` - 获取组合动画类型

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
