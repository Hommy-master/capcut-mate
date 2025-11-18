# ADD_VIDEOS API 接口文档

## 📋 目录

- [🔧 接口信息](#-接口信息)
- [🎯 功能描述](#-功能描述)
- [📥 请求参数](#-请求参数)
- [📤 响应格式](#-响应格式)
- [💻 使用示例](#-使用示例)
- [❌ 错误码说明](#-错误码说明)
- [⚠️ 注意事项](#️-注意事项)
- [🔄 工作流程](#-工作流程)
- [➡️ 下一步操作](#️-下一步操作)
- [🔗 相关接口](#-相关接口)

## 🔧 接口信息

```
POST /openapi/capcut-mate/v1/add_videos
```

## 功能描述

批量向现有草稿中添加视频素材。该接口是一个功能强大的视频添加工具，支持多个视频的批量处理，包括时间范围控制、透明度调整、遮罩效果、转场动画、音量控制、缩放变换等高级功能。特别适合创建复杂的多视频组合场景，如画中画效果、视频拼接、过渡动画等。

## 更多文档

📖 更多详细文档和教程请访问：[https://docs.jcaigc.cn](https://docs.jcaigc.cn)

## 请求参数

```json
{
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
  "video_infos": "[{\"video_url\":\"https://assets.jcaigc.cn/video1.mp4\",\"width\":1024,\"height\":1024,\"start\":0,\"end\":5000000,\"duration\":5000000,\"mask\":\"圆形\",\"transition\":\"淡入淡出\",\"transition_duration\":500000,\"volume\":0.8}]",
  "alpha": 0.5,
  "scale_x": 1.0,
  "scale_y": 1.0,
  "transform_x": 100,
  "transform_y": 200
}
```

### 主要参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| draft_url | string | ✅ | - | 目标草稿的完整URL |
| video_infos | string | ✅ | - | 视频信息数组的JSON字符串 |
| alpha | number | ❌ | 1.0 | 全局透明度(0-1) |
| scale_x | number | ❌ | 1.0 | X轴缩放比例 |
| scale_y | number | ❌ | 1.0 | Y轴缩放比例 |
| transform_x | number | ❌ | 0 | X轴位置偏移(像素) |
| transform_y | number | ❌ | 0 | Y轴位置偏移(像素) |

### video_infos 数组结构

| 字段名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| video_url | string | ✅ | - | 视频文件的URL地址 |
| width | number | ✅ | - | 视频宽度(像素) |
| height | number | ✅ | - | 视频高度(像素) |
| start | number | ✅ | - | 视频开始播放时间(微秒) |
| end | number | ✅ | - | 视频结束播放时间(微秒) |
| duration | number | ✅ | - | 视频总时长(微秒) |
| mask | string | ❌ | - | 遮罩类型 |
| transition | string | ❌ | - | 转场效果名称 |
| transition_duration | number | ❌ | 500000 | 转场持续时间(微秒) |
| volume | number | ❌ | 1.0 | 音量大小(0-1) |

### 参数详解

#### 时间参数
- **start**: 视频在时间轴上的开始时间，单位微秒（1秒 = 1,000,000微秒）
- **end**: 视频在时间轴上的结束时间，单位微秒
- **duration**: 视频文件的总时长，用于素材创建
- **播放时长**: 实际播放时长 = end - start

#### 透明度参数
- **alpha**: 全局透明度，应用于所有添加的视频
  - 1.0 = 完全不透明
  - 0.5 = 半透明
  - 0.0 = 完全透明
  - 范围：0.0 - 1.0

#### 缩放参数
- **scale_x/scale_y**: X/Y轴方向的缩放比例
- 1.0 = 原始大小，0.5 = 缩小一半，2.0 = 放大两倍
- 建议范围：0.1 - 5.0

#### 位置参数
- **transform_x/transform_y**: X/Y轴方向的位置偏移，单位像素
- 正值向右/下移动，负值向左/上移动
- 以画布中心为原点

#### 遮罩类型
支持的遮罩类型：
- `圆形` - 圆形遮罩效果
- `爱心` - 爱心形状遮罩
- `星形` - 星形遮罩
- `矩形` - 矩形遮罩
- `线性` - 线性渐变遮罩
- `镜面` - 镜面反射遮罩

#### 转场效果
- **transition**: 转场效果名称
- **transition_duration**: 转场持续时间
  - 最小值：100,000微秒（0.1秒）
  - 最大值：2,500,000微秒（2.5秒）
  - 推荐值：500,000微秒（0.5秒）

#### 音量控制
- **volume**: 视频音量大小
  - 1.0 = 原始音量
  - 0.5 = 一半音量
  - 0.0 = 静音
  - 范围：0.0 - 1.0

## 响应格式

### 成功响应 (200)

```json
{
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
  "track_id": "video-track-uuid",
  "video_ids": ["video1-uuid", "video2-uuid", "video3-uuid"],
  "segment_ids": ["segment1-uuid", "segment2-uuid", "segment3-uuid"]
}
```

### 响应字段说明

| 字段名 | 类型 | 说明 |
|--------|------|------|
| draft_url | string | 更新后的草稿URL |
| track_id | string | 视频轨道ID |
| video_ids | array | 添加的视频ID列表 |
| segment_ids | array | 片段ID列表 |

## 使用示例

### cURL 示例

#### 1. 基本视频添加

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_videos \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "video_infos": "[{\"video_url\":\"https://assets.jcaigc.cn/video1.mp4\",\"width\":1920,\"height\":1080,\"start\":0,\"end\":5000000,\"duration\":10000000}]"
  }'
```

#### 2. 多视频批量添加

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_videos \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "video_infos": "[{\"video_url\":\"https://assets.jcaigc.cn/video1.mp4\",\"width\":1920,\"height\":1080,\"start\":0,\"end\":5000000,\"duration\":10000000},{\"video_url\":\"https://assets.jcaigc.cn/video2.mp4\",\"width\":1280,\"height\":720,\"start\":5000000,\"end\":10000000,\"duration\":8000000}]",
    "alpha": 0.8
  }'
```

#### 3. 带遮罩和转场的视频

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_videos \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "video_infos": "[{\"video_url\":\"https://assets.jcaigc.cn/video1.mp4\",\"width\":1024,\"height\":1024,\"start\":0,\"end\":5000000,\"duration\":10000000,\"mask\":\"圆形\",\"transition\":\"淡入淡出\",\"transition_duration\":500000,\"volume\":0.8}]",
    "alpha": 1.0,
    "scale_x": 1.2,
    "scale_y": 1.2
  }'
```

#### 4. 画中画效果

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_videos \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "video_infos": "[{\"video_url\":\"https://assets.jcaigc.cn/main.mp4\",\"width\":1920,\"height\":1080,\"start\":0,\"end\":10000000,\"duration\":15000000},{\"video_url\":\"https://assets.jcaigc.cn/pip.mp4\",\"width\":640,\"height\":360,\"start\":2000000,\"end\":8000000,\"duration\":10000000}]",
    "transform_x": 300,
    "transform_y": -200,
    "scale_x": 0.3,
    "scale_y": 0.3
  }'
```

### JavaScript 示例

```javascript
const addVideos = async (draftUrl, videoConfig) => {
  const response = await fetch('/openapi/capcut-mate/v1/add_videos', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      draft_url: draftUrl,
      ...videoConfig
    })
  });
  return response.json();
};

// 基本视频添加
const basicVideos = {
  video_infos: JSON.stringify([
    {
      video_url: "https://assets.jcaigc.cn/video1.mp4",
      width: 1920,
      height: 1080,
      start: 0,
      end: 5000000,
      duration: 10000000
    }
  ])
};

// 多视频序列
const videoSequence = {
  video_infos: JSON.stringify([
    {
      video_url: "https://assets.jcaigc.cn/intro.mp4",
      width: 1920,
      height: 1080,
      start: 0,
      end: 3000000,
      duration: 5000000,
      transition: "淡入淡出",
      transition_duration: 500000
    },
    {
      video_url: "https://assets.jcaigc.cn/main.mp4",
      width: 1920,
      height: 1080,
      start: 3000000,
      end: 15000000,
      duration: 20000000,
      volume: 0.8
    },
    {
      video_url: "https://assets.jcaigc.cn/outro.mp4",
      width: 1920,
      height: 1080,
      start: 15000000,
      end: 18000000,
      duration: 5000000,
      mask: "圆形"
    }
  ]),
  alpha: 1.0
};

// 画中画效果
const pipEffect = {
  video_infos: JSON.stringify([
    {
      video_url: "https://assets.jcaigc.cn/background.mp4",
      width: 1920,
      height: 1080,
      start: 0,
      end: 10000000,
      duration: 15000000
    },
    {
      video_url: "https://assets.jcaigc.cn/overlay.mp4",
      width: 640,
      height: 360,
      start: 2000000,
      end: 8000000,
      duration: 10000000,
      mask: "圆形"
    }
  ]),
  scale_x: 0.8,
  scale_y: 0.8,
  transform_x: 200,
  transform_y: -150,
  alpha: 0.9
};

try {
  const result1 = await addVideos(draftUrl, basicVideos);
  const result2 = await addVideos(draftUrl, videoSequence);
  const result3 = await addVideos(draftUrl, pipEffect);
  
  console.log('视频添加成功:', {
    basic: result1,
    sequence: result2,
    pip: result3
  });
} catch (error) {
  console.error('添加失败:', error);
}
```

### 高级JavaScript示例

```javascript
class VideoManager {
  constructor(baseUrl = 'https://capcut-mate.jcaigc.cn') {
    this.baseUrl = baseUrl;
  }

  async addVideos(draftUrl, videoConfig) {
    const response = await fetch(`${this.baseUrl}/openapi/capcut-mate/v1/add_videos`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        draft_url: draftUrl,
        ...videoConfig
      })
    });
    return response.json();
  }

  // 创建视频序列
  createVideoSequence(videos, transitionType = "淡入淡出", transitionDuration = 500000) {
    let currentTime = 0;
    const videoInfos = videos.map((video, index) => {
      const videoInfo = {
        video_url: video.url,
        width: video.width,
        height: video.height,
        start: currentTime,
        end: currentTime + video.playDuration,
        duration: video.totalDuration,
        volume: video.volume || 1.0
      };

      // 添加转场效果（除了最后一个视频）
      if (index < videos.length - 1) {
        videoInfo.transition = transitionType;
        videoInfo.transition_duration = transitionDuration;
      }

      // 添加遮罩效果
      if (video.mask) {
        videoInfo.mask = video.mask;
      }

      currentTime += video.playDuration;
      return videoInfo;
    });

    return {
      video_infos: JSON.stringify(videoInfos)
    };
  }

  // 创建画中画效果
  createPictureInPicture(mainVideo, overlayVideo, position = { x: 300, y: -200 }, scale = 0.3) {
    const videoInfos = [
      {
        video_url: mainVideo.url,
        width: mainVideo.width,
        height: mainVideo.height,
        start: 0,
        end: mainVideo.duration,
        duration: mainVideo.duration
      },
      {
        video_url: overlayVideo.url,
        width: overlayVideo.width,
        height: overlayVideo.height,
        start: overlayVideo.start || 0,
        end: overlayVideo.end || overlayVideo.duration,
        duration: overlayVideo.duration,
        mask: overlayVideo.mask || "圆形"
      }
    ];

    return {
      video_infos: JSON.stringify(videoInfos),
      transform_x: position.x,
      transform_y: position.y,
      scale_x: scale,
      scale_y: scale
    };
  }

  // 创建分屏效果
  createSplitScreen(videos, layout = "horizontal") {
    const videoInfos = videos.map((video, index) => {
      let transform_x = 0, transform_y = 0;

      if (layout === "horizontal") {
        // 水平分屏
        const sectionWidth = 1 / videos.length;
        transform_x = (index - (videos.length - 1) / 2) * sectionWidth * video.width;
      } else if (layout === "vertical") {
        // 垂直分屏
        const sectionHeight = 1 / videos.length;
        transform_y = (index - (videos.length - 1) / 2) * sectionHeight * video.height;
      }

      return {
        video_url: video.url,
        width: video.width,
        height: video.height,
        start: video.start || 0,
        end: video.end || video.duration,
        duration: video.duration
      };
    });

    return {
      video_infos: JSON.stringify(videoInfos)
    };
  }
}

// 使用示例
const videoManager = new VideoManager();

// 创建视频序列
const sequence = videoManager.createVideoSequence([
  {
    url: "https://assets.jcaigc.cn/intro.mp4",
    width: 1920,
    height: 1080,
    playDuration: 3000000,
    totalDuration: 5000000
  },
  {
    url: "https://assets.jcaigc.cn/main.mp4",
    width: 1920,
    height: 1080,
    playDuration: 10000000,
    totalDuration: 15000000,
    volume: 0.8
  }
]);

// 创建画中画
const pip = videoManager.createPictureInPicture(
  {
    url: "https://assets.jcaigc.cn/background.mp4",
    width: 1920,
    height: 1080,
    duration: 10000000
  },
  {
    url: "https://assets.jcaigc.cn/overlay.mp4",
    width: 640,
    height: 360,
    duration: 6000000,
    start: 2000000,
    end: 8000000,
    mask: "圆形"
  }
);

await videoManager.addVideos(draftUrl, sequence);
await videoManager.addVideos(draftUrl, pip);
```

### Python 示例

```python
import requests
import json
from typing import List, Dict

class VideoProcessor:
    def __init__(self, base_url="https://capcut-mate.jcaigc.cn"):
        self.base_url = base_url

    def add_videos(self, draft_url: str, video_config: Dict) -> Dict:
        response = requests.post(
            f'{self.base_url}/openapi/capcut-mate/v1/add_videos',
            headers={'Content-Type': 'application/json'},
            json={
                "draft_url": draft_url,
                **video_config
            }
        )
        return response.json()

    def create_video_sequence(self, videos: List[Dict], transition_type: str = "淡入淡出") -> Dict:
        current_time = 0
        video_infos = []
        
        for i, video in enumerate(videos):
            video_info = {
                "video_url": video["url"],
                "width": video["width"],
                "height": video["height"],
                "start": current_time,
                "end": current_time + video["play_duration"],
                "duration": video["total_duration"],
                "volume": video.get("volume", 1.0)
            }
            
            # 添加转场效果（除了最后一个）
            if i < len(videos) - 1:
                video_info["transition"] = transition_type
                video_info["transition_duration"] = 500000
            
            # 添加遮罩
            if "mask" in video:
                video_info["mask"] = video["mask"]
            
            video_infos.append(video_info)
            current_time += video["play_duration"]
        
        return {
            "video_infos": json.dumps(video_infos)
        }

    def create_picture_in_picture(self, main_video: Dict, overlay_video: Dict, 
                                position: Dict = None, scale: float = 0.3) -> Dict:
        if position is None:
            position = {"x": 300, "y": -200}
        
        video_infos = [
            {
                "video_url": main_video["url"],
                "width": main_video["width"],
                "height": main_video["height"],
                "start": 0,
                "end": main_video["duration"],
                "duration": main_video["duration"]
            },
            {
                "video_url": overlay_video["url"],
                "width": overlay_video["width"],
                "height": overlay_video["height"],
                "start": overlay_video.get("start", 0),
                "end": overlay_video.get("end", overlay_video["duration"]),
                "duration": overlay_video["duration"],
                "mask": overlay_video.get("mask", "圆形")
            }
        ]
        
        return {
            "video_infos": json.dumps(video_infos),
            "transform_x": position["x"],
            "transform_y": position["y"],
            "scale_x": scale,
            "scale_y": scale
        }

# 使用示例
processor = VideoProcessor()

# 视频序列
videos = [
    {
        "url": "https://assets.jcaigc.cn/intro.mp4",
        "width": 1920,
        "height": 1080,
        "play_duration": 3000000,
        "total_duration": 5000000
    },
    {
        "url": "https://assets.jcaigc.cn/main.mp4",
        "width": 1920,
        "height": 1080,
        "play_duration": 10000000,
        "total_duration": 15000000,
        "volume": 0.8
    }
]

sequence_config = processor.create_video_sequence(videos)
result = processor.add_videos("YOUR_DRAFT_URL", sequence_config)
print(f"结果: {result}")
```

## 错误码说明

| 错误码 | 错误信息 | 说明 | 解决方案 |
|--------|----------|------|----------|
| 400 | draft_url是必填项 | 缺少草稿URL参数 | 提供有效的草稿URL |
| 400 | video_infos是必填项 | 缺少视频信息参数 | 提供有效的视频信息JSON |
| 400 | video_infos格式错误 | JSON格式不正确 | 检查JSON字符串格式 |
| 400 | video_url是必填项 | 视频URL缺失 | 为每个视频提供URL |
| 400 | 视频尺寸无效 | width或height无效 | 提供正数的宽度和高度 |
| 400 | 时间范围无效 | end必须大于start | 确保结束时间大于开始时间 |
| 400 | 透明度值无效 | alpha不在0-1范围内 | 使用0-1之间的透明度值 |
| 404 | 草稿不存在 | 指定的草稿URL无效 | 检查草稿URL是否正确 |
| 404 | 视频资源不存在 | 视频URL无法访问 | 检查视频URL是否可访问 |
| 500 | 视频处理失败 | 内部处理错误 | 联系技术支持 |

## 注意事项

1. **JSON格式**: video_infos必须是合法的JSON字符串
2. **时间单位**: 所有时间参数使用微秒（1秒 = 1,000,000微秒）
3. **视频格式**: 确保视频文件格式被支持（如MP4、AVI等）
4. **文件大小**: 大视频文件可能影响处理速度
5. **网络访问**: 视频URL必须可以正常访问
6. **遮罩限制**: 只支持预定义的遮罩类型
7. **转场限制**: 转场时长有固定范围限制
8. **性能考虑**: 批量添加大量视频可能影响性能

## 工作流程

1. 验证必填参数（draft_url, video_infos）
2. 解析video_infos JSON字符串
3. 验证每个视频的参数配置
4. 获取并解密草稿内容
5. 创建视频轨道
6. 添加视频片段到轨道
7. 应用透明度、缩放和位置变换
8. 添加遮罩和转场效果
9. 设置音量
10. 保存并加密草稿
11. 返回处理结果

## 相关接口

- [创建草稿](./create_draft.md)
- [添加音频](./add_audios.md)
- [添加图片](./add_images.md)
- [保存草稿](./save_draft.md)
- [生成视频](./gen_video.md)

---

<div align="right">

**📚 项目资源**: [GitHub](https://github.com/Hommy-master/capcut-mate) | [Gitee](https://gitee.com/taohongmin-gitee/capcut-mate)

</div>