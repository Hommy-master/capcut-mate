# GET_TEXT_ANIMATIONS API 接口文档

## 接口信息

```bash
POST /openapi/capcut-mate/v1/get_text_animations
```

## 功能描述

获取文字出入场动画列表，返回所有支持的且满足条件的文字出入场动画。支持根据动画类型（入场、出场、循环）和会员模式（所有、VIP、免费）进行筛选。

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
| type | string | ✅ | - | 动画类型：in=入场，out=出场，loop=循环 |

### 参数详解

#### 动画模式参数

- **mode**: 动画筛选模式
  - 0 = 返回所有动画（包括VIP和免费）
  - 1 = 仅返回VIP动画
  - 2 = 仅返回免费动画
  - 默认值：0

#### 动画类型参数

- **type**: 动画类型，必填参数
  - "in" = 入场动画（文字出现时的动画效果）
  - "out" = 出场动画（文字消失时的动画效果）
  - "loop" = 循环动画（文字持续播放的循环动画效果）

#### 动画模式说明

| 模式值 | 模式名称 | 描述 |
|--------|----------|------|
| 0 | 所有 | 返回所有动画（包括VIP和免费） |
| 1 | VIP | 仅返回VIP动画 |
| 2 | 免费 | 仅返回免费动画 |

#### 动画类型说明

| 类型值 | 类型名称 | 描述 |
|--------|----------|------|
| in | 入场动画 | 文字出现时的动画效果 |
| out | 出场动画 | 文字消失时的动画效果 |
| loop | 循环动画 | 文字持续播放的循环动画效果 |

## 响应格式

### 成功响应 (200)

```json
{
  "effects": [
    {
      "resource_id": "7314291622525538843",
      "type": "in",
      "category_id": "ruchang",
      "category_name": "入场",
      "duration": 500000,
      "id": "35395178",
      "name": "冰雪飘动",
      "request_id": "",
      "start": 0,
      "icon_url": "https://lf5-hl-hw-effectcdn-tos.byteeffecttos.com/obj/ies.fe.effect/459c196951cadbd024456a63db89481f",
      "material_type": "sticker",
      "panel": "",
      "path": "",
      "platform": "all"
    },
    {
      "resource_id": "7397306443147252233",
      "type": "in",
      "category_id": "ruchang",
      "category_name": "入场",
      "duration": 500000,
      "id": "77035159",
      "name": "变色输入",
      "request_id": "",
      "start": 0,
      "icon_url": "https://lf5-hl-hw-effectcdn-tos.byteeffecttos.com/obj/ies.fe.effect/c15f5c313f8170c558043abf300a0692",
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
| effects | array | 文字出入场动画对象数组 |

#### 动画对象结构

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

### 错误响应 (4xx/5xx)

```json
{
  "detail": "错误信息描述"
}
```

## 使用示例

### cURL 示例

#### 1. 获取所有入场动画

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_text_animations \
  -H "Content-Type: application/json" \
  -d '{
    "mode": 0,
    "type": "in"
  }'
```

#### 2. 获取VIP出场动画

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_text_animations \
  -H "Content-Type: application/json" \
  -d '{
    "mode": 1,
    "type": "out"
  }'
```

#### 3. 获取免费循环动画

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_text_animations \
  -H "Content-Type: application/json" \
  -d '{
    "mode": 2,
    "type": "loop"
  }'
```

## 错误码说明

| 错误码 | 错误信息 | 说明 | 解决方案 |
|--------|----------|------|----------|
| 400 | type是必填项 | 缺少动画类型参数 | 提供有效的type参数 |
| 400 | mode参数无效 | mode参数超出范围 | 使用0、1或2作为mode值 |
| 400 | type参数无效 | type参数值不正确 | 使用in、out或loop作为type值 |
| 500 | 获取文字动画失败 | 内部处理错误 | 联系技术支持 |

## 注意事项

1. **参数要求**: type参数为必填项，mode参数为可选项
2. **动画类型**: type参数只能是"in"、"out"、"loop"中的一个
3. **动画模式**: mode参数只能是0、1、2中的一个
4. **响应格式**: 与旧版本不同，当前版本直接返回对象数组而非JSON字符串
5. **数据来源**: 当前使用模拟数据，生产环境中应从数据库或API获取

## 工作流程

1. 验证必填参数（type）
2. 验证参数有效性（type和mode）
3. 根据type和mode筛选动画数据
4. 返回符合条件的动画列表

## 相关接口

- [添加字幕](./add_captions.md)
- [创建文本样式](./add_text_style.md)
- [获取图片动画](./get_image_animations.md)

---

<div align="right">

📚 **项目资源**  
**GitHub**: [https://github.com/Hommy-master/capcut-mate](https://github.com/Hommy-master/capcut-mate)  
**Gitee**: [https://gitee.com/taohongmin-gitee/capcut-mate](https://gitee.com/taohongmin-gitee/capcut-mate)

</div>