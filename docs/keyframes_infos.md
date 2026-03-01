# KEYFRAMES_INFOS API Documentation

## 🌐 Language Switch
[中文版](./keyframes_infos.zh.md) | [English](./keyframes_infos.md)

## Interface Information

```
POST /openapi/capcut-mate/v1/keyframes_infos
```

## Function Description

Generate keyframe information based on keyframe type, position ratios, and values. This interface converts keyframe configurations into the keyframe information format required by Jianying drafts.

## More Documentation

📖 For more detailed documentation and tutorials, please visit: [https://docs.jcaigc.cn](https://docs.jcaigc.cn)

## Request Parameters

```json
{
  "ctype": "position",
  "offsets": [0.0, 0.5, 1.0],
  "values": [0.0, 0.5, 1.0],
  "segment_infos": [
    {"id": "segment1", "start": 0, "end": 5000000}
  ],
  "height": 1080,
  "width": 1920
}
```

### Parameter Description

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| ctype | string |✅ | - | Keyframe type |
| offsets | array[number] |✅ | - | Position ratio array |
| values | array[number] |✅ | - | Value array |
| segment_infos | array[object] |✅ | - | Segment information array |
| height | number |❌ | 1080 | Height |
| width | number |❌ | 1920 | Width |

## Response Format

### Success Response (200)

```json
{
  "keyframes_infos": "[{\"ctype\":\"position\",\"offset\":0.0,\"value\":0.0,\"segment_id\":\"segment1\",\"height\":1080,\"width\":1920},{\"ctype\":\"position\",\"offset\":0.5,\"value\":0.5,\"segment_id\":\"segment1\",\"height\":1080,\"width\":1920},{\"ctype\":\"position\",\"offset\":1.0,\"value\":1.0,\"segment_id\":\"segment1\",\"height\":1080,\"width\":1920}]"
}
```

### Response Field Description

| Field | Type | Description |
|-------|------|-------------|
| keyframes_infos | string | Keyframe information JSON string |

### Error Response (4xx/5xx)

```json
{
  "detail": "Error message description"
}
```

## Usage Examples

### cURL Examples

#### 1. Basic Keyframe Information Generation

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/keyframes_infos \
  -H "Content-Type: application/json" \
  -d '{
    "ctype": "scale",
    "offsets": [0.0, 1.0],
    "values": [0.5, 1.5],
    "segment_infos": [{"id": "segment1", "start": 0, "end": 5000000}]
  }'
```

#### 2. Position Keyframe Information

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/keyframes_infos \
  -H "Content-Type: application/json" \
  -d '{
    "ctype": "position",
    "offsets": [0.0, 0.3, 0.7, 1.0],
    "values": [0.0, 0.2, 0.8, 1.0],
    "segment_infos": [{"id": "segment1", "start": 0, "end": 10000000}],
    "height": 1080,
    "width": 1920
  }'
```

## Error Code Description

| Error Code | Error Message | Description | Solution |
|------------|---------------|-------------|----------|
| 400 | ctype is required | Missing keyframe type parameter | Provide valid keyframe type |
| 400 | offsets is required | Missing position ratio parameter | Provide valid position ratio array |
| 400 | values is required | Missing value parameter | Provide valid value array |
| 400 | segment_infos is required | Missing segment information parameter | Provide valid segment information array |
| 400 | Array length mismatch | offsets and values array lengths don't match | Ensure both arrays have the same length |
| 500 | Keyframe information generation failed | Internal processing error | Contact technical support |

## Notes

1. **Array Matching**: offsets and values array lengths must be the same
2. **Time Unit**: All time parameters use microseconds (1 second = 1,000,000 microseconds)
3. **Keyframe Types**: Support position, scale, rotation, etc.
4. **Position Ratios**: offsets values should be in range 0.0-1.0
5. **Resolution Settings**: height and width parameters are used to set coordinate system

## Workflow

1. Validate required parameters (ctype, offsets, values, segment_infos)
2. Check array length matching
3. Validate parameter validity
4. Generate corresponding keyframe information for each offset
5. Apply resolution parameters
6. Convert information to JSON string format
7. Return processing result

## Related Interfaces

- [Create Draft](./create_draft.md)
- [Add Keyframes](./add_keyframes.md)
- [Save Draft](./save_draft.md)

---

<div align="right">

📚 **Project Resources**  
**GitHub**: [https://github.com/Hommy-master/capcut-mate](https://github.com/Hommy-master/capcut-mate)  
**Gitee**: [https://gitee.com/taohongmin-gitee/capcut-mate](https://gitee.com/taohongmin-gitee/capcut-mate)

</div>

### Language Switch
[中文版](./keyframes_infos.zh.md) | [English](./keyframes_infos.md)