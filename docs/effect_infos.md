# EFFECT_INFOS API Documentation

## 🌐 Language Switch
[中文版](./effect_infos.zh.md) | [English](./effect_infos.md)

## Interface Information

```
POST /openapi/capcut-mate/v1/effect_infos
```

## Function Description

Generate effect information based on effect names and timelines. This interface converts effect names and timeline configurations into the effect information format required by Jianying drafts.

## More Documentation

📖 For more detailed documentation and tutorials, please visit: [https://docs.jcaigc.cn](https://docs.jcaigc.cn)

## Request Parameters

```json
{
  "effects": ["blur", "vignette"],
  "timelines": [
    {"start": 0, "end": 3000000},
    {"start": 3000000, "end": 6000000}
  ]
}
```

### Parameter Description

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| effects | array[string] |✅ | - | Effect name array |
| timelines | array[object] |✅ | - | Timeline configuration array |

## Response Format

### Success Response (200)

```json
{
  "infos": "[{\"effect\":\"blur\",\"start\":0,\"end\":3000000,\"duration\":5000000},{\"effect\":\"vignette\",\"start\":3000000,\"end\":6000000,\"duration\":5000000}]"
}
```

### Response Field Description

| Field | Type | Description |
|-------|------|-------------|
| infos | string | Effect information JSON string |

### Error Response (4xx/5xx)

```json
{
  "detail": "Error message description"
}
```

## Usage Examples

### cURL Examples

#### 1. Basic Effect Information Generation

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/effect_infos \
  -H "Content-Type: application/json" \
  -d '{
    "effects": ["blur"],
    "timelines": [{"start": 0, "end": 5000000}]
  }'
```

#### 2. Multiple Effect Information Generation

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/effect_infos \
  -H "Content-Type: application/json" \
  -d '{
    "effects": ["blur", "vignette", "sepia"],
    "timelines": [{"start": 0, "end": 2000000}, {"start": 2000000, "end": 4000000}, {"start": 4000000, "end": 6000000}]
  }'
```

## Error Code Description

| Error Code | Error Message | Description | Solution |
|------------|---------------|-------------|----------|
| 400 | effects is required | Missing effect name parameter | Provide valid effect name array |
| 400 | timelines is required | Missing timeline parameter | Provide valid timeline array |
| 400 | Array length mismatch | effects and timelines array lengths don't match | Ensure both arrays have the same length |
| 500 | Effect information generation failed | Internal processing error | Contact technical support |

## Notes

1. **Array Matching**: effects and timelines array lengths must be the same
2. **Time Unit**: All time parameters use microseconds (1 second = 1,000,000 microseconds)
3. **Effect Names**: Need to use system-supported effect names
4. **Continuity**: Effects are applied in timeline order

## Workflow

1. Validate required parameters (effects, timelines)
2. Check array length matching
3. Validate timeline parameter validity
4. Generate corresponding effect information for each effect name
5. Convert information to JSON string format
6. Return processing result

## Related Interfaces

- [Create Draft](./create_draft.md)
- [Add Effects](./add_effects.md)
- [Timelines](./timelines.md)
- [Save Draft](./save_draft.md)

---

<div align="right">

📚 **Project Resources**  
**GitHub**: [https://github.com/Hommy-master/capcut-mate](https://github.com/Hommy-master/capcut-mate)  
**Gitee**: [https://gitee.com/taohongmin-gitee/capcut-mate](https://gitee.com/taohongmin-gitee/capcut-mate)

</div>

### Language Switch
[中文版](./effect_infos.zh.md) | [English](./effect_infos.md)