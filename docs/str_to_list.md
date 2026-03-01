# STR_TO_LIST API Documentation

###🌐 Language Switch
[中文版](./str_to_list.zh.md) | [English](./str_to_list.md)

## Interface Information

```
POST /openapi/capcut-mate/v1/str_to_list
```

## Function Description

Convert string to list. This interface is used to convert input string to list format.

## More Documentation

📖 For more detailed documentation and tutorials, please visit: [https://docs.jcaigc.cn](https://docs.jcaigc.cn)

## Request Parameters

```json
{
  "obj": "{   \"infos\": [     \"https://assets.jcaigc.cn/min.mp4\",     \"https://assets.jcaigc.cn/max.mp4\"   ] }"
}
```

### Parameter Description

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| obj | string |✅ | - | Object content |

### Parameter Details

#### obj

- **Type**: string
- **Description**: String content to convert
- **Example**: `"{   \"infos\": [     \"https://assets.jcaigc.cn/min.mp4\",     \"https://assets.jcaigc.cn/max.mp4\"   ] }"`

## Response Format

### Success Response (200)

```json
{
  "infos": [
    "{   \"infos\": [     \"https://assets.jcaigc.cn/min.mp4\",     \"https://assets.jcaigc.cn/max.mp4\"   ] }"
  ]
}
```

### Response Field Description

| Field | Type | Description |
|-------|------|-------------|
| infos | array[string] | String list |

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
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/str_to_list \
  -H "Content-Type: application/json" \
  -d '{
    "obj": "{   \"infos\": [     \"https://assets.jcaigc.cn/min.mp4\",     \"https://assets.jcaigc.cn/max.mp4\"   ] }"
  }'
```

## Error Code Description

| Error Code | Error Message | Description | Solution |
|------------|---------------|-------------|----------|
| 400 | obj is required | Missing obj parameter | Provide a valid obj parameter |
| 500 | String to list conversion failed | Internal processing error | Contact technical support |

## Notes

1. **Parameter Requirements**: obj parameter is required
2. **Return Value**: Put input string as single element in list and return

## Workflow

1. Validate required parameter (obj)
2. Call service layer to handle business logic
3. Return converted string list

## Related Interfaces

- [Create Draft](./create_draft.md)

---

<div align="right">

📚 **Project Resources**  
**GitHub**: [https://github.com/Hommy-master/capcut-mate](https://github.com/Hommy-master/capcut-mate)  
**Gitee**: [https://gitee.com/taohongmin-gitee/capcut-mate](https://gitee.com/taohongmin-gitee/capcut-mate)

</div>