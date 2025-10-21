# add_audio 接口文档

## 接口概述

添加音频到剪映草稿中，支持音频裁剪、音量调节、变速、音效等功能。

---

## 接口信息

### RESTful API 端点

```
POST /add_audio
```

### Content-Type

```
application/json
```

---

## 请求参数

### 请求体 (JSON)

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| **audio_url** | string | **是** | - | 音频文件的 URL 地址（必需参数） |
| draft_folder | string | 否 | null | 草稿文件夹路径 |
| draft_id | string | 否 | null | 草稿 ID，不提供则创建新草稿 |
| width | integer | 否 | 1080 | 画布宽度（像素） |
| height | integer | 否 | 1920 | 画布高度（像素） |
| start | number | 否 | 0 | 音频起始时间（秒） |
| end | number | 否 | null | 音频结束时间（秒），null 表示到音频末尾 |
| target_start | number | 否 | 0 | 音频在时间轴上的起始位置（秒） |
| duration | number | 否 | null | 音频显示时长（秒） |

### 播放控制参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| volume | number | 否 | 1.0 | 音量大小，范围 0.0 到 1.0 |
| speed | number | 否 | 1.0 | 播放速度，1.0 为正常速度 |

### 轨道参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| track_name | string | 否 | "audio_main" | 音频轨道名称 |

### 音效参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| effect_type | string | 否 | null | 音效类型名称 |
| effect_params | array | 否 | null | 音效参数列表 |

---

## 响应参数

### 响应体 (JSON)

| 参数名 | 类型 | 说明 |
|--------|------|------|
| success | boolean | 请求是否成功 |
| output | object/string | 成功时返回草稿结果信息 |
| error | string | 失败时的错误信息 |

### 成功响应的 output 字段

| 参数名 | 类型 | 说明 |
|--------|------|------|
| draft_id | string | 草稿唯一标识符 |
| draft_url | string | 草稿预览 URL |

---

## 请求示例

### 示例 1: 基础音频添加

```bash
curl -X POST http://localhost:9001/add_audio \
  -H "Content-Type: application/json" \
  -d '{
    "audio_url": "https://example.com/music.mp3"
  }'
```

**请求体 (JSON):**

```json
{
  "audio_url": "https://example.com/music.mp3"
}
```

### 示例 2: 添加背景音乐（降低音量）

```bash
curl -X POST http://localhost:9001/add_audio \
  -H "Content-Type: application/json" \
  -d '{
    "audio_url": "https://example.com/bgm.mp3",
    "draft_id": "dfd_12345",
    "start": 0,
    "end": 30,
    "volume": 0.3,
    "track_name": "audio_bgm"
  }'
```

**请求体 (JSON):**

```json
{
  "audio_url": "https://example.com/bgm.mp3",
  "draft_id": "dfd_12345",
  "start": 0,
  "end": 30,
  "volume": 0.3,
  "track_name": "audio_bgm"
}
```

### 示例 3: 添加音效并加速

```bash
curl -X POST http://localhost:9001/add_audio \
  -H "Content-Type: application/json" \
  -d '{
    "audio_url": "https://example.com/sound_effect.wav",
    "draft_id": "dfd_12345",
    "target_start": 5.0,
    "duration": 2.0,
    "speed": 1.5,
    "volume": 0.8,
    "track_name": "audio_sfx"
  }'
```

**请求体 (JSON):**

```json
{
  "audio_url": "https://example.com/sound_effect.wav",
  "draft_id": "dfd_12345",
  "target_start": 5.0,
  "duration": 2.0,
  "speed": 1.5,
  "volume": 0.8,
  "track_name": "audio_sfx"
}
```

### 示例 4: 添加带音效的音频

```bash
curl -X POST http://localhost:9001/add_audio \
  -H "Content-Type: application/json" \
  -d '{
    "audio_url": "https://example.com/voice.mp3",
    "draft_id": "dfd_12345",
    "effect_type": "reverb",
    "effect_params": [0.5, 0.3],
    "volume": 1.0
  }'
```

**请求体 (JSON):**

```json
{
  "audio_url": "https://example.com/voice.mp3",
  "draft_id": "dfd_12345",
  "effect_type": "reverb",
  "effect_params": [0.5, 0.3],
  "volume": 1.0
}
```

### 示例 5: Python 请求示例

