# GET_FILTERS API Documentation

## 🌐 Language Switch
[中文版](./get_filters.zh.md) | [English](./get_filters.md)

## Interface Information

```
POST /openapi/capcut-mate/v1/get_filters
```

## Function Description

Return the built-in JianYing filter list, optionally narrowed to VIP or free filters. Use it to look up a valid `filter_title` before calling `add_filters`.

## More Documentation

📖 For more detailed documentation and tutorials, please visit: [https://docs.jcaigc.cn](https://docs.jcaigc.cn)

## Request Parameters

```json
{
  "mode": 0
}
```

### Parameter Description

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| mode | integer | ❌ | 0 | 0 = all filters, 1 = VIP only, 2 = free only |

### Parameter Details

#### mode

- **Type**: integer
- **Description**: Which filters to return
- **Range**: 0-2
- **Default**: 0
- **Values**:
  - `0` - All filters
  - `1` - VIP filters only
  - `2` - Free filters only

## Response Format

### Success Response (200)

```json
{
  "code": 0,
  "message": "success",
  "filters": [
    {
      "name": "1980",
      "is_vip": false,
      "resource_id": "7127828208690433311",
      "effect_id": "7127828208690433311",
      "has_params": false
    }
  ]
}
```

### Response Field Description

| Field | Type | Description |
|-------|------|-------------|
| filters | array | Filter object array |
| filters[].name | string | Filter name; pass it as `filter_title` to `add_filters` |
| filters[].is_vip | boolean | Whether the filter is a VIP filter |
| filters[].resource_id | string | Filter resource ID |
| filters[].effect_id | string | Filter effect ID |
| filters[].has_params | boolean | Whether the filter carries extra parameters |

### Error Response

```json
{
  "code": 2040,
  "message": "Get filter list failed"
}
```

## Usage Examples

### cURL Examples

#### 1. All Filters

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_filters \
  -H "Content-Type: application/json" \
  -d '{
    "mode": 0
  }'
```

#### 2. Free Filters Only

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_filters \
  -H "Content-Type: application/json" \
  -d '{
    "mode": 2
  }'
```

## Error Code Description

| Error Code | Error Message | Description | Solution |
|------------|---------------|-------------|----------|
| 1001 | Parameter validation failed | `mode` is outside 0-2 or has the wrong type | Pass 0, 1 or 2 |
| 2040 | Get filter list failed | Failed while reading the filter metadata | Retry or contact technical support |

## Notes

1. **No Draft Needed**: this interface is read-only and does not touch any draft
2. **Name Matching**: `name` is exactly the value accepted by `add_filters` as `filter_title`
3. **List Size**: the list comes from the local JianYing metadata and changes with the built-in metadata version (currently 1052 filters: 802 VIP, 250 free)
4. **Use with add_filters**: names returned here are guaranteed to resolve; unmatched names make `add_filters` fail with 2039

## Workflow

1. Validate the `mode` parameter
2. Read the filter metadata
3. Keep all / VIP / free filters according to `mode`
4. Return the filter object array

## Related Interfaces

- [Add Filters](./add_filters.md)
- [Filter Infos](./filter_infos.md)

---

<div align="right">

📚 **Project Resources**  
**GitHub**: [https://github.com/Hommy-master/capcut-mate](https://github.com/Hommy-master/capcut-mate)  
**Gitee**: [https://gitee.com/taohongmin-gitee/capcut-mate](https://gitee.com/taohongmin-gitee/capcut-mate)

</div>
