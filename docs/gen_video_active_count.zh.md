# GEN_VIDEO_ACTIVE_COUNT API 接口文档

## 🌐 语言切换
[中文版](./gen_video_active_count.zh.md) | [English](./gen_video_active_count.md)

## 接口信息

```
GET /openapi/capcut-mate/v1/gen_video_active_count
```

## 功能描述

查询当前排队中与渲染中的导出任务数量，即状态为 `pending` 或 `processing` 的任务数；已完成与失败的任务不计入。可在调用 `gen_video` 前用于判断当前导出压力。

## 更多文档

📖 更多详细文档和教程请访问：[https://docs.jcaigc.cn](https://docs.jcaigc.cn)

## 请求参数

本接口无需任何参数。

## 响应格式

### 成功响应 (200)

```json
{
  "code": 0,
  "message": "success",
  "count": 3
}
```

### 响应字段说明

| 字段名 | 类型 | 说明 |
|--------|------|------|
| count | integer | 处于 `pending` 或 `processing` 的任务数量 |

### 错误响应

```json
{
  "code": 9998,
  "message": "系统内部错误"
}
```

## 使用示例

### cURL 示例

#### 1. 查询进行中的导出数量

```bash
curl -X GET https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/gen_video_active_count
```

## 错误码说明

| 错误码 | 错误信息 | 说明 | 解决方案 |
|--------|----------|------|----------|
| 9998 | 系统内部错误 | 统计任务时发生未预期异常 | 稍后重试或联系技术支持 |

## 注意事项

1. **无参数**: 本接口没有请求体，也没有查询参数
2. **统计范围**: 只统计 `pending`（排队中）与 `processing`（渲染中），不含 `completed` 与 `failed`
3. **免费**: 不需要 `apiKey`
4. **配合 gen_video 使用**: 导出并发有上限，count 较大时新提交的任务排队时间会更长

## 工作流程

1. 读取内存中的导出任务列表
2. 统计状态为 `pending` 或 `processing` 的任务
3. 返回数量

## 相关接口

- [生成视频](./gen_video.zh.md)
- [查询导出状态](./gen_video_status.zh.md)

---

<div align="right">

📚 **项目资源**  
**GitHub**: [https://github.com/Hommy-master/capcut-mate](https://github.com/Hommy-master/capcut-mate)  
**Gitee**: [https://gitee.com/taohongmin-gitee/capcut-mate](https://gitee.com/taohongmin-gitee/capcut-mate)

</div>
