# GET_TEXT_ANIMATIONS API Documentation

### 🌐 Language Switch
[中文版](./get_text_animations.zh.md) | [English](./get_text_animations.md)

## Interface Information

```bash
POST /openapi/capcut-mate/v1/get_text_animations
```

## Function Description

Get text entrance/exit animation list, returning all supported and qualified text entrance/exit animations. Support filtering based on animation type (entrance, exit, loop) and membership mode (all, VIP, free).

## More Documentation

📖 For more detailed documentation and tutorials, please visit: [https://docs.jcaigc.cn](https://docs.jcaigc.cn)

## Request Parameters

```json
{
  "mode": 0,
  "type": "in"
}
```

### Parameter Description

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| mode | integer |❌ | 0 | Animation mode: 0=all, 1=VIP, 2=free |
| type | string |✅ | - | Animation type: in=entrance, out=exit, loop=loop |

### Parameter Details

#### Animation Mode Parameter

- **mode**: Animation filtering mode
  - 0 = Return all animations (including VIP and free)
  - 1 = VIP animations only
  - 2 = Free animations only
  - Default: 0

#### Animation Type Parameter

- **type**: Animation type, required parameter
  - "in" = Entrance animation (animation effect when text appears)
  - "out" = Exit animation (animation effect when text disappears)
  - "loop" = Loop animation (continuous loop animation effect while text plays)

#### Animation Mode Description

| Mode Value | Mode Name | Description |
|------------|-----------|-------------|
| 0 | All | Return all animations (including VIP and free) |
| 1 | VIP | VIP animations only |
| 2 | Free | Free animations only |

#### Animation Type Description

| Type Value | Type Name | Description |
|------------|-----------|-------------|
| in | Entrance Animation | Animation effect when text appears |
| out | Exit Animation | Animation effect when text disappears |
| loop | Loop Animation | Continuous loop animation effect while text plays |

## Response Format

### Success Response (200)

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

### Response Field Description

| Field | Type | Description |
|-------|------|-------------|
| effects | array | Text entrance/exit animation object array |

#### Animation Object Structure

Each animation object contains the following fields:

| Field | Type | Description |
|-------|------|-------------|
| resource_id | string | Animation resource ID |
| type | string | Animation type (in/out/loop) |
| category_id | string | Animation category ID |
| category_name | string | Animation category name |
| duration | integer | Animation duration (microseconds) |
| id | string | Animation unique identifier ID |
| name | string | Animation name |
| request_id | string | Request ID (usually empty) |
| start | integer | Animation start time |
| icon_url | string | Animation icon URL |
| material_type | string | Material type (usually "sticker") |
| panel | string | Panel information |
| path | string | Path information |
| platform | string | Supported platform (usually "all") |

### Error Response (4xx/5xx)

```json
{
  "detail": "Error message description"
}
```

## Usage Examples

### cURL Examples

#### 1. Get All Entrance Animations

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_text_animations \
  -H "Content-Type: application/json" \
  -d '{
    "mode": 0,
    "type": "in"
  }'
```

#### 2. Get VIP Exit Animations

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_text_animations \
  -H "Content-Type: application/json" \
  -d '{
    "mode": 1,
    "type": "out"
  }'
```

#### 3. Get Free Loop Animations

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_text_animations \
  -H "Content-Type: application/json" \
  -d '{
    "mode": 2,
    "type": "loop"
  }'
```

## Error Code Description

| Error Code | Error Message | Description | Solution |
|------------|---------------|-------------|----------|
| 400 | type is required | Missing animation type parameter | Provide a valid type parameter |
| 400 | Invalid mode parameter | mode parameter out of range | Use 0, 1, or 2 as mode value |
| 400 | Invalid type parameter | type parameter value incorrect | Use in, out, or loop as type value |
| 500 | Failed to get text animations | Internal processing error | Contact technical support |

## Notes

1. **Parameter Requirements**: type parameter is required, mode parameter is optional
2. **Animation Types**: type parameter can only be one of "in", "out", "loop"
3. **Animation Modes**: mode parameter can only be one of 0, 1, 2
4. **Response Format**: Different from old version, current version directly returns object array instead of JSON string
5. **Data Source**: Currently using mock data, in production environment should get from database or API

## Workflow

1. Validate required parameter (type)
2. Validate parameter validity (type and mode)
3. Filter animation data based on type and mode
4. Return animation list meeting conditions

## Related Interfaces

- [Add Captions](./add_captions.md)
- [Create Text Style](./add_text_style.md)
- [Get Image Animations](./get_image_animations.md)

---

<div align="right">

📚 **Project Resources**  
**GitHub**: [https://github.com/Hommy-master/capcut-mate](https://github.com/Hommy-master/capcut-mate)  
**Gitee**: [https://gitee.com/taohongmin-gitee/capcut-mate](https://gitee.com/taohongmin-gitee/capcut-mate)

</div>