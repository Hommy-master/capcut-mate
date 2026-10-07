# GET_EFFECTS API Documentation

## 🌐 Language Switch
[中文版](./get_effects.zh.md) | [English](./get_effects.md)

## Interface Information

```
POST /openapi/capcut-mate/v1/get_effects
```

## Function Description

Return the built-in JianYing scene effect list, optionally narrowed to VIP or free effects. Use it to look up a valid `effect_title` before calling `add_effects`.

## Request Parameters

```json
{
  "mode": 0
}
```

### Parameter Description

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| mode | integer | ❌ | 0 | 0 = all effects, 1 = VIP only, 2 = free only |

### Parameter Details

#### mode

- **Type**: integer
- **Description**: Which effects to return
- **Range**: 0-2
- **Default**: 0
- **Values**:
  - `0` - All effects
  - `1` - VIP effects only
  - `2` - Free effects only

## Response Format

### Success Response (200)

```json
{
  "code": 0,
  "message": "success",
  "effects": [
    {
      "name": "1998",
      "is_vip": false,
      "resource_id": "6981791065204331044",
      "effect_id": "1183068",
      "icon_url": "",
      "has_params": true
    }
  ]
}
```

### Response Field Description

| Field | Type | Description |
|-------|------|-------------|
| effects | array | Effect object array |
| effects[].name | string | Effect name; pass it as `effect_title` to `add_effects` |
| effects[].is_vip | boolean | Whether the effect is a VIP effect |
| effects[].resource_id | string | Effect resource ID |
| effects[].effect_id | string | Effect effect ID |
| effects[].icon_url | string | Icon URL; always empty, the built-in metadata has no icon |
| effects[].has_params | boolean | Whether the effect carries extra parameters |

### Error Response

```json
{
  "code": 2041,
  "message": "Get effect list failed"
}
```

## Usage Examples

### cURL Examples

#### 1. All Effects

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_effects \
  -H "Content-Type: application/json" \
  -d '{
    "mode": 0
  }'
```

#### 2. Free Effects Only

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_effects \
  -H "Content-Type: application/json" \
  -d '{
    "mode": 2
  }'
```

## Error Code Description

| Error Code | Error Message | Description | Solution |
|------------|---------------|-------------|----------|
| 1001 | Parameter validation failed | `mode` is outside 0-2 or has the wrong type | Pass 0, 1 or 2 |
| 2041 | Get effect list failed | Failed while reading the effect metadata | Retry or contact technical support |

## Notes

1. **No Draft Needed**: this interface is read-only and does not touch any draft
2. **Scene Effects Only**: the list covers scene effects (currently 1097); `add_effects` additionally accepts character effects, whose names are listed in [Add Effects](./add_effects.md)
3. **Name Matching**: `name` is exactly the value accepted by `add_effects` as `effect_title`
4. **icon_url**: reserved field, currently always an empty string

## Workflow

1. Validate the `mode` parameter
2. Read the scene effect metadata
3. Keep all / VIP / free effects according to `mode`
4. Return the effect object array

## Related Interfaces

- [Add Effects](./add_effects.md)
- [Effect Infos](./effect_infos.md)

---

<div align="right">

📚 **Project Resources**  
**GitHub**: [https://github.com/Hommy-master/capcut-mate](https://github.com/Hommy-master/capcut-mate)  
**Gitee**: [https://gitee.com/taohongmin-gitee/capcut-mate](https://gitee.com/taohongmin-gitee/capcut-mate)

</div>
