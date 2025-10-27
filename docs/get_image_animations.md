# get_image_animations 接口文档

## 接口概述

**接口名称**：get_image_animations  
**接口地址**：`POST /openapi/capcut-mate/v1/get_image_animations`  
**功能描述**：获取图片出入场动画列表，返回所有支持的且满足条件的图片出入场动画。支持根据动画类型（入场、出场、循环）和会员模式（所有、VIP、免费）进行筛选。

## 更多文档

📖 更多详细文档和教程请访问：[https://docs.jcaigc.cn](https://docs.jcaigc.cn)

## 请求参数

### 请求体 (application/json)

| 参数名 | 类型 | 必填 | 默认值 | 描述 |
|--------|------|------|--------|------|
| mode | integer | 否 | 0 | 动画模式：0=所有，1=VIP，2=免费 |
| type | string | 是 | - | 动画类型：in=入场，out=出场，loop=循环 |

### 动画模式说明

| 模式值 | 模式名称 | 描述 |
|--------|----------|------|
| 0 | 所有 | 返回所有动画（包括VIP和免费） |
| 1 | VIP | 仅返回VIP动画 |
| 2 | 免费 | 仅返回免费动画 |

### 动画类型说明

| 类型值 | 类型名称 | 描述 |
|--------|----------|------|
| in | 入场动画 | 图片出现时的动画效果 |
| out | 出场动画 | 图片消失时的动画效果 |
| loop | 循环动画 | 图片持续播放的循环动画效果 |

## 请求示例

### 获取所有入场动画

```json
{
  "mode": 0,
  "type": "in"
}
```

### 获取VIP出场动画

```json
{
  "mode": 1,
  "type": "out"
}
```

### 获取免费循环动画

```json
{
  "mode": 2,
  "type": "loop"
}
```

## 响应格式

### 成功响应

```json
{
  "effects": "[{\"resource_id\":\"7314291622525538843\",\"type\":\"in\",\"category_id\":\"ruchang\",\"category_name\":\"入场\",\"duration\":500000,\"id\":\"35395178\",\"name\":\"冰雪飘动\",\"request_id\":\"\",\"start\":0,\"icon_url\":\"https://lf5-hl-hw-effectcdn-tos.byteeffecttos.com/obj/ies.fe.effect/459c196951cadbd024456a63db89481f\",\"material_type\":\"sticker\",\"panel\":\"\",\"path\":\"\",\"platform\":\"all\"},{\"resource_id\":\"7397306443147252233\",\"type\":\"in\",\"category_id\":\"ruchang\",\"category_name\":\"入场\",\"duration\":500000,\"id\":\"77035159\",\"name\":\"变色输入\",\"request_id\":\"\",\"start\":0,\"icon_url\":\"https://lf5-hl-hw-effectcdn-tos.byteeffecttos.com/obj/ies.fe.effect/c15f5c313f8170c558043abf300a0692\",\"material_type\":\"sticker\",\"panel\":\"\",\"path\":\"\",\"platform\":\"all\"}]"
}
```

### 动画对象结构

每个动画对象包含以下字段：

| 字段名 | 类型 | 描述 |
|--------|------|------|
| resource_id | string | 动画资源ID |
| type | string | 动画类型（in/out/loop） |
| category_id | string | 动画分类ID |
| category_name | string | 动画分类名称 |
| duration | integer | 动画时长（微秒） |
| id | string | 动画唯一标识ID |
| name | string | 动画名称 |
| request_id | string | 请求ID（通常为空） |
| start | integer | 动画开始时间 |
| icon_url | string | 动画图标URL |
| material_type | string | 素材类型（通常为"sticker"） |
| panel | string | 面板信息 |
| path | string | 路径信息 |
| platform | string | 支持平台（通常为"all"） |

### 错误响应

#### 400 Bad Request - 参数验证失败

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "请求参数验证失败",
    "details": "type 参数必须为 in、out 或 loop"
  }
}
```

#### 500 Internal Server Error - 获取动画失败

```json
{
  "error": {
    "code": "IMAGE_ANIMATION_GET_FAILED",
    "message": "获取图片动画失败",
    "details": "动画数据获取失败"
  }
}
```

## 错误码说明

| 错误码 | HTTP状态码 | 描述 | 解决方案 |
|--------|------------|------|----------|
| VALIDATION_ERROR | 400 | 请求参数验证失败 | 检查type参数是否为in/out/loop，mode参数是否为0/1/2 |
| IMAGE_ANIMATION_GET_FAILED | 500 | 获取图片动画失败 | 检查服务状态，稍后重试 |

## 使用说明

### 参数说明

1. **type参数**：必填参数，只能选择 "in"、"out"、"loop" 中的一个
2. **mode参数**：可选参数，默认为0（所有动画）
3. **响应数据**：effects字段是JSON字符串格式，需要解析后使用

### 动画应用场景

1. **入场动画（in）**：
   - 适用于图片出现的场景
   - 如淡入效果、缩放入场、滑动入场等
   - 通常时长在0.5-1秒之间

2. **出场动画（out）**：
   - 适用于图片消失的场景
   - 如淡出效果、缩放消失、旋转出场等
   - 通常时长在0.6-0.8秒之间

3. **循环动画（loop）**：
   - 适用于需要持续吸引注意力的图片
   - 如轻微摇摆、缩放呼吸效果等
   - 通常时长在1-1.2秒之间，可无限循环

### 使用建议

- 根据视频内容风格选择合适的动画类型
- VIP动画通常效果更佳，但需要会员权限
- 建议先获取所有动画，再根据需要进行筛选
- 可以结合动画预览图（icon_url）让用户选择
- 图片动画相比文字动画应更加自然流畅

## 示例代码

### JavaScript示例

```javascript
// 获取所有入场动画
const getImageInAnimations = async () => {
  const response = await fetch('/openapi/capcut-mate/v1/get_image_animations', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      mode: 0,
      type: 'in'
    })
  });
  
  const result = await response.json();
  const animations = JSON.parse(result.effects);
  console.log('图片入场动画列表:', animations);
};

