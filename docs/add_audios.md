# ADD_AUDIOS API 接口文档

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
  "audio_infos": "[{\"audio_url\":\"https://assets.jcaigc.cn/audio1.mp3\",\"start\":0,\"end\":5000000,\"duration\":10000000,\"volume\":0.8,\"fade_in\":1000000,\"fade_out\":1000000}]"
}
```

### 主要参数

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
| duration | number | ✅ | - | 音频总时长(微秒) |
| volume | number | ❌ | 1.0 | 音量大小(0-1) |
| fade_in | number | ❌ | 0 | 淡入时长(微秒) |
| fade_out | number | ❌ | 0 | 淡出时长(微秒) |

### 参数详解

#### 时间参数

- **start**: 音频在时间轴上的开始时间，单位为微秒（1秒 = 1,000,000微秒）
- **end**: 音频在时间轴上的结束时间，单位为微秒
- **duration**: 音频文件的总时长，用于素材创建，单位为微秒
- **播放时长**: 实际播放时长 = end - start

#### 音量控制

- **volume**: 音频音量大小
  - 1.0 = 原始音量
  - 0.5 = 一半音量
  - 0.0 = 静音
  - 范围：0.0 - 1.0

#### 淡入淡出效果

- **fade_in**: 淡入效果时长
  - 0 = 无淡入效果
  - 建议范围：500,000 - 3,000,000微秒（0.5-3秒）
  
- **fade_out**: 淡出效果时长
  - 0 = 无淡出效果
  - 建议范围：500,000 - 3,000,000微秒（0.5-3秒）

## 响应格式

### 成功响应 (200)

```json
{
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

### 错误响应 (4xx/5xx)

```json
{
  "detail": "错误信息描述"
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
    "audio_infos": "[{\"audio_url\":\"https://assets.jcaigc.cn/intro.mp3\",\"start\":0,\"end\":3000000,\"duration\":5000000,\"volume\":1.0,\"fade_in\":500000},{\"audio_url\":\"https://assets.jcaigc.cn/bgm.mp3\",\"start\":3000000,\"end\":30000000,\"duration\":35000000,\"volume\":0.6}]"
  }'
```

#### 3. 带淡入淡出效果的音频

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_audios \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "audio_infos": "[{\"audio_url\":\"https://assets.jcaigc.cn/outro.mp3\",\"start\":25000000,\"end\":30000000,\"duration\":8000000,\"volume\":0.9,\"fade_in\":1000000,\"fade_out\":2000000}]"
  }'
```

### JavaScript 示例

```javascript
const addAudios = async (draftUrl, audioConfig) => {
  const response = await fetch('/openapi/capcut-mate/v1/add_audios', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      draft_url: draftUrl,
      ...audioConfig
    })
  });
  return response.json();
};

// 基本音频添加
const basicAudio = {
  audio_infos: JSON.stringify([
    {
      audio_url: "https://assets.jcaigc.cn/bgm.mp3",
      start: 0,
      end: 10000000,
      duration: 15000000,
      volume: 0.8
    }
  ])
};

// 音频序列
const audioSequence = {
  audio_infos: JSON.stringify([
    {
      audio_url: "https://assets.jcaigc.cn/intro.mp3",
      start: 0,
      end: 3000000,
      duration: 5000000,
      volume: 1.0,
      fade_in: 500000
    },
    {
      audio_url: "https://assets.jcaigc.cn/main-bgm.mp3",
      start: 2000000,
      end: 25000000,
      duration: 30000000,
      volume: 0.6
    },
    {
      audio_url: "https://assets.jcaigc.cn/outro.mp3",
      start: 24000000,
      end: 28000000,
      duration: 6000000,
      volume: 0.9,
      fade_out: 1500000
    }
  ])
};

