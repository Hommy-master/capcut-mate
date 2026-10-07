# GEN_VIDEO API 接口文档

## 🌐 语言切换
[中文版](./gen_video.zh.md) | [English](./gen_video.md)

## 接口信息

```
POST /openapi/capcut-mate/v1/gen_video
```

## 功能描述

提交视频生成任务。该接口采用异步处理模式，立即返回任务提交状态，视频生成在后台进行。支持任务排队，确保系统稳定性。

## 更多文档

📖 更多详细文档和教程请访问：[https://docs.jcaigc.cn](https://docs.jcaigc.cn)

## 请求参数

```json
{
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
  "apiKey": "123e4567-e89b-12d3-a456-426614174000"
}
```

### 参数说明

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| draft_url | string | ✅ | - | 目标草稿的完整URL |
| apiKey | string | 按服务端配置 | - | 合法的 UUID；`ENABLE_APIKEY=true` 时必填，可登录 https://jcaigc.cn 获取 |

### 参数详解

#### 草稿URL参数

- **draft_url**: 草稿的完整URL地址
  - 格式：`https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id={草稿ID}`
  - 示例：`"https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258"`
  - 获取方式：通过[创建草稿](./create_draft.md)或[保存草稿](./save_draft.md)接口获取

## 响应格式

### 成功响应 (200)

```json
{
  "code": 0,
  "message": "视频生成任务已提交，请使用draft_url查询进度"
}
```

### 响应字段说明

| 字段名 | 类型 | 说明 |
|--------|------|------|
| message | string | 响应消息 |

### 错误响应

```json
{
  "code": 2001,
  "message": "无效的草稿URL"
}
```

## 使用示例

### cURL 示例

#### 1. 基本视频生成

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/gen_video \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
    "apiKey": "123e4567-e89b-12d3-a456-426614174000"
  }'
```

## 错误码说明

| 错误码 | 错误信息 | 说明 | 解决方案 |
|--------|----------|------|----------|
| 1001 | 参数校验失败 | `apiKey` 不是合法 UUID，或参数类型不正确 | 检查参数类型与必填字段 |
| 2001 | 无效的草稿URL | `draft_url` 缺失或不含 `draft_id` | 传入 `create_draft` 返回的 `draft_url` |
| 2035 | 账户余额不足 | 当前积分不大于 1 | 完成充值后重试 |
| 2036 | 无效的 apiKey | `ENABLE_APIKEY=true` 且未传 `apiKey` | 登录 https://jcaigc.cn 获取 apiKey |
| 9998 | 系统内部错误 | 提交任务时发生未知错误 | 稍后重试或联系技术支持 |

## 注意事项

1. **处理时间**: 视频生成是耗时操作，可能需要几分钟到几十分钟
2. **文件大小**: 草稿复杂度和素材数量会影响处理时间
3. **网络稳定**: 确保素材URL可以稳定访问
4. **超时设置**: 建议设置较长的超时时间或使用轮询机制
5. **并发限制**: 避免同时生成大量视频
6. **存储空间**: 生成的视频文件可能很大，注意存储空间
7. **URL有效期**: 生成的video_url可能有时效性限制
8. **系统要求**: 视频生成功能仅在Windows系统上可用

## 工作流程

1. 验证draft_url参数
2. 解析草稿配置文件
3. 下载所有必需的素材文件
4. 按时间轴排列和处理素材
5. 应用视觉效果和转场
6. 混合音频轨道
7. 渲染最终视频
8. 编码并上传视频文件
9. 返回视频URL

## 相关接口

- [创建草稿](./create_draft.md)
- [保存草稿](./save_draft.md)
- [添加视频](./add_videos.md)
- [添加音频](./add_audios.md)
- [添加图片](./add_images.md)
- [获取草稿](./get_draft.md)
- [查询视频生成状态](./gen_video_status.md)

---

<div align="right">

📚 **项目资源**  
**GitHub**: [https://github.com/Hommy-master/capcut-mate](https://github.com/Hommy-master/capcut-mate)  
**Gitee**: [https://gitee.com/taohongmin-gitee/capcut-mate](https://gitee.com/taohongmin-gitee/capcut-mate)

</div>

### 语言切换
[中文版](./gen_video.zh.md) | [English](./gen_video.md)