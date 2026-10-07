# GET_DRAFT API Documentation

## 🌐 Language Switch
[中文版](./get_draft.zh.md) | [English](./get_draft.md)

## Interface Information

```
GET /openapi/capcut-mate/v1/get_draft
```

## Function Description

Get draft file list. This interface is used to get all file lists corresponding to the specified draft ID, allowing you to view material files, configuration files, etc. in the draft. Usually used for draft content preview, file management or status checking.

## More Documentation

📖 For more detailed documentation and tutorials, please visit: [https://docs.jcaigc.cn](https://docs.jcaigc.cn)

## Request Parameters

### Query Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| draft_id | string | ✅ | - | Draft ID, length 20-32 characters |

### Parameter Details

#### draft_id

- **Type**: String
- **Required**: Yes
- **Length**: 20-32 characters
- **Format**: Usually UUID format or similar unique identifier
- **Example**: `2025092811473036584258`
- **Acquisition Method**: Usually extracted from draft_url or returned by create_draft interface

## Response Format

### Success Response (200)

```json
{
  "code": 0,
  "message": "success",
  "files": [
    "https://capcut-mate.jcaigc.cn/output/draft/2025092811473036584258/draft_info.json",
    "https://capcut-mate.jcaigc.cn/output/draft/2025092811473036584258/draft_content.json",
    "https://capcut-mate.jcaigc.cn/output/draft/2025092811473036584258/draft_meta_info.json"
  ]
}
```

### Response Field Description

| Field | Type | Description |
|-------|------|-------------|
| files | array | Download URLs of the files in the draft |

### Error Response

```json
{
  "code": 2001,
  "message": "Invalid draft URL"
}
```

## Usage Examples

### cURL Examples

#### 1. Basic Get Draft File List

```bash
curl -X GET "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258" \
  -H "Content-Type: application/json"
```

#### 2. Using Complete draft_id

```bash
curl -X GET "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025100512300012345678" \
  -H "Content-Type: application/json"
```

## Error Code Description

| Error Code | Error Message | Description | Solution |
|------------|---------------|-------------|----------|
| 1001 | Parameter validation failed | `draft_id` is missing or its length is not between 20 and 32 characters | Pass a `draft_id` of 20-32 characters |
| 2001 | Invalid draft URL | The draft directory does not exist | Confirm that the `draft_id` is correct and the draft exists |

## Notes

1. **Parameter Format**: Ensure draft_id format is correct and length is between 20-32 characters
2. **ID Extraction**: Correctly extract draft_id from draft_url
3. **File Types**: Returned file list contains multiple types of files
4. **Permission Verification**: Ensure permission to access specified draft
5. **Timeliness**: File list may not be updated in real-time, with some delay
6. **File Status**: Files in the list may be in different processing states

## Workflow

1. Validate draft_id parameter
2. Check draft_id format and length
3. Find specified draft
4. Get all files associated with the draft
5. Return file list

## Related Interfaces

- [Create Draft](./create_draft.md)
- [Save Draft](./save_draft.md)
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
[中文版](./get_draft.zh.md) | [English](./get_draft.md)