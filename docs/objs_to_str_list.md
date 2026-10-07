# OBJS_TO_STR_LIST API Documentation

## 🌐 Language Switch
[中文版](./objs_to_str_list.zh.md) | [English](./objs_to_str_list.md)

## Interface Information

```
POST /openapi/capcut-mate/v1/objs_to_str_list
```

## Function Description

Convert object list to string list. This interface is used to convert input object list to string list format.

## Request Parameters

```json
{
  "outputs": [
    {
      "output": "https://assets.jcaigc.cn/min.mp4"
    },
    {
      "output": "https://assets.jcaigc.cn/max.mp4"
    }
  ]
}
```

### Parameter Description

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| outputs | array[object] |✅ | - | Data objects |

### Parameter Details

#### outputs

- **Type**: array[object]
- **Description**: Object list to convert
- **Example**: `[{"output": "https://assets.jcaigc.cn/min.mp4"}, {"output": "https://assets.jcaigc.cn/max.mp4"}]`

## Response Format

### Success Response (200)

```json
{
  "code": 0,
  "message": "success",
  "infos": [
    "https://assets.jcaigc.cn/min.mp4",
    "https://assets.jcaigc.cn/max.mp4"
  ]
}
```

### Response Field Description

| Field | Type | Description |
|-------|------|-------------|
| infos | array[string] | String list |

### Error Response

```json
{
  "code": 1001,
  "message": "Parameter validation failed"
}
```

## Usage Examples

### cURL Examples

#### 1. Basic Usage

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/objs_to_str_list \
  -H "Content-Type: application/json" \
  -d '{
    "outputs": [
      {
        "output": "https://assets.jcaigc.cn/min.mp4"
      },
      {
        "output": "https://assets.jcaigc.cn/max.mp4"
      }
    ]
  }'
```

## Error Code Description

| Error Code | Error Message | Description | Solution |
|------------|---------------|-------------|----------|
| 1001 | Parameter validation failed | outputs is missing (request body failed schema validation) | Provide a valid outputs parameter |
| 9999 | Unknown error | Unexpected internal processing error | Contact technical support |

## Notes

1. **Parameter Requirements**: outputs parameter is required
2. **Return Value**: Extract output fields from input object list to form string list

## Workflow

1. Validate required parameter (outputs)
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