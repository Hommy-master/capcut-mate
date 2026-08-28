# GET_TEXT_EFFECTS API Documentation

## 🌐 Language Switch
[中文版](./get_text_effects.zh.md) | [English](./get_text_effects.md)

## Interface Information

```bash
POST /openapi/capcut-mate/v1/get_text_effects
```

## Function Description

Get the list of supported text flower effects (decorative text styles), with optional filtering by membership mode (all, VIP, free). This interface follows the same RESTful POST pattern as similar resource list APIs.

## More Documentation

📖 For more detailed documentation and tutorials, please visit: [https://docs.jcaigc.cn](https://docs.jcaigc.cn)

## Request Parameters

```json
{
  "mode": 0
}
```

### Parameter Description

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| mode | integer | ❌ | 0 | Text effect mode: 0=all, 1=VIP, 2=free |

### Parameter Details

#### Text Effect Mode

| Mode Value | Mode Name | Description |
|------------|-----------|-------------|
| 0 | All | Return all text effects (including VIP and free) |
| 1 | VIP | VIP text effects only |
| 2 | Free | Free text effects only |

## Response Format

### Success Response (200)

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

### Response Field Description

| Field | Type | Description |
|-------|------|-------------|
| text_effects | array | Text flower effect object array |

#### TextEffectItem Object

| Field | Type | Description |
|-------|------|-------------|
| id | string | Text effect ID |
| title | string | Text effect name |
| is_vip | boolean | Whether this is a VIP effect |

### Error Response (4xx/5xx)

```json
{
  "detail": "Error message description"
}
```

## Usage Examples

### cURL Examples

#### 1. Get All Text Effects

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_text_effects \
  -H "Content-Type: application/json" \
  -d '{"mode": 0}'
```

#### 2. Get VIP Text Effects

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_text_effects \
  -H "Content-Type: application/json" \
  -d '{"mode": 1}'
```

#### 3. Get Free Text Effects

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_text_effects \
  -H "Content-Type: application/json" \
  -d '{"mode": 2}'
```

### Use with add_captions

```javascript
// 1. Fetch text effects list
const effectsResponse = await fetch('/openapi/capcut-mate/v1/get_text_effects', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ mode: 0 })
});
const effects = await effectsResponse.json();

// 2. User selects a text effect
const selectedEffect = effects.text_effects[0];

// 3. Apply the effect when adding captions
await fetch('/openapi/capcut-mate/v1/add_captions', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    draft_id: "your_draft_id",
    captions: [...],
    text_effect: selectedEffect.title  // or selectedEffect.id
  })
});
```

## Error Code Description

| Error Code | Error Message | Description | Solution |
|------------|---------------|-------------|----------|
| 400 | Invalid mode parameter | mode parameter out of range | Use 0, 1, or 2 as mode value |
| 500 | filter_get_failed | Failed to get text effects list | Contact technical support |

## Notes

1. **Parameter Requirements**: mode is optional and defaults to 0
2. **Mode Values**: mode must be one of 0, 1, or 2
3. **Performance**: The text effects list can be large; client-side caching is recommended
4. **Compatibility**: If there are no VIP effects, the interface returns an empty array without error
5. **Identifier Resolution**: Text effects can be referenced by name or ID when calling `add_captions`

## Related Interfaces

- [Add Captions](./add_captions.md)
- [Create Text Style](./add_text_style.md)
- [Get Text Animations](./get_text_animations.md)

---

<div align="right">

📚 **Project Resources**  
**GitHub**: [https://github.com/Hommy-master/capcut-mate](https://github.com/Hommy-master/capcut-mate)  
**Gitee**: [https://gitee.com/taohongmin-gitee/capcut-mate](https://gitee.com/taohongmin-gitee/capcut-mate)

</div>
