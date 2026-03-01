# ADD_VIDEOS API Documentation

## 🌐 Language Switch
[中文版](./add_videos.zh.md) | [English](./add_videos.md)

## Interface Information

```
POST /openapi/capcut-mate/v1/add_videos
```

## Function Description

Batch add video materials to existing drafts. This interface is a powerful video addition tool that supports batch processing of multiple videos, including time range control, transparency adjustment, mask effects, transition animations, volume control, scaling transformations, and other advanced features. Particularly suitable for creating complex multi-video combination scenes, such as picture-in-picture effects, video splicing, transition animations, etc.

## More Documentation

📖 For more detailed documentation and tutorials, please visit: [https://docs.jcaigc.cn](https://docs.jcaigc.cn)

## Request Parameters

```json
{
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
  "video_infos": "[{\"video_url\":\"https://assets.jcaigc.cn/video1.mp4\",\"width\":1024,\"height\":1024,\"start\":0,\"end\":5000000,\"duration\":5000000,\"mask\":\"circle\",\"transition\":\"fade\",\"transition_duration\":500000,\"volume\":0.8}]",
  "alpha": 0.5,
  "scale_x": 1.0,
  "scale_y": 1.0,
  "transform_x": 100,
  "transform_y": 200
}
```

### Parameter Description

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| draft_url | string | ✅ | - | Complete URL of the target draft |
| video_infos | string | ✅ | - | JSON string of video information array |
| alpha | number | ❌ | 1.0 | Global transparency (0-1) |
| scale_x | number | ❌ | 1.0 | X-axis scaling ratio |
| scale_y | number | ❌ | 1.0 | Y-axis scaling ratio |
| transform_x | number | ❌ | 0 | X-axis position offset (pixels) |
| transform_y | number | ❌ | 0 | Y-axis position offset (pixels) |

### video_infos Array Structure

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| video_url | string | ✅ | - | URL address of the video file |
| width | number | ❌ | - | Video width (pixels), automatically obtained if not provided |
| height | number | ❌ | - | Video height (pixels), automatically obtained if not provided |
| start | number | ✅ | - | Video start playback time (microseconds) |
| end | number | ✅ | - | Video end playback time (microseconds) |
| duration | number | ❌ | end-start | Total video duration (microseconds) |
| mask | string | ❌ | - | Mask type |
| transition | string | ❌ | - | Transition effect name |
| transition_duration | number | ❌ | 500000 | Transition duration (microseconds) |
| volume | number | ❌ | 1.0 | Volume size (0-1) |

### Parameter Details

#### Time Parameters

- **start**: Start time of the video on the timeline, unit microseconds (1 second = 1,000,000 microseconds)
- **end**: End time of the video on the timeline, unit microseconds
- **duration**: Total duration of the video file, used for material creation (optional parameter, defaults to end-start if not provided)
- **Playback Duration**: Actual playback duration = end - start

#### Transparency Parameters

- **alpha**: Global transparency, applied to all added videos
  - 1.0 = Fully opaque
  - 0.5 = Semi-transparent
  - 0.0 = Fully transparent
  - Range: 0.0 - 1.0

#### Scaling Parameters

- **scale_x/scale_y**: Scaling ratios in X/Y axis directions
- 1.0 = Original size, 0.5 = Half size, 2.0 = Double size
- Recommended range: 0.1 - 5.0

#### Position Parameters

- **transform_x/transform_y**: Position offsets in X/Y axis directions, unit pixels
- Positive values move right/down, negative values move left/up
- Canvas center as origin

#### Mask Types

Supported mask types (all optional, default is no mask):
- `circle` - Circular mask effect
- `heart` - Heart-shaped mask
- `star` - Star-shaped mask
- `rectangle` - Rectangular mask
- `linear` - Linear gradient mask
- `mirror` - Mirror reflection mask

#### Transition Effects

- **transition**: Transition effect name
- **transition_duration**: Transition duration
  - Minimum: 100,000 microseconds (0.1 seconds)
  - Maximum: 2,500,000 microseconds (2.5 seconds)
  - Recommended: 500,000 microseconds (0.5 seconds)

#### Volume Control

- **volume**: Video volume size
  - 1.0 = Original volume
  - 0.5 = Half volume
  - 0.0 = Mute
  - Range: 0.0 - 1.0

## Response Format

### Success Response (200)

```json
{
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
  "track_id": "video-track-uuid",
  "video_ids": ["video1-uuid", "video2-uuid", "video3-uuid"],
  "segment_ids": ["segment1-uuid", "segment2-uuid", "segment3-uuid"]
}
```

### Response Field Description

| Field | Type | Description |
|-------|------|-------------|
| draft_url | string | Updated draft URL |
| track_id | string | Video track ID |
| video_ids | array | List of added video IDs |
| segment_ids | array | List of segment IDs |

## Usage Examples

### cURL Examples

#### 1. Basic Video Addition

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_videos \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "video_infos": "[{\"video_url\":\"https://assets.jcaigc.cn/video1.mp4\",\"width\":1920,\"height\":1080,\"start\":0,\"end\":5000000,\"duration\":10000000}]"
  }'
