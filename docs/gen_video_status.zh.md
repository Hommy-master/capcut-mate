# GEN_VIDEO_STATUS API 接口文档

## 🌐 语言切换
[中文版](./gen_video_status.zh.md) | [English](./gen_video_status.md)

## 接口信息

```bash
POST /openapi/capcut-mate/v1/gen_video_status
```

## 功能描述

查询视频生成任务的状态和进度。配合 [gen_video](./gen_video.md) 接口使用，用于实时跟踪视频生成任务的执行情况，包括任务状态、进度百分比、完成结果等信息。

## 请求参数

```json
{
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258"
}
```

### 参数说明

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| draft_url | string | ✅ | - | 草稿URL，与提交任务时使用的URL相同 |

### 参数详解

#### 草稿URL参数

- **draft_url**: 草稿的完整URL，用于标识要查询状态的视频生成任务
  - 格式：必须是有效的URL格式
  - 示例：`"https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258"`
  - 获取方式：通过 [gen_video](./gen_video.md) 接口提交任务后返回的draft_url

## 响应格式

### 成功响应 (200)

#### 任务等待中

```json
{
  "code": 0,
  "message": "success",
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
  "status": "pending",
  "progress": 0,
  "video_url": "",
  "error_message": "",
  "created_at": "2024-09-24T10:30:00.000Z",
  "started_at": null,
  "completed_at": null
}
```

#### 任务处理中

```json
{
  "code": 0,
  "message": "success",
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258", 
  "status": "processing",
  "progress": 70,
  "video_url": "",
  "error_message": "",
  "created_at": "2024-09-24T10:30:00.000Z",
  "started_at": "2024-09-24T10:30:05.000Z",
  "completed_at": null
}
```

#### 任务已完成

```json
{
  "code": 0,
  "message": "success",
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
  "status": "completed",
  "progress": 100,
  "video_url": "https://video-output.assets.jcaigc.cn/generated/video_abc123def456ghi789.mp4",
  "error_message": "",
  "created_at": "2024-09-24T10:30:00.000Z",
  "started_at": "2024-09-24T10:30:05.000Z",
  "completed_at": "2024-09-24T10:35:30.000Z"
}
```

#### 任务失败

```json
{
  "code": 0,
  "message": "success",
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
  "status": "failed",
  "progress": 0,
  "video_url": "",
  "error_message": "导出草稿失败",
  "created_at": "2024-09-24T10:30:00.000Z",
  "started_at": "2024-09-24T10:30:05.000Z",
  "completed_at": "2024-09-24T10:32:15.000Z"
}
```

### 响应字段说明

| 字段名 | 类型 | 说明 |
|--------|------|------|
| draft_url | string | 草稿URL |
| status | string | 任务状态：pending/processing/completed/failed |
| progress | integer | 任务进度（0-100） |
| video_url | string | 生成的视频URL（仅在completed状态时有值） |
| error_message | string | 错误信息（仅在failed状态时有值） |
| created_at | string | 任务创建时间（ISO格式） |
| started_at | string|null | 任务开始时间（ISO格式） |
| completed_at | string|null | 任务完成时间（ISO格式） |

### 错误响应

#### 2031 视频生成任务未找到

```json
{
  "code": 2031,
  "message": "视频生成任务未找到"
}
```

#### 2032 视频任务状态查询失败

```json
{
  "code": 2032,
  "message": "视频任务状态查询失败"
}
```

## 使用示例

### cURL 示例

#### 1. 查询任务状态

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/gen_video_status \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258"
  }'
```

## 错误码说明

| 错误码 | 错误信息 | 说明 | 解决方案 |
|--------|----------|------|----------|
| 1001 | 参数校验失败 | `draft_url` 缺失或不是字符串 | 提供有效的 `draft_url` |
| 2031 | 视频生成任务未找到 | 指定的草稿URL没有对应的视频生成任务 | 确认是否已通过gen_video接口提交任务 |
| 2032 | 视频任务状态查询失败 | 内部处理错误 | 稍后重试或联系技术支持 |

## 注意事项

1. **轮询间隔**: 建议每5-10秒查询一次任务状态
2. **超时设置**: 建议设置总超时时间（如10分钟）
3. **状态处理**: 根据不同状态提供不同的用户反馈
4. **错误处理**: 妥善处理任务失败情况
5. **进度显示**: 利用progress字段显示进度条
6. **任务唯一性**: 同一草稿URL只能有一个进行中的任务

## 工作流程

1. 验证必填参数（draft_url）
2. 从任务管理器中查询任务状态
3. 将内部状态转换为API响应格式
4. 返回任务状态信息

## 相关接口

- [gen_video](./gen_video.md) - 提交视频生成任务
- [create_draft](./create_draft.md) - 创建新的草稿文件
- [save_draft](./save_draft.md) - 保存草稿文件

---

<div align="right">

📚 **项目资源**  
**GitHub**: [https://github.com/Hommy-master/capcut-mate](https://github.com/Hommy-master/capcut-mate)  
**Gitee**: [https://gitee.com/taohongmin-gitee/capcut-mate](https://gitee.com/taohongmin-gitee/capcut-mate)

</div>

### 语言切换
[中文版](./gen_video_status.zh.md) | [English](./gen_video_status.md)