// 音效组合
const soundEffects = {
  audio_infos: JSON.stringify([
    {
      audio_url: "https://assets.jcaigc.cn/applause.mp3",
      start: 5000000,
      end: 8000000,
      duration: 4000000,
      volume: 0.7
    },
    {
      audio_url: "https://assets.jcaigc.cn/transition.mp3",
      start: 12000000,
      end: 13500000,
      duration: 2000000,
      volume: 0.5
    }
  ])
};

try {
  const result1 = await addAudios(draftUrl, basicAudio);
  const result2 = await addAudios(draftUrl, audioSequence);
  const result3 = await addAudios(draftUrl, soundEffects);
  
  console.log('音频添加成功:', {
    basic: result1,
    sequence: result2,
    effects: result3
  });
} catch (error) {
  console.error('添加失败:', error);
}
```

### 高级JavaScript示例

```javascript
class AudioManager {
  constructor(baseUrl = 'https://capcut-mate.jcaigc.cn') {
    this.baseUrl = baseUrl;
  }

  async addAudios(draftUrl, audioConfig) {
    const response = await fetch(`${this.baseUrl}/openapi/capcut-mate/v1/add_audios`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        draft_url: draftUrl,
        ...audioConfig
      })
    });
    return response.json();
  }

  // 创建背景音乐
  createBackgroundMusic(audioUrl, totalDuration, volume = 0.6, loop = false) {
    const audios = [];
    
    if (loop) {
      // 循环播放逻辑
      let currentTime = 0;
      while (currentTime < totalDuration) {
        audios.push({
          audio_url: audioUrl,
          start: currentTime,
          end: Math.min(currentTime + 30000000, totalDuration), // 假设30秒循环
          duration: 30000000,
          volume: volume
        });
        currentTime += 30000000;
      }
    } else {
      audios.push({
        audio_url: audioUrl,
        start: 0,
        end: totalDuration,
        duration: totalDuration,
        volume: volume
      });
    }

    return {
      audio_infos: JSON.stringify(audios)
    };
  }

  // 创建音频序列
  createAudioSequence(audioList, crossFadeDuration = 1000000) {
    const audios = [];
    let currentTime = 0;

    audioList.forEach((audio, index) => {
      const audioInfo = {
        audio_url: audio.url,
        start: currentTime,
        end: currentTime + audio.playDuration,
        duration: audio.totalDuration,
        volume: audio.volume || 1.0
      };

      // 添加交叉淡入淡出
      if (index > 0) {
        audioInfo.fade_in = crossFadeDuration;
        // 调整前一个音频的淡出
        if (audios[index - 1]) {
          audios[index - 1].fade_out = crossFadeDuration;
        }
      }

      // 最后一个音频淡出
      if (index === audioList.length - 1) {
        audioInfo.fade_out = audio.fadeOut || crossFadeDuration;
      }

      audios.push(audioInfo);
      currentTime += audio.playDuration - (index > 0 ? crossFadeDuration : 0);
    });

    return {
      audio_infos: JSON.stringify(audios)
    };
  }

  // 创建音效轨道
  createSoundEffects(effects) {
    const audios = effects.map(effect => ({
      audio_url: effect.url,
      start: effect.startTime,
      end: effect.startTime + effect.duration,
      duration: effect.duration,
      volume: effect.volume || 0.7,
      fade_in: effect.fadeIn || 0,
      fade_out: effect.fadeOut || 0
    }));

    return {
      audio_infos: JSON.stringify(audios)
    };
  }

  // 创建旁白音频
  createNarration(narrationList) {
    const audios = narrationList.map(narration => ({
      audio_url: narration.url,
      start: narration.startTime,
      end: narration.startTime + narration.duration,
      duration: narration.duration,
      volume: narration.volume || 0.9,
      fade_in: 200000, // 0.2秒淡入
      fade_out: 200000  // 0.2秒淡出
    }));

    return {
      audio_infos: JSON.stringify(audios)
    };
  }

  // 批量处理音频
  async batchProcessAudios(draftUrl, audioConfigs) {
    const results = [];
    
    for (const config of audioConfigs) {
      try {
        const result = await this.addAudios(draftUrl, config);
        results.push(result);
        
        // 添加延迟避免请求过快
        await new Promise(resolve => setTimeout(resolve, 100));
      } catch (error) {
        console.error('音频处理失败:', error);
        results.push({ error: error.message });
      }
    }
    
    return results;
  }
}

