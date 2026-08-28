# ADD_VIDEOS API Documentation

## 🌐 Language Switch
[中文版](./add_videos.zh.md) | [English](./add_videos.md)

## Interface Information

```
POST /openapi/capcut-mate/v1/add_videos
```

## Function Description

Batch add video materials to existing drafts. This interface is a powerful video addition tool that supports batch processing of multiple videos, including time range control, transparency adjustment, mask effects, transition animations, volume control, scaling transformations, and other advanced features. Particularly suitable for creating complex multi-video combination scenes, such as picture-in-picture effects, video splicing, transition animations, etc.

## More Documentation

📖 For more detailed documentation and tutorials, please visit: [https://docs.jcaigc.cn](https://docs.jcaigc.cn)

## Request Parameters

```json
{
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
  "video_infos": "[{\"video_url\":\"https://assets.jcaigc.cn/video1.mp4\",\"width\":1024,\"height\":1024,\"start\":0,\"end\":5000000,\"duration\":5000000,\"mask\":\"circle\",\"transition\":\"叠化\",\"transition_duration\":500000,\"volume\":0.8}]",
  "scene_timelines": [{"start":0,"end":2500000}],
  "alpha": 0.5,
  "scale_x": 1.0,
  "scale_y": 1.0,
  "transform_x": 100,
  "transform_y": 200
}
```

### Parameter Description

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| draft_url | string | ✅ | - | Complete URL of the target draft |
| video_infos | string | ✅ | - | JSON string of video information array |
| scene_timelines | array[object] | ❌ | - | Scene timeline array for video speed change, corresponds one-to-one with video_infos |
| alpha | number | ❌ | 1.0 | Global transparency (0-1) |
| scale_x | number | ❌ | 1.0 | X-axis scaling ratio |
| scale_y | number | ❌ | 1.0 | Y-axis scaling ratio |
| transform_x | number | ❌ | 0 | X-axis position offset (pixels) |
| transform_y | number | ❌ | 0 | Y-axis position offset (pixels) |

### video_infos Array Structure

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| video_url | string | ✅ | - | URL address of the video file |
| width | number | ❌ | - | Video width (pixels), automatically obtained if not provided |
| height | number | ❌ | - | Video height (pixels), automatically obtained if not provided |
| start | number | ✅ | - | Video start playback time (microseconds) |
| end | number | ✅ | - | Video end playback time (microseconds) |
| duration | number | ❌ | end-start | Total video duration (microseconds) |
| mask | string | ❌ | - | Mask type |
| transition | string | ❌ | - | Transition name from Supported Transition Names below |
| transition_duration | number | ❌ | 500000 | Transition duration (microseconds) |
| volume | number | ❌ | 1.0 | Volume size (0-1) |

### scene_timelines Array Structure

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| start | number | ✅ | Scene start time (microseconds) |
| end | number | ✅ | Scene end time (microseconds) |

### Parameter Details

#### Time Parameters

- **start**: Start time of the video on the timeline, unit microseconds (1 second = 1,000,000 microseconds)
- **end**: End time of the video on the timeline, unit microseconds
- **duration**: Total duration of the video file, used for material creation (optional parameter, defaults to end-start if not provided)
- **Playback Duration**: Actual playback duration = end - start

#### Transparency Parameters

- **alpha**: Global transparency, applied to all added videos
  - 1.0 = Fully opaque
  - 0.5 = Semi-transparent
  - 0.0 = Fully transparent
  - Range: 0.0 - 1.0

#### Scaling Parameters

- **scale_x/scale_y**: Scaling ratios in X/Y axis directions
- 1.0 = Original size, 0.5 = Half size, 2.0 = Double size
- Recommended range: 0.1 - 5.0

#### Position Parameters

- **transform_x/transform_y**: Position offsets in X/Y axis directions, unit pixels
- Positive values move right/down, negative values move left/up
- Canvas center as origin

#### Mask Types

Supported mask types (all optional, default is no mask):
- `circle` - Circular mask effect
- `heart` - Heart-shaped mask
- `star` - Star-shaped mask
- `rectangle` - Rectangular mask
- `linear` - Linear gradient mask
- `mirror` - Mirror reflection mask

#### Transition Effects

- **transition**: Transition effect name
- **transition_duration**: Transition duration
  - Minimum: 100,000 microseconds (0.1 seconds)
  - Maximum: 2,500,000 microseconds (2.5 seconds)
  - Recommended: 500,000 microseconds (0.5 seconds)

#### Volume Control

- **volume**: Video volume size
  - 1.0 = Original volume
  - 0.5 = Half volume
  - 0.0 = Mute
  - Range: 0.0 - 1.0

#### Video Speed Change (scene_timelines)

- **scene_timelines**: Scene timeline array for video speed change, corresponds one-to-one with video_infos
  - Each item contains `start` and `end` fields (microseconds)
  - Speed calculation: `speed = (video.end - video.start) / (scene_timeline.end - scene_timeline.start)`
  - Example: If video timeline is 0-2000000 (2 seconds) and scene_timeline is 0-1000000 (1 second), the video will play at 2x speed
  - If not provided, video plays at normal speed (1.0x)

**Speed Change Example**:
```json
// Original video: 2 seconds on timeline (0-2000000)
// To make it 2x speed (play in 1 second):
{
  "video_infos": "[{\"video_url\":\"...\", \"start\":0, \"end\":2000000}]",
  "scene_timelines": "[{\"start\":0, \"end\":1000000}]"
}
// Result: Video plays at 2x speed, actual playback duration is 1 second
```

<!-- MEDIA_EFFECT_LIST_START -->
### Supported Transition Names (`transition` values)

Use the names below directly as `video_infos.transition` (same as CapCut/Jianying display names). Unmatched names are ignored.

Total: **453** transitions:

```text
2024回忆流
3D空间
X形震闪
万花筒
三屏放大
三屏滑入
三屏闪切
上下翻页
上移
下滑
下移
中心切开
中心旋转
二次元烟效
云朵
云朵 II
亮点模糊
便利贴
信号故障
信号故障 II
倒影
倾斜拉伸
倾斜拉开
倾斜模糊
像素冲屏
光束
全息投影
六边形变焦
冰雪结晶
冲屏扭曲
冲鸭
几何分割
几何滑动
分割
分割 II
分割 III
分割 IV
分屏下滑
前后对比
前后对比 II
剧烈摇晃
动漫云朵
动漫漩涡
动漫火焰
动漫闪电
卡片弹出
压缩
发光变焦
叠加
叠化
叠化扭曲
可爱爆炸
可爱龙龙
右移
吃掉
后台切换
向上
向上擦除
向上波动
向下
向下抖动
向下拖拽
向下擦除
向下流动
向右
向右上
向右下
向右拉伸
向右擦除
向右流动
向左
向左上
向左下
向左拉伸
向左拉屏
向左擦除
向左波动
吸入
喜欢
四屏转换
四格展开
回忆
回忆 II
回忆下滑
回忆拉屏
回忆拉屏 II
图片放大
圆形分割
圆形分割 II
圆形扫描
圆形遮罩
圆形遮罩 II
圆盘旋转
圣诞光斑
圣诞光斑II
圣诞树
圣诞礼盒
复古叠影
复古放映
复古放映 II
复古漏光
复古漏光 II
复古胶片
多层环形
多屏定格
大圆盘
大波浪
字母拼贴
射灯
小喇叭
小恶魔
岁月的痕迹
左下角 II
左移
左移弹动
幻影
幻觉
开幕
开心
弹出
弹动发光
弹幕转场
弹跳
彩色像素
彩色滑片
往上翻页
微抖动
心形叠化
快涂擦除
快速缩放
快速震闪
快门
惊悚屏闪
手机屏放大
打板转场 I
打板转场 II
扫光
扭曲弹动
扭曲旋入
扭曲溶解
扭转弹动
抖动
抖动 II
抖动放大
抖动缩小
抖动缩小  II
折痕胶带
抠像旋转
抽象前景
抽象前景 II
拉伸
拉伸 II
拉开
拉框入屏
拉远
拍摄器
拍摄器 II
拍摄器 III
挤压分屏
推近
推近 II
推远 II
摄像机
摇晃描边
摇晃震动
摇镜
撕纸
撕纸拉屏
撕纸掉落
收缩抖动
放大左移
放大镜
放射
故障
故障扫描
故障拼贴
故障模糊
数字矩阵
斜向分割
斜向模糊
斜向闪光
斜线翻页
新篇章
新篇章 II
方形分割
方形变焦
方形模糊
方形模糊 II
方片翻转
旋焦
旋转圆球
旋转圆盘
旋转圆盘 II
旋转快门
旋转拨盘
旋转模糊
旋转穿越
旋转纵深
旋转翻页
旋转震动
无缝撕裂
无限穿越 I
无限穿越 II
日历转场
旧胶片
旧胶片 II
时光穿梭
星光
星光叠化
星光炸开
星星
星星 II
星星 III
星星变焦
星星吸入
星星模糊
春日光斑
暧昧光晕
曝光拉丝
曝光摇镜
未来光谱
未来光谱II
条形模糊
模糊
模糊放大
模糊细闪
模糊缩小
横向分割
横向分屏
横向拉幕
横向模糊
横向滑动
横向震动
横条挤压
横移模糊
横线
樱花飞舞
气泡转场
水墨
水波卷动
水波向右
水波向左
水滴
水滴 II
水滴 III
水滴溶解
汇聚
泛光
泛白
泡泡模糊
波光粼粼
波动
波动 II
波动故障
波点向右
泼墨晕染
流光
涂鸦放大
渐变擦除
溶解推进
滑动
滑动压迫感
滑动弹出
滑动放大
滑块拼贴
滚动立方
漩涡
漩涡扭曲
漫画撕纸
火焰湍流
炫光
炫光 II
炫光 III
炫光弹动
炫光扫描
炫光扭动
炸弹
烟花光斑
烟雾弹
烟雾转场
热成像
燃烧
燃烧 II
燃烧 III
爆米花
爆闪
爆闪 II
爱心
爱心 II
爱心上升
爱心冲击
爱心模糊
爱心气球
爱心软糖
爱心遮罩
环回推近
环形色散
玻璃破碎
玻璃破碎 II
珠光模糊
生气
电光
电光 II
电流
电视故障 I
电视故障 II
画笔擦除
畸变回弹
白光快闪
白色墨花
白色烟雾
百叶窗
百叶窗 II
相机缩小
相片切换
相片拼贴
眨眼
矩形分割
礼物落下
空间上移
空间弹动
空间弹动 II
空间弹动 III
空间弹动 IV
空间旋转
空间旋转 II
空间旋转 III
空间翻转
空间翻转 II
空间跳跃
穿越
穿越 II
穿越 III
窗格
立体旋转
立体翻转
立体翻页
立体翻页 II
立方体
立方旋转
竖向分割
竖向拉伸
竖向拉幕
竖向模糊
竖向模糊 II
竖移模糊
竖线
笔迹涂抹
箭头向右
粉色反转片
粒子
红包雨
纵向滑动
纸团
翻书转场
翻篇
翻转冲屏
翻页
翻页 II
聚光灯
胶卷滑动
胶片切闪
胶片定格
胶片擦除
胶片融化
胶片闪光
色块故障
色差故障
色差逆时针
色差顺时针
色彩溶解
色彩溶解 II
色彩溶解 III
色彩溶解 IV
色彩溶解 V
色彩负片
色散晃镜
色散波纹
色散漩涡
色散闪烁
色散闪烁 II
草图转场
荧光爆闪
菱格翻转
蓝光扫描
蓝色反转片
蓝色线条
虹光旋入
融化
融化 II
课本转场
负片下滑
赛博马赛克
超赞
边框切换
运镜压缩
迷幻波纹
迷幻频闪
逆时针旋转
逆时针旋转 II
透镜故障
重叠上滑
金币祝福
金沙
金色光斑
钱兔无量
镜像翻转
镜头速移
长曝光
闪光灯
闪光灯 II
闪光灯 III
闪动光斑
闪动光斑 II
闪回
闪屏故障
闪白
闪白 II
闪黑
闪黑 II
闹钟
雨刷转场
雪花叠化
雪花四散
雪花故障
雪花环绕
雪雾
雾化
震动
震动 II
震动缩小
霓虹闪光
霓虹闪光 II
顺时针三角
顺时针旋转
顺时针旋转 II
频闪
风车
飘雪
飘雪 II
马赛克
马赛克 II
马赛克III
鱼眼
鱼眼 II
鱼眼 III
鱼眼波纹
鸿运四叶草
黑板擦除
黑白摇镜
黑色反转片
黑色块
黑色烟雾
```
<!-- MEDIA_EFFECT_LIST_END -->

## Response Format

### Success Response (200)

```json
{
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
  "track_id": "video-track-uuid",
  "video_ids": ["video1-uuid", "video2-uuid", "video3-uuid"],
  "segment_ids": ["segment1-uuid", "segment2-uuid", "segment3-uuid"]
}
```

### Response Field Description

| Field | Type | Description |
|-------|------|-------------|
| draft_url | string | Updated draft URL |
| track_id | string | Video track ID |
| video_ids | array | List of added video IDs |
| segment_ids | array | List of segment IDs |

## Usage Examples

### cURL Examples

#### 1. Basic Video Addition

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_videos \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "video_infos": "[{\"video_url\":\"https://assets.jcaigc.cn/video1.mp4\",\"width\":1920,\"height\":1080,\"start\":0,\"end\":5000000,\"duration\":10000000}]"
  }'
