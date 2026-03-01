# ADD_IMAGES API Documentation

## 🌐 Language Switch
[中文版](./add_images.zh.md) | [English](./add_images.md)

## Interface Information

```
POST /openapi/capcut-mate/v1/add_images
```

## Function Description

Add images to existing drafts. This interface is used to add image materials to Jianying drafts within specified time periods, supporting transparency, scaling and position adjustments for images. Images can be used to enhance video visual effects, such as background images, watermarks, decorative images, etc.

## More Documentation

📖 For more detailed documentation and tutorials, please visit: [https://docs.jcaigc.cn](https://docs.jcaigc.cn)

## Request Parameters

```json
{
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
  "image_infos": "[{\"image_url\":\"https://assets.jcaigc.cn/image1.jpg\",\"width\":1920,\"height\":1080,\"start\":0,\"end\":5000000}]",
  "alpha": 1.0,
  "scale_x": 1.0,
  "scale_y": 1.0,
  "transform_x": 0,
  "transform_y": 0
}
```

### Parameter Description

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| draft_url | string | ✅ | - | Complete URL of the target draft |
| image_infos | string | ✅ | - | JSON string of image information array |
| alpha | number | ❌ | 1.0 | Image transparency, recommended range [0.0, 1.0] |
| scale_x | number | ❌ | 1.0 | Image X-axis scaling ratio |
| scale_y | number | ❌ | 1.0 | Image Y-axis scaling ratio |
| transform_x | number | ❌ | 0 | X-axis position offset (pixels) |
| transform_y | number | ❌ | 0 | Y-axis position offset (pixels) |

### image_infos Array Structure

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| image_url | string | ✅ | - | URL address of the image file |
| width | number | ✅ | - | Image width (pixels) |
| height | number | ✅ | - | Image height (pixels) |
| start | number | ✅ | - | Image start display time (microseconds) |
| end | number | ✅ | - | Image end display time (microseconds) |

### Parameter Details

#### Time Parameters

- **start**: Start time of the image on the timeline, unit microseconds (1 second = 1,000,000 microseconds)
- **end**: End time of the image on the timeline, unit microseconds
- **duration**: Image display duration = end - start

#### Transparency Parameters

- **alpha**: Image transparency
  - 1.0 = Fully opaque
  - 0.5 = Semi-transparent
  - 0.0 = Fully transparent
  - Recommended range: 0.0 - 1.0

#### Scaling Parameters

- **scale_x**: Image scaling ratio in X-axis direction
  - 1.0 = Original size
  - 0.5 = Shrink to half
  - 2.0 = Enlarge to double

- **scale_y**: Image scaling ratio in Y-axis direction
  - 1.0 = Original size
  - 0.5 = Shrink to half
  - 2.0 = Enlarge to double

#### Position Parameters

- **transform_x**: Image position offset in X-axis direction, unit pixels
  - Positive value moves right
  - Negative value moves left
  - Canvas center as origin
  - Actually stored as half-canvas-width units (assuming canvas width 1920, divided by 960)

- **transform_y**: Image position offset in Y-axis direction, unit pixels
  - Positive value moves down
  - Negative value moves up
  - Canvas center as origin
  - Actually stored as half-canvas-height units (assuming canvas height 1080, divided by 540)

#### Image Information Description

- **image_url**: URL address of the image
  - Format: Valid image URL
  - Example: `"https://assets.jcaigc.cn/image1.jpg"`
  - Supported formats: JPG, PNG and other common image formats

- **width/height**: Original size of the image
  - Used to calculate conversion ratio for position offset
  - Unit: pixels

## Response Format

### Success Response (200)

```json
{
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
  "track_id": "video-track-uuid",
  "image_ids": ["image1-uuid", "image2-uuid"],
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
| track_id | string | Video track ID |
| image_ids | array | List of image IDs |
| segment_ids | array | List of segment IDs |
| segment_infos | array | List of segment information, containing ID, start time and end time for each segment |

### Error Response (4xx/5xx)

```json
{
  "detail": "Error message description"
}
```

## Usage Examples

### cURL Examples

#### 1. Basic Image Addition

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_images \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "image_infos": "[{\"image_url\":\"https://assets.jcaigc.cn/photo1.jpg\",\"width\":1920,\"height\":1080,\"start\":0,\"end\":5000000}]"
  }'
```

#### 2. Image with Transparency

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_images \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "image_infos": "[{\"image_url\":\"https://assets.jcaigc.cn/logo.png\",\"width\":800,\"height\":600,\"start\":1000000,\"end\":6000000}]",
    "alpha": 0.8
  }'
```

#### 3. Image with Scaling and Position Offset

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_images \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "image_infos": "[{\"image_url\":\"https://assets.jcaigc.cn/watermark.png\",\"width\":300,\"height\":100,\"start\":2000000,\"end\":7000000}]",
    "scale_x": 0.5,
    "scale_y": 0.5,
    "transform_x": 700,
    "transform_y": -400
  }'
```

## Error Code Description

| Error Code | Error Message | Description | Solution |
|------------|---------------|-------------|----------|
| 400 | draft_url is required | Missing draft URL parameter | Provide a valid draft_url |
| 400 | image_infos is required | Missing image information parameter | Provide valid image_infos |
| 400 | image_url is required | Image URL missing | Provide URL for each image |
| 400 | Image dimensions invalid | width or height invalid | Provide positive width and height |
| 400 | Time range invalid | end must be greater than start | Ensure end time is greater than start time |
| 400 | Transparency invalid | alpha exceeds recommended range | Use transparency value within 0.0-1.0 range |
| 404 | Draft does not exist | Specified draft URL invalid | Check if draft URL is correct |
| 404 | Image does not exist | Specified image URL invalid | Confirm if image URL is correct |
| 500 | Image addition failed | Internal processing error | Contact technical support |

## Notes

1. **Time Unit**: All time parameters use microseconds (1 second = 1,000,000 microseconds)
2. **Image URL**: Ensure using valid image URL
3. **Time Range**: end must be greater than start
4. **Transparency Range**: alpha recommended within 0.0-1.0 range
5. **Position Parameters**: transform_x and transform_y unit is pixels, but internally converted to half-canvas units for storage
   - transform_x conversion formula: actual value / 960 (assuming canvas width 1920)
   - transform_y conversion formula: actual value / 540 (assuming canvas height 1080)
6. **Track Management**: System automatically creates video track
7. **Performance Consideration**: Avoid adding large number of images simultaneously

## Workflow

1. Validate required parameters (draft_url, image_infos)
2. Check validity of time ranges
3. Get draft from cache
4. Create video track (images as VideoSegment)
5. Create image adjustment settings
6. Create image segments
7. Add segments to track
8. Save draft
9. Return image information

## Related Interfaces

- [Create Draft](./create_draft.md)
- [Add Videos](./add_videos.md)
- [Add Audios](./add_audios.md)
- [Add Stickers](./add_sticker.md)
- [Save Draft](./save_draft.md)
- [Generate Video](./gen_video.md)

---

<div align="right">

📚 **Project Resources**  
**GitHub**: [https://github.com/Hommy-master/capcut-mate](https://github.com/Hommy-master/capcut-mate)  
**Gitee**: [https://gitee.com/taohongmin-gitee/capcut-mate](https://gitee.com/taohongmin-gitee/capcut-mate)

</div>