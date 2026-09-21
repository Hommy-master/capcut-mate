# ADD_KEYFRAMES API Documentation

## 🌐 Language Switch
[中文版](./add_keyframes.zh.md) | [English](./add_keyframes.md)

## Interface Information

```
POST /openapi/capcut-mate/v1/add_keyframes
```

## Function Description

Add keyframe animations to existing visual segments in a draft. Keyframes control how properties such as position, scale, rotation, opacity, color adjustments, and volume change over time on a target segment.

Mask keyframes are not handled by this API; use [Add Mask Keyframes](./add_mask_keyframes.md) instead.

## More Documentation

📖 For more detailed documentation and tutorials, please visit: [https://docs.jcaigc.cn](https://docs.jcaigc.cn)

## Request Parameters

```json
{
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
  "keyframes": "[{\"segment_id\":\"d62994b4-25fe-422a-a123-87ef05038558\",\"property\":\"KFTypePositionX\",\"offset\":5000000,\"value\":-0.1}]"
}
```

### Parameter Description

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| draft_url | string | ✅ | "" | Complete URL of the target draft |
| keyframes | string | ✅ | "" | JSON string of a keyframe object array |

### keyframes Array Structure

`keyframes` is a JSON string containing an array of keyframe objects. Each object has these fields:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| segment_id | string | ✅ | Target segment ID |
| property | string | ✅ | Animation property type (see table below) |
| offset | number | ✅ | Time offset from the segment start, in microseconds (non-negative) |
| value | number | ✅ | Property value at that time |

#### offset

- Absolute time in microseconds from the segment start (for example, `5000000` = 5 seconds).
- Converted internally to a relative position within the segment, then written as a microsecond offset.
- Values beyond the segment duration are clamped to the segment end (`0`–`1` relative range).

#### Supported Properties

| Property | Description | Value notes |
|----------|-------------|-------------|
| KFTypePositionX | Horizontal position | Prefer normalized units (half canvas width). If `\|value\| > 1`, treated as pixels and divided by draft width |
| KFTypePositionY | Vertical position | Prefer normalized units (half canvas height). If `\|value\| > 1`, treated as pixels and divided by draft height |
| KFTypeScaleX | Horizontal scale | `1.0` = original; mutually exclusive with `UNIFORM_SCALE` |
| KFTypeScaleY | Vertical scale | `1.0` = original; mutually exclusive with `UNIFORM_SCALE` |
| KFTypeRotation | Rotation angle | Degrees, clockwise |
| KFTypeAlpha | Opacity | `0.0`–`1.0` (`1.0` = fully opaque); visual segments |
| UNIFORM_SCALE | Uniform scale | Scales X and Y together (`1.0` = original); mutually exclusive with `KFTypeScaleX` / `KFTypeScaleY` |
| KFTypeSaturation | Saturation | `-1.0`–`1.0` (`0.0` = original); video segments |
| KFTypeContrast | Contrast | `-1.0`–`1.0` (`0.0` = original); video segments |
| KFTypeBrightness | Brightness | `-1.0`–`1.0` (`0.0` = original); video segments |
| KFTypeVolume | Volume | `1.0` = original; video segments supported by this API |

Position coordinates: right is positive for X; up is positive for Y (Jianying display convention / draft width or height).

## Response Format

### Success Response (200)

```json
{
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
  "keyframes_added": 3,
  "affected_segments": ["d62994b4-25fe-422a-a123-87ef05038558"]
}
```

### Response Field Description

| Field | Type | Description |
|-------|------|-------------|
| draft_url | string | Draft URL |
| keyframes_added | integer | Number of keyframes successfully written |
| affected_segments | array | Segment IDs that received at least one keyframe |

Items that fail at apply time (unknown `segment_id`, non-visual segment, property mismatch, and so on) are skipped. The request can still return success with a partial `keyframes_added` count.

### Error Response

```json
{
  "detail": "Error message description"
}
```

## Usage Examples

### cURL Examples

#### 1. Uniform scale animation (microsecond offsets)

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_keyframes \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "keyframes": "[{\"segment_id\":\"segment-id\",\"property\":\"UNIFORM_SCALE\",\"offset\":0,\"value\":1},{\"segment_id\":\"segment-id\",\"property\":\"UNIFORM_SCALE\",\"offset\":5000000,\"value\":1.3}]"
  }'
