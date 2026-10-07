# GET_AUDIO_DURATION API 接口文档

## 🌐 语言切换
[中文版](./get_audio_duration.zh.md) | [English](./get_audio_duration.md)

## 接口信息

```
POST /openapi/capcut-mate/v1/get_audio_duration
```

## 功能描述

获取音频文件的时长，支持各种常见的音频格式。使用FFprobe工具进行精确的音频分析，返回音频文件的准确时长，单位为微秒。

## 请求参数

```json
{
  "mp3_url": "https://assets.jcaigc.cn/audio/sample.mp3"
}
```

### 参数说明

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| mp3_url | string | ✅ | - | 音频文件URL，支持mp3、wav、m4a等常见音频格式 |

### 参数详解

#### 音频URL参数

- **mp3_url**: 音频文件的完整URL地址
  - 支持格式：mp3、wav、aac、flac、m4a等常见音频格式
  - 需要确保URL可访问且文件完整

## 响应格式

### 成功响应 (200)

```json
{
  "code": 0,
  "message": "success",
  "duration": 2325333
}
```

### 响应字段说明

| 字段名 | 类型 | 说明 |
|--------|------|------|
| duration | integer | 音频时长，单位：微秒 |

### 错误响应

```json
{
  "code": 2034,
  "message": "获取音频时长失败"
}
```

## 使用示例

### cURL 示例

#### 1. 基本获取音频时长

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_audio_duration \
  -H "Content-Type: application/json" \
  -d '{
    "mp3_url": "https://assets.jcaigc.cn/audio/sample.mp3"
  }'
```

## 错误码说明

| 错误码 | 错误信息 | 说明 | 解决方案 |
|--------|----------|------|----------|
| 1001 | 参数校验失败 | `mp3_url` 缺失或不是合法 URL | 提供有效的 `mp3_url` |
| 2004 | 文件大小超出限制 | 音频文件超过服务端下载大小限制 | 使用更小的音频文件 |
| 2005 | 下载文件失败 | 音频文件下载失败 | 检查音频URL是否可公开访问 |
| 2034 | 获取音频时长失败 | 读取音频时长失败 | 检查音频文件格式 |

## 注意事项

1. **时间单位**: 返回的时长使用微秒（1秒 = 1,000,000微秒）
2. **音频格式**: 支持mp3、wav、aac、flac、m4a等常见音频格式
3. **文件大小**: 建议控制在合理范围内，过大的文件可能导致处理超时
4. **网络访问**: 确保提供的音频URL可以正常访问

## 工作流程

1. 验证必填参数（mp3_url）
2. 下载音频文件到临时目录
3. 使用ffprobe分析音频文件获取时长
4. 清理临时文件
5. 返回音频时长信息

## 相关接口

- [添加音频](./add_audios.md)
- [添加视频](./add_videos.md)
- [创建草稿](./create_draft.md)

---

<div align="right">

📚 **项目资源**  
**GitHub**: [https://github.com/Hommy-master/capcut-mate](https://github.com/Hommy-master/capcut-mate)  
**Gitee**: [https://gitee.com/taohongmin-gitee/capcut-mate](https://gitee.com/taohongmin-gitee/capcut-mate)

</div>

<div align="right">

📚 **项目资源**  
**GitHub**: [https://github.com/Hommy-master/capcut-mate](https://github.com/Hommy-master/capcut-mate)  
**Gitee**: [https://gitee.com/taohongmin-gitee/capcut-mate](https://gitee.com/taohongmin-gitee/capcut-mate)

</div>