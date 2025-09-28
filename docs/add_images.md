# ADD_IMAGES API 接口文档

## 接口信息

```
POST /openapi/capcut-mate/v1/add_images
```

## 功能描述

批量向现有草稿中添加图片素材。该接口支持多个图片的批量处理，包括透明度调整、缩放变换、位置偏移、动画效果等功能。在剪映系统中，图片被作为VideoSegment处理。

## 请求参数

```json
{
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
  "image_infos": "[{\"image_url\":\"https://example.com/image1.jpg\",\"width\":1920,\"height\":1080,\"start\":0,\"end\":5000000,\"duration\":5000000,\"animation\":\"淡入淡出\",\"transition\":\"溶解\",\"transition_duration\":500000}]",
  "alpha": 1.0,
  "scale_x": 1.0,
  "scale_y": 1.0,
  "transform_x": 0,
  "transform_y": 0
}
```

### 主要参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| draft_url | string | ✅ | - | 目标草稿的完整URL |
| image_infos | string | ✅ | - | 图片信息数组的JSON字符串 |
| alpha | number | ❌ | 1.0 | 全局透明度(0-1) |
| scale_x | number | ❌ | 1.0 | X轴缩放比例 |
| scale_y | number | ❌ | 1.0 | Y轴缩放比例 |
| transform_x | number | ❌ | 0 | X轴位置偏移(像素) |
| transform_y | number | ❌ | 0 | Y轴位置偏移(像素) |

### image_infos 数组结构

| 字段名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| image_url | string | ✅ | - | 图片文件的URL地址 |
| width | number | ✅ | - | 图片宽度(像素) |
| height | number | ✅ | - | 图片高度(像素) |
| start | number | ✅ | - | 图片开始显示时间(微秒) |
| end | number | ✅ | - | 图片结束显示时间(微秒) |
| duration | number | ✅ | - | 图片显示总时长(微秒) |
| animation | string | ❌ | - | 动画效果名称 |
| transition | string | ❌ | - | 转场效果名称 |
| transition_duration | number | ❌ | 500000 | 转场持续时间(微秒) |

### 参数详解

#### 时间参数
- **start**: 图片开始显示时间，单位微秒（1秒 = 1,000,000微秒）
- **end**: 图片结束显示时间，单位微秒
- **duration**: 图片总显示时长，通常等于 end - start

#### 透明度和变换
- **alpha**: 全局透明度，范围0.0-1.0
- **scale_x/scale_y**: 缩放比例，1.0为原始大小
- **transform_x/transform_y**: 位置偏移，以画布中心为原点

#### 动画和转场
- **animation**: 支持"淡入淡出"、"缩放入场"、"滑动入场"等
- **transition**: 转场效果名称
- **transition_duration**: 转场时长，范围100,000-2,500,000微秒

## 响应格式

### 成功响应 (200)

```json
{
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
  "track_id": "video-track-uuid",
  "image_ids": ["image1-uuid", "image2-uuid"],
  "segment_ids": ["segment1-uuid", "segment2-uuid"],
  "segment_infos": [
    {
      "id": "segment1-uuid",
      "start": 0,
      "end": 5000000
    }
  ]
}
```

### 响应字段说明

| 字段名 | 类型 | 说明 |
|--------|------|------|
| draft_url | string | 更新后的草稿URL |
| track_id | string | 视频轨道ID |
| image_ids | array | 添加的图片ID列表 |
| segment_ids | array | 片段ID列表 |
| segment_infos | array | 片段详细信息列表 |

## 使用示例

### cURL 示例

#### 基本图片添加

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_images \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "image_infos": "[{\"image_url\":\"https://example.com/photo1.jpg\",\"width\":1920,\"height\":1080,\"start\":0,\"end\":5000000,\"duration\":5000000}]"
  }'
```

#### 带动画效果的图片

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_images \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "image_infos": "[{\"image_url\":\"https://example.com/logo.png\",\"width\":800,\"height\":600,\"start\":1000000,\"end\":4000000,\"duration\":3000000,\"animation\":\"缩放入场\",\"transition\":\"淡入淡出\"}]",
    "alpha": 0.9,
    "scale_x": 1.2,
    "scale_y": 1.2,
    "transform_x": 200,
    "transform_y": -100
  }'
```

### JavaScript 示例

