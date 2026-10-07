# KEYFRAMES_INFOS API Documentation

## 🌐 Language Switch
[中文版](./keyframes_infos.zh.md) | [English](./keyframes_infos.md)

## Interface Information

```
POST /openapi/capcut-mate/v1/keyframes_infos
```

## Function Description

Generate keyframe information based on keyframe type, position ratios, and values. This interface converts keyframe configurations into the keyframe information format required by Jianying drafts.

## Request Parameters

```json
{
  "ctype": "KFTypePositionX",
  "offsets": "0|50|100",
  "values": "0|960|1920",
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
| ctype | string |✅ | - | Keyframe type: `KFTypePositionX` (X-axis move, needs `width`), `KFTypePositionY` (Y-axis move, needs `height`), `KFTypeRotation` (0-360), `UNIFORM_SCALE` (0.01-5), `KFTypeAlpha` (0-1) |
| offsets | string |✅ | - | Position ratios separated by `\|`, e.g. `"0\|100"` (start and end) or `"0\|50\|100"` (start, middle, end) |
| values | string |✅ | - | Values for each offset separated by `\|`; the element count must match `offsets`, e.g. `"1\|2"` or `"1\|2\|1"` |
| segment_infos | array[object] |✅ | - | Track data array; each item has `id`, `start`, `end` (microseconds) |
| height | integer |❌ | None | Video height, used to normalize `KFTypePositionY` values |
| width | integer |❌ | None | Video width, used to normalize `KFTypePositionX` values |

## Response Format

### Success Response (200)

```json
{
  "code": 0,
  "message": "success",
  "keyframes_infos": "[{\"offset\":0,\"property\":\"KFTypePositionX\",\"segment_id\":\"segment1\",\"value\":0.0},{\"offset\":2500000,\"property\":\"KFTypePositionX\",\"segment_id\":\"segment1\",\"value\":0.5},{\"offset\":5000000,\"property\":\"KFTypePositionX\",\"segment_id\":\"segment1\",\"value\":1.0}]"
}
```

### Response Field Description

| Field | Type | Description |
|-------|------|-------------|
| keyframes_infos | string | Keyframe information JSON string |

### Error Response

```json
{
  "code": 1001,
  "message": "Parameter validation failed"
}
```

## Usage Examples

### cURL Examples

#### 1. Basic Keyframe Information Generation

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/keyframes_infos \
  -H "Content-Type: application/json" \
  -d '{
    "ctype": "UNIFORM_SCALE",
    "offsets": "0|100",
    "values": "0.5|1.5",
    "segment_infos": [{"id": "segment1", "start": 0, "end": 5000000}]
  }'
```

#### 2. Position Keyframe Information

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/keyframes_infos \
  -H "Content-Type: application/json" \
  -d '{
    "ctype": "KFTypePositionX",
    "offsets": "0|30|70|100",
    "values": "0|384|1536|1920",
    "segment_infos": [{"id": "segment1", "start": 0, "end": 10000000}],
    "height": 1080,
    "width": 1920
  }'
```

## Error Code Description

| Error Code | Error Message | Description | Solution |
|------------|---------------|-------------|----------|
| 1001 | Parameter validation failed | Request body failed schema validation (`ctype`/`offsets`/`values`/`segment_infos` missing, or `offsets`/`values` not strings) | Check parameter types and required fields |
| 9998 | Internal server error | The number of `\|`-separated elements in `offsets` and `values` differs | Make the element counts of `offsets` and `values` identical |

## Notes

1. **Element Matching**: offsets and values must contain the same number of `|`-separated elements
2. **Time Unit**: All time parameters use microseconds (1 second = 1,000,000 microseconds)
3. **Keyframe Types**: KFTypePositionX, KFTypePositionY, KFTypeRotation, UNIFORM_SCALE, KFTypeAlpha
4. **Position Ratios**: offsets values are percentages in range 0-100, and each keyframe offset is computed relative to the segment start
5. **Resolution Settings**: with `KFTypePositionX`/`KFTypePositionY`, the value is divided by `width`/`height` for normalization

## Workflow

1. Validate required parameters (ctype, offsets, values, segment_infos)
2. Check that offsets and values have the same number of elements
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