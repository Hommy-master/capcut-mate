# EASY_CREATE_MATERIAL API Documentation

## 🌐 Language Switch
[中文版](./easy_create_material.zh.md) | [English](./easy_create_material.md)

## Interface Information

```
POST /openapi/capcut-mate/v1/easy_create_material
```

## Function Description

Add multiple types of material content to existing drafts, including audio, video, images, and text. This interface can add multiple media materials to drafts at once, automatically handling material duration, dimensions, and other properties, and intelligently managing different types of media tracks. It is one of the core interfaces for video creation.

## More Documentation

📖 For more detailed documentation and tutorials, please visit: [https://docs.jcaigc.cn](https://docs.jcaigc.cn)

## Request Parameters

```json
{
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
  "audio_url": "https://assets.jcaigc.cn/audio.mp3",
  "text": "Hello World",
  "img_url": "https://s.coze.cn/t/JTa5Ne6_liY/",
  "video_url": "https://assets.jcaigc.cn/video.mp4",
  "text_color": "#ff0000",
  "font_size": 20,
  "text_transform_y": 100
}
```

### Parameter Description

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| draft_url | string |✅ | - | Complete URL of the target draft |
| audio_url | string |✅ | - | Audio file URL, cannot be empty or null |
| text | string |❌ | null | Text content to add |
| img_url | string |❌ | null | Image file URL |
| video_url | string |❌ | null | Video file URL |
| text_color | string |❌ | "#ffffff" | Text color (hexadecimal format) |
| font_size | integer |❌ | 15 | Font size |
| text_transform_y | integer |❌ | 0 | Text Y-axis position offset |

### Parameter Details

#### Required Parameters

- **draft_url**: Complete URL of the target draft
  - Format: Must be a valid Jianying draft URL
  - Example: `"https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258"`

- **audio_url**: Audio file URL
  - Required parameter, cannot be empty or "null"
  - Supported formats: MP3, WAV, AAC and other common audio formats
  - Note: Audio is a required parameter, other material types are optional

#### Optional Parameters

- **text**: Text content to add
  - Type: UTF-8 text
  - Default: null (no text added)
  - Note: If provided, text material will be added to the draft

- **img_url**: Image file URL
  - Type: Valid image URL
  - Default: null (no image added)
  - Supported formats: JPEG, PNG, GIF and other common image formats
  - Note: If provided, image material will be added to the draft

- **video_url**: Video file URL
  - Type: Valid video URL
  - Default: null (no video added)
  - Supported formats: MP4, AVI, MOV and other common video formats
  - Note: If provided, video material will be added to the draft

- **text_color**: Text color
  - Type: Hexadecimal color code
  - Default: `"#ffffff"` (white)
  - Note: Set text color using standard hexadecimal format (e.g. #ffffff, #000000)

- **font_size**: Font size
  - Type: Integer
  - Default: 15
  - Note: Set text font size, recommended range 10-50

- **text_transform_y**: Text Y-axis position offset
  - Type: Integer
  - Default: 0
  - Note: Adjust vertical position of text in the frame, unit pixels

#### Material Processing Rules

- **Audio Processing**:
  - Automatically parse audio duration
  - Add to audio track
  - Support multiple audio formats

- **Video Processing**:
  - Fixed display duration 5 seconds
  - Maintain original resolution ratio
  - Add to video track

- **Image Processing**:
  - Default display duration 3 seconds
  - Automatically get image dimensions
  - Add to image track

- **Text Processing**:
  - Default display duration 5 seconds
  - Support color and font size settings
  - Adjustable vertical position

## Response Format

### Success Response (200)

```json
{
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258"
}
```

### Response Field Description

| Field | Type | Description |
|-------|------|-------------|
| draft_url | string | Updated draft URL |

### Error Response (4xx/5xx)

```json
{
  "detail": "Error message description"
}
```

## Usage Examples

### cURL Examples

#### 1. Add All Types of Materials

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/easy_create_material \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "audio_url": "https://assets.jcaigc.cn/audio.mp3",
    "text": "Hello World",
    "img_url": "https://s.coze.cn/t/JTa5Ne6_liY/",
    "video_url": "https://assets.jcaigc.cn/video.mp4",
    "text_color": "#ff0000",
    "font_size": 20,
    "text_transform_y": 100
  }'
```

#### 2. Add Only Audio and Text

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/easy_create_material \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "audio_url": "https://assets.jcaigc.cn/background_music.mp3",
    "text": "Welcome to watch",
    "text_color": "#0066ff",
    "font_size": 18
  }'
```

#### 3. Minimal Request (Audio Only)

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/easy_create_material \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "audio_url": "https://assets.jcaigc.cn/audio.wav"
  }'
```

## Error Code Description

| Error Code | Error Message | Description | Solution |
|------------|---------------|-------------|----------|
| 400 | draft_url is required | Missing draft URL parameter | Provide a valid draft_url |
| 400 | audio_url is required | Missing audio URL parameter | Provide a valid audio_url |
| 400 | Invalid draft information, please check draft parameters | Draft parameter validation failed | Check if draft parameters meet requirements |
| 404 | Draft does not exist | Specified draft URL invalid | Check if draft URL is correct |
| 500 | Material creation failed | Internal processing error | Contact technical support |

## Notes

1. **Audio Required**: audio_url is a required parameter, cannot be empty or null
2. **Material URLs**: Material URLs must be publicly accessible, HTTPS protocol recommended
3. **Text Color**: text_color uses standard hexadecimal format (e.g. #ffffff, #000000)
4. **Font Size**: font_size recommended range 10-50
5. **Position Offset**: text_transform_y used to adjust vertical position of text in the frame
6. **Duration Settings**: Different material types have different default display durations
   - Audio: Automatically get original duration
   - Video: Fixed 5 seconds
   - Image: Default 3 seconds
   - Text: Default 5 seconds
7. **Track Management**: System automatically creates tracks for different types of materials
8. **Performance Consideration**: Avoid adding large numbers of materials simultaneously

## Workflow

1. Validate required parameters (draft_url, audio_url)
2. Get draft from cache
3. Create audio track and add audio material
4. If provided, create video track and add video material
5. If provided, create image track and add image material
6. If provided, create text track and add text material
7. Save draft
8. Return updated draft URL

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