// 使用示例
const audioManager = new AudioManager();

// 创建背景音乐
const bgm = audioManager.createBackgroundMusic(
  "https://assets.jcaigc.cn/bgm.mp3", 
  60000000, // 60秒
  0.6, 
  true // 循环播放
);

// 创建音频序列
const sequence = audioManager.createAudioSequence([
  {
    url: "https://assets.jcaigc.cn/intro.mp3",
    playDuration: 5000000,
    totalDuration: 5000000,
    volume: 1.0
  },
  {
    url: "https://assets.jcaigc.cn/main.mp3",
    playDuration: 20000000,
    totalDuration: 25000000,
    volume: 0.8
  },
  {
    url: "https://assets.jcaigc.cn/outro.mp3",
    playDuration: 3000000,
    totalDuration: 3000000,
    volume: 1.0,
    fadeOut: 2000000
  }
]);

// 创建音效
const effects = audioManager.createSoundEffects([
  {
    url: "https://assets.jcaigc.cn/whoosh.mp3",
    startTime: 10000000,
    duration: 1500000,
    volume: 0.5
  },
  {
    url: "https://assets.jcaigc.cn/ding.mp3",
    startTime: 25000000,
    duration: 1000000,
    volume: 0.8
  }
]);

// 批量处理
await audioManager.batchProcessAudios(draftUrl, [bgm, sequence, effects]);
```

### Python 示例

```python
import requests
import json
from typing import List, Dict, Optional

class AudioProcessor:
    def __init__(self, base_url="https://capcut-mate.jcaigc.cn"):
        self.base_url = base_url

    def add_audios(self, draft_url: str, audio_config: Dict) -> Dict:
        response = requests.post(
            f'{self.base_url}/openapi/capcut-mate/v1/add_audios',
            headers={'Content-Type': 'application/json'},
            json={
                "draft_url": draft_url,
                **audio_config
            }
        )
        return response.json()

    def create_background_music(self, audio_url: str, total_duration: int, 
                              volume: float = 0.6, loop: bool = False) -> Dict:
        """创建背景音乐"""
        audios = []
        
        if loop:
            current_time = 0
            audio_duration = 30000000  # 假设30秒循环
            
            while current_time < total_duration:
                end_time = min(current_time + audio_duration, total_duration)
                audios.append({
                    "audio_url": audio_url,
                    "start": current_time,
                    "end": end_time,
                    "duration": audio_duration,
                    "volume": volume
                })
                current_time += audio_duration
        else:
            audios.append({
                "audio_url": audio_url,
                "start": 0,
                "end": total_duration,
                "duration": total_duration,
                "volume": volume
            })
        
        return {"audio_infos": json.dumps(audios)}

    def create_audio_sequence(self, audio_list: List[Dict], 
                            cross_fade_duration: int = 1000000) -> Dict:
        """创建音频序列"""
        audios = []
        current_time = 0
        
        for i, audio in enumerate(audio_list):
            audio_info = {
                "audio_url": audio["url"],
                "start": current_time,
                "end": current_time + audio["play_duration"],
                "duration": audio["total_duration"],
                "volume": audio.get("volume", 1.0)
            }
            
            # 添加交叉淡入淡出
            if i > 0:
                audio_info["fade_in"] = cross_fade_duration
                if audios:
                    audios[-1]["fade_out"] = cross_fade_duration
            
            # 最后一个音频淡出
            if i == len(audio_list) - 1:
                audio_info["fade_out"] = audio.get("fade_out", cross_fade_duration)
            
            audios.append(audio_info)
            current_time += audio["play_duration"] - (cross_fade_duration if i > 0 else 0)
        
        return {"audio_infos": json.dumps(audios)}

    def create_sound_effects(self, effects: List[Dict]) -> Dict:
        """创建音效轨道"""
        audios = []
        
        for effect in effects:
            audios.append({
                "audio_url": effect["url"],
                "start": effect["start_time"],
                "end": effect["start_time"] + effect["duration"],
                "duration": effect["duration"],
                "volume": effect.get("volume", 0.7),
                "fade_in": effect.get("fade_in", 0),
                "fade_out": effect.get("fade_out", 0)
            })
        
        return {"audio_infos": json.dumps(audios)}