```python
import requests

url = "http://localhost:9001/add_audio"
headers = {
    "Content-Type": "application/json"
}
data = {
    "audio_url": "https://example.com/music.mp3",
    "draft_id": "dfd_abc123",
    "start": 10,
    "end": 40,
    "target_start": 0,
    "volume": 0.5,
    "speed": 1.0,
    "track_name": "audio_main"
}

response = requests.post(url, json=data, headers=headers)
result = response.json()

print(f"Success: {result['success']}")
if result['success']:
    print(f"Draft ID: {result['output']['draft_id']}")
    print(f"Draft URL: {result['output']['draft_url']}")
else:
    print(f"Error: {result['error']}")
```

---

## 响应示例

### 成功响应

**状态码:** 200 OK

```json
{
  "success": true,
  "output": {
    "draft_id": "dfd_1234567890abcdef",
    "draft_url": "http://example.com/preview?draft_id=dfd_1234567890abcdef"
  },
  "error": ""
}
```

### 失败响应 - 缺少必需参数

**状态码:** 200 OK

```json
{
  "success": false,
  "output": "",
  "error": "Hi, the required parameters 'audio_url' are missing."
}
```

### 失败响应 - 处理错误

**状态码:** 200 OK

```json
{
  "success": false,
  "output": "",
  "error": "Error occurred while processing audio: Invalid audio format."
}
```

---

## 错误码说明

| 错误信息 | 说明 | 解决方案 |
|---------|------|---------|
| "Hi, the required parameters 'audio_url' are missing." | 缺少必需的 audio_url 参数 | 请在请求体中提供 audio_url 参数 |
| "Error occurred while processing audio: ..." | 音频处理过程中出错 | 检查音频 URL 是否有效，格式是否支持 |

---

## 使用场景

### 场景 1: 添加背景音乐

```json
{
  "audio_url": "https://example.com/bgm.mp3",
  "volume": 0.2,
  "track_name": "audio_bgm"
}
```

### 场景 2: 添加配音

```json
{
  "audio_url": "https://example.com/voiceover.mp3",
  "target_start": 2.0,
  "duration": 15.0,
  "volume": 1.0,
  "track_name": "audio_voice"
}
```

### 场景 3: 添加音效

```json
{
  "audio_url": "https://example.com/swoosh.wav",
  "target_start": 5.5,
  "duration": 0.5,
  "volume": 0.8,
  "track_name": "audio_sfx"
}
```

### 场景 4: 音频循环

```json
{
  "audio_url": "https://example.com/loop.mp3",
  "start": 0,
  "end": 10,
  "volume": 0.4,
  "speed": 1.0
}
```

### 场景 5: 音频变速（慢放）

```json
{
  "audio_url": "https://example.com/speech.mp3",
  "speed": 0.75,
  "volume": 1.0
}
```

---

## 音频格式支持

| 格式 | 扩展名 | 说明 |
|------|--------|------|
| MP3 | .mp3 | 最常用，兼容性好 |
| WAV | .wav | 无损音质，文件较大 |
| AAC | .aac, .m4a | 高质量压缩格式 |
| OGG | .ogg | 开源格式 |
| FLAC | .flac | 无损压缩 |

---

## 注意事项

1. **必需参数**: `audio_url` 是唯一的必需参数
2. **时间参数**: `start` 和 `end` 的单位都是秒，支持小数
3. **音量范围**: volume 的有效范围是 0.0（静音）到 1.0（原始音量）
4. **速度调节**: speed 可以大于 1（加速）或小于 1（减速），建议范围 0.5-2.0
5. **音频格式**: 支持常见音频格式（MP3, WAV, AAC 等）
6. **URL 要求**: audio_url 必须是可访问的完整 URL
7. **多轨道**: 可以通过不同的 track_name 添加多个音频轨道
8. **时长优先级**: 如果同时提供 `end` 和 `duration`，`duration` 优先级更高

---

## 音效类型

可通过 `/get_audio_effect_types` 接口获取支持的音效类型：

- **Tone effects**: 变调效果（如低音、高音）
- **Scene effects**: 场景效果（如回声、混响）
- **Speech to song**: 语音转唱歌

---

## 相关接口

- `POST /create_draft` - 创建新草稿
- `POST /save_draft` - 保存草稿
- `GET /get_audio_effect_types` - 获取可用音效类型
- `POST /add_video` - 添加视频
- `POST /add_text` - 添加文字

---

## 更新日志

| 版本 | 日期 | 说明 |
|------|------|------|
| 1.0 | 2025-10-21 | 初始版本 |

---

## 技术支持

如有问题，请联系：
- Email: sguann2023@gmail.com
- GitHub Issues: https://github.com/sun-guannan/CapCutAPI/issues