```

#### 2. Batch Adding Multiple Videos

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_videos \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "video_infos": "[{\"video_url\":\"https://assets.jcaigc.cn/video1.mp4\",\"width\":1920,\"height\":1080,\"start\":0,\"end\":5000000,\"duration\":10000000},{\"video_url\":\"https://assets.jcaigc.cn/video2.mp4\",\"width\":1280,\"height\":720,\"start\":5000000,\"end\":10000000,\"duration\":8000000}]",
    "alpha": 0.8
  }'
```

#### 3. Video with Mask and Transition

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_videos \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "video_infos": "[{\"video_url\":\"https://assets.jcaigc.cn/video1.mp4\",\"width\":1024,\"height\":1024,\"start\":0,\"end\":5000000,\"duration\":10000000,\"mask\":\"circle\",\"transition\":\"叠化\",\"transition_duration\":500000,\"volume\":0.8}]",
    "alpha": 1.0,
    "scale_x": 1.2,
    "scale_y": 1.2
  }'
```

#### 4. Picture-in-Picture Effect

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

#### 5. Video with Speed Change (2x Speed)

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_videos \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "video_infos": "[{\"video_url\":\"https://assets.jcaigc.cn/video1.mp4\",\"start\":0,\"end\":2000000}]",
    "scene_timelines": [{"start":0, "end":1000000}]
  }'
```

