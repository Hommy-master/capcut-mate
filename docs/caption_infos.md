# CAPTION_INFOS API Documentation

## 🌐 Language Switch
[中文版](./caption_infos.zh.md) | [English](./caption_infos.md)

## Interface Information

```
POST /openapi/capcut-mate/v1/caption_infos
```

## Function Description

Generate caption information based on text and timelines. This interface converts text content and timeline configurations into the caption information format required by Jianying drafts, supporting keyword highlighting, animation effects, and transition settings.

## More Documentation

📖 For more detailed documentation and tutorials, please visit: [https://docs.jcaigc.cn](https://docs.jcaigc.cn)

## Request Parameters

```json
{
  "texts": ["Welcome to watch", "This is an example"],
  "timelines": [
    {"start": 0, "end": 3000000},
    {"start": 3000000, "end": 6000000}
  ],
  "font_size": 24,
  "keyword_color": "#FF0000",
  "keyword_font_size": 28,
  "keywords": ["example"],
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
| texts | array[string] |✅ | - | Text content array |
| timelines | array[object] |✅ | - | Timeline configuration array |
| font_size | number |❌ | 24 | Font size |
| keyword_color | string |❌ | "#FF0000" | Keyword color |
| keyword_font_size | number |❌ | 28 | Keyword font size |
| keywords | array[string] |❌ | [] | Keyword array |
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
  "infos": "[{\"text\":\"Welcome to watch\",\"start\":0,\"end\":3000000,\"duration\":5000000,\"font_size\":24,\"keyword_color\":\"#FF0000\",\"keyword_font_size\":28,\"keywords\":[\"watch\"],\"in_animation\":\"fade_in\",\"in_animation_duration\":500000,\"loop_animation\":\"bounce\",\"loop_animation_duration\":1000000,\"out_animation\":\"fade_out\",\"out_animation_duration\":500000,\"transition\":\"cross_fade\",\"transition_duration\":300000},{\"text\":\"This is an example\",\"start\":3000000,\"end\":6000000,\"duration\":5000000,\"font_size\":24,\"keyword_color\":\"#FF0000\",\"keyword_font_size\":28,\"keywords\":[\"example\"],\"in_animation\":\"fade_in\",\"in_animation_duration\":500000,\"loop_animation\":\"bounce\",\"loop_animation_duration\":1000000,\"out_animation\":\"fade_out\",\"out_animation_duration\":500000,\"transition\":\"cross_fade\",\"transition_duration\":300000}]"
}
```

### Response Field Description

| Field | Type | Description |
|-------|------|-------------|
| infos | string | Caption information JSON string |

### Error Response (4xx/5xx)

```json
{
  "detail": "Error message description"
}
```

## Usage Examples

### cURL Examples

#### 1. Basic Caption Information Generation

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/caption_infos \
  -H "Content-Type: application/json" \
  -d '{
    "texts": ["Hello World"],
    "timelines": [{"start": 0, "end": 3000000}],
    "font_size": 28
  }'
```

#### 2. Caption Information with Highlighting

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/caption_infos \
  -H "Content-Type: application/json" \
  -d '{
    "texts": ["Welcome to watch our video", "This is a wonderful example"],
    "timelines": [{"start": 0, "end": 3000000}, {"start": 3000000, "end": 6000000}],
    "keyword_color": "#FF5500",
    "keywords": ["wonderful", "video"],
    "in_animation": "fade_in",
    "loop_animation": "bounce"
  }'
```

## Error Code Description

| Error Code | Error Message | Description | Solution |
|------------|---------------|-------------|----------|
| 400 | texts is required | Missing text content parameter | Provide valid text content array |
| 400 | timelines is required | Missing timeline parameter | Provide valid timeline array |
| 400 | Array length mismatch | texts and timelines array lengths don't match | Ensure both arrays have the same length |
| 400 | font_size must be greater than 0 | Invalid font size parameter | Use font size value greater than 0 |
| 500 | Caption information generation failed | Internal processing error | Contact technical support |

## Notes

1. **Array Matching**: texts and timelines array lengths must be the same
2. **Time Unit**: All time parameters use microseconds (1 second = 1,000,000 microseconds)
3. **Keyword Matching**: Keywords in keywords array will be highlighted in text
4. **Animation Effects**: Support entrance animation, loop animation, exit animation, and transition effects
5. **Color Format**: keyword_color uses hexadecimal color format (e.g., "#FF0000")
6. **Font Size**: Font size is in pixels

## Workflow

1. Validate required parameters (texts, timelines)
2. Check array length matching
3. Validate timeline parameter validity
4. Set font and color parameters
5. Apply animation effect parameters
6. Generate corresponding caption information for each text content
7. Convert information to JSON string format
8. Return processing result

## Related Interfaces

- [Create Draft](./create_draft.md)
- [Add Captions](./add_captions.md)
- [Timelines](./timelines.md)
- [Save Draft](./save_draft.md)

---

<div align="right">

📚 **Project Resources**  
**GitHub**: [https://github.com/Hommy-master/capcut-mate](https://github.com/Hommy-master/capcut-mate)  
**Gitee**: [https://gitee.com/taohongmin-gitee/capcut-mate](https://gitee.com/taohongmin-gitee/capcut-mate)

</div>

### Language Switch
[中文版](./caption_infos.zh.md) | [English](./caption_infos.md)