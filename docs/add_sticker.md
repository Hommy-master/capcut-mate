# ADD_STICKER API 接口文档

## 接口信息

```
POST /v1/add_sticker
```

## 功能描述

向现有草稿中添加贴纸。该接口用于在指定的时间段内添加贴纸素材到剪映草稿中，支持贴纸的缩放和位置调整。贴纸可以用于增强视频的视觉效果，如表情、装饰、文字等。

## 请求参数

```json
{
  "draft_url": "https://ts.fyshark.com/#/cozeToJianyin?drafId=https://video-snot-12220.oss-cn-shanghai.aliyuncs.com/2025-05-28/draft/2f52a63b-8c6a-4417-8b01-1b2a569ccb6c.json",
  "sticker_id": "7326810673609018675",
  "start": 0,
  "end": 5000000,
  "scale": 1.0,
  "transform_x": 0,
  "transform_y": 0
}
```

### 参数说明

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| draft_url | string | ✅ | - | 目标草稿的完整URL |
| sticker_id | string | ✅ | - | 贴纸的唯一标识ID |
| start | number | ✅ | - | 贴纸开始时间（微秒） |
| end | number | ✅ | - | 贴纸结束时间（微秒） |
| scale | number | ❌ | 1.0 | 贴纸缩放比例，建议范围[0.1, 5.0] |
| transform_x | number | ❌ | 0 | X轴位置偏移（像素） |
| transform_y | number | ❌ | 0 | Y轴位置偏移（像素） |

### 参数详解

#### 时间参数

- **start**: 贴纸在时间轴上的开始时间，单位为微秒（1秒 = 1,000,000微秒）
- **end**: 贴纸在时间轴上的结束时间，单位为微秒
- **duration**: 贴纸显示时长 = end - start

#### 缩放参数

- **scale**: 贴纸的缩放比例
  - 1.0 = 原始大小
  - 0.5 = 缩小到一半
  - 2.0 = 放大到两倍
  - 建议范围：0.1 - 5.0

#### 位置参数

- **transform_x**: 贴纸在X轴方向的位置偏移，单位为像素
  - 正值向右移动
  - 负值向左移动
  - 以画布中心为原点

- **transform_y**: 贴纸在Y轴方向的位置偏移，单位为像素
  - 正值向下移动
  - 负值向上移动
  - 以画布中心为原点

#### 贴纸ID说明

- **sticker_id**: 贴纸的唯一标识符
  - 格式：通常为数字字符串
  - 示例：`"7326810673609018675"`
  - 获取方式：通过剪映贴纸库或相关API获取

## 响应格式

### 成功响应 (200)

```json
{
  "draft_url": "https://ts.fyshark.com/#/cozeToJianyin?drafId=...",
  "sticker_id": "7326810673609018675",
  "track_id": "track-uuid",
  "segment_id": "segment-uuid",
  "duration": 5000000
}
```

### 响应字段说明

| 字段名 | 类型 | 说明 |
|--------|------|------|
| draft_url | string | 更新后的草稿URL |
| sticker_id | string | 贴纸的唯一标识ID |
| track_id | string | 贴纸轨道ID |
| segment_id | string | 贴纸片段ID |
| duration | number | 贴纸显示时长（微秒） |

### 错误响应 (4xx/5xx)

```json
{
  "detail": "错误信息描述"
}
```

## 使用示例

### cURL 示例

#### 1. 基本贴纸添加

```bash
curl -X POST https://api.example.com/v1/add_sticker \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "sticker_id": "7326810673609018675",
    "start": 0,
    "end": 5000000
  }'
```

#### 2. 带缩放的贴纸

```bash
curl -X POST https://api.example.com/v1/add_sticker \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "sticker_id": "7326810673609018675",
    "start": 1000000,
    "end": 6000000,
    "scale": 1.5
  }'
```

#### 3. 带位置偏移的贴纸

```bash
curl -X POST https://api.example.com/v1/add_sticker \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "sticker_id": "7326810673609018675",
    "start": 2000000,
    "end": 7000000,
    "scale": 0.8,
    "transform_x": 200,
    "transform_y": -100
  }'
```

### JavaScript 示例