```

#### 2. Batch Adding Multiple Videos

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_videos \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "video_infos": "[{\"video_url\":\"https://assets.jcaigc.cn/video1.mp4\",\"width\":1920,\"height\":1080,\"start\":0,\"end\":5000000,\"duration\":10000000},{\"video_url\":\"https://assets.jcaigc.cn/video2.mp4\",\"width\":1280,\"height\":720,\"start\":5000000,\"end\":10000000,\"duration\":8000000}]",
    "alpha": 0.8
  }'
```

#### 3. Video with Mask and Transition

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_videos \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "video_infos": "[{\"video_url\":\"https://assets.jcaigc.cn/video1.mp4\",\"width\":1024,\"height\":1024,\"start\":0,\"end\":5000000,\"duration\":10000000,\"mask\":\"circle\",\"transition\":\"fade\",\"transition_duration\":500000,\"volume\":0.8}]",
    "alpha": 1.0,
    "scale_x": 1.2,
    "scale_y": 1.2
  }'
```

#### 4. Picture-in-Picture Effect

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_videos \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "video_infos": "[{\"video_url\":\"https://assets.jcaigc.cn/main.mp4\",\"width\":1920,\"height\":1080,\"start\":0,\"end\":10000000,\"duration\":15000000},{\"video_url\":\"https://assets.jcaigc.cn/pip.mp4\",\"width\":640,\"height\":360,\"start\":2000000,\"end\":8000000,\"duration\":10000000}]",
    "transform_x": 300,
    "transform_y": -200,
    "scale_x": 0.3,
    "scale_y": 0.3
  }'
```

## Error Code Description

| Error Code | Error Message | Description | Solution |
|------------|---------------|-------------|----------|
| 400 | draft_url is required | Missing draft URL parameter | Provide a valid draft URL |
| 400 | video_infos is required | Missing video information parameter | Provide valid video information JSON |
| 400 | video_infos format error | JSON format is incorrect | Check JSON string format |
| 400 | video_url is required | Video URL missing | Provide URL for each video |
| 400 | Video dimensions invalid | width or height invalid | Provide positive width and height |
| 400 | Time range invalid | end must be greater than start | Ensure end time is greater than start time |
| 400 | Transparency value invalid | alpha not in 0-1 range | Use transparency value between 0-1 |
| 404 | Draft does not exist | Specified draft URL invalid | Check if draft URL is correct |
| 404 | Video resource does not exist | Video URL inaccessible | Check if video URL is accessible |
| 500 | Video processing failed | Internal processing error | Contact technical support |

## Notes

1. **JSON Format**: video_infos must be a valid JSON string
2. **Time Unit**: All time parameters use microseconds (1 second = 1,000,000 microseconds)
3. **Video Format**: Ensure video file format is supported (e.g., MP4, AVI, etc.)
4. **File Size**: Large video files may affect processing speed
5. **Network Access**: Video URL must be accessible
6. **Mask Limitation**: Only predefined mask types are supported
7. **Transition Limitation**: Transition duration has fixed range limitations
8. **Performance Consideration**: Batch adding a large number of videos may affect performance

## Workflow

1. Validate required parameters (draft_url, video_infos)
2. Parse video_infos JSON string
3. Validate parameter configuration for each video
4. Obtain and decrypt draft content
5. Create video track
6. Add video segments to track
7. Apply transparency, scaling and position transformation
8. Add mask and transition effects
9. Set volume
10. Save and encrypt draft
11. Return processing result

## Related Interfaces

- [Create Draft](./create_draft.md)
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