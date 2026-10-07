# GEN_VIDEO API Documentation

## 🌐 Language Switch
[中文版](./gen_video.zh.md) | [English](./gen_video.md)

## Interface Information

```
POST /openapi/capcut-mate/v1/gen_video
```

## Function Description

Submit video generation task. This interface uses asynchronous processing mode, immediately returning task submission status, with video generation performed in the background. Supports task queuing to ensure system stability.

## More Documentation

📖 For more detailed documentation and tutorials, please visit: [https://docs.jcaigc.cn](https://docs.jcaigc.cn)

## Request Parameters

```json
{
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
  "apiKey": "123e4567-e89b-12d3-a456-426614174000"
}
```

### Parameter Description

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| draft_url | string | ✅ | - | Complete URL of the target draft |
| apiKey | string | Per server config | - | A valid UUID; required when `ENABLE_APIKEY=true`, get one at https://jcaigc.cn |

### Parameter Details

#### Draft URL Parameter

- **draft_url**: Complete URL address of the draft
  - Format: `https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id={draft_ID}`
  - Example: `"https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258"`
  - Acquisition Method: Obtained via [Create Draft](./create_draft.md) or [Save Draft](./save_draft.md) interfaces

## Response Format

### Success Response (200)

```json
{
  "code": 0,
  "message": "视频生成任务已提交，请使用draft_url查询进度"
}
```

### Response Field Description

| Field | Type | Description |
|-------|------|-------------|
| message | string | Response message |

### Error Response

```json
{
  "code": 2001,
  "message": "Invalid draft URL"
}
```

## Usage Examples

### cURL Examples

#### 1. Basic Video Generation

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/gen_video \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
    "apiKey": "123e4567-e89b-12d3-a456-426614174000"
  }'
```

## Error Code Description

| Error Code | Error Message | Description | Solution |
|------------|---------------|-------------|----------|
| 1001 | Parameter validation failed | `apiKey` is not a valid UUID, or a parameter has the wrong type | Check parameter types and required fields |
| 2001 | Invalid draft URL | `draft_url` is missing or does not contain a `draft_id` | Pass the `draft_url` returned by `create_draft` |
| 2035 | Insufficient account balance | The account has no more than 1 point | Recharge the account and retry |
| 2036 | Invalid apiKey | `ENABLE_APIKEY=true` and `apiKey` is missing | Log in at https://jcaigc.cn to get an apiKey |
| 9998 | Internal server error | Unexpected error while submitting the task | Retry later or contact technical support |

## Notes

1. **Processing Time**: Video generation is time-consuming, may take minutes to tens of minutes
2. **File Size**: Draft complexity and number of materials affect processing time
3. **Network Stability**: Ensure material URLs are stably accessible
4. **Timeout Settings**: Suggest setting longer timeout or using polling mechanism
5. **Concurrency Limit**: Avoid generating large numbers of videos simultaneously
6. **Storage Space**: Generated video files may be large, pay attention to storage space
7. **URL Validity**: Generated video_url may have time-based restrictions
8. **System Requirements**: Video generation feature only available on Windows systems

## Workflow

1. Validate draft_url parameter
2. Parse draft configuration file
3. Download all required material files
4. Arrange and process materials according to timeline
5. Apply visual effects and transitions
6. Mix audio tracks
7. Render final video
8. Encode and upload video file
9. Return video URL

## Related Interfaces

- [Create Draft](./create_draft.md)
- [Save Draft](./save_draft.md)
- [Add Videos](./add_videos.md)
- [Add Audios](./add_audios.md)
- [Add Images](./add_images.md)
- [Get Draft](./get_draft.md)
- [Query Video Generation Status](./gen_video_status.md)

---

<div align="right">

📚 **Project Resources**  
**GitHub**: [https://github.com/Hommy-master/capcut-mate](https://github.com/Hommy-master/capcut-mate)  
**Gitee**: [https://gitee.com/taohongmin-gitee/capcut-mate](https://gitee.com/taohongmin-gitee/capcut-mate)

</div>

### Language Switch
[中文版](./gen_video.zh.md) | [English](./gen_video.md)