```javascript
const addImages = async (draftUrl, imageConfig) => {
  const response = await fetch('/openapi/capcut-mate/v1/add_images', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      draft_url: draftUrl,
      ...imageConfig
    })
  });
  return response.json();
};

// 基本图片添加
const basicImages = {
  image_infos: JSON.stringify([
    {
      image_url: "https://example.com/cover.jpg",
      width: 1920,
      height: 1080,
      start: 0,
      end: 5000000,
      duration: 5000000
    }
  ])
};

// 图片幻灯片
const slideshow = {
  image_infos: JSON.stringify([
    {
      image_url: "https://example.com/slide1.jpg",
      width: 1920,
      height: 1080,
      start: 0,
      end: 3000000,
      duration: 3000000,
      animation: "淡入淡出",
      transition: "淡入淡出"
    },
    {
      image_url: "https://example.com/slide2.jpg",
      width: 1920,
      height: 1080,
      start: 3000000,
      end: 6000000,
      duration: 3000000,
      animation: "滑动入场",
      transition: "滑动"
    }
  ])
};

// 图片水印
const watermark = {
  image_infos: JSON.stringify([
    {
      image_url: "https://example.com/logo.png",
      width: 300,
      height: 100,
      start: 0,
      end: 30000000,
      duration: 30000000,
      animation: "淡入淡出"
    }
  ]),
  alpha: 0.7,
  scale_x: 0.5,
  scale_y: 0.5,
  transform_x: 700,
  transform_y: -400
};

try {
  const result1 = await addImages(draftUrl, basicImages);
  const result2 = await addImages(draftUrl, slideshow);
  const result3 = await addImages(draftUrl, watermark);
  
  console.log('图片添加成功');
} catch (error) {
  console.error('添加失败:', error);
}
```

### Python 示例

```python
import requests
import json

class ImageProcessor:
    def __init__(self, base_url="https://capcut-mate.jcaigc.cn"):
        self.base_url = base_url

    def add_images(self, draft_url: str, image_config: dict) -> dict:
        response = requests.post(
            f'{self.base_url}/openapi/capcut-mate/v1/add_images',
            headers={'Content-Type': 'application/json'},
            json={
                "draft_url": draft_url,
                **image_config
            }
        )
        return response.json()

    def create_slideshow(self, images: list, slide_duration: int = 3000000) -> dict:
        """创建幻灯片播放"""
        current_time = 0
        image_infos = []
        
        for image in images:
            image_info = {
                "image_url": image["url"],
                "width": image["width"], 
                "height": image["height"],
                "start": current_time,
                "end": current_time + slide_duration,
                "duration": slide_duration,
                "animation": image.get("animation", "淡入淡出")
            }
            image_infos.append(image_info)
            current_time += slide_duration
        
        return {"image_infos": json.dumps(image_infos)}

# 使用示例
processor = ImageProcessor()

slideshow_config = processor.create_slideshow([
    {
        "url": "https://example.com/slide1.jpg",
        "width": 1920,
        "height": 1080,
        "animation": "淡入淡出"
    }
])

result = processor.add_images("YOUR_DRAFT_URL", slideshow_config)
print(f"图片添加成功: {result['track_id']}")
```

## 错误码说明

| 错误码 | 错误信息 | 说明 | 解决方案 |
|--------|----------|------|----------|
| 400 | draft_url是必填项 | 缺少草稿URL | 提供有效的草稿URL |
| 400 | image_infos是必填项 | 缺少图片信息 | 提供有效的图片信息JSON |
| 400 | image_infos格式错误 | JSON格式不正确 | 检查JSON字符串格式 |
| 400 | image_url是必填项 | 图片URL缺失 | 为每个图片提供URL |
| 400 | 图片尺寸无效 | width或height无效 | 提供正数的宽度和高度 |
| 400 | 时间范围无效 | end必须大于start | 确保结束时间大于开始时间 |
| 404 | 草稿不存在 | 草稿URL无效 | 检查草稿URL是否正确 |
| 404 | 图片资源不存在 | 图片URL无法访问 | 检查图片URL是否可访问 |
| 500 | 图片处理失败 | 内部处理错误 | 联系技术支持 |

## 注意事项

1. **JSON格式**: image_infos必须是合法的JSON字符串
2. **时间单位**: 所有时间参数使用微秒（1秒 = 1,000,000微秒）
3. **图片格式**: 支持JPG、PNG、GIF等格式
4. **网络访问**: 图片URL必须可以正常访问
5. **透明度范围**: alpha值必须在0.0-1.0范围内
6. **图片处理**: 图片在剪映中作为VideoSegment处理
7. **动画效果**: 不是所有动画效果都兼容所有转场效果

## 工作流程

1. 验证必填参数（draft_url, image_infos）
2. 解析image_infos JSON字符串
3. 验证每个图片的参数配置
4. 获取并解密草稿内容
5. 创建视频轨道（图片作为VideoSegment）
6. 添加图片片段到轨道
7. 应用透明度、缩放和位置变换
8. 添加动画和转场效果
9. 保存并加密草稿
10. 返回处理结果

## 相关接口

- [创建草稿](./create_draft.md)
- [添加视频](./add_videos.md)
- [添加音频](./add_audios.md)
- [保存草稿](./save_draft.md)
- [生成视频](./gen_video.md)