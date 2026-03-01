# ADD_CAPTIONS API Documentation

## 🌐 Language Switch
[中文版](./add_captions.zh.md) | [English](./add_captions.md)

## Interface Information

```
POST /openapi/capcut-mate/v1/add_captions
```

## Function Description

Batch add captions to existing drafts. This interface is used to add captions to Jianying drafts within specified time periods, supporting rich caption style settings including text color, border color, alignment, transparency, font, font size, letter spacing, line spacing, scaling, and position adjustments.

## More Documentation

📖 For more detailed documentation and tutorials, please visit: [https://docs.jcaigc.cn](https://docs.jcaigc.cn)

## Request Parameters

```json
{
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
  "captions": "[{\"start\":0,\"end\":10000000,\"text\":\"Hello, Jianying\",\"keyword\":\"Hello\",\"keyword_color\":\"#457616\",\"keyword_font_size\":15,\"font_size\":15}]",
  "text_color": "#ffffff",
  "border_color": null,
  "alignment": 1,
  "alpha": 1.0,
  "font": null,
  "font_size": 15,
  "letter_spacing": null,
  "line_spacing": null,
  "scale_x": 1.0,
  "scale_y": 1.0,
  "transform_x": 0.0,
  "transform_y": 0.0,
  "style_text": false
}
```

### Parameter Description

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| draft_url | string |✅ | - | Complete URL of the target draft |
| captions | string |✅ | - | JSON string of caption information list |
| text_color | string | ❌ | "#ffffff" | Text color (hexadecimal) |
| border_color | string |❌ | null | Border color (hexadecimal) |
| alignment | integer |❌ | 1 | Text alignment (0-5) |
| alpha | number |❌ | 1.0 | Text transparency (0.0-1.0) |
| font | string |❌ | null | Font name |
| font_size | integer |❌ | 15 | Font size |
| letter_spacing | number |❌ | null | Letter spacing |
| line_spacing | number | ❌ | null | Line spacing |
| scale_x | number |❌ | 1.0 | Horizontal scaling factor |
| scale_y | number | ❌ | 1.0 | Vertical scaling factor |
| transform_x | number | ❌ | 0.0 | Horizontal position offset |
| transform_y | number | ❌ | 0.0 | Vertical position offset |
| style_text | boolean |❌ | false | Whether to apply rich text styling |

### Parameter Details

#### captions Array Structure

`captions` is a JSON string containing an array of caption objects, each with the following fields:

```json
[
  {
    "start": 0,
    "end": 10000000,
    "text": "Hello, Jianying",
    "keyword": "Hello",
    "keyword_color": "#457616",
    "keyword_font_size": 15,
    "font_size": 15
  }
]
```

**Field Description**:
- `start`: Caption start time (microseconds)
- `end`: Caption end time (microseconds)
- `text`: Caption text content
- `keyword`: Keyword to highlight
- `keyword_color`: Keyword highlight color
- `keyword_font_size`: Keyword font size
- `font_size`: Base font size

#### Time Parameters

- **start**: Start time of the caption on the timeline, unit microseconds (1 second = 1,000,000 microseconds)
- **end**: End time of the caption on the timeline, unit microseconds
- **Duration**: Caption duration = end - start

#### Style Parameters

- **text_color**: Main text color in hexadecimal format (e.g., "#ffffff" for white)
- **border_color**: Text border color, null means no border
- **alignment**: Text alignment mode (0-5)
- **alpha**: Text transparency (0.0 = fully transparent, 1.0 = fully opaque)
- **font_size**: Base font size in pixels
- **scale_x/scale_y**: Horizontal/vertical scaling factors
- **transform_x/transform_y**: Position offset values

## Response Format

### Success Response (200)

```json
{
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
  "track_id": "caption-track-uuid",
  "text_ids": ["text1-uuid", "text2-uuid"],
  "segment_ids": ["segment1-uuid", "segment2-uuid"],
  "segment_infos": [
    {
      "id": "segment1-uuid",
      "start": 0,
      "end": 5000000
    }
  ]
}
```

### Response Field Description

| Field | Type | Description |
|-------|------|-------------|
| draft_url | string | Updated draft URL |
| track_id | string | Caption track ID |
| text_ids | array | List of added text IDs |
| segment_ids | array | List of segment IDs |
| segment_infos | array | Segment information array |

### Error Response (4xx/5xx)

```json
{
  "detail": "Error message description"
}
```

## Usage Examples

### cURL Examples

#### 1. Basic Caption Addition

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_captions \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "captions": "[{\"start\":0,\"end\":5000000,\"text\":\"Welcome to Jianying\"}]",
    "text_color": "#ffffff",
    "font_size": 18
  }'
