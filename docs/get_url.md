# GET_URL API Documentation

### 🌐 Language Switch
[中文版](./get_url.zh.md) | [English](./get_url.md)

## Interface Information

```
POST /openapi/capcut-mate/v1/get_url
```

## Function Description

Extract links. This interface is used to extract link information from input content, converting multiple values into single value return.

## More Documentation

📖 For more detailed documentation and tutorials, please visit: [https://docs.jcaigc.cn](https://docs.jcaigc.cn)

## Request Parameters

```json
{
  "output": "[魂牵梦萦https://sf.com；中国人https://jcaigc.cn],\"[]\""
}
```

### Parameter Description

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| output | string |✅ | - | Content to extract |

### Parameter Details

#### output

- **Type**: string
- **Description**: Content from which to extract links
- **Example**: `"[魂牵梦萦https://sf.com；中国人https://jcaigc.cn],\"[]\""`

## Response Format

### Success Response (200)

```json
{
  "output": "[魂牵梦萦https://sf.com；中国人https://jcaigc.cn],\"[]\""
}
```

### Response Field Description

| Field | Type | Description |
|-------|------|-------------|
| output | string | Extraction result |

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
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_url \
  -H "Content-Type: application/json" \
  -d '{
    "output": "[魂牵梦萦https://sf.com；中国人https://jcaigc.cn],\"[]\""
  }'
```

## Error Code Description

| Error Code | Error Message | Description | Solution |
|------------|---------------|-------------|----------|
| 400 | output is required | Missing output parameter | Provide a valid output parameter |
| 500 | Link extraction failed | Internal processing error | Contact technical support |

## Notes

1. **Parameter Requirements**: output parameter is required
2. **Return Value**: Current version directly returns input content without additional processing

## Workflow

1. Validate required parameter (output)
2. Call service layer to handle business logic
3. Return processing result

## Related Interfaces

- [Create Draft](./create_draft.md)

---

<div align="right">

📚 **Project Resources**  
**GitHub**: [https://github.com/Hommy-master/capcut-mate](https://github.com/Hommy-master/capcut-mate)  
**Gitee**: [https://gitee.com/taohongmin-gitee/capcut-mate](https://gitee.com/taohongmin-gitee/capcut-mate)

</div>