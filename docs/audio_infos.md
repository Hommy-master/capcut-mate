# AUDIO_INFOS API Documentation

## 🌐 Language Switch
[中文版](./audio_infos.zh.md) | [English](./audio_infos.md)

## Interface Information

```
POST /openapi/capcut-mate/v1/audio_infos
```

## Function Description

Generate audio information based on audio URLs and timelines. This interface converts audio file URLs and timeline configurations into the audio information format required by Jianying drafts, supporting volume control and audio effect settings.

## More Documentation

📖 For more detailed documentation and tutorials, please visit: [https://docs.jcaigc.cn](https://docs.jcaigc.cn)

## Request Parameters

```json
{
  "mp3_urls": ["https://assets.jcaigc.cn/audio1.mp3", "https://assets.jcaigc.cn/audio2.mp3"],
  "timelines": [
    {"start": 0, "end": 3000000},
    {"start": 3000000, "end": 8000000}
  ],
  "audio_effect": "reverb",
  "volume": 0.8
}
```

### Parameter Description

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| mp3_urls | array[string] |✅ | - | Audio file URL array |
| timelines | array[object] |✅ | - | Timeline configuration array |
| audio_effect | string |❌ | None | Audio effect name |
| volume | number |❌ | 1.0 | Volume level (0.0-2.0) |

### Parameter Details

#### mp3_urls
- **Type**: array[string]
- **Description**: Array of audio file URL addresses
- **Example**: ["https://assets.jcaigc.cn/bgm.mp3", "https://assets.jcaigc.cn/sfx.mp3"]

#### timelines
- **Type**: array[object]
- **Description**: Timeline configuration array, each element contains start and end fields
- **Example**: [{"start": 0, "end": 5000000}, {"start": 5000000, "end": 10000000}]

#### audio_effect
- **Type**: string
- **Description**: Audio effect name
- **Default**: None
- **Example**: "reverb", "echo", "bass_boost"

#### volume
- **Type**: number
- **Description**: Audio volume level
- **Default**: 1.0
- **Range**: 0.0 - 2.0
- **Example**: 0.8 (80% volume)

## Response Format

### Success Response (200)

```json
{
  "infos": "[{\"audio_url\":\"https://assets.jcaigc.cn/audio1.mp3\",\"start\":0,\"end\":3000000,\"duration\":5000000,\"volume\":0.8,\"audio_effect\":\"reverb\"},{\"audio_url\":\"https://assets.jcaigc.cn/audio2.mp3\",\"start\":3000000,\"end\":8000000,\"duration\":8000000,\"volume\":1.0,\"audio_effect\":null}]"
}
```

### Response Field Description

| Field | Type | Description |
|-------|------|-------------|
| infos | string | Audio information JSON string |

### Error Response (4xx/5xx)

```json
{
  "detail": "Error message description"
}
```

## Usage Examples

### cURL Examples

#### 1. Basic Audio Information Generation

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/audio_infos \
  -H "Content-Type: application/json" \
  -d '{
    "mp3_urls": ["https://assets.jcaigc.cn/bgm.mp3"],
    "timelines": [{"start": 0, "end": 10000000}],
    "volume": 0.7
  }'
```

#### 2. Audio Information with Effects

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/audio_infos \
  -H "Content-Type: application/json" \
  -d '{
    "mp3_urls": ["https://assets.jcaigc.cn/intro.mp3", "https://assets.jcaigc.cn/content.mp3"],
    "timelines": [{"start": 0, "end": 2000000}, {"start": 2000000, "end": 12000000}],
    "audio_effect": "reverb",
    "volume": 0.9
  }'
```

## Error Code Description

| Error Code | Error Message | Description | Solution |
|------------|---------------|-------------|----------|
| 400 | mp3_urls is required | Missing audio URL parameter | Provide valid audio URL array |
| 400 | timelines is required | Missing timeline parameter | Provide valid timeline array |
| 400 | Array length mismatch | mp3_urls and timelines array lengths don't match | Ensure both arrays have the same length |
| 400 | Invalid volume value | Volume not in range 0.0-2.0 | Use volume value between 0.0-2.0 |
| 404 | Audio resource not found | Audio URL inaccessible | Check if audio URL is accessible |
| 500 | Audio information generation failed | Internal processing error | Contact technical support |

## Notes

1. **Array Matching**: mp3_urls and timelines array lengths must be the same
2. **Time Unit**: All time parameters use microseconds (1 second = 1,000,000 microseconds)
3. **Volume Range**: volume value must be between 0.0-2.0
4. **Effect Support**: audio_effect needs to be a supported audio effect name
5. **JSON Format**: Returned infos is a JSON string that needs to be parsed before use
6. **Network Access**: Audio URLs must be accessible

## Workflow

1. Validate required parameters (mp3_urls, timelines)
2. Check array length matching
3. Validate timeline parameter validity
4. Validate volume parameter range
5. Generate corresponding audio information for each audio URL
6. Apply volume and audio effect settings
7. Convert information to JSON string format
8. Return processing result

## Related Interfaces

- [Create Draft](./create_draft.md)
- [Add Audios](./add_audios.md)
- [Audio Timelines](./audio_timelines.md)
- [Save Draft](./save_draft.md)

---

<div align="right">

📚 **Project Resources**  
**GitHub**: [https://github.com/Hommy-master/capcut-mate](https://github.com/Hommy-master/capcut-mate)  
**Gitee**: [https://gitee.com/taohongmin-gitee/capcut-mate](https://gitee.com/taohongmin-gitee/capcut-mate)

</div>

### Language Switch
[中文版](./audio_infos.zh.md) | [English](./audio_infos.md)