// 获取免费循环动画
const getFreeImageLoopAnimations = async () => {
  const response = await fetch('/openapi/capcut-mate/v1/get_image_animations', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      mode: 2,
      type: 'loop'
    })
  });
  
  const result = await response.json();
  const animations = JSON.parse(result.effects);
  console.log('免费图片循环动画列表:', animations);
};
```

### Python示例

```python
import requests
import json

def get_image_animations(mode=0, animation_type='in'):
    """获取图片动画列表"""
    url = 'http://localhost:8000/v1/get_image_animations'
    data = {
        'mode': mode,
        'type': animation_type
    }
    
    response = requests.post(url, json=data)
    if response.status_code == 200:
        result = response.json()
        animations = json.loads(result['effects'])
        return animations
    else:
        print(f"请求失败: {response.status_code}")
        return []

# 使用示例
in_animations = get_image_animations(mode=0, animation_type='in')
print(f"获取到 {len(in_animations)} 个图片入场动画")

vip_out_animations = get_image_animations(mode=1, animation_type='out')
print(f"获取到 {len(vip_out_animations)} 个VIP图片出场动画")
```

## 相关接口

- [add_images](./add_images.md) - 批量添加图片（可使用动画效果）
- [add_effects](./add_effects.md) - 添加视频特效
- [get_text_animations](./get_text_animations.md) - 获取文字出入场动画

## 技术实现

### 文件结构

```
src/
├── schemas/get_image_animations.py    # 请求/响应数据模型
├── service/get_image_animations.py    # 业务逻辑实现
└── router/v1.py                       # API路由定义
```

### 核心逻辑

1. **参数验证**：验证type和mode参数的有效性
2. **数据筛选**：根据type和mode参数筛选图片动画数据
3. **数据格式化**：将动画数据转换为JSON字符串格式
4. **响应返回**：返回符合规范的API响应

### 数据来源

目前使用模拟数据，实际项目中应该：
- 从数据库获取图片动画数据
- 或从第三方API获取动画资源
- 支持动画资源的动态更新
- 区分图片动画和文字动画的不同特性

---

**版本信息**：v1.0  
**最后更新**：2024-09-24