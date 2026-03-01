# ADD_STICKER API Documentation

### 🌐 Language Switch
[中文版](./add_sticker.zh.md) | [English](./add_sticker.md)

## Interface Information

```
POST /openapi/capcut-mate/v1/add_sticker
```

## Function Description

Add stickers to existing drafts. This interface is used to add sticker materials to Jianying drafts within specified time periods, supporting sticker scaling and position adjustments. Stickers can be used to enhance the visual effects of videos, such as expressions, decorations, text, etc.

## More Documentation

📖 For more detailed documentation and tutorials, please visit: [https://docs.jcaigc.cn](https://docs.jcaigc.cn)

## Request Parameters

```json
{
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
  "sticker_id": "7326810673609018675",
  "start": 0,
  "end": 5000000,
  "scale": 1.0,
  "transform_x": 0,
  "transform_y": 0
}
```

### Parameter Description

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| draft_url | string |✅ | - | Complete URL of the target draft |
| sticker_id | string |✅ | - | Unique ID of the sticker |
| start | number |✅ | - | Sticker start time (microseconds) |
| end | number | ✅ | - | Sticker end time (microseconds) |
| scale | number |❌ | 1.0 | Sticker scale ratio, recommended range [0.1, 5.0] |
| transform_x | number | ❌ | 0 | X-axis position offset (pixels) |
| transform_y | number | ❌ | 0 | Y-axis position offset (pixels) |

### Parameter Details

#### Time Parameters

- **start**: Start time of the sticker on the timeline, unit microseconds (1 second = 1,000,000 microseconds)
- **end**: End time of the sticker on the timeline, unit microseconds
- **duration**: Sticker display duration = end - start

#### Scale Parameters

- **scale**: Scale ratio of the sticker
  - 1.0 = Original size
  - 0.5 = Half size
  - 2.0 = Double size
  - Recommended range: 0.1 - 5.0

#### Position Parameters

- **transform_x**: X-axis position offset of the sticker, unit pixels
  - Positive values move right
  - Negative values move left
  - Origin at canvas center
  - Actually stored in half canvas width units (assuming canvas width 1920, i.e., divided by 960)

- **transform_y**: Y-axis position offset of the sticker, unit pixels
  - Positive values move down
  - Negative values move up
  - Origin at canvas center
  - Actually stored in half canvas height units (assuming canvas height 1080, i.e., divided by 540)

#### Sticker ID Description

- **sticker_id**: Unique identifier of the sticker
  - Format: Usually numeric string
  - Example: `"7326810673609018675"`
  - Acquisition: Through Jianying sticker library or related APIs

## Response Format

### Success Response (200)

```json
{
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
  "sticker_id": "7326810673609018675",
  "track_id": "track-uuid",
  "segment_id": "segment-uuid",
  "duration": 5000000
}
```

### Response Field Description

| Field | Type | Description |
|-------|------|-------------|
| draft_url | string | Updated draft URL |
| sticker_id | string | Unique ID of the sticker |
| track_id | string | Sticker track ID |
| segment_id | string | Sticker segment ID |
| duration | number | Sticker display duration (microseconds) |

### Error Response (4xx/5xx)

```json
{
  "detail": "Error message description"
}
```

## Usage Examples

### cURL Examples

#### 1. Basic Sticker Addition

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_sticker \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "sticker_id": "7326810673609018675",
    "start": 0,
    "end": 5000000
  }'
```

#### 2. Sticker with Scaling

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_sticker \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "sticker_id": "7326810673609018675",
    "start": 1000000,
    "end": 6000000,
    "scale": 1.5
  }'
```

#### 3. Sticker with Position Offset

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_sticker \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "sticker_id": "7326810673609018675",
    "start": 2000000,
    "end": 7000000,
    "scale": 0.8,
    "transform_x": 200,
    "transform_y": -100
  }'
```

## Error Code Description

| Error Code | Error Message | Description | Solution |
|------------|---------------|-------------|----------|
| 400 | draft_url is required | Missing draft URL parameter | Provide a valid draft_url |
| 400 | sticker_id is required | Missing sticker ID parameter | Provide a valid sticker_id |
| 400 | start is required | Missing start time parameter | Provide a valid start time |
| 400 | end is required | Missing end time parameter | Provide a valid end time |
| 400 | Time range invalid | end must be greater than start | Ensure end time is greater than start time |
| 400 | Scale ratio invalid | scale out of recommended range | Use scale values within 0.1-5.0 range |
| 400 | Invalid sticker information, please check sticker parameters | Sticker parameter validation failed | Check if sticker parameters meet requirements |
| 404 | Draft does not exist | Specified draft URL invalid | Check if draft URL is correct |
| 404 | Sticker does not exist | Specified sticker ID invalid | Confirm if sticker ID is correct |
| 500 | Sticker addition failed | Internal processing error | Contact technical support |

## Notes

1. **Time Unit**: All time parameters use microseconds (1 second = 1,000,000 microseconds)
2. **Sticker ID**: Ensure using valid sticker ID
3. **Time Range**: end must be greater than start
4. **Scale Range**: scale recommended within 0.1-5.0 range
5. **Position Parameters**: transform_x and transform_y units are pixels, but internally converted to half canvas units for storage
   - transform_x conversion formula: actual value / 960 (assuming canvas width 1920)
   - transform_y conversion formula: actual value / 540 (assuming canvas height 1080)
6. **Track Management**: System automatically creates sticker track
7. **Performance Consideration**: Avoid adding large numbers of stickers simultaneously

## Workflow

1. Validate required parameters (draft_url, sticker_id, start, end)
2. Check validity of time range
3. Get draft from cache
4. Create sticker track (if not exists)
5. Create image adjustment settings
6. Create sticker segment
7. Add segment to track
8. Save draft
9. Return sticker information

## Related Interfaces

- [Create Draft](./create_draft.md)
- [Add Videos](./add_videos.md)
- [Add Audios](./add_audios.md)
- [Add Images](./add_images.md)
- [Save Draft](./save_draft.md)
- [Generate Video](./gen_video.md)

---

<div align="right">

📚 **Project Resources**  
**GitHub**: [https://github.com/Hommy-master/capcut-mate](https://github.com/Hommy-master/capcut-mate)  
**Gitee**: [https://gitee.com/taohongmin-gitee/capcut-mate](https://gitee.com/taohongmin-gitee/capcut-mate)

</div>