# OBJS_TO_STR_LIST API 接口文档

## 🌐 语言切换
[中文版](./add_audios.zh.md) | [English](./add_audios.md)

## 接口信息

```
POST /openapi/capcut-mate/v1/objs_to_str_list
```

## 功能描述

对象列表转化成字符串列表。该接口用于将输入的对象列表转换为字符串列表格式。

## 更多文档

📖 更多详细文档和教程请访问：[https://docs.jcaigc.cn](https://docs.jcaigc.cn)

## 请求参数

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

### 参数说明

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| outputs | array[object] | ✅ | - | 数据对象 |

### 参数详解

#### outputs

- **类型**: array[object]
- **说明**: 需要转换的对象列表
- **示例**: `[{"output": "https://assets.jcaigc.cn/min.mp4"}, {"output": "https://assets.jcaigc.cn/max.mp4"}]`

## 响应格式

### 成功响应 (200)

```json
{
  "infos": [
    "https://assets.jcaigc.cn/min.mp4",
    "https://assets.jcaigc.cn/max.mp4"
  ]
}
```

### 响应字段说明

| 字段名 | 类型 | 说明 |
|--------|------|------|
| infos | array[string] | 字符串列表 |

### 错误响应 (4xx/5xx)

```json
{
  "detail": "错误信息描述"
}
```

## 使用示例

### cURL 示例

#### 1. 基本使用

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

## 错误码说明

| 错误码 | 错误信息 | 说明 | 解决方案 |
|--------|----------|------|----------|
| 400 | outputs是必填项 | 缺少outputs参数 | 提供有效的outputs参数 |
| 500 | 对象列表转换失败 | 内部处理错误 | 联系技术支持 |

## 注意事项

1. **参数要求**: outputs参数为必填项
2. **返回值**: 将输入的对象列表中的output字段提取出来组成字符串列表

## 工作流程

1. 验证必填参数（outputs）
2. 调用服务层处理业务逻辑
3. 返回转换后的字符串列表

## 相关接口

- [创建草稿](./create_draft.md)

---

<div align="right">

📚 **项目资源**  
**GitHub**: [https://github.com/Hommy-master/capcut-mate](https://github.com/Hommy-master/capcut-mate)  
**Gitee**: [https://gitee.com/taohongmin-gitee/capcut-mate](https://gitee.com/taohongmin-gitee/capcut-mate)

</div>