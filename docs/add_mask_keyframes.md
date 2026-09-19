# ADD_MASK_KEYFRAMES API Documentation

## 🌐 Language Switch
[中文版](./add_mask_keyframes.zh.md) | [English](./add_mask_keyframes.md)

## Interface Information

```
POST /openapi/capcut-mate/v1/add_mask_keyframes
```

## Function Description

Add mask keyframes to video segments that already have a mask. Keyframes are written on the segment `common_keyframes` list and can animate position (X/Y), feather, and rotation. Units match `add_masks`: pixels for position, 0–100 for feather, degrees for rotation.

The segment must already have a mask from `add_masks`. This API does not create a mask and does not change the mask material's static `config`.

## More Documentation

📖 For more detailed documentation and tutorials, please visit: [https://docs.jcaigc.cn](https://docs.jcaigc.cn)

## Request Parameters

```json
{
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
  "keyframes": [
    {"segment_id": "d62994b4-25fe-422a-a123-87ef05038558", "offset": 0, "X": 0, "Y": 0, "feather": 0, "rotation": 0},
    {"segment_id": "d62994b4-25fe-422a-a123-87ef05038558", "offset": 5000000, "X": -360, "Y": -200, "feather": 100, "rotation": 180}
  ]
}
```

### Parameter Description

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| draft_url | string | ✅ | "" | Full URL of the target draft |
| keyframes | array | ✅ | [] | Mask keyframe list |

### keyframes

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| segment_id | string | ✅ | Target video segment ID |
| offset | integer | ✅ | Time offset from the segment start, in microseconds |
| X | number | ❌ | Mask center X in pixels, relative to material center, right is positive |
| Y | number | ❌ | Mask center Y in pixels, relative to material center, down is positive |
| feather | number | ❌ | Feather amount, 0–100 |
| rotation | number | ❌ | Rotation in degrees |

`X`, `Y`, `feather`, and `rotation` are optional, but each item must include at least one of them. `0` is a valid value. For position animation, send both `X` and `Y` at the same `offset`. Sending only `X` writes the X-axis keyframe only.

Writing the same property at the same timestamp on the same segment overwrites the previous value.

## Response

```json
{
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
  "keyframes_added": 8,
  "affected_segments": ["d62994b4-25fe-422a-a123-87ef05038558"]
}
```

| Field | Type | Description |
|-------|------|-------------|
| draft_url | string | Draft URL |
| keyframes_added | integer | Number of draft properties written (X and Y each count as 1) |
| affected_segments | array | Segment IDs that received keyframes |

## Examples

### Position keyframes

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_mask_keyframes \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "keyframes": [
      {"segment_id": "segment-id", "offset": 0, "X": 0, "Y": 0},
      {"segment_id": "segment-id", "offset": 5000000, "X": -360, "Y": -200}
    ]
  }'
```

### Feather and rotation

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_mask_keyframes \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "keyframes": [
      {"segment_id": "segment-id", "offset": 0, "feather": 0, "rotation": 0},
      {"segment_id": "segment-id", "offset": 5000000, "feather": 100, "rotation": 180}
    ]
  }'
```

## Error Codes

| Code | Message | Description | Solution |
|------|---------|-------------|----------|
| 2001 | Invalid draft URL | Draft missing or not in cache | Check `draft_url` |
| 2015 | Segment not found | `segment_id` does not exist | Confirm the segment ID |
| 2016 | Invalid segment type | Not a video segment | Call this API only on video/image segments |
| 2046 | Invalid mask keyframe information | Missing property, invalid feather, or bad format | Check `keyframes` |
| 2047 | No mask found on the segment | The segment has no mask yet | Call `add_masks` first |
| 2048 | Mask keyframe addition failed | Failed to save the draft | Retry or contact support |

## Notes

- Call [Add Masks](./add_masks.md) before adding mask keyframes.
- Position conversion uses the material size (pixels / half material dimension), not the canvas size.
- An `offset` beyond the segment duration is clamped to the end of the segment.
- Width, height, and round-corner keyframes are not supported.

## Related Interfaces

- [Add Masks](./add_masks.md)
- [Add Keyframes](./add_keyframes.md)
- [Save Draft](./save_draft.md)

---

<div align="right">

📚 **Project Resources**  
**GitHub**: [https://github.com/Hommy-master/capcut-mate](https://github.com/Hommy-master/capcut-mate)  
**Gitee**: [https://gitee.com/taohongmin-gitee/capcut-mate](https://gitee.com/taohongmin-gitee/capcut-mate)

</div>