```

#### 2. Caption with Keyword Highlighting

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_captions \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "captions": "[{\"start\":0,\"end\":3000000,\"text\":\"Hello World\",\"keyword\":\"Hello\",\"keyword_color\":\"#ff0000\",\"keyword_font_size\":20}]",
    "text_color": "#ffffff",
    "font_size": 16
  }'
```

#### 3. Styled Caption with Positioning

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_captions \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "captions": "[{\"start\":2000000,\"end\":7000000,\"text\":\"Styled Caption\"}]",
    "text_color": "#00ff00",
    "border_color": "#000000",
    "alignment": 2,
    "alpha": 0.8,
    "font_size": 20,
    "scale_x": 1.2,
    "scale_y": 1.2,
    "transform_x": 100,
    "transform_y": 50
  }'
```

## Error Code Description

| Error Code | Error Message | Description | Solution |
|------------|---------------|-------------|----------|
| 400 | draft_url is required | Missing draft URL parameter | Provide a valid draft URL |
| 400 | captions is required | Missing caption information parameter | Provide valid caption information JSON |
| 400 | captions format error | JSON format is incorrect | Check JSON string format |
| 400 | Caption configuration validation failed | Caption parameters do not meet requirements | Check parameters for each caption |
| 400 | start is required | Caption start time missing | Provide start time for each caption |
| 400 | end is required | Caption end time missing | Provide end time for each caption |
| 400 | text is required | Caption text content missing | Provide text content for each caption |
| 400 | Time range invalid | end must be greater than start | Ensure end time is greater than start time |
| 400 | Font size invalid | font_size must be positive | Use positive font size value |
| 400 | Alpha value invalid | alpha not in 0.0-1.0 range | Use alpha value between 0.0-1.0 |
| 404 | Draft does not exist | Specified draft URL invalid | Check if draft URL is correct |
| 500 | Caption processing failed | Internal processing error | Contact technical support |

## Notes

1. **JSON Format**: captions must be a valid JSON string
2. **Time Unit**: All time parameters use microseconds (1 second = 1,000,000 microseconds)
3. **Color Format**: Colors use hexadecimal format (e.g., "#ffffff")
4. **Font Support**: Ensure font names are supported by the system
5. **Position Range**: transform_x and transform_y values should be within reasonable ranges
6. **Scaling**: Scale factors should typically be between 0.1-5.0
7. **Track Management**: Multiple captions will be added to the same caption track

## Workflow

1. Validate required parameters (draft_url, captions)
2. Parse captions JSON string
3. Validate parameter configuration for each caption
4. Obtain and decrypt draft content
5. Create caption track
6. Add text segments to track
7. Apply styling and positioning
8. Save and encrypt draft
9. Return processing result

## Related Interfaces

- [Create Draft](./create_draft.md)
- [Add Videos](./add_videos.md)
- [Add Images](./add_images.md)
- [Add Text Style](./add_text_style.md)
- [Save Draft](./save_draft.md)

---

<div align="right">

📚 **Project Resources**  
**GitHub**: [https://github.com/Hommy-master/capcut-mate](https://github.com/Hommy-master/capcut-mate)  
**Gitee**: [https://gitee.com/taohongmin-gitee/capcut-mate](https://gitee.com/taohongmin-gitee/capcut-mate)

</div>