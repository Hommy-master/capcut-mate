# ADD_STICKER API Documentation

## 🌐 Language Switch
[中文版](./add_sticker.zh.md) | [English](./add_sticker.md)

## Interface Information

```
POST /openapi/capcut-mate/v1/add_sticker
```

## Function Description

Add stickers to existing drafts. This interface is used to add sticker materials to Jianying drafts within specified time periods, supporting sticker scaling and position adjustments. Stickers can be used to enhance the visual effects of videos, such as expressions, decorations, text, etc.

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
  - Actually stored in half canvas width units (divided by the draft canvas width, e.g. 1920 for a 1920×1080 draft)

- **transform_y**: Y-axis position offset of the sticker, unit pixels
  - Positive values move down
  - Negative values move up
  - Origin at canvas center
  - Actually stored in half canvas height units (divided by the draft canvas height, e.g. 1080 for a 1920×1080 draft)

#### Sticker ID Description

- **sticker_id**: Unique identifier of the sticker
  - Format: Usually numeric string
  - Example: `"7326810673609018675"`
  - Acquisition: Through Jianying sticker library or related APIs

## Response Format

### Success Response (200)

```json
{
  "code": 0,
  "message": "success",
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

### Error Response

```json
{
  "code": 2011,
  "message": "Invalid sticker information, please check if sticker parameters are correct."
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
| 1001 | Parameter validation failed | Request body failed schema validation, e.g. a required field is missing or has the wrong type | Check parameter types and required fields |
| 2001 | Invalid draft URL | `draft_url` is missing, malformed, or the draft is not in the cache | Pass the `draft_url` returned by `create_draft` |
| 2011 | Invalid sticker information | `end` is not greater than `start` | Ensure end time is greater than start time |
| 2012 | Sticker addition failed | Failed while creating the sticker track/segment or saving the draft | Check the draft state and retry |
| 2042 | Draft lock acquisition timeout | Only one operation is allowed on a draft at a time | Retry later |

## Notes

1. **Time Unit**: All time parameters use microseconds (1 second = 1,000,000 microseconds)
2. **Sticker ID**: Ensure using valid sticker ID
3. **Time Range**: end must be greater than start
4. **Scale Range**: scale recommended within 0.1-5.0 range
5. **Position Parameters**: transform_x and transform_y units are pixels, but internally converted to half canvas units for storage
   - transform_x conversion formula: actual value / draft canvas width (e.g. 1920)
   - transform_y conversion formula: actual value / draft canvas height (e.g. 1080)
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