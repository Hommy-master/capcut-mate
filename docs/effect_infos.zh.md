# EFFECT_INFOS API 接口文档

## 🌐 语言切换
[中文版](./effect_infos.zh.md) | [English](./effect_infos.md)

## 接口信息

```
POST /openapi/capcut-mate/v1/effect_infos
```

## 功能描述

根据特效名称和时间线生成特效信息。该接口将特效名称和时间线配置转换为剪映草稿所需的特效信息格式。

## 请求参数

```json
{
  "effects": ["blur", "vignette"],
  "timelines": [
    {"start": 0, "end": 3000000},
    {"start": 3000000, "end": 6000000}
  ]
}
```

### 参数说明

| 参数名 | 类型 |必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| effects | array[string] |✅ | - |特名称数组 |
| timelines | array[object] |✅ | - | 时间线配置数组 |

##响应格式

### 成功响应 (200)

```json
{
  "code": 0,
  "message": "success",
  "infos": "[{\"effect_title\":\"blur\",\"start\":0,\"end\":3000000},{\"effect_title\":\"vignette\",\"start\":3000000,\"end\":6000000}]"
}
```

###响应字段说明

| 字段名 | 类型 | 说明 |
|--------|------|------|
| infos | string |特效信息JSON字符串 |

### 错误响应

```json
{
  "code": 1001,
  "message": "参数校验失败"
}
```

## 使用示例

### cURL 示例

#### 1. 基本特效信息生成

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/effect_infos \
  -H "Content-Type: application/json" \
  -d '{
    "effects": ["blur"],
    "timelines": [{"start": 0, "end": 5000000}]
  }'
```

#### 2.多特效信息生成

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/effect_infos \
  -H "Content-Type: application/json" \
  -d '{
    "effects": ["blur", "vignette", "sepia"],
    "timelines": [{"start": 0, "end": 2000000}, {"start": 2000000, "end": 4000000}, {"start": 4000000, "end": 6000000}]
  }'
```

##错误码说明

|错误码 | 错误信息 | 说明 | 解决方案 |
|--------|----------|------|----------|
| 1001 | 参数校验失败 | 请求体未通过字段校验（缺少 `effects`/`timelines`、时间线项缺少 `start`/`end`，或类型错误） | 检查参数类型与必填字段 |

## 注意事项

1. **数组匹配**: `effects` 与 `timelines` 长度不一致时，按较短长度截断后继续生成（不会直接报错）
2. **时间单位**:所有时间参数使用微秒（1秒 = 1,000,000微秒）
3. **特效名称**:需要使用系统支持的特效名称
4. **连续性**:特效按时间线顺序应用

##工作流程

1.验证必填参数（effects, timelines）
2.按较短长度对齐两个数组
3.验证时间线参数有效性
4. 为每个特效名称生成对应的特效信息
5.将信息转换为JSON字符串格式
6. 返回处理结果

##相关接口

- [创建草稿](./create_draft.md)
- [添加特效](./add_effects.md)
- [时间线](./timelines.md)
- [保存草稿](./save_draft.md)

---

<div align="right">

📚 **项目资源**  
**GitHub**: [https://github.com/Hommy-master/capcut-mate](https://github.com/Hommy-master/capcut-mate)  
**Gitee**: [https://gitee.com/taohongmin-gitee/capcut-mate](https://gitee.com/taohongmin-gitee/capcut-mate)

</div>

### 语言切换
[中文版](./effect_infos.zh.md) | [English](./effect_infos.md)