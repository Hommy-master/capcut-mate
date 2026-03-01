# ADD_KEYFRAMES API Documentation

###🌐 Language Switch
[中文版](./add_keyframes.zh.md) | [English](./add_keyframes.md)

## Interface Information

```
POST /openapi/capcut-mate/v1/add_keyframes
```

## Function Description

Add keyframe animations to existing drafts. This interface is used to create property animations for position, scale, rotation, and other properties in Jianying drafts. Keyframes allow precise control over how properties change over time.

## More Documentation

📖 For more detailed documentation and tutorials, please visit: [https://docs.jcaigc.cn](https://docs.jcaigc.cn)

## Request Parameters

```json
{
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
  "keyframes": "[{\"property\":\"position.x\",\"time\":0,\"value\":0},{\"property\":\"position.x\",\"time\":1000000,\"value\":100}]"
}
```

### Parameter Description

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| draft_url | string |✅ | - | Complete URL of the target draft |
| keyframes | string |✅ | - | JSON string of keyframe information |

### Parameter Details

#### keyframes Array Structure

`keyframes` is a JSON string containing an array of keyframe objects, each with the following fields:

```json
[
  {
    "property": "position.x",  // Property name, required
    "time": 0,                 // Keyframe time (microseconds), required
    "value": 0                 // Property value, required
  }
]
```

**Supported Properties**:
- `position.x` - Horizontal position
- `position.y` - Vertical position
- `scale.x` - Horizontal scale
- `scale.y` - Vertical scale
- `rotation.z` - Rotation angle
- `opacity` - Transparency

## Response Format

### Success Response (200)

```json
{
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
  "keyframes_added": 5,
  "affected_segments": ["segment1-uuid", "segment2-uuid"]
}
```

### Response Field Description

| Field | Type | Description |
|-------|------|-------------|
| draft_url | string | Updated draft URL |
| keyframes_added | integer | Number of keyframes added |
| affected_segments | array | List of affected segment IDs |

### Error Response (4xx/5xx)

```json
{
  "detail": "Error message description"
}
```

## Usage Examples

### cURL Examples

#### 1. Basic Position Animation

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_keyframes \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "keyframes": "[{\"property\":\"position.x\",\"time\":0,\"value\":0},{\"property\":\"position.x\",\"time\":1000000,\"value\":100}]"
  }'
```

#### 2. Scale Animation

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_keyframes \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "keyframes": "[{\"property\":\"scale.x\",\"time\":0,\"value\":1.0},{\"property\":\"scale.x\",\"time\":2000000,\"value\":1.5}]"
  }'
```

#### 3. Rotation Animation

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_keyframes \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "keyframes": "[{\"property\":\"rotation.z\",\"time\":0,\"value\":0},{\"property\":\"rotation.z\",\"time\":3000000,\"value\":360}]"
  }'
```

## Error Code Description

| Error Code | Error Message | Description | Solution |
|------------|---------------|-------------|----------|
| 400 | draft_url is required | Missing draft URL parameter | Provide a valid draft URL |
| 400 | keyframes is required | Missing keyframe information | Provide valid keyframe JSON |
| 400 | keyframes format error | JSON format is incorrect | Check JSON string format |
| 400 | Invalid property name | Unsupported property | Use supported property names |
| 400 | Time value invalid | Time must be non-negative | Use valid time values |
| 404 | Draft does not exist | Specified draft URL invalid | Check if draft URL is correct |
| 500 | Keyframe processing failed | Internal processing error | Contact technical support |

## Notes

1. **JSON Format**: keyframes must be a valid JSON string
2. **Time Unit**: Time values use microseconds (1 second = 1,000,000 microseconds)
3. **Property Names**: Must use exact property names as specified
4. **Value Ranges**: Different properties have different valid value ranges
5. **Interpolation**: Keyframes are automatically interpolated between key times

## Workflow

1. Validate required parameters (draft_url, keyframes)
2. Parse keyframes JSON string
3. Validate property names and values
4. Obtain and decrypt draft content
5. Apply keyframe animations to segments
6. Save and encrypt draft
7. Return processing result

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