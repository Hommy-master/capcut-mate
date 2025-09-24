# get_audio_duration 接口文档

## 接口概述

**接口名称**：get_audio_duration  
**接口地址**：`POST /v1/get_audio_duration`  
**功能描述**：获取音频文件的时长，支持各种常见的音频格式。使用FFprobe工具进行精确的音频分析，返回音频文件的准确时长，单位为微秒。

## 请求参数

### 请求体 (application/json)

| 参数名 | 类型 | 必填 | 默认值 | 描述 |
|--------|------|------|--------|------|
| mp3_url | string | 是 | - | 音频文件URL，支持mp3等常见音频格式 |

### 参数说明

- **mp3_url**: 音频文件的完整URL地址
  - 支持格式：mp3、wav、aac、flac等常见音频格式
  - 需要确保URL可访问且文件完整
  - 建议文件大小不超过100MB

## 请求示例

### 获取MP3文件时长

```json
{
  "mp3_url": "https://example.com/audio/sample.mp3"
}
```

### 获取WAV文件时长

```json
{
  "mp3_url": "https://example.com/audio/music.wav"
}
```

## 响应格式

### 成功响应

```json
{
  "duration": 120000000
}
```

### 响应字段说明

| 字段名 | 类型 | 描述 |
|--------|------|------|
| duration | integer | 音频时长，单位：微秒。例如：120000000表示120秒（2分钟） |

### 时长单位转换

- **微秒到秒**：duration ÷ 1,000,000
- **微秒到毫秒**：duration ÷ 1,000
- **示例**：
  - 120000000微秒 = 120秒 = 2分钟
  - 30000000微秒 = 30秒
  - 5000000微秒 = 5秒

### 错误响应

#### 400 Bad Request - 参数验证失败

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "请求参数验证失败",
    "details": "mp3_url 参数不能为空"
  }
}
```

#### 500 Internal Server Error - 获取音频时长失败

```json
{
  "error": {
    "code": "AUDIO_DURATION_GET_FAILED",
    "message": "获取音频时长失败",
    "details": "下载音频文件失败或文件格式不支持"
  }
}
```

## 错误码说明

| 错误码 | HTTP状态码 | 描述 | 解决方案 |
|--------|------------|------|----------|
| VALIDATION_ERROR | 400 | 请求参数验证失败 | 检查mp3_url参数是否正确提供 |
| AUDIO_DURATION_GET_FAILED | 500 | 获取音频时长失败 | 检查音频URL是否可访问，文件格式是否支持 |

## 使用说明

### 参数要求

1. **mp3_url参数**：必填参数，需要提供完整的音频文件URL
2. **文件格式**：虽然参数名为mp3_url，但实际支持多种音频格式
3. **文件大小**：建议控制在合理范围内，过大的文件可能导致处理超时

### 使用场景

1. **视频编辑预处理**：
   - 在添加音频到视频项目前，先获取音频时长
   - 用于计算音频片段的合理切分

2. **音频素材管理**：
   - 批量获取音频库中文件的时长信息
   - 用于音频素材的分类和筛选

3. **同步处理**：
   - 确保音频和视频的时长匹配
   - 计算音频淡入淡出效果的时长

### 技术说明

- **时长计算**：使用FFprobe工具进行精确的音频分析
- **精度**：返回的时长为高精度的实际值，支持小数点后6位精度
- **性能**：接口会下载音频文件进行分析，处理时间取决于文件大小和网络速度

## 示例代码

### JavaScript示例

```javascript
// 获取音频时长
const getAudioDuration = async (audioUrl) => {
  const response = await fetch('/v1/get_audio_duration', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      mp3_url: audioUrl
    })
  });
  
  const result = await response.json();
  
  if (response.ok) {
    const durationSeconds = result.duration / 1000000;
    console.log(`音频时长: ${durationSeconds}秒`);
    return result.duration;
  } else {
    console.error('获取音频时长失败:', result.error);
    throw new Error(result.error.message);
  }
};

