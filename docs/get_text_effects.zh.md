# GET_TEXT_EFFECTS API 接口文档

## 🌐 语言切换
[中文版](./get_text_effects.zh.md) | [English](./get_text_effects.md)

## 接口信息

```bash
POST /openapi/capcut-mate/v1/get_text_effects
```

## 功能描述

获取所有支持的花字效果列表，支持按 VIP/免费进行筛选。本接口参考滤镜列表接口的实现模式，提供 RESTful 风格的 POST 请求方式。

## 更多文档

📖 更多详细文档和教程请访问：[https://docs.jcaigc.cn](https://docs.jcaigc.cn)

## 请求参数

```json
{
  "mode": 0
}
```

### 参数说明

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| mode | integer | ❌ | 0 | 花字效果模式：0=所有，1=VIP，2=免费 |

### 参数详解

#### 花字效果模式

| 模式值 | 模式名称 | 说明 |
|--------|----------|------|
| 0 | 所有 | 返回所有花字效果（包括 VIP 和免费） |
| 1 | VIP | 仅返回 VIP 花字效果 |
| 2 | 免费 | 仅返回免费花字效果 |

## 响应格式

### 成功响应 (200)

```json
{
  "text_effects": [
    {
      "id": "7539407429763796249",
      "title": "红黄火焰综艺花字",
      "is_vip": false
    },
    {
      "id": "7351316503771368713",
      "title": "综艺 - 黑暗斑驳红色",
      "is_vip": false
    }
  ]
}
```

### 响应字段说明

| 字段名 | 类型 | 说明 |
|--------|------|------|
| text_effects | array | 花字效果对象数组 |

#### TextEffectItem 对象

| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | string | 花字效果 ID |
| title | string | 花字效果名称 |
| is_vip | boolean | 是否为 VIP 效果 |

### 错误响应 (4xx/5xx)

```json
{
  "detail": "错误信息描述"
}
```

## 使用示例

### cURL 示例

#### 1. 获取所有花字效果

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_text_effects \
  -H "Content-Type: application/json" \
  -d '{"mode": 0}'
```

#### 2. 获取 VIP 花字效果

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_text_effects \
  -H "Content-Type: application/json" \
  -d '{"mode": 1}'
```

#### 3. 获取免费花字效果

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_text_effects \
  -H "Content-Type: application/json" \
  -d '{"mode": 2}'
```

### 配合 add_captions 使用

```javascript
// 1. 先获取花字效果列表
const effectsResponse = await fetch('/openapi/capcut-mate/v1/get_text_effects', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ mode: 0 })
});
const effects = await effectsResponse.json();

// 2. 用户选择一个花字效果
const selectedEffect = effects.text_effects[0];

// 3. 在添加字幕时使用该花字
await fetch('/openapi/capcut-mate/v1/add_captions', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    draft_id: "your_draft_id",
    captions: [...],
    text_effect: selectedEffect.title  // 或 selectedEffect.id
  })
});
```

## 错误码说明

| 错误码 | 错误信息 | 说明 | 解决方案 |
|--------|----------|------|----------|
| 400 | Invalid mode parameter | mode 参数超出范围 | 使用 0、1 或 2 作为 mode 值 |
| 500 | filter_get_failed | 获取花字效果列表失败 | 联系技术支持 |

## 注意事项

1. **参数要求**：mode 参数为可选，默认值为 0
2. **模式取值**：mode 只能是 0、1、2 之一
3. **性能考虑**：花字效果数量较多，建议客户端使用缓存机制
4. **兼容性**：即使没有 VIP 效果，接口也会正常返回空数组，不会报错
5. **标识解析**：可通过名称或 ID 在 `add_captions` 中引用花字效果

## 相关接口

- [添加字幕](./add_captions.zh.md)
- [创建文本样式](./add_text_style.zh.md)
- [获取文本动画](./get_text_animations.zh.md)

---

<div align="right">

📚 **项目资源**  
**GitHub**: [https://github.com/Hommy-master/capcut-mate](https://github.com/Hommy-master/capcut-mate)  
**Gitee**: [https://gitee.com/taohongmin-gitee/capcut-mate](https://gitee.com/taohongmin-gitee/capcut-mate)

</div>
