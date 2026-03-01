# GET_AUDIO_DURATION API Documentation

### 🌐 Language Switch
[中文版](./get_audio_duration.zh.md) | [English](./get_audio_duration.md)

## Interface Information

```
POST /openapi/capcut-mate/v1/get_audio_duration
```

## More Documentation

📖 For more detailed documentation and tutorials, please visit: [https://docs.jcaigc.cn](https://docs.jcaigc.cn)

## Function Description

Get the duration of audio files, supporting various common audio formats. Use FFprobe tool for precise audio analysis, returning the accurate duration of audio files in microseconds.

## More Documentation

📖 For more detailed documentation and tutorials, please visit: [https://docs.jcaigc.cn](https://docs.jcaigc.cn)

## Request Parameters

```json
{
  "mp3_url": "https://assets.jcaigc.cn/audio/sample.mp3"
}
```

### Parameter Description

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| mp3_url | string |✅ | - | Audio file URL, supporting mp3, wav, m4a and other common audio formats |

### Parameter Details

#### Audio URL Parameter

- **mp3_url**: Complete URL address of the audio file
  - Supported formats: mp3, wav, aac, flac, m4a and other common audio formats
  - Need to ensure URL is accessible and file is complete

## Response Format

### Success Response (200)

```json
{
  "duration": 2325333
}
```

### Response Field Description

| Field | Type | Description |
|-------|------|-------------|
| duration | number | Audio duration, unit: microseconds |

### Error Response (4xx/5xx)

```json
{
  "detail": "Error message description"
}
```

## Usage Examples

### cURL Examples

#### 1. Basic Audio Duration Retrieval

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_audio_duration \
  -H "Content-Type: application/json" \
  -d '{
    "mp3_url": "https://assets.jcaigc.cn/audio/sample.mp3"
  }'
```

## Error Code Description

| Error Code | Error Message | Description | Solution |
|------------|---------------|-------------|----------|
| 400 | mp3_url is required | Missing audio URL parameter | Provide a valid mp3_url |
| 404 | Audio file cannot be accessed | Specified audio URL invalid | Check if audio URL is correct |
| 500 | Audio duration retrieval failed | Internal processing error | Contact technical support |

## Notes

1. **Time Unit**: Returned duration uses microseconds (1 second = 1,000,000 microseconds)
2. **Audio Formats**: Support mp3, wav, aac, flac, m4a and other common audio formats
3. **File Size**: Recommended to control within reasonable range, overly large files may cause timeout
4. **Network Access**: Ensure provided audio URL can be accessed normally

## Workflow

1. Validate required parameter (mp3_url)
2. Download audio file to temporary directory
3. Use ffprobe to analyze audio file and get duration
4. Clean up temporary files
5. Return audio duration information

## Related Interfaces

- [Add Audios](./add_audios.md)
- [Add Videos](./add_videos.md)
- [Create Draft](./create_draft.md)

---

<div align="right">

📚 **Project Resources**  
**GitHub**: [https://github.com/Hommy-master/capcut-mate](https://github.com/Hommy-master/capcut-mate)  
**Gitee**: [https://gitee.com/taohongmin-gitee/capcut-mate](https://gitee.com/taohongmin-gitee/capcut-mate)

</div>