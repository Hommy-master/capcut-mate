# GET_EFFECTS API 接口文档

## 🌐 语言切换
[中文版](./get_effects.zh.md) | [English](./get_effects.md)

## 接口信息

```
POST /openapi/capcut-mate/v1/get_effects
```

## 功能描述

获取剪映内置画面特效列表，可按 VIP / 免费筛选。调用 `add_effects` 前可用本接口查询合法的 `effect_title`。

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
| mode | integer | ❌ | 0 | 0=全部特效，1=仅 VIP，2=仅免费 |

### 参数详解

#### mode

- **类型**: integer
- **说明**: 返回哪一类特效
- **取值范围**: 0-2
- **默认值**: 0
- **可选值**:
  - `0` - 全部特效
  - `1` - 仅 VIP 特效
  - `2` - 仅免费特效

## 响应格式

### 成功响应 (200)

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

### 响应字段说明

| 字段名 | 类型 | 说明 |
|--------|------|------|
| effects | array | 特效对象数组 |
| effects[].name | string | 特效名称，可直接作为 `add_effects` 的 `effect_title` |
| effects[].is_vip | boolean | 是否为 VIP 特效 |
| effects[].resource_id | string | 特效资源 ID |
| effects[].effect_id | string | 特效效果 ID |
| effects[].icon_url | string | 图标 URL；固定为空字符串，内置元数据中没有图标 |
| effects[].has_params | boolean | 是否带额外参数 |

### 错误响应

```json
{
  "code": 2041,
  "message": "获取特效列表失败"
}
```

## 使用示例

### cURL 示例

#### 1. 获取全部特效

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_effects \
  -H "Content-Type: application/json" \
  -d '{
    "mode": 0
  }'
```

#### 2. 只获取免费特效

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_effects \
  -H "Content-Type: application/json" \
  -d '{
    "mode": 2
  }'
```

## 错误码说明

| 错误码 | 错误信息 | 说明 | 解决方案 |
|--------|----------|------|----------|
| 1001 | 参数校验失败 | `mode` 超出 0-2 或类型错误 | 传入 0、1 或 2 |
| 2041 | 获取特效列表失败 | 读取特效元数据出错 | 重试或联系技术支持 |

## 注意事项

1. **无需草稿**: 本接口为只读接口，不涉及任何草稿
2. **仅画面特效**: 本清单只含画面特效（当前 1097 个）；`add_effects` 还支持人物特效，名称见[添加特效](./add_effects.zh.md)
3. **名称匹配**: `name` 就是 `add_effects` 的 `effect_title` 所接受的值
4. **icon_url**: 预留字段，当前固定为空字符串

## 工作流程

1. 校验 `mode` 参数
2. 读取画面特效元数据
3. 按 `mode` 保留全部 / VIP / 免费特效
4. 返回特效对象数组

## 相关接口

- [添加特效](./add_effects.zh.md)
- [特效信息](./effect_infos.zh.md)

---

<div align="right">

📚 **项目资源**  
**GitHub**: [https://github.com/Hommy-master/capcut-mate](https://github.com/Hommy-master/capcut-mate)  
**Gitee**: [https://gitee.com/taohongmin-gitee/capcut-mate](https://gitee.com/taohongmin-gitee/capcut-mate)

</div>
