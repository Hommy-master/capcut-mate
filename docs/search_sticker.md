# SEARCH_STICKER API Documentation

## 🌐 Language Switch
[中文版](./search_sticker.zh.md) | [English](./search_sticker.md)

## Interface Information

```
POST /openapi/capcut-mate/v1/search_sticker
```

## Function Description

Search stickers by keywords. This interface is used to search for related sticker materials based on keywords provided by users, returning a list of matching stickers, including detailed information such as image URLs, dimensions, types, etc.

## Request Parameters

```json
{
  "keyword": "人"
}
```

### Parameter Description

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| keyword | string |✅ | - | Search keyword |

### Parameter Details

#### keyword

- **Type**: string
- **Description**: Keyword to search for stickers
- **Example**: "人", "花", "动物"

## Response Format

### Success Response (200)

```json
{
  "code": 0,
  "message": "success",
  "data": [
    {
      "title": "大笑",
      "sticker_id": "7521200021564427545",
      "image_url": "https://p3-heycan-jy-sign.byteimg.com/tos-cn-i-3jr8j4ixpe/29351205dbd943658d94c8feb17e5ed4~tplv-3jr8j4ixpe-resize:1920:1920.png?x-expires=1797257777&x-signature=r18I9uLQzgm%2FcvF8WNLbgw8BRwg%3D"
    }
  ]
}
```

### Response Field Description

| Field | Type | Description |
|-------|------|-------------|
| data | array | Sticker data list |
| title | string | Sticker title (the only search key) |
| sticker_id | string | Sticker ID, the input for `add_sticker` |
| image_url | string | Sticker preview image URL (1920×1920) |

> Earlier versions also returned `sticker.large_image`, `sticker.track_thumbnail`, `sticker.sticker_package`, `sticker.sticker_type` and `sticker.preview_cover`. These have been removed: `preview_cover` is an empty string in every entry, and the rest are read by no code. The response is now flat instead of nested, so callers must be updated accordingly.

### Error Response

```json
{
  "code": 1001,
  "message": "Parameter validation failed"
}
```

## Usage Examples

### cURL Examples

#### 1. Search Stickers with Keyword "人"

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/search_sticker \
  -H "Content-Type: application/json" \
  -d '{
    "keyword": "人"
  }'
```

#### 2. Search Stickers with Keyword "动物"

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/search_sticker \
  -H "Content-Type: application/json" \
  -d '{
    "keyword": "动物"
  }'
```

## Error Code Description

| Error Code | Error Message | Description | Solution |
|------------|---------------|-------------|----------|
| 1001 | Parameter validation failed | keyword is missing (request body failed schema validation) | Provide a valid keyword parameter |

## Notes

1. **Keyword Matching**: Current implementation uses simple title matching, can be extended to full-text search in actual applications
2. **Data Source**: Currently returns mock data, in actual applications should connect to sticker database or call external APIs
3. **Performance Consideration**: For large sticker datasets, should consider pagination and caching mechanisms

## Workflow

1. Validate required parameter (keyword)
2. Call service layer to search for stickers
3. Return matching sticker list

## Related Interfaces

- [Add Sticker](./add_sticker.md)
- [Create Draft](./create_draft.md)

---

<div align="right">

📚 **Project Resources**  
**GitHub**: [https://github.com/Hommy-master/capcut-mate](https://github.com/Hommy-master/capcut-mate)  
**Gitee**: [https://gitee.com/taohongmin-gitee/capcut-mate](https://gitee.com/taohongmin-gitee/capcut-mate)

</div>