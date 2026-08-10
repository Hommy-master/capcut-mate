# ADD_IMAGES API Documentation

## 🌐 Language Switch
[中文版](./add_images.zh.md) | [English](./add_images.md)

## Interface Information

```
POST /openapi/capcut-mate/v1/add_images
```

## Function Description

Add images to existing drafts. This interface is used to add image materials to Jianying drafts within specified time periods, supporting transparency, scaling and position adjustments for images. Images can be used to enhance video visual effects, such as background images, watermarks, decorative images, etc.

## More Documentation

📖 For more detailed documentation and tutorials, please visit: [https://docs.jcaigc.cn](https://docs.jcaigc.cn)

## Request Parameters

```json
{
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
  "image_infos": "[{\"image_url\":\"https://assets.jcaigc.cn/image1.jpg\",\"start\":0,\"end\":5000000}]",
  "alpha": 1.0,
  "scale_x": 1.0,
  "scale_y": 1.0,
  "transform_x": 0,
  "transform_y": 0
}
```

### Parameter Description

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| draft_url | string | ✅ | - | Complete URL of the target draft |
| image_infos | string | ✅ | - | JSON string of image information array |
| alpha | number | ❌ | 1.0 | Image transparency, recommended range [0.0, 1.0] |
| scale_x | number | ❌ | 1.0 | Image X-axis scaling ratio |
| scale_y | number | ❌ | 1.0 | Image Y-axis scaling ratio |
| transform_x | number | ❌ | 0 | X-axis position offset (pixels) |
| transform_y | number | ❌ | 0 | Y-axis position offset (pixels) |

### image_infos Array Structure

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| image_url | string | ✅ | - | Image file URL (must start with `http://` or `https://`) |
| start | number | ✅ | - | Image start display time (microseconds) |
| end | number | ✅ | - | Image end display time (microseconds) |
| width | number | ❌ | Draft canvas width | Image width in pixels (optional); segment size follows the image file |
| height | number | ❌ | Draft canvas height | Image height in pixels (optional); segment size follows the image file |
| in_animation | string | ❌ | - | Intro animation name from Intro animations below |
| out_animation | string | ❌ | - | Outro animation name from Outro animations below |
| loop_animation | string | ❌ | - | Loop animation name from Loop animations below |
| in_animation_duration | number | ❌ | - | Intro animation duration in μs (optional) |
| out_animation_duration | number | ❌ | - | Outro animation duration in μs (optional) |
| loop_animation_duration | number | ❌ | - | Single loop duration in μs (optional) |
| transition | string | ❌ | - | Transition name from Transitions below |
| transition_duration | number | ❌ | 500000 | Transition duration in μs (optional), range 100000–2500000 |

### Parameter Details

#### Time Parameters

- **start**: Start time of the image on the timeline, unit microseconds (1 second = 1,000,000 microseconds)
- **end**: End time of the image on the timeline, unit microseconds
- **duration**: Image display duration = end - start

#### Transparency Parameters

- **alpha**: Image transparency
  - 1.0 = Fully opaque
  - 0.5 = Semi-transparent
  - 0.0 = Fully transparent
  - Recommended range: 0.0 - 1.0

#### Scaling Parameters

- **scale_x**: Image scaling ratio in X-axis direction
  - 1.0 = Original size
  - 0.5 = Shrink to half
  - 2.0 = Enlarge to double

- **scale_y**: Image scaling ratio in Y-axis direction
  - 1.0 = Original size
  - 0.5 = Shrink to half
  - 2.0 = Enlarge to double

#### Position Parameters

- **transform_x**: Image position offset on the X axis, in pixels
  - Positive moves right, negative moves left; origin at canvas center
  - Stored as half-canvas-width units (divided by the **current draft canvas width**)

- **transform_y**: Image position offset on the Y axis, in pixels
  - Positive moves down, negative moves up; origin at canvas center
  - Stored as half-canvas-height units (divided by the **current draft canvas height**)

#### Image Information Description

- **image_url**: Image URL
  - Must start with `http://` or `https://`
  - Supported formats: JPG, PNG, and other common image formats

- **width / height** (optional)
  - **Not required**; the API works without them
  - If provided, must be integers greater than 0
  - On-screen size is mainly determined by the **image file** and `scale_x` / `scale_y`, not these fields

<!-- MEDIA_EFFECT_LIST_START -->
### Supported Transitions and Animations

Use the names below directly as `image_infos` field values (same as CapCut/Jianying display names). Unmatched names are ignored.

#### Transitions (transition, 453 total)

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

#### Intro animations (in_animation, 155 total)

```text
2024
2025
Kira游动
PASSION
三屏下滑
三屏切闪
上下抖动
九宫格
交叉震动
交错开幕
侧滑
便利贴
冬季雪花
冰块
冰雪融化
冲撞
分屏横移
分屏组合
分屏翻转
分身模糊
划水
动感放大
动感缩小
区域色块滑动
十字震动
卡片扫光
发光矩形
变速扩大
变速时空
向上滑动
向上滚动
向上转入
向上转入 II
向上闪入
向下滑动
向下甩入
向下甩动
向右上甩入
向右下甩入
向右滑动
向右甩入
向右转入
向左上甩入
向左下甩入
向左滑动
向左转入
四屏转换
圆形开幕
多层环形
多屏分割I
多屏分割II
多维空间
展开
左右抖动
幸运圣诞树
开辟2025
弹力分割
弹近
录像带分屏
心形放大
快速翻页
手写云朵
手机倒数
扫描
抖动下降
抖动变焦
抖动横移
折叠开幕
报纸拼贴
报纸拼贴Ⅱ
拉丝滑入
拼图
探灯聚焦
放大
斜切
斜向拉丝
旋转
旋转圆球
旋转开幕
时间倒计时
晃动抽帧
曝光放射
果冻 I
果冻 II
枫叶遮罩
模糊聚焦
横向模糊
水墨
水滴遮罩
油画描边变色
波纹弹动
流金
渐显
游蛇开幕
滑片滑动
漩涡旋转
灼烧出现
点开
烟雾弹
照片回忆
爱心碰撞
玫瑰
玻璃聚集
画出爱心
画面擦除
砸出波纹
神奇弹窗
空间扭曲
立体交叉
立体翻转
立方分体
竖向拼接
粒子爱心
缩小
翻书
翻入
翻卡
老电视
聚合
能量立方
脉冲
色散波纹
荧光爆闪
负片闪屏
跳转开幕
转圈圈
轻微抖动
轻微抖动 II
轻微抖动 III
轻微放大
迷幻流光
金沙
钟摆
钱币遮罩
镜像翻转
镜面组成
闪屏
闪现
闪电分屏
雨刷
雨刷 II
雪花遮罩
震动波纹
震撼倒数
震波
震波 II
震波 III
鞭炮遮罩
音量大小
飞近
马赛克
魔方 III
魔法粒子I
魔法粒子II
黑白画中画
```

#### Outro animations (out_animation, 124 total)

```text
2024
2025
Kira游动
PASSION
三屏下滑
三屏切闪
九宫格
交叉震动
交错闭幕
侧滑
便利贴
冬季雪花
冰块
冰雪融化
冲撞
分屏横移
分屏组合
分屏翻转
分身模糊
划水
区域色块滑动
十字震动
卡片扫光
发光矩形
变速扩大
变速时空
向上滑动
向上滚动
向上转出
向上转出 II
向上闪出
向下滑动
向下甩动
向右滑动
向左滑动
四屏转换
圆形闭幕
多层环形
多屏分割I
多屏分割II
多维空间
幕布
幸运圣诞树
弹力分割
弹远
录像带分屏
心形缩小
快速翻页
手写云朵
扫描
抖动变焦
抖动横移
折叠
折叠闭幕
报纸拼贴
报纸拼贴Ⅱ
拉丝滑出
拼图
探灯聚焦
放大
斜切
斜向拉丝
旋转
旋转圆球
旋转闭幕
晃动抽帧
曝光放射
枫叶遮罩
模糊聚焦
横向模糊
水墨
水滴遮罩
油画描边变色
波纹弹动
流金
渐隐
滑片滑动
漩涡旋转
灼烧出现
烟雾弹
照片回忆
爱心碰撞
玫瑰
玻璃爆开
画出爱心
画面擦除
砸出波纹
空间扭曲
立体交叉
立体翻转
立方合体
竖向拼接
粒子爱心
缩小
翻出
翻卡
老电视
能量立方
脉冲
色散波纹
荧光爆闪
负片闪屏
跳转闭幕
转圈圈
轻微放大
迷幻流光
金沙
钱币遮罩
镜像翻转
镜面拆分
闪屏
闪现
闪电分屏
雪花遮罩
震动波纹
震波 III
鞭炮遮罩
音量大小
飘散
飞远
马赛克
魔法粒子I
魔法粒子II
黑白画中画
```

#### Loop animations (loop_animation, 123 total)

```text
三分割
三分割 II
上下分割
上下分割 II
上升旋转
下降向右
下降向左
中间分割
中间分割 II
分身
分身 II
动感摇晃I
动感摇晃II
叠叠乐
叠叠乐 II
叠叠乐 III
叠叠乐 IV
叠叠乐 V
叠叠乐 Ⅵ
右拉镜
向右下降
向右缩小
向左下降
向左缩小
哈哈镜
哈哈镜 II
四格滑动
四格滑动 II
四格翻转
四格翻转 II
四格转动
四格转动 II
回弹伸缩
回忆旋转
坠落
夹心饼干
夹心饼干 II
小火车
小火车 II
小火车 III
小火车 IV
小陀螺
小陀螺 II
左右分割
左右分割 II
左拉镜
弹入旋转
弹动冲屏
形变右缩
形变左缩
形变缩小
悠悠球
悠悠球 II
手机
手机 II
手机 III
扭曲拉伸
抖入放大
拉伸扭曲
放大弹动
斜转
斜转 II
方片转动
方片转动 II
旋入晃动
旋出渐隐
旋转上升
旋转伸缩
旋转回吸
旋转缩小
旋转降落
晃动旋出
水晶
水晶 II
波动吸收
波动放大
波动滑出
海盗船
海盗船 II
海盗船 III
海盗船 IV
滑入波动
滑滑梯
滑滑梯 II
百叶窗
百叶窗 II
相框滑动
碎块滑动
碎块滑动 II
立方体
立方体 II
立方体 III
立方体 IV
立方体 V
红酒摇晃
绕圈圈
绕圈圈 II
绕圈圈 III
绕圈圈 IV
缩小弹动
缩小旋转
缩小转出
缩放
缩放 II
翻转
翻转 II
翻转 III
翻转 IV
翻转 V
翻转 VI
荡秋千
荡秋千 II
跳跳糖
转入转出
转入转出 II
转圈圈
过山车
过山车 II
闪光放大
闪光放大 II
降落旋转
魔方
魔方 II
```
<!-- MEDIA_EFFECT_LIST_END -->

## Response Format

### Success Response (200)

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

### Response Field Description

| Field | Type | Description |
|-------|------|-------------|
| draft_url | string | Updated draft URL |
| track_id | string | Video track ID |
| image_ids | array | List of image IDs |
| segment_ids | array | List of segment IDs |
| segment_infos | array | List of segment information, containing ID, start time and end time for each segment |

### Error Response (4xx/5xx)

```json
{
  "detail": "Error message description"
}
```

## Usage Examples

### cURL Examples

#### 1. Basic Image Addition (minimum fields)

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_images \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "image_infos": "[{\"image_url\":\"https://assets.jcaigc.cn/photo1.jpg\",\"start\":0,\"end\":5000000}]"
  }'