```javascript
const addSticker = async (draftUrl, stickerConfig) => {
  const response = await fetch('/v1/add_sticker', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      draft_url: draftUrl,
      ...stickerConfig
    })
  });
  return response.json();
};

// 基本贴纸添加
const basicSticker = {
  sticker_id: "7326810673609018675",
  start: 0,
  end: 5000000
};

// 自定义大小和位置的贴纸
const customSticker = {
  sticker_id: "7326810673609018675",
  start: 3000000,
  end: 8000000,
  scale: 1.2,
  transform_x: 150,
  transform_y: -50
};

// 小尺寸装饰贴纸
const decorationSticker = {
  sticker_id: "7326810673609018675",
  start: 10000000,
  end: 15000000,
  scale: 0.6,
  transform_x: -200,
  transform_y: 200
};

try {
  const result1 = await addSticker(draftUrl, basicSticker);
  const result2 = await addSticker(draftUrl, customSticker);
  const result3 = await addSticker(draftUrl, decorationSticker);
  
  console.log('贴纸添加成功:', {
    basic: result1,
    custom: result2,
    decoration: result3
  });
} catch (error) {
  console.error('添加失败:', error);
}
```

### 高级JavaScript示例

```javascript
class StickerManager {
  constructor(baseUrl = 'https://api.example.com') {
    this.baseUrl = baseUrl;
  }

  async addSticker(draftUrl, stickerConfig) {
    const response = await fetch(`${this.baseUrl}/v1/add_sticker`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        draft_url: draftUrl,
        ...stickerConfig
      })
    });
    
    if (!response.ok) {
      throw new Error(`贴纸添加失败: ${response.statusText}`);
    }
    
    return response.json();
  }

  // 创建贴纸序列
  createStickerSequence(stickers, intervalDuration = 1000000) {
    return stickers.map((sticker, index) => ({
      sticker_id: sticker.id,
      start: index * intervalDuration,
      end: (index + 1) * intervalDuration,
      scale: sticker.scale || 1.0,
      transform_x: sticker.x || 0,
      transform_y: sticker.y || 0
    }));
  }

  // 创建动画贴纸效果
  createAnimatedSticker(stickerId, startTime, duration, keyframes) {
    const configs = [];
    const segmentDuration = duration / keyframes.length;
    
    keyframes.forEach((keyframe, index) => {
      configs.push({
        sticker_id: stickerId,
        start: startTime + (index * segmentDuration),
        end: startTime + ((index + 1) * segmentDuration),
        scale: keyframe.scale || 1.0,
        transform_x: keyframe.x || 0,
        transform_y: keyframe.y || 0
      });
    });
    
    return configs;
  }

  // 创建随机位置贴纸
  createRandomPositionStickers(stickerId, count, startTime, duration) {
    const configs = [];
    const segmentDuration = duration / count;
    
    for (let i = 0; i < count; i++) {
      configs.push({
        sticker_id: stickerId,
        start: startTime + (i * segmentDuration),
        end: startTime + ((i + 1) * segmentDuration),
        scale: 0.5 + Math.random() * 1.0, // 0.5-1.5倍缩放
        transform_x: (Math.random() - 0.5) * 400, // -200到200像素
        transform_y: (Math.random() - 0.5) * 400  // -200到200像素
      });
    }
    
    return configs;
  }

  // 批量添加贴纸
  async batchAddStickers(draftUrl, stickerConfigs) {
    const results = [];
    
    for (const config of stickerConfigs) {
      try {
        const result = await this.addSticker(draftUrl, config);
        results.push(result);
        
        // 添加延迟避免请求过快
        await new Promise(resolve => setTimeout(resolve, 100));
      } catch (error) {
        console.error('贴纸添加失败:', error);
        results.push({ error: error.message });
      }
    }
    
    return results;
  }

  // 创建贴纸模板
  createStickerTemplate(templateType, stickerId, baseTime, baseDuration) {
    switch (templateType) {
      case 'corner-decoration':
        return [
          {
            sticker_id: stickerId,
            start: baseTime,
            end: baseTime + baseDuration,
            scale: 0.3,
            transform_x: -400,
            transform_y: -300
          },
          {
            sticker_id: stickerId,
            start: baseTime,
            end: baseTime + baseDuration,
            scale: 0.3,
            transform_x: 400,
            transform_y: -300
          },
          {
            sticker_id: stickerId,
            start: baseTime,
            end: baseTime + baseDuration,
            scale: 0.3,
            transform_x: -400,
            transform_y: 300
          },
          {
            sticker_id: stickerId,
            start: baseTime,
            end: baseTime + baseDuration,
            scale: 0.3,
            transform_x: 400,
            transform_y: 300
          }
        ];
      
      case 'center-highlight':
        return [{
          sticker_id: stickerId,
          start: baseTime,
          end: baseTime + baseDuration,
          scale: 2.0,
          transform_x: 0,
          transform_y: 0
        }];
      
      case 'floating-animation':
        return this.createAnimatedSticker(stickerId, baseTime, baseDuration, [
          { x: -100, y: -100, scale: 0.8 },
          { x: 100, y: -100, scale: 1.0 },
          { x: 100, y: 100, scale: 1.2 },
          { x: -100, y: 100, scale: 1.0 },
          { x: -100, y: -100, scale: 0.8 }
        ]);
      
      default:
        return [{
          sticker_id: stickerId,
          start: baseTime,
          end: baseTime + baseDuration,
          scale: 1.0,
          transform_x: 0,
          transform_y: 0
        }];
    }
  }
}

// 使用示例
const stickerManager = new StickerManager();

// 创建贴纸序列
const stickerSequence = stickerManager.createStickerSequence([
  { id: "7326810673609018675", scale: 1.0, x: 0, y: 0 },
  { id: "7326810673609018676", scale: 1.2, x: 100, y: -50 },
  { id: "7326810673609018677", scale: 0.8, x: -100, y: 50 }
], 2000000);

// 创建动画贴纸
const animatedSticker = stickerManager.createAnimatedSticker(
  "7326810673609018675",
  5000000,
  3000000,
  [
    { x: -200, y: 0, scale: 0.5 },
    { x: 0, y: 0, scale: 1.0 },
    { x: 200, y: 0, scale: 1.5 },
    { x: 0, y: 0, scale: 1.0 }
  ]
);

// 创建模板贴纸
const cornerDecorations = stickerManager.createStickerTemplate(
  'corner-decoration',
  "7326810673609018675",
  0,
  10000000
);

// 批量添加
const allConfigs = [...stickerSequence, ...animatedSticker, ...cornerDecorations];
await stickerManager.batchAddStickers(draftUrl, allConfigs);
```

