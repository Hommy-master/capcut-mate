# SAVE_DRAFT API Documentation

### 🌐 Language Switch
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
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258"
}
```

### Response Field Description

| Field | Type | Description |
|-------|------|-------------|
| draft_url | string | Saved draft URL, usually the same as the URL in the request |

### Error Response (4xx/5xx)

```json
{
  "detail": "Error message description"
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
| 400 | draft_url is required | Missing draft URL parameter | Provide a valid draft_url |
| 400 | Invalid draft_url format | URL format is incorrect | Check if URL format is correct |
| 404 | Draft does not exist | Specified draft cannot be found | Confirm that draft URL is correct and exists |
| 500 | Save failed | Internal service error | Contact technical support or retry later |
| 503 | Service unavailable | System maintenance | Retry later |

## Notes

1. **URL Validity**: Ensure the passed draft_url is valid and exists
2. **Network Stability**: Save operation requires stable network connection
3. **Frequency Control**: Avoid overly frequent save operations
4. **Concurrency Safety**: Concurrent saves of the same draft may cause conflicts

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