```

#### 2. Image with Transparency

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_images \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "image_infos": "[{\"image_url\":\"https://assets.jcaigc.cn/logo.png\",\"width\":800,\"height\":600,\"start\":1000000,\"end\":6000000}]",
    "alpha": 0.8
  }'
```

#### 3. Image with Scaling and Position Offset

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_images \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "image_infos": "[{\"image_url\":\"https://assets.jcaigc.cn/watermark.png\",\"width\":300,\"height\":100,\"start\":2000000,\"end\":7000000}]",
    "scale_x": 0.5,
    "scale_y": 0.5,
    "transform_x": 700,
    "transform_y": -400
  }'
```

## Error Code Description

| Error Code | Error Message | Description | Solution |
|------------|---------------|-------------|----------|
| 400 | draft_url is required | Missing draft URL parameter | Provide a valid draft_url |
| 400 | image_infos is required | Missing image information parameter | Provide valid image_infos |
| 400 | image_url is required | Image URL missing | Provide URL for each image |
| 400 | Image dimensions invalid | Explicit width or height ≤ 0 | Omit width/height, or pass positive integers |
| 400 | Time range invalid | end must be greater than start | Ensure end time is greater than start time |
| 400 | Transparency invalid | alpha exceeds recommended range | Use transparency value within 0.0-1.0 range |
| 404 | Draft does not exist | Specified draft URL invalid | Check if draft URL is correct |
| 404 | Image does not exist | Specified image URL invalid | Confirm if image URL is correct |
| 500 | Image addition failed | Internal processing error | Contact technical support |

## Notes

1. **Time Unit**: All time parameters use microseconds (1 second = 1,000,000 microseconds)
2. **Required fields**: Each `image_infos` item needs `image_url`, `start`, and `end`
3. **Optional dimensions**: `width` and `height` may be omitted; if set, they must be positive integers
4. **Image URL**: Must start with `http://` or `https://`
5. **Time Range**: `end` must be greater than `start`
6. **Transparency Range**: `alpha` recommended within the 0.0–1.0 range
7. **Position Parameters**: `transform_x` / `transform_y` are in pixels, converted using the **draft canvas** width and height
8. **Track Management**: System automatically creates a video track (images are added as `VideoSegment`)
9. **Performance Consideration**: Avoid adding a large number of images at once

## Workflow

1. Validate required parameters (draft_url, image_infos)
2. Check validity of time ranges
3. Get draft from cache
4. Create video track (images as VideoSegment)
5. Create image adjustment settings
6. Create image segments
7. Add segments to track
8. Save draft
9. Return image information

## Related Interfaces

- [Create Draft](./create_draft.md)
- [Add Videos](./add_videos.md)
- [Add Audios](./add_audios.md)
- [Add Stickers](./add_sticker.md)
- [Save Draft](./save_draft.md)
- [Generate Video](./gen_video.md)

---

<div align="right">

📚 **Project Resources**  
**GitHub**: [https://github.com/Hommy-master/capcut-mate](https://github.com/Hommy-master/capcut-mate)  
**Gitee**: [https://gitee.com/taohongmin-gitee/capcut-mate](https://gitee.com/taohongmin-gitee/capcut-mate)

</div>