#### 6. Multiple Videos with Different Speeds

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_videos \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "video_infos": "[{\"video_url\":\"https://assets.jcaigc.cn/video1.mp4\",\"start\":0,\"end\":3000000},{\"video_url\":\"https://assets.jcaigc.cn/video2.mp4\",\"start\":3000000,\"end\":6000000}]",
    "scene_timelines": [{"start":0, "end":1500000},{"start":0, "end":4000000}]
  }'
# video1: 3000000/1500000 = 2x speed
# video2: 3000000/4000000 = 0.75x speed (slow motion)
```

## Error Code Description

| Error Code | Error Message | Description | Solution |
|------------|---------------|-------------|----------|
| 400 | draft_url is required | Missing draft URL parameter | Provide a valid draft URL |
| 400 | video_infos is required | Missing video information parameter | Provide valid video information JSON |
| 400 | video_infos format error | JSON format is incorrect | Check JSON string format |
| 400 | video_url is required | Video URL missing | Provide URL for each video |
| 400 | Video dimensions invalid | width or height invalid | Provide positive width and height |
| 400 | Time range invalid | end must be greater than start | Ensure end time is greater than start time |
| 400 | Transparency value invalid | alpha not in 0-1 range | Use transparency value between 0-1 |
| 404 | Draft does not exist | Specified draft URL invalid | Check if draft URL is correct |
| 404 | Video resource does not exist | Video URL inaccessible | Check if video URL is accessible |
| 500 | Video processing failed | Internal processing error | Contact technical support |

## Notes

1. **JSON Format**: video_infos must be a valid JSON string
2. **Time Unit**: All time parameters use microseconds (1 second = 1,000,000 microseconds)
3. **Video Format**: Ensure video file format is supported (e.g., MP4, AVI, etc.)
4. **File Size**: Large video files may affect processing speed
5. **Network Access**: Video URL must be accessible
6. **Mask Limitation**: Only predefined mask types are supported
7. **Transition Limitation**: Transition duration has fixed range limitations
8. **Performance Consideration**: Batch adding a large number of videos may affect performance
9. **Speed Change**: scene_timelines is an object array, length should match video_infos array length

## Workflow

1. Validate required parameters (draft_url, video_infos)
2. Parse video_infos JSON string
3. Validate parameter configuration for each video
4. Obtain and decrypt draft content
5. Create video track
6. Add video segments to track
7. Apply transparency, scaling and position transformation
8. Add mask and transition effects
9. Set volume
10. Save and encrypt draft
11. Return processing result

## Related Interfaces

- [Create Draft](./create_draft.md)
- [Add Audios](./add_audios.md)
- [Add Images](./add_images.md)
- [Save Draft](./save_draft.md)
- [Generate Video](./gen_video.md)

---

<div align="right">

📚 **Project Resources**  
**GitHub**: [https://github.com/Hommy-master/capcut-mate](https://github.com/Hommy-master/capcut-mate)  
**Gitee**: [https://gitee.com/taohongmin-gitee/capcut-mate](https://gitee.com/taohongmin-gitee/capcut-mate)

</div>