# 使用示例
processor = AudioProcessor()

# 背景音乐
bgm_config = processor.create_background_music(
    "https://assets.jcaigc.cn/bgm.mp3",
    60000000,  # 60秒
    volume=0.6,
    loop=True
)

# 音频序列
sequence_config = processor.create_audio_sequence([
    {
        "url": "https://assets.jcaigc.cn/intro.mp3",
        "play_duration": 5000000,
        "total_duration": 5000000,
        "volume": 1.0
    },
    {
        "url": "https://assets.jcaigc.cn/main.mp3",
        "play_duration": 20000000,
        "total_duration": 25000000,
        "volume": 0.8
    }
])

# 音效
effects_config = processor.create_sound_effects([
    {
        "url": "https://assets.jcaigc.cn/whoosh.mp3",
        "start_time": 10000000,
        "duration": 1500000,
        "volume": 0.5
    }
])

# 添加到草稿
draft_url = "YOUR_DRAFT_URL"
results = []

for config in [bgm_config, sequence_config, effects_config]:
    result = processor.add_audios(draft_url, config)
    results.append(result)
    print(f"音频添加成功: {result['track_id']}")
```

## 错误码说明

| 错误码 | 错误信息 | 说明 | 解决方案 |
|--------|----------|------|----------|
| 400 | draft_url是必填项 | 缺少草稿URL参数 | 提供有效的草稿URL |
| 400 | audio_infos是必填项 | 缺少音频信息参数 | 提供有效的音频信息JSON |
| 400 | audio_infos格式错误 | JSON格式不正确 | 检查JSON字符串格式 |
| 400 | 音频配置验证失败 | 音频参数不符合要求 | 检查每个音频的参数 |
| 400 | audio_url是必填项 | 音频URL缺失 | 为每个音频提供URL |
| 400 | 时间范围无效 | end必须大于start | 确保结束时间大于开始时间 |
| 400 | 音量值无效 | volume不在0-1范围内 | 使用0-1之间的音量值 |
| 404 | 草稿不存在 | 指定的草稿URL无效 | 检查草稿URL是否正确 |
| 404 | 音频资源不存在 | 音频URL无法访问 | 检查音频URL是否可访问 |
| 500 | 音频处理失败 | 内部处理错误 | 联系技术支持 |

## 注意事项

1. **JSON格式**: audio_infos必须是合法的JSON字符串
2. **时间单位**: 所有时间参数使用微秒（1秒 = 1,000,000微秒）
3. **音频格式**: 确保音频文件格式被支持（如MP3、WAV、AAC等）
4. **文件大小**: 大音频文件可能影响处理速度
5. **网络访问**: 音频URL必须可以正常访问
6. **音量范围**: 音量值必须在0.0-1.0范围内
7. **淡入淡出**: 淡入淡出时长不能超过音频播放时长
8. **轨道限制**: 同一时间段可能存在音频重叠

## 工作流程

1. 验证必填参数（draft_url, audio_infos）
2. 解析audio_infos JSON字符串
3. 验证每个音频的参数配置
4. 获取并解密草稿内容
5. 创建音频轨道
6. 添加音频片段到轨道
7. 应用音量和淡入淡出效果
8. 保存并加密草稿
9. 返回处理结果

## 相关接口

- [创建草稿](./create_draft.md)
- [添加视频](./add_videos.md)
- [添加图片](./add_images.md)
- [保存草稿](./save_draft.md)
- [生成视频](./gen_video.md)