```

#### 2. Multi-property keyframes

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_keyframes \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "keyframes": "[{\"segment_id\":\"segment-uuid\",\"property\":\"KFTypePositionX\",\"offset\":0,\"value\":0},{\"segment_id\":\"segment-uuid\",\"property\":\"KFTypePositionY\",\"offset\":0,\"value\":0},{\"segment_id\":\"segment-uuid\",\"property\":\"KFTypeRotation\",\"offset\":2500000,\"value\":90},{\"segment_id\":\"segment-uuid\",\"property\":\"KFTypeAlpha\",\"offset\":5000000,\"value\":0}]"
  }'
```

#### 3. Position with pixel values (auto-normalized when `|value| > 1`)

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_keyframes \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "keyframes": "[{\"segment_id\":\"segment-uuid\",\"property\":\"KFTypePositionX\",\"offset\":0,\"value\":0},{\"segment_id\":\"segment-uuid\",\"property\":\"KFTypePositionX\",\"offset\":1000000,\"value\":100}]"
  }'
```

## Error Codes

| Code | Message | Description | Solution |
|------|---------|-------------|----------|
| 2001 | Invalid draft URL | Draft missing or not in cache | Check `draft_url` |
| 2013 | Invalid keyframe information | JSON invalid, not a list, missing fields, unsupported `property`, or bad `offset`/`value` | Fix the `keyframes` JSON |
| 2014 | Keyframe addition failed | Draft save failed | Retry or contact support |
| 2042 | Draft lock acquisition timeout | Another write is holding the draft lock | Retry later |

## Notes

1. **JSON format**: `keyframes` must be a valid JSON string of an object array; an empty array is rejected (`2013`).
2. **Segment requirement**: Each item needs a valid `segment_id`. Only visual segments (video, image, sticker, text) are accepted; others are skipped.
3. **Time unit**: `offset` uses microseconds (`1` second = `1,000,000` microseconds).
4. **Position units**: Values with `|value| ≤ 1` are treated as already normalized; larger magnitudes are treated as pixels relative to the draft canvas size.
5. **Scale exclusivity**: Setting `KFTypeScaleX` or `KFTypeScaleY` unlocks uniform scale. Setting `UNIFORM_SCALE` after independent X/Y scale fails for that item and is skipped.
6. **Duplicate times**: Adding the same property at the same timestamp appends another keyframe (does not replace).
7. **Mask properties**: Use [Add Mask Keyframes](./add_mask_keyframes.md) for mask position/size/feather/rotation.
8. **Helper API**: [Keyframes Infos](./keyframes_infos.md) can generate a compatible `keyframes` JSON string.

## Workflow

1. Validate `draft_url` and load the draft from cache
2. Parse and validate the `keyframes` JSON string
3. For each item: find the segment, validate type and property, normalize the value, write the keyframe
4. Save the draft
5. Return `draft_url`, `keyframes_added`, and `affected_segments`

## Related Interfaces

- [Create Draft](./create_draft.md)
- [Add Videos](./add_videos.md)
- [Add Images](./add_images.md)
- [Keyframes Infos](./keyframes_infos.md)
- [Add Mask Keyframes](./add_mask_keyframes.md)
- [Save Draft](./save_draft.md)

---

<div align="right">

📚 **Project Resources**  
**GitHub**: [https://github.com/Hommy-master/capcut-mate](https://github.com/Hommy-master/capcut-mate)  
**Gitee**: [https://gitee.com/taohongmin-gitee/capcut-mate](https://gitee.com/taohongmin-gitee/capcut-mate)

</div>
