# ADD_VIDEOS API 接口文档

## 🌐 语言切换
[中文版](./add_videos.zh.md) | [English](./add_videos.md)

## 接口信息

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
  "scene_timelines": [{"start":0,"end":2500000}],
  "alpha": 0.5,
  "scale_x": 1.0,
  "scale_y": 1.0,
  "transform_x": 100,
  "transform_y": 200
}
```

### 参数说明

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| draft_url | string | ✅ | - | 目标草稿的完整URL |
| video_infos | string | ✅ | - | 视频信息数组的JSON字符串 |
| scene_timelines | array[object] | ❌ | - | 场景时间线数组，用于视频变速，与video_infos一一对应 |
| alpha | number | ❌ | 1.0 | 全局透明度(0-1) |
| scale_x | number | ❌ | 1.0 | X轴缩放比例 |
| scale_y | number | ❌ | 1.0 | Y轴缩放比例 |
| transform_x | number | ❌ | 0 | X轴位置偏移(像素) |
| transform_y | number | ❌ | 0 | Y轴位置偏移(像素) |

### video_infos 数组结构

| 字段名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| video_url | string | ✅ | - | 视频文件的URL地址 |
| width | number | ❌ | - | 视频宽度(像素)，不传则自动获取视频文件尺寸 |
| height | number | ❌ | - | 视频高度(像素)，不传则自动获取视频文件尺寸 |
| start | number | ✅ | - | 视频开始播放时间(微秒) |
| end | number | ✅ | - | 视频结束播放时间(微秒) |
| duration | number | ❌ | end-start | 视频总时长(微秒) |
| mask | string | ❌ | - | 遮罩类型 |
| transition | string | ❌ | - | 转场效果名称 |
| transition_duration | number | ❌ | 500000 | 转场持续时间(微秒) |
| volume | number | ❌ | 1.0 | 音量大小(0-1) |

### scene_timelines 数组结构

| 字段名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| start | number | ✅ | 场景开始时间（微秒） |
| end | number | ✅ | 场景结束时间（微秒） |

### 参数详解

#### 时间参数

- **start**: 视频在时间轴上的开始时间，单位微秒（1秒 = 1,000,000微秒）
- **end**: 视频在时间轴上的结束时间，单位微秒
- **duration**: 视频文件的总时长，用于素材创建（可选参数，如果不传则默认为end-start）
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

#### 视频变速 (scene_timelines)

- **scene_timelines**: 场景时间线数组，用于视频变速，与video_infos一一对应
  - 每个项包含 `start` 和 `end` 字段（微秒）
  - 速度计算：`speed = (video.end - video.start) / (scene_timeline.end - scene_timeline.start)`
  - 示例：如果视频时间线是 0-2000000（2秒），场景时间线是 0-1000000（1秒），则视频将以2倍速播放
  - 如果不提供，视频以正常速度（1.0倍）播放

**变速示例**：
```json
// 原始视频：时间轴上占2秒（0-2000000）
// 要变为2倍速（1秒内播完）：
{
  "video_infos": "[{\"video_url\":\"...\", \"start\":0, \"end\":2000000}]",
  "scene_timelines": "[{\"start\":0, \"end\":1000000}]"
}
// 结果：视频以2倍速播放，实际播放时长为1秒
```

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

#### 5. 视频变速（2倍速）

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_videos \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "video_infos": "[{\"video_url\":\"https://assets.jcaigc.cn/video1.mp4\",\"start\":0,\"end\":2000000}]",
    "scene_timelines": [{"start":0, "end":1000000}]
  }'
```

#### 6. 多个视频不同速度

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_videos \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "video_infos": "[{\"video_url\":\"https://assets.jcaigc.cn/video1.mp4\",\"start\":0,\"end\":3000000},{\"video_url\":\"https://assets.jcaigc.cn/video2.mp4\",\"start\":3000000,\"end\":6000000}]",
    "scene_timelines": [{"start":0, "end":1500000},{"start":0, "end":4000000}]
  }'
# video1: 3000000/1500000 = 2倍速
# video2: 3000000/4000000 = 0.75倍速（慢放）
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
9. **变速功能**: scene_timelines是对象数组，长度应与video_infos数组长度一致

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

📚 **项目资源**  
**GitHub**: [https://github.com/Hommy-master/capcut-mate](https://github.com/Hommy-master/capcut-mate)  
**Gitee**: [https://gitee.com/taohongmin-gitee/capcut-mate](https://gitee.com/taohongmin-gitee/capcut-mate)

</div>

### 语言切换
[中文版](./add_videos.zh.md) | [English](./add_videos.md)