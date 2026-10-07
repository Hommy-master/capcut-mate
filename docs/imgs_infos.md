# IMGS_INFOS API Documentation

## 🌐 Language Switch
[中文版](./imgs_infos.zh.md) | [English](./imgs_infos.md)

## Interface Information

```
POST /openapi/capcut-mate/v1/imgs_infos
```

## Function Description

Generate image information based on image URLs and timelines. This interface converts image file URLs and timeline configurations into the image information format required by Jianying drafts, supporting animation effects and transition settings.

## More Documentation

📖 For more detailed documentation and tutorials, please visit: [https://docs.jcaigc.cn](https://docs.jcaigc.cn)

## Request Parameters

```json
{
  "imgs": ["https://assets.jcaigc.cn/img1.jpg", "https://assets.jcaigc.cn/img2.png"],
  "timelines": [
    {"start": 0, "end": 3000000},
    {"start": 3000000, "end": 6000000}
  ],
  "height": 1080,
  "width": 1920,
  "in_animation": "渐显",
  "in_animation_duration": 500000,
  "loop_animation": "动感摇晃I",
  "loop_animation_duration": 1000000,
  "out_animation": "渐隐",
  "out_animation_duration": 500000,
  "transition": "叠化",
  "transition_duration": 300000
}
```

### Parameter Description

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| imgs | array[string] |✅ | - | Image file URL array |
| timelines | array[object] |✅ | - | Timeline configuration array |
| height | integer |❌ | None | Image height |
| width | integer |❌ | None | Image width |
| in_animation | string |❌ | None | Intro animation name; see [add_images](./add_images.md) |
| in_animation_duration | integer |❌ | None | Entrance animation duration (microseconds) |
| loop_animation | string |❌ | None | Loop animation name; see [add_images](./add_images.md) |
| loop_animation_duration | integer |❌ | None | Loop animation duration (microseconds) |
| out_animation | string |❌ | None | Outro animation name; see [add_images](./add_images.md) |
| out_animation_duration | integer |❌ | None | Exit animation duration (microseconds) |
| transition | string |❌ | None | Transition name; see [add_images](./add_images.md) / [add_videos](./add_videos.md) |
| transition_duration | integer |❌ | None | Transition duration (microseconds) |

### Available Transitions and Animations

For the full lists of valid `transition` / `in_animation` / `out_animation` / `loop_animation` values, see [add_images](./add_images.md) → Supported Transitions and Animations.

## Response Format

### Success Response (200)

```json
{
  "code": 0,
  "message": "success",
  "infos": "[{\"image_url\":\"https://assets.jcaigc.cn/img1.jpg\",\"start\":0,\"end\":3000000,\"height\":1080,\"width\":1920,\"in_animation\":\"渐显\",\"in_animation_duration\":500000,\"out_animation\":\"渐隐\",\"out_animation_duration\":500000,\"loop_animation\":\"动感摇晃I\",\"loop_animation_duration\":1000000,\"transition\":\"叠化\",\"transition_duration\":300000},{\"image_url\":\"https://assets.jcaigc.cn/img2.png\",\"start\":3000000,\"end\":6000000,\"height\":1080,\"width\":1920,\"in_animation\":\"渐显\",\"in_animation_duration\":500000,\"out_animation\":\"渐隐\",\"out_animation_duration\":500000,\"loop_animation\":\"动感摇晃I\",\"loop_animation_duration\":1000000,\"transition\":\"叠化\",\"transition_duration\":300000}]"
}
```

### Response Field Description

| Field | Type | Description |
|-------|------|-------------|
| infos | string | Image information JSON string |

### Error Response

```json
{
  "code": 1001,
  "message": "Parameter validation failed"
}
```

## Usage Examples

### cURL Examples

#### 1. Basic Image Information Generation

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/imgs_infos \
  -H "Content-Type: application/json" \
  -d '{
    "imgs": ["https://assets.jcaigc.cn/cover.jpg"],
    "timelines": [{"start": 0, "end": 5000000}],
    "height": 1080,
    "width": 1920
  }'
```

#### 2. Image Information with Animation Effects

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/imgs_infos \
  -H "Content-Type: application/json" \
  -d '{
    "imgs": ["https://assets.jcaigc.cn/slide1.jpg", "https://assets.jcaigc.cn/slide2.jpg"],
    "timelines": [{"start": 0, "end": 3000000}, {"start": 3000000, "end": 6000000}],
    "in_animation": "渐显",
    "loop_animation": "动感摇晃I",
    "out_animation": "渐隐",
    "transition": "叠化"
  }'
```

## Error Code Description

| Error Code | Error Message | Description | Solution |
|------------|---------------|-------------|----------|
| 1001 | Parameter validation failed | Request body failed schema validation (`imgs`/`timelines` missing, timeline item lacking `start`/`end`, or wrong types) | Check parameter types and required fields |

## Notes

1. **Array Matching**: if `imgs` and `timelines` lengths differ, the shorter length is used (no hard error)
2. **Time Unit**: All time parameters use microseconds (1 second = 1,000,000 microseconds)
3. **Resolution Settings**: height and width parameters are used to set image display resolution
4. **Animation Effects**: Support entrance animation, loop animation, exit animation, and transition effects
5. **Network Access**: Image URLs must be accessible
6. **Format Support**: Support common image formats (JPG, PNG, GIF, etc.)

## Workflow

1. Validate required parameters (imgs, timelines)
2. Align the two arrays by the shorter length
3. Validate timeline parameter validity
4. Set image resolution parameters
5. Apply animation effect parameters
6. Generate corresponding image information for each image URL
7. Convert information to JSON string format
8. Return processing result

## Related Interfaces

- [Create Draft](./create_draft.md)
- [Add Images](./add_images.md)
- [Timelines](./timelines.md)
- [Save Draft](./save_draft.md)

---

<div align="right">

📚 **Project Resources**  
**GitHub**: [https://github.com/Hommy-master/capcut-mate](https://github.com/Hommy-master/capcut-mate)  
**Gitee**: [https://gitee.com/taohongmin-gitee/capcut-mate](https://gitee.com/taohongmin-gitee/capcut-mate)

</div>

### Language Switch
[中文版](./imgs_infos.zh.md) | [English](./imgs_infos.md)