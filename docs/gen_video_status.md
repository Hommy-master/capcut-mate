# GEN_VIDEO_STATUS API Documentation

## Interface Information

```bash
POST /openapi/capcut-mate/v1/gen_video_status
```

## Function Description

Query the status and progress of video generation tasks. Used together with the [gen_video](./gen_video.md) interface to track the execution of video generation tasks in real-time, including task status, progress percentage, completion results, and other information.

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
| draft_url | string | ✅ | - | Draft URL, same as the URL used when submitting the task |

### Parameter Details

#### Draft URL Parameter

- **draft_url**: Complete URL of the draft, used to identify the video generation task to query status for
  - Format: Must be a valid URL format
  - Example: `"https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258"`
  - Acquisition Method: draft_url returned after submitting task via [gen_video](./gen_video.md) interface

## Response Format

### Success Response (200)

#### Task Waiting

```json
{
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
  "status": "pending",
  "progress": 0,
  "video_url": "",
  "error_message": "",
  "created_at": "2024-09-24T10:30:00.000Z",
  "started_at": null,
  "completed_at": null
}
```

#### Task Processing

```json
{
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258", 
  "status": "processing",
  "progress": 65,
  "video_url": "",
  "error_message": "",
  "created_at": "2024-09-24T10:30:00.000Z",
  "started_at": "2024-09-24T10:30:05.000Z",
  "completed_at": null
}
```

#### Task Completed

```json
{
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
  "status": "completed",
  "progress": 100,
  "video_url": "https://video-output.assets.jcaigc.cn/generated/video_abc123def456ghi789.mp4",
  "error_message": "",
  "created_at": "2024-09-24T10:30:00.000Z",
  "started_at": "2024-09-24T10:30:05.000Z",
  "completed_at": "2024-09-24T10:35:30.000Z"
}
```

#### Task Failed

```json
{
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
  "status": "failed",
  "progress": 0,
  "video_url": "",
  "error_message": "Export draft failed: Jianying export ended but target file was not generated, please check disk space or Jianying version",
  "created_at": "2024-09-24T10:30:00.000Z",
  "started_at": "2024-09-24T10:30:05.000Z",
  "completed_at": "2024-09-24T10:32:15.000Z"
}
```

### Response Field Description

| Field | Type | Description |
|-------|------|-------------|
| draft_url | string | Draft URL |
| status | string | Task status: pending/processing/completed/failed |
| progress | integer | Task progress (0-100) |
| video_url | string | Generated video URL (only has value in completed status) |
| error_message | string | Error message (only has value in failed status) |
| created_at | string | Task creation time (ISO format) |
| started_at | string|null | Task start time (ISO format) |
| completed_at | string|null | Task completion time (ISO format) |

### Error Response (4xx/5xx)

#### 404 Not Found - Task Does Not Exist

```json
{
  "detail": "Video generation task not found"
}
```

#### 500 Internal Server Error - Query Failed

```json
{
  "detail": "Video task status query failed"
}
```

## Usage Examples

### cURL Examples

#### 1. Query Task Status

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/gen_video_status \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL"
  }'
```

## Error Code Description

| Error Code | Error Message | Description | Solution |
|------------|---------------|-------------|----------|
| 400 | draft_url is required | Missing draft URL parameter | Provide a valid draft_url |
| 400 | Invalid draft URL | draft_url format is incorrect | Check if draft URL format is correct |
| 404 | Video generation task not found | Specified draft URL has no corresponding video generation task | Confirm if task has been submitted via gen_video interface |
| 500 | Video task status query failed | Internal processing error | Retry later or contact technical support |

## Notes

1. **Polling Interval**: Suggest querying task status every 5-10 seconds
2. **Timeout Settings**: Suggest setting total timeout time (e.g. 10 minutes)
3. **Status Handling**: Provide different user feedback based on different statuses
4. **Error Handling**: Properly handle task failure situations
5. **Progress Display**: Utilize progress field to display progress bar
6. **Task Uniqueness**: Same draft URL can only have one ongoing task

## Workflow

1. Validate required parameters (draft_url)
2. Query task status from task manager
3. Convert internal status to API response format
4. Return task status information

## Related Interfaces

- [gen_video](./gen_video.md) - Submit video generation task
- [create_draft](./create_draft.md) - Create new draft file
- [save_draft](./save_draft.md) - Save draft file

---

<div align="right">

📚 **Project Resources**  
**GitHub**: [https://github.com/Hommy-master/capcut-mate](https://github.com/Hommy-master/capcut-mate)  
**Gitee**: [https://gitee.com/taohongmin-gitee/capcut-mate](https://gitee.com/taohongmin-gitee/capcut-mate)

</div>

### Language Switch
[中文版](./gen_video_status.zh.md) | [English](./gen_video_status.md)