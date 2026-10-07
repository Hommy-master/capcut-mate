# ADD_MASKS API Documentation

## 🌐 Language Switch
[中文版](./add_masks.zh.md) | [English](./add_masks.md)

## Interface Information

```
POST /openapi/capcut-mate/v1/add_masks
```

## Function Description

Add mask effects to existing drafts. This interface is used to add various shape masks to control visible areas of the screen in Jianying drafts. Masks can be used to create interesting visual effects and focus attention on specific areas.

## More Documentation

📖 For more detailed documentation and tutorials, please visit: [https://docs.jcaigc.cn](https://docs.jcaigc.cn)

## Request Parameters

```json
{
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
  "segment_ids": ["segment1-uuid", "segment2-uuid"],
  "name": "圆形",
  "X": 100,
  "Y": 200,
  "width": 300,
  "height": 300,
  "feather": 20,
  "rotation": 0,
  "invert": false,
  "roundCorner": 0
}
```

### Parameter Description

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| draft_url | string |✅ | - | Complete URL of the target draft |
| segment_ids | array |✅ | - | List of segment IDs to apply masks |
| name | string |❌ | "线性" | Mask type name: `线性` / `镜面` / `圆形` / `矩形` / `爱心` / `星形` |
| X | integer |❌ | 0 | Mask center X in pixels, relative to the material center (positive = right) |
| Y | integer |❌ | 0 | Mask center Y in pixels, relative to the material center (positive = down) |
| width | integer |❌ | 512 | Mask width in pixels |
| height | integer |❌ | 512 | Mask height in pixels |
| feather | integer |❌ | 0 | Feather edge softness (0-100) |
| rotation | integer | ❌ | 0 | Rotation angle (degrees) |
| invert | boolean | ❌ | false | Invert mask effect |
| roundCorner | integer | ❌ | 0 | Rounded corner radius (0-100), rectangle mask only |

## Response Format

### Success Response (200)

```json
{
  "code": 0,
  "message": "success",
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
  "masks_added": 2,
  "affected_segments": ["segment1-uuid", "segment2-uuid"],
  "mask_ids": ["mask1-uuid", "mask2-uuid"]
}
```

### Response Field Description

| Field | Type | Description |
|-------|------|-------------|
| draft_url | string | Updated draft URL |
| masks_added | integer | Number of masks added |
| affected_segments | array | List of affected segment IDs |
| mask_ids | array | List of added mask IDs |

### Error Response

```json
{
  "code": 2023,
  "message": "Invalid mask information, please check if mask parameters are correct."
}
```

## Usage Examples

### cURL Examples

#### 1. Basic Circle Mask

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_masks \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "segment_ids": ["segment1-uuid"],
    "name": "圆形",
    "X": 0,
    "Y": 0,
    "width": 400,
    "height": 400
  }'
```

#### 2. Rectangle Mask with Effects

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_masks \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "segment_ids": ["segment1-uuid", "segment2-uuid"],
    "name": "矩形",
    "X": 100,
    "Y": 50,
    "width": 400,
    "height": 300,
    "feather": 10,
    "roundCorner": 10
  }'
```

#### 3. Inverted Mask

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_masks \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "segment_ids": ["segment1-uuid"],
    "name": "爱心",
    "X": 0,
    "Y": 0,
    "width": 300,
    "height": 300,
    "invert": true
  }'
```

## Error Code Description

| Error Code | Error Message | Description | Solution |
|------------|---------------|-------------|----------|
| 1001 | Parameter validation failed | Request body failed schema validation (e.g. a non-integer `X` / `width`) | Check parameter types and required fields |
| 2001 | Invalid draft URL | `draft_url` is missing, malformed, or the draft is not in the cache | Pass the `draft_url` returned by `create_draft` |
| 2015 | Segment not found | A `segment_id` does not exist in the draft | Check the segment IDs |
| 2016 | Invalid segment type | The segment is not a video segment, which cannot take a mask | Apply masks only to video segments |
| 2023 | Invalid mask information | `segment_ids` is empty | Provide at least one segment ID |
| 2024 | Mask addition failed | Failed while writing the mask into the draft | Check the draft state and retry |
| 2025 | Mask type not found | `name` is not one of the supported mask names | Use `线性` / `镜面` / `圆形` / `矩形` / `爱心` / `星形` |
| 2042 | Draft lock acquisition timeout | Only one operation is allowed on a draft at a time | Retry later |

## Notes

1. **Coordinate System**: `X` / `Y` are pixels, with the origin at the material center (positive X = right, positive Y = down)
2. **Size Values**: `width` / `height` are pixels (default 512), not normalized ratios
3. **Mask Types**: `name` must be the Chinese mask name — `线性` / `镜面` / `圆形` / `矩形` / `爱心` / `星形`; an unknown name returns error 2025
4. **Feather Effect**: Softens mask edges for natural transitions
5. **Rotation**: Rotation angle in degrees
6. **Invert**: When true, shows area outside the mask

## Workflow

1. Validate required parameters
2. Check segment existence
3. Create mask with specified parameters
4. Apply mask to segments
5. Save the draft
6. Return processing result

## Related Interfaces

- [Create Draft](./create_draft.md)
- [Add Videos](./add_videos.md)
- [Add Images](./add_images.md)
- [Add Mask Keyframes](./add_mask_keyframes.md)
- [Save Draft](./save_draft.md)

---

<div align="right">

📚 **Project Resources**  
**GitHub**: [https://github.com/Hommy-master/capcut-mate](https://github.com/Hommy-master/capcut-mate)  
**Gitee**: [https://gitee.com/taohongmin-gitee/capcut-mate](https://gitee.com/taohongmin-gitee/capcut-mate)

</div>