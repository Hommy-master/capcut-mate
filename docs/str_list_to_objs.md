# STR_LIST_TO_OBJS API Documentation

## 🌐 Language Switch
[中文版](./str_list_to_objs.zh.md) | [English](./str_list_to_objs.md)

## Interface Information

```
POST /openapi/capcut-mate/v1/str_list_to_objs
```

## Function Description

Convert string list to object list. This interface is used to convert input string list to object list format.

## More Documentation

📖 For more detailed documentation and tutorials, please visit: [https://docs.jcaigc.cn](https://docs.jcaigc.cn)

## Request Parameters

```json
{
  "infos": [
    "https://assets.jcaigc.cn/min.mp4",
    "https://assets.jcaigc.cn/max.mp4"
  ]
}
```

### Parameter Description

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| infos | array[string] |✅ | - | String list |

### Parameter Details

#### infos

- **Type**: array[string]
- **Description**: String list to convert
- **Example**: `["https://assets.jcaigc.cn/min.mp4", "https://assets.jcaigc.cn/max.mp4"]`

## Response Format

### Success Response (200)

```json
{
  "infos": [
    {
      "output": "https://assets.jcaigc.cn/min.mp4"
    },
    {
      "output": "https://assets.jcaigc.cn/max.mp4"
    }
  ]
}
```

### Response Field Description

| Field | Type | Description |
|-------|------|-------------|
| infos | array[object] | Object list |
| output | string | URL address |

### Error Response (4xx/5xx)

```json
{
  "detail": "Error message description"
}
```

## Usage Examples

### cURL Examples

#### 1. Basic Usage

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/str_list_to_objs \
  -H "Content-Type: application/json" \
  -d '{
    "infos": [
      "https://assets.jcaigc.cn/min.mp4",
      "https://assets.jcaigc.cn/max.mp4"
    ]
  }'
```

## Error Code Description

| Error Code | Error Message | Description | Solution |
|------------|---------------|-------------|----------|
| 400 | infos is required | Missing infos parameter | Provide a valid infos parameter |
| 500 | String list conversion failed | Internal processing error | Contact technical support |

## Notes

1. **Parameter Requirements**: infos parameter is required
2. **Return Value**: Convert input string list to object list containing output fields

## Workflow

1. Validate required parameter (infos)
2. Call service layer to handle business logic
3. Return converted object list

## Related Interfaces

- [Create Draft](./create_draft.md)

---

<div align="right">

📚 **Project Resources**  
**GitHub**: [https://github.com/Hommy-master/capcut-mate](https://github.com/Hommy-master/capcut-mate)  
**Gitee**: [https://gitee.com/taohongmin-gitee/capcut-mate](https://gitee.com/taohongmin-gitee/capcut-mate)

</div>