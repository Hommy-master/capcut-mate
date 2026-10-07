# GET_URL API 接口文档

## 🌐 语言切换
[中文版](./get_url.zh.md) | [English](./get_url.md)

## 接口信息

```
POST /openapi/capcut-mate/v1/get_url
```

## 功能描述

提取链接。该接口用于提取输入内容中的链接信息，用于多值返回变成单值返回。

## 请求参数

```json
{
  "output": "[魂牵梦萦https://sf.com；中国人https://jcaigc.cn],\"[]\""
}
```

### 参数说明

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| output | string | ✅ | - | 提取内容 |

### 参数详解

#### output

- **类型**: string
- **说明**: 需要提取链接的内容
- **示例**: `"[魂牵梦萦https://sf.com；中国人https://jcaigc.cn],\"[]\""`

## 响应格式

### 成功响应 (200)

```json
{
  "code": 0,
  "message": "success",
  "output": "[魂牵梦萦https://sf.com；中国人https://jcaigc.cn],\"[]\""
}
```

### 响应字段说明

| 字段名 | 类型 | 说明 |
|--------|------|------|
| output | string | 提取结果 |

### 错误响应

```json
{
  "code": 1001,
  "message": "参数校验失败"
}
```

## 使用示例

### cURL 示例

#### 1. 基本使用

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_url \
  -H "Content-Type: application/json" \
  -d '{
    "output": "[魂牵梦萦https://sf.com；中国人https://jcaigc.cn],\"[]\""
  }'
```

## 错误码说明

| 错误码 | 错误信息 | 说明 | 解决方案 |
|--------|----------|------|----------|
| 1001 | 参数校验失败 | 缺少 output 参数（请求体未通过参数校验） | 提供有效的output参数 |
| 9999 | 未知异常 | 内部处理异常 | 联系技术支持 |

## 注意事项

1. **参数要求**: output参数为必填项
2. **返回值**: 当前版本直接返回输入的内容，不做额外处理

## 工作流程

1. 验证必填参数（output）
2. 调用服务层处理业务逻辑
3. 返回处理结果

## 相关接口

- [创建草稿](./create_draft.md)

---

<div align="right">

📚 **项目资源**  
**GitHub**: [https://github.com/Hommy-master/capcut-mate](https://github.com/Hommy-master/capcut-mate)  
**Gitee**: [https://gitee.com/taohongmin-gitee/capcut-mate](https://gitee.com/taohongmin-gitee/capcut-mate)

</div>