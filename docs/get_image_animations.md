# GET_IMAGE_ANIMATIONS API Documentation

## 🌐 Language Switch
[中文版](./get_image_animations.zh.md) | [English](./get_image_animations.md)

## Interface Information

```
POST /openapi/capcut-mate/v1/get_image_animations
```

## Function Description

Get image entrance/exit animation list, returning all supported and qualified image entrance/exit animations. Support filtering based on animation type (entrance, exit, loop) and membership mode (all, VIP, free).

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
  - 0 = All animations (including VIP and free)
  - 1 = VIP animations only
  - 2 = Free animations only
  - Default: 0

#### Animation Type Parameter

- **type**: Animation type (required)
  - "in" = Entrance animation (effect when image appears)
  - "out" = Exit animation (effect when image disappears)
  - "loop" = Loop animation (continuous effect while image plays)

#### Animation Mode Description

| Mode Value | Mode Name | Description |
|------------|-----------|-------------|
| 0 | All | Return all animations (including VIP and free) |
| 1 | VIP | Return VIP animations only |
| 2 | Free | Return free animations only |

#### Animation Type Description

| Type Value | Type Name | Description |
|------------|-----------|-------------|
| in | Entrance Animation | Animation effect when image appears |
| out | Exit Animation | Animation effect when image disappears |
| loop | Loop Animation | Continuous loop animation effect while image plays |

## Response Format

### Success Response (200)

```json
{
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

### Response Field Description

| Field | Type | Description |
|-------|------|-------------|
| effects | array | Image animation object array |

#### Single Animation Object Field Description

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
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_image_animations \
  -H "Content-Type: application/json" \
  -d '{
    "mode": 0,
    "type": "in"
  }'
```

#### 2. Get VIP Exit Animations

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_image_animations \
  -H "Content-Type: application/json" \
  -d '{
    "mode": 1,
    "type": "out"
  }'
```

#### 3. Get Free Loop Animations

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_image_animations \
  -H "Content-Type: application/json" \
  -d '{
    "mode": 2,
    "type": "loop"
  }'
```

## Error Code Description

| Error Code | Error Message | Description | Solution |
|------------|---------------|-------------|----------|
| 400 | type parameter must be in, out, or loop | Invalid animation type parameter | Use correct type values: "in", "out", or "loop" |
| 400 | mode parameter must be 0, 1, or 2 | Invalid animation mode parameter | Use correct mode values: 0, 1, or 2 |
| 500 | Failed to get image animations | Internal processing error | Contact technical support |

## Notes

1. **type parameter**: Required parameter, can only choose one from "in", "out", "loop"
2. **mode parameter**: Optional parameter, default is 0 (all animations)
3. **Response data**: Different from text animations, image animations have specialized categories and effects
4. **Animation duration**: Unit is microseconds (1 second = 1,000,000 microseconds)
5. **VIP identification**: Some animations may require VIP permissions to use

## Workflow

1. Validate required parameter (type)
2. Validate optional parameter (mode) validity
3. Filter image animation data based on type and mode
4. Return animation object array meeting conditions
5. Server automatically handles data formatting

## Related Interfaces

- [Add Images](./add_images.md)
- [Get Text Animations](./get_text_animations.md)
- [Add Effects](./add_effects.md)

---

<div align="right">

📚 **Project Resources**  
**GitHub**: [https://github.com/Hommy-master/capcut-mate](https://github.com/Hommy-master/capcut-mate)  
**Gitee**: [https://gitee.com/taohongmin-gitee/capcut-mate](https://gitee.com/taohongmin-gitee/capcut-mate)

</div>