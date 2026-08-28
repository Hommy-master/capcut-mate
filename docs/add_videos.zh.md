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
  "video_infos": "[{\"video_url\":\"https://assets.jcaigc.cn/video1.mp4\",\"width\":1024,\"height\":1024,\"start\":0,\"end\":5000000,\"duration\":5000000,\"mask\":\"圆形\",\"transition\":\"叠化\",\"transition_duration\":500000,\"volume\":0.8}]",
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
| transition | string | ❌ | - | 转场名称，须为下方「支持的转场名称」列表中的值 |
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

- **transition**: 转场名称，须为下方「支持的转场名称」列表中的值
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

<!-- MEDIA_EFFECT_LIST_START -->
### 支持的转场名称（transition 可用值）

下列名称可直接作为 `video_infos` 中 `transition` 的值（与剪映端展示名一致）。未匹配到时该转场不会生效。

当前共 **453** 种转场：

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
    "video_infos": "[{\"video_url\":\"https://assets.jcaigc.cn/video1.mp4\",\"width\":1024,\"height\":1024,\"start\":0,\"end\":5000000,\"duration\":10000000,\"mask\":\"圆形\",\"transition\":\"叠化\",\"transition_duration\":500000,\"volume\":0.8}]",
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