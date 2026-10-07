# TIMELINES API Documentation

## 🌐 Language Switch
[中文版](./timelines.zh.md) | [English](./timelines.md)

## Interface Information

```
POST /openapi/capcut-mate/v1/timelines
```

## Function Description

Create timelines based on specified duration and quantity. This interface is used to generate timeline configurations needed for video editing, supporting multiple timeline types and start time settings, providing time reference for subsequent material addition and editing.

## Request Parameters

```json
{
  "duration": 10000000,
  "num": 3,
  "start": 0,
  "type": 0
}
```

### Parameter Description

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| duration | integer |✅ | - | Total duration (microseconds) |
| num | integer |✅ | - | Number of time segments |
| start | integer |✅ | - | Start time (microseconds) |
| type | integer |✅ | - | 0: equal split, 1: random split |

### Parameter Details

#### duration
- **Type**: integer
- **Description**: Total duration in microseconds (1 second = 1,000,000 microseconds)
- **Example**: 10000000 (10 seconds)

#### num
- **Type**: integer
- **Description**: Number of time segments to create
- **Example**: 3 (Create 3 time segments)

#### start
- **Type**: integer
- **Description**: Start time of the timeline in microseconds
- **Example**: 2000000 (Start from 2 seconds)

#### type
- **Type**: integer
- **Description**: Timeline segmentation type
- **Options**: 
  - 0 - Equal division timeline
  - 1 - Random timeline
- **Example**: 0

## Response Format

### Success Response (200)

```json
{
  "code": 0,
  "message": "success",
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

### Error Response

```json
{
  "code": 1001,
  "message": "Parameter validation failed"
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
    "type": 0
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
    "type": 0
  }'
```

## Error Code Description

| Error Code | Error Message | Description | Solution |
|------------|---------------|-------------|----------|
| 1001 | Parameter validation failed | Request body failed schema validation (`duration`/`num`/`start`/`type` missing or not integers) | Check parameter types and required fields |

## Notes

1. **Time Unit**: All time parameters use microseconds (1 second = 1,000,000 microseconds)
2. **Parameter Requirements**: duration, num, start and type are required parameters
3. **Time Range**: `all_timelines` spans `start` to `start + duration`, and the segmented timelines are generated inside that range
4. **Type Selection**: Choose appropriate timeline type based on actual needs
5. **Precision Consideration**: Microsecond-level time precision is suitable for precise video editing

## Workflow

1. Validate required parameters (duration, num, start, type)
2. Check parameter types (integers)
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