# SAVE_DRAFT API Documentation

## 🌐 Language Switch
[中文版](./save_draft.zh.md) | [English](./save_draft.md)

## Interface Information

```
POST /openapi/capcut-mate/v1/save_draft
```

## Function Description

Save Jianying draft. This interface is used to save the current draft state, ensuring that edited content is persistently stored. Usually called after completing a series of editing operations to prevent loss of edited content.

## More Documentation

📖 For more detailed documentation and tutorials, please visit: [https://docs.jcaigc.cn](https://docs.jcaigc.cn)

## Request Parameters

```json
{
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258"
}
```

### Parameter Description

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| draft_url | string | ✅ | - | Draft URL to be saved |

### Parameter Details

#### draft_url

- **Type**: String
- **Required**: Yes
- **Format**: Complete draft URL, usually returned by create_draft interface
- **Example**: `https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258`

## Response Format

### Success Response (200)

```json
{
  "code": 0,
  "message": "success",
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258"
}
```

### Response Field Description

| Field | Type | Description |
|-------|------|-------------|
| draft_url | string | Saved draft URL, usually the same as the URL in the request |

### Error Response

```json
{
  "code": 2001,
  "message": "Invalid draft URL"
}
```

## Usage Examples

### cURL Examples

#### 1. Basic Save Draft

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/save_draft \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258"
  }'
```

## Error Code Description

| Error Code | Error Message | Description | Solution |
|------------|---------------|-------------|----------|
| 1001 | Parameter validation failed | `draft_url` is not a string | Check parameter types |
| 2001 | Invalid draft URL | `draft_url` has no `draft_id`, or the draft is not in the cache | Pass the `draft_url` returned by `create_draft` |
| 2042 | Draft lock acquisition timeout | The draft is locked by another operation and the 30-second wait timed out | Retry later |

## Notes

1. **URL Validity**: Ensure the passed draft_url is valid and exists
2. **Network Stability**: Save operation requires stable network connection
3. **Frequency Control**: Avoid overly frequent save operations
4. **Concurrency Safety**: Concurrent operations on the same draft are serialized by a draft lock; a request that cannot acquire the lock within 30 seconds returns error code `2042`

## Workflow

1. Validate draft_url parameter
2. Check if draft exists
3. Get current draft state
4. Persistently save draft data
5. Return save result

## Related Interfaces

- [Create Draft](./create_draft.md)
- [Add Videos](./add_videos.md)
- [Add Audios](./add_audios.md)
- [Add Images](./add_images.md)
- [Generate Video](./gen_video.md)

---

<div align="right">

📚 **Project Resources**  
**GitHub**: [https://github.com/Hommy-master/capcut-mate](https://github.com/Hommy-master/capcut-mate)  
**Gitee**: [https://gitee.com/taohongmin-gitee/capcut-mate](https://gitee.com/taohongmin-gitee/capcut-mate)

</div>

### Language Switch
[中文版](./save_draft.zh.md) | [English](./save_draft.md)