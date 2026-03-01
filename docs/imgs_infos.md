# IMGS_INFOS API Documentation

###🌐 Language Switch
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
  "in_animation": "fade_in",
  "in_animation_duration": 500000,
  "loop_animation": "bounce",
  "loop_animation_duration": 1000000,
  "out_animation": "fade_out",
  "out_animation_duration": 500000,
  "transition": "cross_fade",
  "transition_duration": 300000
}
```

### Parameter Description

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| imgs | array[string] |✅ | - | Image file URL array |
| timelines | array[object] |✅ | - | Timeline configuration array |
| height | number |❌ | 1080 | Image height |
| width | number |❌ | 1920 | Image width |
| in_animation | string |❌ | None | Entrance animation effect |
| in_animation_duration | number |❌ | 500000 | Entrance animation duration (microseconds) |
| loop_animation | string |❌ | None | Loop animation effect |
| loop_animation_duration | number |❌ | 1000000 | Loop animation duration (microseconds) |
| out_animation | string |❌ | None | Exit animation effect |
| out_animation_duration | number |❌ | 500000 | Exit animation duration (microseconds) |
| transition | string |❌ | None | Transition effect |
| transition_duration | number |❌ | 300000 | Transition duration (microseconds) |

## Response Format

### Success Response (200)

```json
{
  "infos": "[{\"img_url\":\"https://assets.jcaigc.cn/img1.jpg\",\"start\":0,\"end\":3000000,\"duration\":5000000,\"height\":1080,\"width\":1920,\"in_animation\":\"fade_in\",\"in_animation_duration\":500000,\"loop_animation\":\"bounce\",\"loop_animation_duration\":1000000,\"out_animation\":\"fade_out\",\"out_animation_duration\":500000,\"transition\":\"cross_fade\",\"transition_duration\":300000},{\"img_url\":\"https://assets.jcaigc.cn/img2.png\",\"start\":3000000,\"end\":6000000,\"duration\":5000000,\"height\":1080,\"width\":1920,\"in_animation\":\"fade_in\",\"in_animation_duration\":500000,\"loop_animation\":\"bounce\",\"loop_animation_duration\":1000000,\"out_animation\":\"fade_out\",\"out_animation_duration\":500000,\"transition\":\"cross_fade\",\"transition_duration\":300000}]"
}
```

### Response Field Description

| Field | Type | Description |
|-------|------|-------------|
| infos | string | Image information JSON string |

### Error Response (4xx/5xx)

```json
{
  "detail": "Error message description"
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
    "in_animation": "fade_in",
    "loop_animation": "bounce",
    "out_animation": "fade_out",
    "transition": "cross_fade"
  }'
```

## Error Code Description

| Error Code | Error Message | Description | Solution |
|------------|---------------|-------------|----------|
| 400 | imgs is required | Missing image URL parameter | Provide valid image URL array |
| 400 | timelines is required | Missing timeline parameter | Provide valid timeline array |
| 400 | Array length mismatch | imgs and timelines array lengths don't match | Ensure both arrays have the same length |
| 404 | Image resource not found | Image URL inaccessible | Check if image URL is accessible |
| 500 | Image information generation failed | Internal processing error | Contact technical support |

## Notes

1. **Array Matching**: imgs and timelines array lengths must be the same
2. **Time Unit**: All time parameters use microseconds (1 second = 1,000,000 microseconds)
3. **Resolution Settings**: height and width parameters are used to set image display resolution
4. **Animation Effects**: Support entrance animation, loop animation, exit animation, and transition effects
5. **Network Access**: Image URLs must be accessible
6. **Format Support**: Support common image formats (JPG, PNG, GIF, etc.)

## Workflow

1. Validate required parameters (imgs, timelines)
2. Check array length matching
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