# GET_IMAGE_ANIMATIONS API 接口文档

## 🌐 语言切换
[中文版](./get_image_animations.zh.md) | [English](./get_image_animations.md)

## 接口信息

```
POST /openapi/capcut-mate/v1/get_image_animations
```

## 功能描述

获取图片出入场动画列表，返回所有支持的且满足条件的图片出入场动画。支持根据动画类型（入场、出场、循环）和会员模式（所有、VIP、免费）进行筛选。

## 更多文档

📖 更多详细文档和教程请访问：[https://docs.jcaigc.cn](https://docs.jcaigc.cn)

## 请求参数

```json
{
  "mode": 0,
  "type": "in"
}
```

### 参数说明

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| mode | integer | ❌ | 0 | 动画模式：0=所有，1=VIP，2=免费 |
| type | string | ❌ | null | 动画类型：in=入场，out=出场，loop=循环；不传则返回全部 |

### 参数详解

#### 动画模式参数

- **mode**: 动画筛选模式
  - 0 = 所有动画（包括VIP和免费）
  - 1 = 仅VIP动画
  - 2 = 仅免费动画
  - 默认值：0

#### 动画类型参数

- **type**: 动画类型（可选，不传则返回全部类型）
  - "in" = 入场动画（图片出现时的效果）
  - "out" = 出场动画（图片消失时的效果）
  - "loop" = 循环动画（图片持续播放的效果）

#### 动画模式说明

| 模式值 | 模式名称 | 描述 |
|--------|----------|------|
| 0 | 所有 | 返回所有动画（包括VIP和免费） |
| 1 | VIP | 仅返回VIP动画 |
| 2 | 免费 | 仅返回免费动画 |

#### 动画类型说明

| 类型值 | 类型名称 | 描述 |
|--------|----------|------|
| in | 入场动画 | 图片出现时的动画效果 |
| out | 出场动画 | 图片消失时的动画效果 |
| loop | 循环动画 | 图片持续播放的循环动画效果 |

## 响应格式

### 成功响应 (200)

```json
{
  "code": 0,
  "message": "success",
  "effects": [
    {
      "resource_id": "7314291622525538844",
      "type": "in",
      "category_id": "pic_ruchang",
      "category_name": "图片入场",
      "duration": 600000,
      "id": "35395179",
      "name": "渐显出现",
      "request_id": "",
      "start": 0,
      "icon_url": "https://lf5-hl-hw-effectcdn-tos.byteeffecttos.com/obj/ies.fe.effect/fade_in_pic_icon",
      "material_type": "sticker",
      "panel": "",
      "path": "",
      "platform": "all"
    }
  ]
}
```

### 响应字段说明

| 字段名 | 类型 | 说明 |
|--------|------|------|
| effects | array | 图片动画对象数组 |

#### 单个动画对象字段说明

| 字段名 | 类型 | 说明 |
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

```json
{
  "code": 2033,
  "message": "获取图片动画失败"
}
```

## 使用示例

### cURL 示例

#### 1. 获取所有入场动画

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_image_animations \
  -H "Content-Type: application/json" \
  -d '{
    "mode": 0,
    "type": "in"
  }'
```

#### 2. 获取VIP出场动画

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_image_animations \
  -H "Content-Type: application/json" \
  -d '{
    "mode": 1,
    "type": "out"
  }'
```

#### 3. 获取免费循环动画

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_image_animations \
  -H "Content-Type: application/json" \
  -d '{
    "mode": 2,
    "type": "loop"
  }'
```

## 错误码说明

| 错误码 | 错误信息 | 说明 | 解决方案 |
|--------|----------|------|----------|
| 1001 | 参数校验失败 | type 不在 in、out、loop 取值范围内（请求体未通过参数校验） | 使用正确的type值："in"、"out"或"loop" |
| 2033 | 获取图片动画失败 | mode 不是 0、1、2，或内部处理出错 | 使用正确的mode值：0、1或2，或联系技术支持 |

## 注意事项

1. **type参数**：可选参数，不传则返回全部类型；传值时只能选择 "in"、"out"、"loop" 中的一个
2. **mode参数**：可选参数，默认为0（所有动画）
3. **响应数据**：与文字动画不同，图片动画有专门的分类和效果
4. **动画时长**：单位为微秒（1秒 = 1,000,000微秒）
5. **VIP标识**：部分动画可能需要VIP权限才能使用

## 工作流程

1. 验证可选参数（type）
2. 验证可选参数（mode）的有效性
3. 根据type和mode筛选图片动画数据
4. 返回符合条件的动画对象数组
5. 服务端自动处理数据格式化

## 相关接口

- [添加图片](./add_images.md)
- [获取文字动画](./get_text_animations.md)
- [添加特效](./add_effects.md)

---

<div align="right">

📚 **项目资源**  
**GitHub**: [https://github.com/Hommy-master/capcut-mate](https://github.com/Hommy-master/capcut-mate)  
**Gitee**: [https://gitee.com/taohongmin-gitee/capcut-mate](https://gitee.com/taohongmin-gitee/capcut-mate)

</div>