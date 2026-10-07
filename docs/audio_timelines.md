# AUDIO_TIMELINES API Documentation

## 🌐 Language Switch
[中文版](./audio_timelines.zh.md) | [English](./audio_timelines.md)

## Interface Information

```
POST /openapi/capcut-mate/v1/audio_timelines
```

## Function Description

Calculate timelines based on audio file durations. This interface analyzes the duration information of input audio files and automatically calculates and generates appropriate timeline configurations for precise time arrangement of audio materials in video editing.

## Request Parameters

```json
{
  "links": [
    "https://assets.jcaigc.cn/audio1.mp3",
    "https://assets.jcaigc.cn/audio2.mp3"
  ]
}
```

### Parameter Description

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| links | array[string] |✅ | - | Audio file URL array |

### links Array Structure

Each links array element is a single audio file URL string:

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| links[] | string |✅ | - | Audio file URL address |

### Parameter Details

#### links[]
- **Type**: string
- **Description**: Complete URL address of the audio file; the duration is measured from the downloaded file and is not passed in the request
- **Example**: "https://assets.jcaigc.cn/background.mp3"

## Response Format

### Success Response (200)

```json
{
  "code": 0,
  "message": "success",
  "timelines": [
    {
      "start": 0,
      "end": 5000000
    },
    {
      "start": 5000000,
      "end": 8000000
    }
  ],
  "all_timelines": [
    {
      "start": 0,
      "end": 8000000
    }
  ]
}
```

### Response Field Description

| Field | Type | Description |
|-------|------|-------------|
| timelines | array | Segmented audio timeline array |
| all_timelines | array | Complete audio timeline array |
| start | number | Start time of time segment (microseconds) |
| end | number | End time of time segment (microseconds) |

### Error Response

```json
{
  "code": 2034,
  "message": "Get audio duration failed"
}
```

## Usage Examples

### cURL Examples

#### 1. Basic Audio Timeline Calculation

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/audio_timelines \
  -H "Content-Type: application/json" \
  -d '{
    "links": [
      "https://assets.jcaigc.cn/intro.mp3",
      "https://assets.jcaigc.cn/bgm.mp3"
    ]
  }'
```

#### 2. Multiple Audio Timeline Calculation

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/audio_timelines \
  -H "Content-Type: application/json" \
  -d '{
    "links": [
      "https://assets.jcaigc.cn/opening.mp3",
      "https://assets.jcaigc.cn/content.mp3",
      "https://assets.jcaigc.cn/ending.mp3"
    ]
  }'
```

## Error Code Description

| Error Code | Error Message | Description | Solution |
|------------|---------------|-------------|----------|
| 1001 | Parameter validation failed | `links` is missing or is not an array of strings | Provide a valid array of audio file URLs |
| 2004 | File size exceeds the limit | The downloaded audio exceeds the download size limit | Use a smaller audio file |
| 2005 | Download file failed | The audio file could not be downloaded | Check that the audio URL is publicly accessible |
| 2034 | Get audio duration failed | The duration of a downloaded audio file could not be read | Use a valid, playable audio file |

## Notes

1. **Time Unit**: All time parameters use microseconds (1 second = 1,000,000 microseconds)
2. **Parameter Requirements**: links array is required, and each element is an audio file URL string
3. **Duration Source**: each audio duration is measured from the downloaded file (microseconds), it is not passed in the request
4. **Network Access**: Audio URLs must be accessible, because the files are downloaded to measure their durations
5. **Continuity**: Timelines are arranged continuously in audio order without gaps
6. **Total Duration**: The end value of complete timeline equals the sum of all audio durations

## Workflow

1. Validate required parameter (links)
2. Download each audio file and obtain its duration
3. Fail with code 2034 when a duration cannot be obtained
4. Calculate time segments for each audio in order
5. Generate segmented audio timeline array
6. Generate complete audio timeline array
7. Return timeline configuration result

## Related Interfaces

- [Create Draft](./create_draft.md)
- [Timelines](./timelines.md)
- [Audio Infos](./audio_infos.md)
- [Generate Video](./gen_video.md)

---

<div align="right">

📚 **Project Resources**  
**GitHub**: [https://github.com/Hommy-master/capcut-mate](https://github.com/Hommy-master/capcut-mate)  
**Gitee**: [https://gitee.com/taohongmin-gitee/capcut-mate](https://gitee.com/taohongmin-gitee/capcut-mate)

</div>

### Language Switch
[中文版](./audio_timelines.zh.md) | [English](./audio_timelines.md)