# UPLOAD_FILE API Documentation

## 🌐 Language Switch
[中文版](./upload_file.zh.md) | [English](./upload_file.md)

## Interface Information

```
POST /openapi/capcut-mate/v1/upload_file
Content-Type: multipart/form-data
```

## Function Description

Upload a file to object storage (server-relayed). The client sends the file bytes to this service,
which relays them to object storage, charges by the actual file size (0.0005 CNY/MB) after a
successful upload, and returns a signed download URL.
Object storage credentials stay on the server and are never exposed to the client.

## More Documentation

📖 For more documentation and tutorials, please visit: [https://docs.jcaigc.cn](https://docs.jcaigc.cn)

## Request Parameters

Sent as `multipart/form-data`: the file goes in the `file` field, the key in the `apiKey` field.

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/upload_file \
  -F "file=@demo.mp4" \
  -F "apiKey=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
```

### Parameter Description

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| file | file | ✅ | - | File to upload, max 500MB |
| apiKey | string | Per server config | - | A valid UUID; required when `ENABLE_APIKEY=true`, get one at https://jcaigc.cn |

### Parameter Details

#### file

- **Type**: file (multipart/form-data)
- **Description**: Common audio/video/image formats are supported: mp4, mov, m4v, avi, mkv, flv, webm, wmv, mp3, wav, m4a, aac, flac, ogg, jpg, jpeg, png, gif, webp, bmp
- **Limits**: max 500MB per file; empty files are rejected

#### apiKey

- **Type**: string
- **Description**: Must be a valid UUID; required when the server enforces apiKey, and the account balance must be greater than 1

## Response Format

### Success Response (200)

```json
{
  "code": 0,
  "message": "success",
  "url": "https://bucket.oss-cn-hangzhou.aliyuncs.com/jianchuang/2026-10-06/8f3a1c2d5e6b7a90_demo.mp4?OSSAccessKeyId=xxx&Expires=xxx&Signature=xxx",
  "key": "jianchuang/2026-10-06/8f3a1c2d5e6b7a90_demo.mp4",
  "size": 10485760,
  "size_mb": 10.0,
  "cost": 0.005,
  "url_expire_days": 7
}
```

### Response Field Description

| Field | Type | Description |
|-------|------|-------------|
| url | string | Signed temporary download URL from object storage; pass it directly to add_videos / add_images / add_audios |
| key | string | Object storage object key |
| size | int | Actual file size in bytes |
| size_mb | float | File size in MB (3 decimal places) |
| cost | float | Cost of this upload in CNY; 0 when billing is disabled |
| url_expire_days | int | URL validity in days; comes from `VIDEO_GEN_RETENTION_DAYS` (7 by default) |

### Error Response

```json
{
  "code": 2050,
  "message": "Unsupported file type, please upload a supported format"
}
```

## Usage Examples

### cURL Example

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/upload_file \
  -F "file=@demo.mp4" \
  -F "apiKey=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
```

### Python Example

```python
import requests

with open("demo.mp4", "rb") as f:
    resp = requests.post(
        "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/upload_file",
        files={"file": ("demo.mp4", f, "video/mp4")},
        data={"apiKey": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"},
        timeout=600,
    )

result = resp.json()
video_url = result["url"]  # ready for add_videos / add_images / add_audios
print("size:", result["size_mb"], "MB", "cost:", result["cost"], "CNY")
```

## Error Codes

| Code | Message | Description | Solution |
|------|---------|-------------|----------|
| 1001 | Parameter validation failed | Missing file field, apiKey is not a valid UUID, or the file is empty | Check the request payload |
| 2004 | File size exceeds the limit | File is larger than 500MB | Compress or split the file and retry |
| 2035 | Insufficient account balance | The account balance must be greater than 1 | Top up and retry |
| 2036 | Invalid apiKey | `ENABLE_APIKEY=true` and apiKey is missing or invalid | Get an apiKey at https://jcaigc.cn |
| 2049 | Invalid file name | File name is empty or nothing usable remains after sanitization | Provide a valid file name |
| 2050 | Unsupported file type | Extension not in the built-in whitelist | Use a supported format |
| 9998 | Internal server error | No object storage configured, or the upload failed | Check the server storage configuration |

## Notes

1. **Server-relayed**: the file is uploaded to this service first and then relayed to object storage; storage credentials are never sent to the client
2. **Billing**: 0.0005 CNY/MB based on the actual file size (6 decimal places), charged only after a successful object storage upload
3. **Size limit**: max 500MB per file; behind nginx you must also raise `client_max_body_size` (the stock 1MB default returns 413)
4. **Expiry**: the returned `url` is a signed temporary address whose lifetime comes from `VIDEO_GEN_RETENTION_DAYS` (7 days by default)
5. **Ready to use**: `url` can be passed directly to add_videos / add_images / add_audios

## Workflow

1. Validate the apiKey (when `ENABLE_APIKEY=true`) and the account balance (must be greater than 1)
2. Sanitize the file name and check the extension whitelist
3. Stream the file to disk while counting bytes (reject when empty or over 500MB)
4. Upload the file to object storage (COS / OSS / TOS)
5. Charge by size after a successful upload
6. Return the signed download URL

## Related Interfaces

- [Create Draft](./create_draft.md)
- [Add Videos](./add_videos.md)

---

<div align="right">

📚 **Project Resources**  
**GitHub**: [https://github.com/Hommy-master/capcut-mate](https://github.com/Hommy-master/capcut-mate)  
**Gitee**: [https://gitee.com/taohongmin-gitee/capcut-mate](https://gitee.com/taohongmin-gitee/capcut-mate)

</div>
