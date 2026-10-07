# VIDEO_INFOS API Documentation

## 🌐 Language Switch
[中文版](./video_infos.zh.md) | [English](./video_infos.md)

## Interface Information

```
POST /openapi/capcut-mate/v1/video_infos
```

## Function Description

Generate video information based on video URLs and timelines. This interface converts video file URLs and timeline configurations into the video information format required by Jianying drafts, supporting transition settings.

## More Documentation

📖 For more detailed documentation and tutorials, please visit: [https://docs.jcaigc.cn](https://docs.jcaigc.cn)

## Request Parameters

```json
{
  "video_urls": ["https://assets.jcaigc.cn/video1.mp4", "https://assets.jcaigc.cn/video2.mp4"],
  "timelines": [
    {"start": 0, "end": 3000000},
    {"start": 3000000, "end": 6000000}
  ],
  "height": 1080,
  "width": 1920,
  "mask": "圆形",
  "transition": "叠化",
  "transition_duration": 300000,
  "volume": 1.0
}
```

### Parameter Description

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| video_urls | array[string] |✅ | - | Video file URL array |
| timelines | array[object] |✅ | - | Timeline configuration array |
| height | integer |❌ | None | Video height |
| width | integer |❌ | None | Video width |
| mask | string |❌ | None | Mask name: 圆形, 矩形, 爱心, 星形; carried into `video_infos` but not applied by [add_videos](./add_videos.md) — use `add_masks` |
| transition | string |❌ | None | Transition name; see [add_videos](./add_videos.md) |
| transition_duration | integer |❌ | None | Transition duration (microseconds) |
| volume | number |❌ | 1.0 | Volume level (0-10) |

### Available Transition Names

For the full list of valid `transition` values, see [add_videos](./add_videos.md) → Supported Transition Names. For intro/outro/loop clip animations, see [add_images](./add_images.md).

## Response Format

### Success Response (200)

```json
{
  "code": 0,
  "message": "success",
  "infos": "[{\"video_url\":\"https://assets.jcaigc.cn/video1.mp4\",\"start\":0,\"end\":3000000,\"duration\":3000000,\"height\":1080,\"width\":1920,\"mask\":\"圆形\",\"transition\":\"叠化\",\"transition_duration\":300000,\"volume\":1.0},{\"video_url\":\"https://assets.jcaigc.cn/video2.mp4\",\"start\":3000000,\"end\":6000000,\"duration\":3000000,\"height\":1080,\"width\":1920,\"mask\":\"圆形\",\"transition\":\"叠化\",\"transition_duration\":300000,\"volume\":1.0}]"
}
```

### Response Field Description

| Field | Type | Description |
|-------|------|-------------|
| infos | string | Video information JSON string |

### Error Response

```json
{
  "code": 1001,
  "message": "Parameter validation failed"
}
```

## Usage Examples

### cURL Examples

#### 1. Basic Video Information Generation

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/video_infos \
  -H "Content-Type: application/json" \
  -d '{
    "video_urls": ["https://assets.jcaigc.cn/intro.mp4"],
    "timelines": [{"start": 0, "end": 5000000}],
    "height": 1080,
    "width": 1920
  }'
```

#### 2. Video Information with Mask and Transition

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/video_infos \
  -H "Content-Type: application/json" \
  -d '{
    "video_urls": ["https://assets.jcaigc.cn/clip1.mp4", "https://assets.jcaigc.cn/clip2.mp4"],
    "timelines": [{"start": 0, "end": 3000000}, {"start": 3000000, "end": 6000000}],
    "mask": "圆形",
    "transition": "叠化",
    "volume": 0.8
  }'
```

## Error Code Description

| Error Code | Error Message | Description | Solution |
|------------|---------------|-------------|----------|
| 1001 | Parameter validation failed | Request body failed schema validation (`video_urls`/`timelines` missing, timeline item lacking `start`/`end`, or wrong types) | Check parameter types and required fields |

## Notes

1. **Array Matching**: if `video_urls` and `timelines` lengths differ, the shorter length is used (no hard error)
2. **Time Unit**: All time parameters use microseconds (1 second = 1,000,000 microseconds)
3. **Resolution Settings**: height and width parameters are used to set video display resolution
4. **Mask Types**: `mask` is written into `video_infos` as 圆形, 矩形, 爱心 or 星形, but `add_videos` does not apply it — mask the segment with `add_masks`
5. **Volume Range**: volume value must be between 0-10
6. **Network Access**: Video URLs must be accessible

## Workflow

1. Validate required parameters (video_urls, timelines)
2. Align the two arrays by the shorter length
3. Validate timeline parameter validity
4. Set video resolution parameters
5. Apply transition parameters and carry `mask` through (not applied by `add_videos`)
6. Generate corresponding video information for each video URL
7. Convert information to JSON string format
8. Return processing result

## Related Interfaces

- [Create Draft](./create_draft.md)
- [Add Videos](./add_videos.md)
- [Timelines](./timelines.md)
- [Save Draft](./save_draft.md)

---

<div align="right">

📚 **Project Resources**  
**GitHub**: [https://github.com/Hommy-master/capcut-mate](https://github.com/Hommy-master/capcut-mate)  
**Gitee**: [https://gitee.com/taohongmin-gitee/capcut-mate](https://gitee.com/taohongmin-gitee/capcut-mate)

</div>

### Language Switch
[中文版](./video_infos.zh.md) | [English](./video_infos.md)