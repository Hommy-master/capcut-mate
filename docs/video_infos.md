# VIDEO_INFOS API Documentation

###🌐 Language Switch
[中文版](./video_infos.zh.md) | [English](./video_infos.md)

## Interface Information

```
POST /openapi/capcut-mate/v1/video_infos
```

## Function Description

Generate video information based on video URLs and timelines. This interface converts video file URLs and timeline configurations into the video information format required by Jianying drafts, supporting mask and transition settings.

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
  "mask": "circle",
  "transition": "cross_fade",
  "transition_duration": 300000,
  "volume": 1.0
}
```

### Parameter Description

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| video_urls | array[string] |✅ | - | Video file URL array |
| timelines | array[object] |✅ | - | Timeline configuration array |
| height | number |❌ | 1080 | Video height |
| width | number |❌ | 1920 | Video width |
| mask | string |❌ | None | Mask type |
| transition | string |❌ | None | Transition effect |
| transition_duration | number |❌ | 300000 | Transition duration (microseconds) |
| volume | number |❌ | 1.0 | Volume level (0.0-2.0) |

## Response Format

### Success Response (200)

```json
{
  "infos": "[{\"video_url\":\"https://assets.jcaigc.cn/video1.mp4\",\"start\":0,\"end\":3000000,\"duration\":5000000,\"height\":1080,\"width\":1920,\"mask\":\"circle\",\"transition\":\"cross_fade\",\"transition_duration\":300000,\"volume\":1.0},{\"video_url\":\"https://assets.jcaigc.cn/video2.mp4\",\"start\":3000000,\"end\":6000000,\"duration\":5000000,\"height\":1080,\"width\":1920,\"mask\":\"circle\",\"transition\":\"cross_fade\",\"transition_duration\":300000,\"volume\":1.0}]"
}
```

### Response Field Description

| Field | Type | Description |
|-------|------|-------------|
| infos | string | Video information JSON string |

### Error Response (4xx/5xx)

```json
{
  "detail": "Error message description"
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
    "mask": "circle",
    "transition": "cross_fade",
    "volume": 0.8
  }'
```

## Error Code Description

| Error Code | Error Message | Description | Solution |
|------------|---------------|-------------|----------|
| 400 | video_urls is required | Missing video URL parameter | Provide valid video URL array |
| 400 | timelines is required | Missing timeline parameter | Provide valid timeline array |
| 400 | Array length mismatch | video_urls and timelines array lengths don't match | Ensure both arrays have the same length |
| 400 | Invalid volume value | Volume not in range 0.0-2.0 | Use volume value between 0.0-2.0 |
| 404 | Video resource not found | Video URL inaccessible | Check if video URL is accessible |
| 500 | Video information generation failed | Internal processing error | Contact technical support |

## Notes

1. **Array Matching**: video_urls and timelines array lengths must be the same
2. **Time Unit**: All time parameters use microseconds (1 second = 1,000,000 microseconds)
3. **Resolution Settings**: height and width parameters are used to set video display resolution
4. **Mask Types**: Support circle, rectangle, etc. mask types
5. **Volume Range**: volume value must be between 0.0-2.0
6. **Network Access**: Video URLs must be accessible

## Workflow

1. Validate required parameters (video_urls, timelines)
2. Check array length matching
3. Validate timeline parameter validity
4. Set video resolution parameters
5. Apply mask and transition parameters
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