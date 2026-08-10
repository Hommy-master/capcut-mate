# FILTER_INFOS API Documentation

## 🌐 Language Switch
[中文版](./filter_infos.zh.md) | [English](./filter_infos.md)

## Interface Information

```
POST /openapi/capcut-mate/v1/filter_infos
```

## Function Description

Generate filter information based on filter names, timelines, and intensities. This interface converts filter names and timeline configurations into the filter information format required by Jianying drafts.

## More Documentation

📖 For more detailed documentation and tutorials, please visit: [https://docs.jcaigc.cn](https://docs.jcaigc.cn)

## Request Parameters

```json
{
  "filters": ["复古", "黑白"],
  "timelines": [
    {"start": 0, "end": 3000000},
    {"start": 3000000, "end": 6000000}
  ],
  "intensities": [80, 100]
}
```

### Parameter Description

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| filters | array[string] |✅ | - | Filter name array |
| timelines | array[object] |✅ | - | Timeline configuration array |
| intensities | array[number] | ❌ | 100 | Filter intensity array (0-100), optional, defaults to 100 for all |

## Response Format

### Success Response (200)

```json
{
  "infos": "[{\"filter_title\":\"复古\",\"start\":0,\"end\":3000000,\"intensity\":80},{\"filter_title\":\"黑白\",\"start\":3000000,\"end\":6000000,\"intensity\":100}]"
}
```

### Response Field Description

| Field | Type | Description |
|-------|------|-------------|
| infos | string | Filter information JSON string |

### Error Response (4xx/5xx)

```json
{
  "detail": "Error message description"
}
```

## Usage Examples

### cURL Examples

#### 1. Basic Filter Information Generation

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/filter_infos \
  -H "Content-Type: application/json" \
  -d '{
    "filters": ["复古"],
    "timelines": [{"start": 0, "end": 5000000}]
  }'
```

#### 2. Filter Information with Custom Intensity

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/filter_infos \
  -H "Content-Type: application/json" \
  -d '{
    "filters": ["黑白"],
    "timelines": [{"start": 0, "end": 5000000}],
    "intensities": [60]
  }'
```

#### 3. Multiple Filter Information Generation

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/filter_infos \
  -H "Content-Type: application/json" \
  -d '{
    "filters": ["复古", "黑白", "电影感"],
    "timelines": [{"start": 0, "end": 2000000}, {"start": 2000000, "end": 4000000}, {"start": 4000000, "end": 6000000}],
    "intensities": [80, 100, 90]
  }'
```

## Error Code Description

| Error Code | Error Message | Description | Solution |
|------------|---------------|-------------|----------|
| 400 | filters is required | Missing filter name parameter | Provide valid filter name array |
| 400 | timelines is required | Missing timeline parameter | Provide valid timeline array |
| 400 | Array length mismatch | filters, timelines, and intensities array lengths don't match | Ensure all arrays have the same length |
| 400 | Intensity out of range | Intensity must be between 0-100 | Provide valid intensity values |
| 500 | Filter information generation failed | Internal processing error | Contact technical support |

## Notes

1. **Array Matching**: filters and timelines array lengths must be the same; intensities length should also match if provided
2. **Time Unit**: All time parameters use microseconds (1 second = 1,000,000 microseconds)
3. **Filter Names**: Need to use system-supported filter names
4. **Intensity Range**: Intensity values must be between 0-100, default is 100
5. **Continuity**: Filters are applied in timeline order

## Workflow

1. Validate required parameters (filters, timelines)
2. Check array length matching
3. Validate timeline parameter validity
4. Validate intensity range (if provided)
5. Generate corresponding filter information for each filter name
6. Convert information to JSON string format
7. Return processing result

## Related Interfaces

- [Create Draft](./create_draft.md)
- [Add Filters](./add_filters.md)
- [Timelines](./timelines.md)
- [Save Draft](./save_draft.md)

---

<div align="right">

📚 **Project Resources**  
**GitHub**: [https://github.com/Hommy-master/capcut-mate](https://github.com/Hommy-master/capcut-mate)  
**Gitee**: [https://gitee.com/taohongmin-gitee/capcut-mate](https://gitee.com/taohongmin-gitee/capcut-mate)

</div>

### Language Switch
[中文版](./filter_infos.zh.md) | [English](./filter_infos.md)
