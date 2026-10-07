# GET_FILTERS API 接口文档

## 🌐 语言切换
[中文版](./get_filters.zh.md) | [English](./get_filters.md)

## 接口信息

```
POST /openapi/capcut-mate/v1/get_filters
```

## 功能描述

获取剪映内置滤镜列表，可按 VIP / 免费筛选。调用 `add_filters` 前可用本接口查询合法的 `filter_title`。

## 更多文档

📖 更多详细文档和教程请访问：[https://docs.jcaigc.cn](https://docs.jcaigc.cn)

## 请求参数

```json
{
  "mode": 0
}
```

### 参数说明

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| mode | integer | ❌ | 0 | 0=全部滤镜，1=仅 VIP，2=仅免费 |

### 参数详解

#### mode

- **类型**: integer
- **说明**: 返回哪一类滤镜
- **取值范围**: 0-2
- **默认值**: 0
- **可选值**:
  - `0` - 全部滤镜
  - `1` - 仅 VIP 滤镜
  - `2` - 仅免费滤镜

## 响应格式

### 成功响应 (200)

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

### 响应字段说明

| 字段名 | 类型 | 说明 |
|--------|------|------|
| filters | array | 滤镜对象数组 |
| filters[].name | string | 滤镜名称，可直接作为 `add_filters` 的 `filter_title` |
| filters[].is_vip | boolean | 是否为 VIP 滤镜 |
| filters[].resource_id | string | 滤镜资源 ID |
| filters[].effect_id | string | 滤镜效果 ID |
| filters[].has_params | boolean | 是否带额外参数 |

### 错误响应

```json
{
  "code": 2040,
  "message": "获取滤镜列表失败"
}
```

## 使用示例

### cURL 示例

#### 1. 获取全部滤镜

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_filters \
  -H "Content-Type: application/json" \
  -d '{
    "mode": 0
  }'
```

#### 2. 只获取免费滤镜

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_filters \
  -H "Content-Type: application/json" \
  -d '{
    "mode": 2
  }'
```

## 错误码说明

| 错误码 | 错误信息 | 说明 | 解决方案 |
|--------|----------|------|----------|
| 1001 | 参数校验失败 | `mode` 超出 0-2 或类型错误 | 传入 0、1 或 2 |
| 2040 | 获取滤镜列表失败 | 读取滤镜元数据出错 | 重试或联系技术支持 |

## 注意事项

1. **无需草稿**: 本接口为只读接口，不涉及任何草稿
2. **名称匹配**: `name` 就是 `add_filters` 的 `filter_title` 所接受的值
3. **清单规模**: 清单来自本地剪映元数据，随内置元数据版本变化（当前共 1052 个滤镜：802 个 VIP、250 个免费）
4. **与 add_filters 配合**: 这里返回的名称一定能解析成功；名称匹配不到时 `add_filters` 会返回 2039

## 工作流程

1. 校验 `mode` 参数
2. 读取滤镜元数据
3. 按 `mode` 保留全部 / VIP / 免费滤镜
4. 返回滤镜对象数组

## 相关接口

- [添加滤镜](./add_filters.zh.md)
- [滤镜信息](./filter_infos.zh.md)

---

<div align="right">

📚 **项目资源**  
**GitHub**: [https://github.com/Hommy-master/capcut-mate](https://github.com/Hommy-master/capcut-mate)  
**Gitee**: [https://gitee.com/taohongmin-gitee/capcut-mate](https://gitee.com/taohongmin-gitee/capcut-mate)

</div>