### Python 示例

```python
import requests
import time
import random
from typing import List, Dict

class StickerProcessor:
    def __init__(self, base_url: str = "https://api.example.com"):
        self.base_url = base_url

    def add_sticker(self, draft_url: str, sticker_config: Dict) -> Dict:
        response = requests.post(
            f'{self.base_url}/v1/add_sticker',
            headers={'Content-Type': 'application/json'},
            json={
                "draft_url": draft_url,
                **sticker_config
            }
        )
        response.raise_for_status()
        return response.json()

    def create_sticker_sequence(self, stickers: List[Dict], interval_duration: int = 1000000) -> List[Dict]:
        """创建贴纸序列"""
        configs = []
        for i, sticker in enumerate(stickers):
            configs.append({
                "sticker_id": sticker["id"],
                "start": i * interval_duration,
                "end": (i + 1) * interval_duration,
                "scale": sticker.get("scale", 1.0),
                "transform_x": sticker.get("x", 0),
                "transform_y": sticker.get("y", 0)
            })
        return configs

    def create_animated_sticker(self, sticker_id: str, start_time: int, 
                              duration: int, keyframes: List[Dict]) -> List[Dict]:
        """创建动画贴纸效果"""
        configs = []
        segment_duration = duration // len(keyframes)
        
        for i, keyframe in enumerate(keyframes):
            configs.append({
                "sticker_id": sticker_id,
                "start": start_time + (i * segment_duration),
                "end": start_time + ((i + 1) * segment_duration),
                "scale": keyframe.get("scale", 1.0),
                "transform_x": keyframe.get("x", 0),
                "transform_y": keyframe.get("y", 0)
            })
        
        return configs

    def create_random_stickers(self, sticker_id: str, count: int, 
                             start_time: int, duration: int) -> List[Dict]:
        """创建随机位置贴纸"""
        configs = []
        segment_duration = duration // count
        
        for i in range(count):
            configs.append({
                "sticker_id": sticker_id,
                "start": start_time + (i * segment_duration),
                "end": start_time + ((i + 1) * segment_duration),
                "scale": 0.5 + random.random() * 1.0,  # 0.5-1.5倍缩放
                "transform_x": int((random.random() - 0.5) * 400),  # -200到200像素
                "transform_y": int((random.random() - 0.5) * 400)   # -200到200像素
            })
        
        return configs

    def batch_add_stickers(self, draft_url: str, sticker_configs: List[Dict]) -> List[Dict]:
        """批量添加贴纸"""
        results = []
        
        for config in sticker_configs:
            try:
                result = self.add_sticker(draft_url, config)
                results.append(result)
                time.sleep(0.1)  # 避免请求过快
            except Exception as e:
                print(f"贴纸添加失败: {e}")
                results.append({"error": str(e)})
        
        return results

# 使用示例
processor = StickerProcessor()

# 基本贴纸
basic_config = {
    "sticker_id": "7326810673609018675",
    "start": 0,
    "end": 5000000,
    "scale": 1.0
}

# 贴纸序列
sequence_configs = processor.create_sticker_sequence([
    {"id": "7326810673609018675", "scale": 1.0, "x": 0, "y": 0},
    {"id": "7326810673609018676", "scale": 1.2, "x": 100, "y": -50},
    {"id": "7326810673609018677", "scale": 0.8, "x": -100, "y": 50}
], interval_duration=2000000)

# 动画贴纸
animated_configs = processor.create_animated_sticker(
    "7326810673609018675",
    start_time=10000000,
    duration=4000000,
    keyframes=[
        {"x": -200, "y": 0, "scale": 0.5},
        {"x": 0, "y": 0, "scale": 1.0},
        {"x": 200, "y": 0, "scale": 1.5},
        {"x": 0, "y": 0, "scale": 1.0}
    ]
)

# 批量添加
draft_url = "YOUR_DRAFT_URL"
all_configs = [basic_config] + sequence_configs + animated_configs
results = processor.batch_add_stickers(draft_url, all_configs)

for i, result in enumerate(results):
    if "error" not in result:
        print(f"贴纸 {i+1} 添加成功: {result['segment_id']}")
    else:
        print(f"贴纸 {i+1} 添加失败: {result['error']}")
```

