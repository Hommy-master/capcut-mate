# GET_DRAFT API Documentation

### 🌐 Language Switch
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
- **Example**: `2f52a63b-8c6a-4417-8b01-1b2a569ccb6c`
- **Acquisition Method**: Usually extracted from draft_url or returned by create_draft interface

## Response Format

### Success Response (200)

```json
{
  "files": [
    "2f52a63b-8c6a-4417-8b01-1b2a569ccb6c.json",
    "video_123456789.mp4",
    "audio_987654321.mp3",
    "image_555666777.jpg",
    "thumbnail_888999000.png"
  ]
}
```

### Response Field Description

| Field | Type | Description |
|-------|------|-------------|
| files | array | List of files related to the draft |

### Error Response (4xx/5xx)

```json
{
  "detail": "Error message description"
}
```

## Usage Examples

### cURL Examples

#### 1. Basic Get Draft File List

```bash
curl -X GET "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2f52a63b-8c6a-4417-8b01-1b2a569ccb6c" \
  -H "Content-Type: application/json"
```

#### 2. Using Complete draft_id

```bash
curl -X GET "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=7e8f9a0b-1c2d-3e4f-5g6h-7i8j9k0l1m2n" \
  -H "Content-Type: application/json"
```

## Error Code Description

| Error Code | Error Message | Description | Solution |
|------------|---------------|-------------|----------|
| 400 | draft_id is required | Missing draft_id parameter | Provide a valid draft_id |
| 400 | Invalid draft_id length | draft_id length not within 20-32 characters range | Check if draft_id format is correct |
| 400 | Invalid draft_id format | draft_id format is incorrect | Ensure using correct draft ID format |
| 404 | Draft does not exist | Specified draft ID cannot be found | Confirm that draft ID is correct and exists |
| 500 | Failed to get file list | Internal service error | Contact technical support or retry later |
| 503 | Service unavailable | System maintenance | Retry later |

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