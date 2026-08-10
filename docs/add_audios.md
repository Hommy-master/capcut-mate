# ADD_AUDIOS API Documentation

## 🌐 Language Switch
[中文版](./add_audios.zh.md) | [English](./add_audios.md)

## Interface Information

```
POST /openapi/capcut-mate/v1/add_audios
```

## Function Description

Batch add audio materials to existing drafts. This interface supports adding multiple audio files to Jianying drafts, creating background music, sound effects, narration and other audio content for videos. Audio will be added to separate audio tracks without affecting video content.

## More Documentation

📖 For more detailed documentation and tutorials, please visit: [https://docs.jcaigc.cn](https://docs.jcaigc.cn)

## Request Parameters

```json
{
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
  "audio_infos": "[{\"audio_url\":\"https://assets.jcaigc.cn/audio1.mp3\",\"start\":0,\"end\":5000000,\"duration\":10000000,\"volume\":1.0,\"audio_effect\":\"reverb\"}]"
}
```

### Parameter Description

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| draft_url | string | ✅ | - | Complete URL of the target draft |
| audio_infos | string | ✅ | - | JSON string of audio information array |

### audio_infos Array Structure

audio_infos is a JSON string that resolves to an array, with each element containing the following fields:

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| audio_url | string | ✅ | - | URL address of the audio file |
| start | number | ✅ | - | Audio start playback time (microseconds) |
| end | number | ✅ | - | Audio end playback time (microseconds) |
| duration | number | ❌ | Automatically obtained | Total audio duration (microseconds), automatically obtained if not provided |
| volume | number | ❌ | 1.0 | Volume size (0.0-2.0) |
| audio_effect | string | ❌ | None | Audio effect name |

### Parameter Details

#### Time Parameters

- **start**: Start time of the audio on the timeline, unit microseconds (1 second = 1,000,000 microseconds)
- **end**: End time of the audio on the timeline, unit microseconds
- **duration**: Total duration of the audio file, used for material creation, unit microseconds, automatically obtained if not provided
- **Playback Duration**: Actual playback duration = end - start

#### Volume Control

- **volume**: Audio volume size
  - 1.0 = Original volume
  - 0.5 = Half volume
  - 0.0 = Mute
  - Range: 0.0 - 2.0

#### Audio Effects

- **audio_effect**: Audio effect name
  - None = No audio effect
  - Example: `"reverb"` (reverb effect)

## Response Format

### Success Response (200)

```json
{
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
  "track_id": "audio-track-uuid",
  "audio_ids": ["audio1-uuid", "audio2-uuid", "audio3-uuid"]
}
```

### Response Field Description

| Field | Type | Description |
|-------|------|-------------|
| draft_url | string | Updated draft URL |
| track_id | string | Audio track ID |
| audio_ids | array | List of added audio IDs |

### Error Response (4xx/5xx)

```json
{
  "detail": "Error message description"
}
```

## Usage Examples

### cURL Examples

#### 1. Basic Audio Addition

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_audios \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "audio_infos": "[{\"audio_url\":\"https://assets.jcaigc.cn/bgm.mp3\",\"start\":0,\"end\":10000000,\"duration\":15000000,\"volume\":0.8}]"
  }'
```

#### 2. Batch Adding Multiple Audios

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_audios \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "audio_infos": "[{\"audio_url\":\"https://assets.jcaigc.cn/intro.mp3\",\"start\":0,\"end\":3000000,\"duration\":5000000,\"volume\":1.0},{\"audio_url\":\"https://assets.jcaigc.cn/bgm.mp3\",\"start\":3000000,\"end\":30000000,\"duration\":35000000,\"volume\":0.6}]"
  }'
```

#### 3. Audio with Fade In/Out Effects

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_audios \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "audio_infos": "[{\"audio_url\":\"https://assets.jcaigc.cn/outro.mp3\",\"start\":25000000,\"end\":30000000,\"duration\":8000000,\"volume\":0.9,\"audio_effect\":\"reverb\"}]"
  }'
```

## Error Code Description

| Error Code | Error Message | Description | Solution |
|------------|---------------|-------------|----------|
| 400 | draft_url is required | Missing draft URL parameter | Provide a valid draft URL |
| 400 | audio_infos is required | Missing audio information parameter | Provide valid audio information JSON |
| 400 | audio_infos format error | JSON format is incorrect | Check JSON string format |
| 400 | Audio configuration validation failed | Audio parameters do not meet requirements | Check parameters for each audio |
| 400 | audio_url is required | Audio URL missing | Provide URL for each audio |
| 400 | Time range invalid | end must be greater than start | Ensure end time is greater than start time |
| 400 | Volume value invalid | volume not in 0.0-2.0 range | Use volume value between 0.0-2.0 |
| 404 | Draft does not exist | Specified draft URL invalid | Check if draft URL is correct |
| 404 | Audio resource does not exist | Audio URL inaccessible | Check if audio URL is accessible |
| 500 | Audio processing failed | Internal processing error | Contact technical support |

## Notes

1. **JSON Format**: audio_infos must be a valid JSON string
2. **Time Unit**: All time parameters use microseconds (1 second = 1,000,000 microseconds)
3. **Audio Format**: Ensure audio file format is supported (e.g., MP3, WAV, AAC, etc.)
4. **File Size**: Large audio files may affect processing speed
5. **Network Access**: Audio URL must be accessible
6. **Volume Range**: Volume value must be within 0.0-2.0 range
7. **Track Limitation**: Audio overlap may occur in the same time period

## Workflow

1. Validate required parameters (draft_url, audio_infos)
2. Parse audio_infos JSON string
3. Validate parameter configuration for each audio
4. Obtain and decrypt draft content
5. Create audio track
6. Add audio segments to track
7. Apply volume and audio effects
8. Save and encrypt draft
9. Return processing result

## Related Interfaces

- [Create Draft](./create_draft.md)
- [Add Videos](./add_videos.md)
- [Add Images](./add_images.md)
- [Save Draft](./save_draft.md)
- [Generate Video](./gen_video.md)

---

<div align="right">

📚 **Project Resources**  
**GitHub**: [https://github.com/Hommy-master/capcut-mate](https://github.com/Hommy-master/capcut-mate)  
**Gitee**: [https://gitee.com/taohongmin-gitee/capcut-mate](https://gitee.com/taohongmin-gitee/capcut-mate)

</div>