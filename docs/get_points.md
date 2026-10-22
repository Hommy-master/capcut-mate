# GET_POINTS API Documentation

## 🌐 Language Switch
[中文版](./get_points.zh.md) | [English](./get_points.md)

## Interface Information

```
GET https://jcaigc.cn/openapi/v1/user/points
```

## Function Description

Query the recharge balance (in CNY) of the account that owns the given apiKey. The endpoint is served directly by the Jianchuang open platform (jcaigc.cn) and uses the same recharge balance that `gen_video` and `upload_file` deduct from; the request does not go through the CapCut Mate service. Call it before billed endpoints to avoid rejections caused by insufficient balance.

## Request Parameters

Parameters are passed in the URL query string. There is no request body.

```bash
curl -X GET "https://jcaigc.cn/openapi/v1/user/points?apiKey=123e4567-e89b-12d3-a456-426614174000"
```

### Parameter Description

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| apiKey | string | ✅ | - | API Key of the account. Always a 36-character UUID. View it at https://jcaigc.cn/user-info |

### Parameter Details

#### apiKey

- **Type**: string
- **Description**: Must be a complete 36-character UUID (hyphens included). A missing key or a length other than 36 returns 10002
- **How to get it**: Sign in at https://jcaigc.cn/user-info to view or regenerate it

## Response Format

### Success Response (200)

```json
{
  "code": 0,
  "message": "success",
  "traceid": "067b0e601f4a4784afe4068da658e555",
  "data": {
    "points": 12.34
  }
}
```

### Response Field Description

| Field | Type | Description |
|-------|------|-------------|
| code | int | Business status code. 0 means success |
| message | string | Status message; returns "成功" for Chinese requests and "success" for English requests |
| traceid | string | Trace ID of this request. Provide it to support when troubleshooting |
| data | object | Business data |
| data.points | float | Account recharge balance in CNY. The field name follows the gateway's `points` |

### Error Response

```json
{
  "code": 10007,
  "message": "Invalid apiKey",
  "traceid": "845b5403cd8a999ad7df7b6c4649336d",
  "data": null
}
```

## Usage Examples

### cURL Examples

#### 1. Query the account balance

```bash
curl -X GET "https://jcaigc.cn/openapi/v1/user/points?apiKey=123e4567-e89b-12d3-a456-426614174000"
```

#### 2. Request Chinese error messages

```bash
curl -X GET "https://jcaigc.cn/openapi/v1/user/points?apiKey=123e4567-e89b-12d3-a456-426614174000" \
  -H "Accept-Language: zh-CN"
```

### Python Example

```python
import requests

resp = requests.get(
    "https://jcaigc.cn/openapi/v1/user/points",
    params={"apiKey": "123e4567-e89b-12d3-a456-426614174000"},
    headers={"Accept-Language": "zh-CN"},
    timeout=10,
)
result = resp.json()

if result["code"] == 0:
    print("Balance:", result["data"]["points"], "CNY")
else:
    print("Query failed:", result["code"], result["message"], result["traceid"])
```

## Error Code Description

| Error Code | Error Message | Description | Solution |
|------------|---------------|-------------|----------|
| 10002 | Invalid parameter | apiKey is missing, or its length is not 36 | Pass a complete 36-character UUID |
| 10007 | Invalid apiKey | The format is valid but no account matches the key | Verify the API Key, or get it again at https://jcaigc.cn/user-info |
| 10001 | Internal server error | Unexpected gateway error | Retry later; if it persists, contact support with the traceid |

## Notes

1. **Endpoint ownership**: Served by the Jianchuang open platform (jcaigc.cn), not the CapCut Mate service. `gen_video` and `upload_file` internally call the same endpoint to check the balance
2. **Free**: Balance queries are not billed
3. **Unit**: `points` is the gateway's historical field name; the value is the recharge balance in CNY
4. **apiKey in the URL**: Always use HTTPS, and do not write full URLs containing the apiKey into logs or share them publicly
5. **Membership discount**: This endpoint returns the balance before any discount. Billing applies the membership discount (SVIP 40% off, VIP 20% off)

## Workflow

1. Validate apiKey: missing or length not 36 returns 10002
2. Look up the account by apiKey: no match returns 10007
3. Return the current recharge balance of the account

## Related Interfaces

- [Generate Video](./gen_video.md)
- [Upload File](./upload_file.md)

---

<div align="right">

📚 **Project Resources**  
**GitHub**: [https://github.com/Hommy-master/capcut-mate](https://github.com/Hommy-master/capcut-mate)  
**Gitee**: [https://gitee.com/taohongmin-gitee/capcut-mate](https://gitee.com/taohongmin-gitee/capcut-mate)

</div>
