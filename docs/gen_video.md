# GEN_VIDEO API Documentation

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
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258"
}
```

### Parameter Description

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| draft_url | string | ✅ | - | Complete URL of the target draft |

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
  "message": "Video generation task submitted, please use draft_url to check progress"
}
```

### Response Field Description

| Field | Type | Description |
|-------|------|-------------|
| message | string | Response message |

### Error Response (4xx/5xx)

```json
{
  "detail": "Error message description"
}
```

## Usage Examples

### cURL Examples

#### 1. Basic Video Generation

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/gen_video \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL"
  }'
```

## Error Code Description

| Error Code | Error Message | Description | Solution |
|------------|---------------|-------------|----------|
| 400 | draft_url is required | Missing draft URL parameter | Provide a valid draft_url |
| 400 | Invalid draft_url format | URL format is incorrect | Check if URL format is correct |
| 404 | Draft does not exist | Specified draft cannot be found | Confirm that draft URL is correct and exists |
| 400 | Draft content is empty | Draft contains no exportable content | Ensure draft contains video, audio or image materials |
| 400 | Material inaccessible | Material files in draft cannot be downloaded | Check if material URLs are valid |
| 500 | Video rendering failed | Error occurred during video processing | Check draft content or contact technical support |
| 500 | Audio processing failed | Error occurred during audio mixing | Check audio format or contact technical support |
| 500 | Encoding failed | Final video encoding failed | Contact technical support |
| 503 | Service busy | Rendering server overloaded | Retry later |
| 504 | Processing timeout | Video generation timed out | Simplify draft content or retry later |
| 500 | Video generation task submission failed | Internal processing error | Contact technical support |

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