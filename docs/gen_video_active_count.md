# GEN_VIDEO_ACTIVE_COUNT API Documentation

## 🌐 Language Switch
[中文版](./gen_video_active_count.zh.md) | [English](./gen_video_active_count.md)

## Interface Information

```
GET /openapi/capcut-mate/v1/gen_video_active_count
```

## Function Description

Return how many draft exports are currently queued or rendering, i.e. tasks in `pending` or `processing`. Completed and failed tasks are not counted. Useful for checking export load before calling `gen_video`.

## More Documentation

📖 For more detailed documentation and tutorials, please visit: [https://docs.jcaigc.cn](https://docs.jcaigc.cn)

## Request Parameters

This interface takes no parameters.

## Response Format

### Success Response (200)

```json
{
  "code": 0,
  "message": "success",
  "count": 3
}
```

### Response Field Description

| Field | Type | Description |
|-------|------|-------------|
| count | integer | Number of tasks in `pending` or `processing` |

### Error Response

```json
{
  "code": 9998,
  "message": "Internal server error"
}
```

## Usage Examples

### cURL Examples

#### 1. Query Active Export Count

```bash
curl -X GET https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/gen_video_active_count
```

## Error Code Description

| Error Code | Error Message | Description | Solution |
|------------|---------------|-------------|----------|
| 9998 | Internal server error | Unexpected error while counting tasks | Retry later or contact technical support |

## Notes

1. **No Parameters**: the interface takes no request body and no query string
2. **Counted States**: `pending` (queued) and `processing` (rendering); `completed` and `failed` are excluded
3. **Free**: no `apiKey` is required
4. **Use Together with gen_video**: the export worker has a concurrency limit, so a high count means a newly submitted task waits longer

## Workflow

1. Read the in-memory export task list
2. Count the tasks whose status is `pending` or `processing`
3. Return the count

## Related Interfaces

- [Generate Video](./gen_video.md)
- [Query Export Status](./gen_video_status.md)

---

<div align="right">

📚 **Project Resources**  
**GitHub**: [https://github.com/Hommy-master/capcut-mate](https://github.com/Hommy-master/capcut-mate)  
**Gitee**: [https://gitee.com/taohongmin-gitee/capcut-mate](https://gitee.com/taohongmin-gitee/capcut-mate)

</div>
