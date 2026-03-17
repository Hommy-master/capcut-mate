# ADD_FILTERS API Documentation

## 🌐 Language Switch
[中文版](./add_filters.zh.md) | [English](./add_filters.md)

## Interface Information

```
POST /openapi/capcut-mate/v1/add_filters
```

## Function Description

Add video filters to existing drafts. This interface is used to add filter materials to Jianying drafts within specified time periods, supporting various filter types such as vintage, black and white, cinematic, etc. Filters can be used to adjust the color tone and visual style of videos.

## More Documentation

📖 For more detailed documentation and tutorials, please visit: [https://docs.jcaigc.cn](https://docs.jcaigc.cn)

## Request Parameters

```json
{
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
  "filter_infos": "[{\"filter_title\": \"复古\", \"start\": 0, \"end\": 5000000, \"intensity\": 80}, {\"filter_title\": \"黑白\", \"start\": 2000000, \"end\": 7000000}]"
}
```

### Parameter Description

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| draft_url | string |✅ | - | Complete URL of the target draft |
| filter_infos | string |✅ | - | JSON string of filter information list |

### Parameter Details

#### filter_infos Array Structure

`filter_infos` is a JSON string containing an array of filter objects, each with the following fields:

```json
[
  {
    "filter_title": "复古",       // Filter name/title, required parameter
    "start": 0,                   // Filter start time (microseconds), required parameter
    "end": 5000000,               // Filter end time (microseconds), required parameter
    "intensity": 80               // Filter intensity (0-100), optional, default 100
  }
]
```

**Field Description**:
- `filter_title`: Filter name, must be an existing filter name in the system
- `start`: Filter start time in microseconds
- `end`: Filter end time in microseconds
- `intensity`: Filter intensity (0-100), controls the strength of the filter effect, default is 100

#### Time Parameters

- **start**: Start time of the filter on the timeline, unit microseconds (1 second = 1,000,000 microseconds)
- **end**: End time of the filter on the timeline, unit microseconds
- **Duration**: Filter duration = end - start

#### Intensity Parameter

- **intensity**: Controls the strength of the filter effect
  - Range: 0-100
  - Default: 100 (full intensity)
  - Lower values result in a more subtle filter effect
  - Example: `intensity: 50` applies the filter at 50% strength

## Response Format

### Success Response (200)

```json
{
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
  "track_id": "filter-track-uuid",
  "filter_ids": ["filter1-uuid", "filter2-uuid"],
  "segment_ids": ["segment1-uuid", "segment2-uuid"]
}
```

### Response Field Description

| Field | Type | Description |
|-------|------|-------------|
| draft_url | string | Updated draft URL |
| track_id | string | Filter track ID |
| filter_ids | array | List of added filter IDs |
| segment_ids | array | List of segment IDs |

### Error Response (4xx/5xx)

```json
{
  "detail": "Error message description"
}
```

## Usage Examples

### cURL Examples

#### 1. Basic Filter Addition

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_filters \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "filter_infos": "[{\"filter_title\":\"复古\",\"start\":0,\"end\":10000000}]"
  }'
```

#### 2. Filter with Custom Intensity

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_filters \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "filter_infos": "[{\"filter_title\":\"黑白\",\"start\":0,\"end\":5000000,\"intensity\":60}]"
  }'
```

#### 3. Multiple Filters

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_filters \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "filter_infos": "[{\"filter_title\":\"复古\",\"start\":0,\"end\":5000000,\"intensity\":80},{\"filter_title\":\"电影感\",\"start\":3000000,\"end\":8000000,\"intensity\":100}]"
  }'
```

## Error Code Description

| Error Code | Error Message | Description | Solution |
|------------|---------------|-------------|----------|
| 400 | draft_url is required | Missing draft URL parameter | Provide a valid draft URL |
| 400 | filter_infos is required | Missing filter information parameter | Provide valid filter information JSON |
| 400 | filter_infos format error | JSON format is incorrect | Check JSON string format |
| 400 | Filter configuration validation failed | Filter parameters do not meet requirements | Check parameters for each filter |
| 400 | filter_title is required | Filter title missing | Provide title for each filter |
| 400 | start is required | Filter start time missing | Provide start time for each filter |
| 400 | end is required | Filter end time missing | Provide end time for each filter |
| 400 | Time range invalid | end must be greater than start | Ensure end time is greater than start time |
| 400 | Intensity out of range | Intensity must be between 0-100 | Provide valid intensity value |
| 404 | Draft does not exist | Specified draft URL invalid | Check if draft URL is correct |
| 404 | Filter not found | Specified filter does not exist | Check if filter title is valid |
| 500 | Filter addition failed | Internal processing error | Contact technical support |

## Notes

1. **JSON Format**: filter_infos must be a valid JSON string
2. **Time Unit**: All time parameters use microseconds (1 second = 1,000,000 microseconds)
3. **Filter Names**: Filter titles must match exactly with system filter names
4. **Intensity Range**: Intensity must be between 0-100, default is 100
5. **Time Overlap**: Multiple filters can be applied to the same time period
6. **Filter Priority**: Filters are applied in the order they appear in the array
7. **Performance**: Complex filters may affect video processing performance

## Workflow

1. Validate required parameters (draft_url, filter_infos)
2. Parse filter_infos JSON string
3. Validate parameter configuration for each filter
4. Obtain and decrypt draft content
5. Create filter track
6. Add filter segments to track
7. Save and encrypt draft
8. Return processing result

## Related Interfaces

- [Create Draft](./create_draft.md)
- [Add Videos](./add_videos.md)
- [Add Images](./add_images.md)
- [Add Effects](./add_effects.md)
- [Save Draft](./save_draft.md)
- [Generate Video](./gen_video.md)

---

<div align="right">

📚 **Project Resources**  
**GitHub**: [https://github.com/Hommy-master/capcut-mate](https://github.com/Hommy-master/capcut-mate)  
**Gitee**: [https://gitee.com/taohongmin-gitee/capcut-mate](https://gitee.com/taohongmin-gitee/capcut-mate)

</div>