## 错误码说明

| 错误码 | 错误信息 | 说明 | 解决方案 |
|--------|----------|------|----------|
| 400 | draft_url是必填项 | 缺少草稿URL参数 | 提供有效的draft_url |
| 400 | sticker_id是必填项 | 缺少贴纸ID参数 | 提供有效的sticker_id |
| 400 | start是必填项 | 缺少开始时间参数 | 提供有效的start时间 |
| 400 | end是必填项 | 缺少结束时间参数 | 提供有效的end时间 |
| 400 | 时间范围无效 | end必须大于start | 确保结束时间大于开始时间 |
| 400 | 缩放比例无效 | scale超出建议范围 | 使用0.1-5.0范围内的缩放值 |
| 404 | 草稿不存在 | 指定的草稿URL无效 | 检查草稿URL是否正确 |
| 404 | 贴纸不存在 | 指定的贴纸ID无效 | 确认贴纸ID是否正确 |
| 500 | 贴纸添加失败 | 内部处理错误 | 联系技术支持 |

## 注意事项

1. **时间单位**: 所有时间参数使用微秒（1秒 = 1,000,000微秒）
2. **贴纸ID**: 确保使用有效的贴纸ID
3. **时间范围**: end必须大于start
4. **缩放范围**: scale建议在0.1-5.0范围内
5. **位置范围**: transform_x和transform_y应在合理范围内
6. **轨道管理**: 系统自动创建贴纸轨道
7. **性能考虑**: 避免同时添加大量贴纸

## 工作流程

1. 验证必填参数（draft_url, sticker_id, start, end）
2. 检查时间范围的有效性
3. 从缓存中获取草稿
4. 创建贴纸轨道（如果不存在）
5. 创建图像调节设置
6. 创建贴纸片段
7. 添加片段到轨道
8. 保存草稿
9. 返回贴纸信息

## 相关接口

- [创建草稿](./create_draft.md)
- [添加视频](./add_videos.md)
- [添加音频](./add_audios.md)
- [添加图片](./add_images.md)
- [保存草稿](./save_draft.md)
- [生成视频](./gen_video.md)