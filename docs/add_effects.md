# ADD_EFFECTS API Documentation

### 🌐 Language Switch
[中文版](./add_effects.zh.md) | [English](./add_effects.md)

## Interface Information

```
POST /openapi/capcut-mate/v1/add_effects
```

## Function Description

Add video effects to existing drafts. This interface is used to add effect materials to Jianying drafts within specified time periods, supporting multiple effect types such as border effects, filter effects, and dynamic effects. Effects can be used to enhance the visual impact of videos.

## More Documentation

📖 For more detailed documentation and tutorials, please visit: [https://docs.jcaigc.cn](https://docs.jcaigc.cn)

## Request Parameters

```json
{
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
  "effect_infos": "[{\"effect_title\": \"Recording Border III\", \"start\": 0, \"end\": 5000000}, {\"effect_title\": \"Vintage Filter\", \"start\": 2000000, \"end\": 7000000}]"
}
```

### Parameter Description

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| draft_url | string |✅ | - | Complete URL of the target draft |
| effect_infos | string |✅ | - | JSON string of effect information list |

### Parameter Details

#### effect_infos Array Structure

`effect_infos` is a JSON string containing an array of effect objects, each with the following fields:

```json
[
  {
    "effect_title": "Recording Border III",  // Effect name/title, required parameter
    "start": 0,                              // Effect start time (microseconds), required parameter
    "end": 5000000                           // Effect end time (microseconds), required parameter
  }
]
```

**Field Description**:
- `effect_title`: Effect name, must be an existing effect name in the system
- `start`: Effect start time in microseconds
- `end`: Effect end time in microseconds

#### Time Parameters

- **start**: Start time of the effect on the timeline, unit microseconds (1 second = 1,000,000 microseconds)
- **end**: End time of the effect on the timeline, unit microseconds
- **Duration**: Effect duration = end - start

## Response Format

### Success Response (200)

```json
{
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
  "track_id": "effect-track-uuid",
  "effect_ids": ["effect1-uuid", "effect2-uuid"],
  "segment_ids": ["segment1-uuid", "segment2-uuid"]
}
```

### Response Field Description

| Field | Type | Description |
|-------|------|-------------|
| draft_url | string | Updated draft URL |
| track_id | string | Effect track ID |
| effect_ids | array | List of added effect IDs |
| segment_ids | array | List of segment IDs |

### Error Response (4xx/5xx)

```json
{
  "detail": "Error message description"
}
```

## Usage Examples

### cURL Examples

#### 1. Basic Effect Addition

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_effects \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "effect_infos": "[{\"effect_title\":\"Vignette\",\"start\":0,\"end\":10000000}]"
  }'
```

#### 2. Multiple Effects

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_effects \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "effect_infos": "[{\"effect_title\":\"Border Effect\",\"start\":0,\"end\":5000000},{\"effect_title\":\"Color Filter\",\"start\":3000000,\"end\":8000000}]"
  }'
```

#### 3. Sequential Effects

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_effects \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "effect_infos": "[{\"effect_title\":\"Fade In\",\"start\":0,\"end\":1000000},{\"effect_title\":\"Main Effect\",\"start\":1000000,\"end\":9000000},{\"effect_title\":\"Fade Out\",\"start\":9000000,\"end\":10000000}]"
  }'
```

## Error Code Description

| Error Code | Error Message | Description | Solution |
|------------|---------------|-------------|----------|
| 400 | draft_url is required | Missing draft URL parameter | Provide a valid draft URL |
| 400 | effect_infos is required | Missing effect information parameter | Provide valid effect information JSON |
| 400 | effect_infos format error | JSON format is incorrect | Check JSON string format |
| 400 | Effect configuration validation failed | Effect parameters do not meet requirements | Check parameters for each effect |
| 400 | effect_title is required | Effect title missing | Provide title for each effect |
| 400 | start is required | Effect start time missing | Provide start time for each effect |
| 400 | end is required | Effect end time missing | Provide end time for each effect |
| 400 | Time range invalid | end must be greater than start | Ensure end time is greater than start time |
| 400 | Effect title not found | Specified effect does not exist | Check if effect title is valid |
| 404 | Draft does not exist | Specified draft URL invalid | Check if draft URL is correct |
| 500 | Effect processing failed | Internal processing error | Contact technical support |

## Notes

1. **JSON Format**: effect_infos must be a valid JSON string
2. **Time Unit**: All time parameters use microseconds (1 second = 1,000,000 microseconds)
3. **Effect Names**: Effect titles must match exactly with system effect names
4. **Time Overlap**: Multiple effects can be applied to the same time period
5. **Effect Priority**: Effects are applied in the order they appear in the array
6. **Performance**: Complex effects may affect video processing performance

## Workflow

1. Validate required parameters (draft_url, effect_infos)
2. Parse effect_infos JSON string
3. Validate parameter configuration for each effect
4. Obtain and decrypt draft content
5. Create effect track
6. Add effect segments to track
7. Apply effects to video segments
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