# TIMELINES API Documentation

### 🌐 Language Switch
[中文版](./timelines.zh.md) | [English](./timelines.md)

## Interface Information

```
POST /openapi/capcut-mate/v1/timelines
```

## Function Description

Create timelines based on specified duration and quantity. This interface is used to generate timeline configurations needed for video editing, supporting multiple timeline types and start time settings, providing time reference for subsequent material addition and editing.

## More Documentation

📖 For more detailed documentation and tutorials, please visit: [https://docs.jcaigc.cn](https://docs.jcaigc.cn)

## Request Parameters

```json
{
  "duration": 10000000,
  "num": 3,
  "start": 0,
  "type": "equal"
}
```

### Parameter Description

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| duration | number |✅ | - | Total duration (microseconds) |
| num | number |✅ | - | Number of time segments |
| start | number |❌ | 0 | Start time (microseconds) |
| type | string |❌ | "equal" | Timeline type |

### Parameter Details

#### duration
- **Type**: number
- **Description**: Total duration in microseconds (1 second = 1,000,000 microseconds)
- **Example**: 10000000 (10 seconds)

#### num
- **Type**: number
- **Description**: Number of time segments to create
- **Example**: 3 (Create 3 time segments)

#### start
- **Type**: number
- **Description**: Start time of the timeline in microseconds
- **Default**: 0
- **Example**: 2000000 (Start from 2 seconds)

#### type
- **Type**: string
- **Description**: Timeline segmentation type
- **Options**: 
  - "equal" - Equal division timeline
  - "custom" - Custom timeline
- **Default**: "equal"

## Response Format

### Success Response (200)

```json
{
  "timelines": [
    {
      "start": 0,
      "end": 3333333
    },
    {
      "start": 3333333,
      "end": 6666666
    },
    {
      "start": 6666666,
      "end": 10000000
    }
  ],
  "all_timelines": [
    {
      "start": 0,
      "end": 10000000
    }
  ]
}
```

### Response Field Description

| Field | Type | Description |
|-------|------|-------------|
| timelines | array | Array of segmented timelines |
| all_timelines | array | Array of complete timelines |
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

#### 1. Basic Timeline Creation

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/timelines \
  -H "Content-Type: application/json" \
  -d '{
    "duration": 15000000,
    "num": 5,
    "start": 0,
    "type": "equal"
  }'
```

#### 2. Timeline with Start Time

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/timelines \
  -H "Content-Type: application/json" \
  -d '{
    "duration": 20000000,
    "num": 4,
    "start": 5000000,
    "type": "equal"
  }'
```

## Error Code Description

| Error Code | Error Message | Description | Solution |
|------------|---------------|-------------|----------|
| 400 | duration is required | Missing total duration parameter | Provide valid duration parameter |
| 400 | num is required | Missing time segment count parameter | Provide valid num parameter |
| 400 | duration must be greater than 0 | Invalid duration parameter | Use duration value greater than 0 |
| 400 | num must be greater than 0 | Invalid count parameter | Use count value greater than 0 |
| 400 | Invalid timeline type | Unsupported type parameter | Use supported timeline type |
| 500 | Timeline calculation failed | Internal processing error | Contact technical support |

## Notes

1. **Time Unit**: All time parameters use microseconds (1 second = 1,000,000 microseconds)
2. **Parameter Requirements**: duration and num are required parameters
3. **Time Range**: Ensure start + (duration/num) * num <= total duration
4. **Type Selection**: Choose appropriate timeline type based on actual needs
5. **Precision Consideration**: Microsecond-level time precision is suitable for precise video editing

## Workflow

1. Validate required parameters (duration, num)
2. Check parameter validity (positive numbers, reasonable range)
3. Calculate timeline segmentation method based on type
4. Generate segmented timeline array
5. Generate complete timeline array
6. Return timeline configuration result

## Related Interfaces

- [Create Draft](./create_draft.md)
- [Audio Timelines](./audio_timelines.md)
- [Video Infos](./video_infos.md)
- [Images Infos](./imgs_infos.md)

---

<div align="right">

📚 **Project Resources**  
**GitHub**: [https://github.com/Hommy-master/capcut-mate](https://github.com/Hommy-master/capcut-mate)  
**Gitee**: [https://gitee.com/taohongmin-gitee/capcut-mate](https://gitee.com/taohongmin-gitee/capcut-mate)

</div>

### Language Switch
[中文版](./timelines.zh.md) | [English](./timelines.md)