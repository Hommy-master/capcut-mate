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
  "name": "Circle Mask",
  "X": 0.5,
  "Y": 0.5,
  "width": 0.3,
  "height": 0.3,
  "feather": 0.1,
  "rotation": 0,
  "invert": false,
  "roundCorner": 0.2
}
```

### Parameter Description

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| draft_url | string |✅ | - | Complete URL of the target draft |
| segment_ids | array |✅ | - | List of segment IDs to apply masks |
| name | string |✅ | - | Mask name/type |
| X | number |✅ | - | Horizontal position (0.0-1.0) |
| Y | number |✅ | - | Vertical position (0.0-1.0) |
| width | number |✅ | - | Mask width (0.0-1.0) |
| height | number |✅ | - | Mask height (0.0-1.0) |
| feather | number |❌ | 0.0 | Feather edge softness |
| rotation | number | ❌ | 0 | Rotation angle (degrees) |
| invert | boolean | ❌ | false | Invert mask effect |
| roundCorner | number | ❌ | 0.0 | Rounded corner radius |

## Response Format

### Success Response (200)

```json
{
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

### Error Response (4xx/5xx)

```json
{
  "detail": "Error message description"
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
    "name": "Circle Mask",
    "X": 0.5,
    "Y": 0.5,
    "width": 0.4,
    "height": 0.4
  }'
```

#### 2. Rectangle Mask with Effects

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_masks \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "segment_ids": ["segment1-uuid", "segment2-uuid"],
    "name": "Rectangle Mask",
    "X": 0.3,
    "Y": 0.4,
    "width": 0.5,
    "height": 0.3,
    "feather": 0.1,
    "roundCorner": 0.1
  }'
```

#### 3. Inverted Mask

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_masks \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "segment_ids": ["segment1-uuid"],
    "name": "Heart Mask",
    "X": 0.5,
    "Y": 0.5,
    "width": 0.3,
    "height": 0.3,
    "invert": true
  }'
```

## Error Code Description

| Error Code | Error Message | Description | Solution |
|------------|---------------|-------------|----------|
| 400 | draft_url is required | Missing draft URL parameter | Provide a valid draft URL |
| 400 | segment_ids is required | Missing segment IDs | Provide valid segment ID list |
| 400 | name is required | Missing mask name | Provide mask name |
| 400 | Position values invalid | X/Y must be between 0.0-1.0 | Use valid position values |
| 400 | Size values invalid | width/height must be between 0.0-1.0 | Use valid size values |
| 404 | Draft does not exist | Specified draft URL invalid | Check if draft URL is correct |
| 404 | Segment not found | Specified segment ID does not exist | Check segment IDs |
| 500 | Mask processing failed | Internal processing error | Contact technical support |

## Notes

1. **Coordinate System**: Position values use normalized coordinates (0.0-1.0)
2. **Size Values**: Width and height are relative to screen size
3. **Mask Types**: Support various mask shapes (circle, rectangle, heart, etc.)
4. **Feather Effect**: Softens mask edges for natural transitions
5. **Rotation**: Rotation angle in degrees
6. **Invert**: When true, shows area outside the mask

## Workflow

1. Validate required parameters
2. Check segment existence
3. Create mask with specified parameters
4. Apply mask to segments
5. Save and encrypt draft
6. Return processing result

## Related Interfaces

- [Create Draft](./create_draft.md)
- [Add Videos](./add_videos.md)
- [Add Images](./add_images.md)
- [Save Draft](./save_draft.md)

---

<div align="right">

📚 **Project Resources**  
**GitHub**: [https://github.com/Hommy-master/capcut-mate](https://github.com/Hommy-master/capcut-mate)  
**Gitee**: [https://gitee.com/taohongmin-gitee/capcut-mate](https://gitee.com/taohongmin-gitee/capcut-mate)

</div>