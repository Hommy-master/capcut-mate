# AUDIO_TIMELINES API Documentation

## 🌐 Language Switch
[中文版](./audio_timelines.zh.md) | [English](./audio_timelines.md)

## Interface Information

```
POST /openapi/capcut-mate/v1/audio_timelines
```

## Function Description

Calculate timelines based on audio file durations. This interface analyzes the duration information of input audio files and automatically calculates and generates appropriate timeline configurations for precise time arrangement of audio materials in video editing.

## More Documentation

📖 For more detailed documentation and tutorials, please visit: [https://docs.jcaigc.cn](https://docs.jcaigc.cn)

## Request Parameters

```json
{
  "links": [
    {
      "url": "https://assets.jcaigc.cn/audio1.mp3",
      "duration": 5000000
    },
    {
      "url": "https://assets.jcaigc.cn/audio2.mp3",
      "duration": 3000000
    }
  ]
}
```

### Parameter Description

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| links | array[object] |✅ | - | Audio link information array |

### links Array Structure

Each links array element contains the following fields:

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| url | string |✅ | - | Audio file URL address |
| duration | number |✅ | - | Audio duration (microseconds) |

### Parameter Details

#### url
- **Type**: string
- **Description**: Complete URL address of the audio file
- **Example**: "https://assets.jcaigc.cn/background.mp3"

#### duration
- **Type**: number
- **Description**: Duration of the audio file in microseconds (1 second = 1,000,000 microseconds)
- **Example**: 5000000 (5 seconds)

## Response Format

### Success Response (200)

```json
{
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

### Error Response (4xx/5xx)

```json
{
  "detail": "Error message description"
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
      {
        "url": "https://assets.jcaigc.cn/intro.mp3",
        "duration": 3000000
      },
      {
        "url": "https://assets.jcaigc.cn/bgm.mp3",
        "duration": 15000000
      }
    ]
  }'
```

#### 2. Multiple Audio Timeline Calculation

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/audio_timelines \
  -H "Content-Type: application/json" \
  -d '{
    "links": [
      {
        "url": "https://assets.jcaigc.cn/opening.mp3",
        "duration": 2000000
      },
      {
        "url": "https://assets.jcaigc.cn/content.mp3",
        "duration": 10000000
      },
      {
        "url": "https://assets.jcaigc.cn/ending.mp3",
        "duration": 3000000
      }
    ]
  }'
```

## Error Code Description

| Error Code | Error Message | Description | Solution |
|------------|---------------|-------------|----------|
| 400 | links is required | Missing audio link parameter | Provide valid links array |
| 400 | links format error | Invalid JSON format | Check JSON array format |
| 400 | url is required | Missing audio URL | Provide URL for each audio |
| 400 | duration is required | Missing audio duration | Provide duration for each audio |
| 400 | duration must be greater than 0 | Invalid duration parameter | Use duration value greater than 0 |
| 404 | Audio resource not found | Audio URL inaccessible | Check if audio URL is accessible |
| 500 | Audio timeline calculation failed | Internal processing error | Contact technical support |

## Notes

1. **Time Unit**: All time parameters use microseconds (1 second = 1,000,000 microseconds)
2. **Parameter Requirements**: links array is required, and each element needs url and duration
3. **Duration Accuracy**: Ensure the provided duration parameter accurately reflects the actual audio duration
4. **Network Access**: Audio URLs must be accessible (for verification)
5. **Continuity**: Timelines are arranged continuously in audio order without gaps
6. **Total Duration**: The end value of complete timeline equals the sum of all audio durations

## Workflow

1. Validate required parameter (links)
2. Parse audio information from each element in links array
3. Validate url and duration parameters for each audio
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