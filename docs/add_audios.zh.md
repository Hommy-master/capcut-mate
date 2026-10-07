# ADD_AUDIOS API 接口文档

## 🌐 语言切换
[中文版](./add_audios.zh.md) | [English](./add_audios.md)

## 接口信息

```
POST /openapi/capcut-mate/v1/add_audios
```

## 功能描述

批量向现有草稿中添加音频素材。该接口支持添加多个音频文件到剪映草稿，为视频创建背景音乐、音效、旁白等音频内容。音频将被添加到独立的音频轨道中，不会影响视频内容。

## 更多文档

📖 更多详细文档和教程请访问：[https://docs.jcaigc.cn](https://docs.jcaigc.cn)

## 请求参数

```json
{
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
  "audio_infos": "[{\"audio_url\":\"https://assets.jcaigc.cn/audio1.mp3\",\"start\":0,\"end\":5000000,\"duration\":10000000,\"volume\":1.0,\"audio_effect\":\"reverb\"}]"
}
```

### 参数说明

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| draft_url | string | ✅ | - | 目标草稿的完整URL |
| audio_infos | string | ✅ | - | 音频信息数组的JSON字符串 |

### audio_infos 数组结构

audio_infos是一个JSON字符串，解析后为数组，每个元素包含以下字段：

| 字段名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| audio_url | string | ✅ | - | 音频文件的URL地址 |
| start | number | ✅ | - | 音频开始播放时间(微秒) |
| end | number | ✅ | - | 音频结束播放时间(微秒) |
| duration | number | ❌ | 自动获取 | 音频总时长(微秒)，如果不提供将自动获取 |
| volume | number | ❌ | 1.0 | 音量大小(0.0-2.0) |
| audio_effect | string | ❌ | None | 音频效果名称 |

### 参数详解

#### 时间参数

- **start**: 音频在时间轴上的开始时间，单位为微秒（1秒 = 1,000,000微秒）
- **end**: 音频在时间轴上的结束时间，单位为微秒
- **duration**: 音频文件的总时长，用于素材创建，单位为微秒，如果不提供将自动获取
- **播放时长**: 实际播放时长 = end - start

#### 音量控制

- **volume**: 音频音量大小
  - 1.0 = 原始音量
  - 0.5 = 一半音量
  - 0.0 = 静音
  - 范围：0.0 - 2.0

#### 音频效果

- **audio_effect**: 音频效果名称
  - None = 无音频效果
  - 示例：`"reverb"`（混响效果）

## 响应格式

### 成功响应 (200)

```json
{
  "code": 0,
  "message": "success",
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
  "track_id": "audio-track-uuid",
  "audio_ids": ["audio1-uuid", "audio2-uuid", "audio3-uuid"]
}
```

### 响应字段说明

| 字段名 | 类型 | 说明 |
|--------|------|------|
| draft_url | string | 更新后的草稿URL |
| track_id | string | 音频轨道ID |
| audio_ids | array | 添加的音频ID列表 |

### 错误响应

```json
{
  "code": 2007,
  "message": "无效的音频信息，请检查audio_infos字段值是否正确"
}
```

## 使用示例

### cURL 示例

#### 1. 基本音频添加

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_audios \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "audio_infos": "[{\"audio_url\":\"https://assets.jcaigc.cn/bgm.mp3\",\"start\":0,\"end\":10000000,\"duration\":15000000,\"volume\":0.8}]"
  }'
```

#### 2. 多音频批量添加

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_audios \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "audio_infos": "[{\"audio_url\":\"https://assets.jcaigc.cn/intro.mp3\",\"start\":0,\"end\":3000000,\"duration\":5000000,\"volume\":1.0},{\"audio_url\":\"https://assets.jcaigc.cn/bgm.mp3\",\"start\":3000000,\"end\":30000000,\"duration\":35000000,\"volume\":0.6}]"
  }'
```

#### 3. 带淡入淡出效果的音频

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_audios \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "audio_infos": "[{\"audio_url\":\"https://assets.jcaigc.cn/outro.mp3\",\"start\":25000000,\"end\":30000000,\"duration\":8000000,\"volume\":0.9,\"audio_effect\":\"reverb\"}]"
  }'
```

## 错误码说明

| 错误码 | 错误信息 | 说明 | 解决方案 |
|--------|----------|------|----------|
| 1001 | 参数校验失败 | 请求体未通过字段校验，如 `audio_infos` 不是合法 JSON、不是数组，或 `audio_url` 未以 `http://` / `https://` 开头 | 检查参数类型与必填字段 |
| 2001 | 无效的草稿URL | `draft_url` 缺失、格式错误，或草稿不在缓存中 | 传入 `create_draft` 返回的 `draft_url` |
| 2005 | 下载文件失败 | 无法从 `audio_url` 下载音频文件 | 检查音频 URL 是否可公开访问 |
| 2007 | 无效的音频信息 | `audio_infos` 不是合法 JSON、某项缺少 `audio_url`/`start`/`end`、`start` 为负、`end` 不大于 `start`，或 `duration` 不为正数 | 修正 JSON 字符串与必填字段 |
| 2008 | 音频添加失败 | 添加音频片段或保存草稿时出错 | 检查草稿状态后重试 |
| 2042 | 草稿锁获取超时 | 同一时间只允许一个操作，草稿正被占用 | 稍后重试 |

## 注意事项

1. **JSON格式**: audio_infos必须是合法的JSON字符串
2. **时间单位**: 所有时间参数使用微秒（1秒 = 1,000,000微秒）
3. **音频格式**: 确保音频文件格式被支持（如MP3、WAV、AAC等）
4. **文件大小**: 大音频文件可能影响处理速度
5. **网络访问**: 音频URL必须可以正常访问
6. **音量范围**: 音量值必须在0.0-2.0范围内
7. **轨道限制**: 同一时间段可能存在音频重叠

## 工作流程

1. 验证必填参数（draft_url, audio_infos）
2. 解析audio_infos JSON字符串
3. 验证每个音频的参数配置
4. 获取并解密草稿内容
5. 创建音频轨道
6. 添加音频片段到轨道
7. 应用音量和音频效果
8. 保存并加密草稿
9. 返回处理结果

## 相关接口

- [创建草稿](./create_draft.md)
- [添加视频](./add_videos.md)
- [添加图片](./add_images.md)
- [保存草稿](./save_draft.md)
- [生成视频](./gen_video.md)

---

<div align="right">

📚 **项目资源**  
**GitHub**: [https://github.com/Hommy-master/capcut-mate](https://github.com/Hommy-master/capcut-mate)  
**Gitee**: [https://gitee.com/taohongmin-gitee/capcut-mate](https://gitee.com/taohongmin-gitee/capcut-mate)

</div>

### 语言切换
[中文版](./add_audios.zh.md) | [English](./add_audios.md)