// 使用示例
getAudioDuration('https://example.com/audio/sample.mp3')
  .then(duration => {
    console.log(`音频时长（微秒）: ${duration}`);
    console.log(`音频时长（秒）: ${duration / 1000000}`);
  })
  .catch(error => {
    console.error('错误:', error.message);
  });
```

### Python示例

```python
import requests

def get_audio_duration(mp3_url):
    """获取音频文件时长"""
    url = 'http://localhost:8000/v1/get_audio_duration'
    data = {
        'mp3_url': mp3_url
    }
    
    response = requests.post(url, json=data)
    if response.status_code == 200:
        result = response.json()
        duration_microseconds = result['duration']
        duration_seconds = duration_microseconds / 1_000_000
        return duration_microseconds, duration_seconds
    else:
        print(f"请求失败: {response.status_code}")
        print(response.json())
        return None

# 使用示例
audio_url = "https://example.com/audio/sample.mp3"
duration_info = get_audio_duration(audio_url)

if duration_info:
    duration_microseconds, duration_seconds = duration_info
    print(f"音频时长: {duration_seconds:.2f}秒 ({duration_microseconds}微秒)")
    
    # 时长格式化
    minutes = int(duration_seconds // 60)
    seconds = int(duration_seconds % 60)
    print(f"格式化时长: {minutes}分{seconds}秒")
```

### 批量处理示例

```python
import requests
import json
from concurrent.futures import ThreadPoolExecutor
import time

def get_audio_duration_batch(audio_urls):
    """批量获取音频时长"""
    def get_single_duration(url):
        try:
            response = requests.post(
                'http://localhost:8000/v1/get_audio_duration',
                json={'mp3_url': url},
                timeout=30
            )
            if response.status_code == 200:
                duration = response.json()['duration']
                return {'url': url, 'duration': duration, 'success': True}
            else:
                return {'url': url, 'error': response.json(), 'success': False}
        except Exception as e:
            return {'url': url, 'error': str(e), 'success': False}
    
    # 并发处理
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(get_single_duration, audio_urls))
    
    return results

# 使用示例
audio_urls = [
    "https://example.com/audio1.mp3",
    "https://example.com/audio2.wav",
    "https://example.com/audio3.aac"
]

results = get_audio_duration_batch(audio_urls)

for result in results:
    if result['success']:
        duration_seconds = result['duration'] / 1_000_000
        print(f"✓ {result['url']}: {duration_seconds:.2f}秒")
    else:
        print(f"✗ {result['url']}: {result['error']}")
```

## 相关接口

- [add_audios](./add_audios.md) - 批量添加音频到剪映草稿
- [add_videos](./add_videos.md) - 批量添加视频到剪映草稿
- [easy_create_material](./easy_create_material.md) - 快速创建多媒体素材

## 技术实现

### 文件结构

```
src/
├── schemas/get_audio_duration.py    # 请求/响应数据模型
├── service/get_audio_duration.py    # 业务逻辑实现
└── router/v1.py                     # API路由定义
```

### 核心逻辑

1. **参数验证**：验证mp3_url参数的有效性
2. **文件下载**：从URL下载音频文件到临时目录
3. **FFprobe分析**：使用FFprobe工具获取精确的音频元数据
4. **时长提取**：从格式信息或流信息中提取时长数据
5. **资源清理**：清理临时下载的文件
6. **响应返回**：返回符合规范的API响应

### 当前实现特点

- 使用FFmpeg项目的FFprobe工具进行音频分析
- 支持多种音频格式（MP3、WAV、AAC、FLAC等）
- 提供高精度的时长数据（微秒级别）
- 完善的错误处理和资源清理机制
- 支持超时控制，防止长时间阻塞

### 优势说明

相比于之前基于文件大小的估算方法，新的FFprobe实现提供了：
- **更高的精度**：直接从音频元数据中读取时长
- **更广泛的支持**：支持所有FFprobe可识别的音频格式
- **更可靠的结果**：不依赖于比特率估算，直接读取实际数据

---

**版本信息**：v1.0  
**最后更新**：2024-09-24