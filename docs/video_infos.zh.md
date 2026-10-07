# VIDEO_INFOS API 接口文档

## 🌐 语言切换
[中文版](./video_infos.zh.md) | [English](./video_infos.md)

## 接口信息

```
POST /openapi/capcut-mate/v1/video_infos
```

## 功能描述

根据视频URL和时间线生成视频信息。该接口将视频文件URL和时间线配置转换为剪映草稿所需的视频信息格式，支持转场设置。

## 请求参数

```json
{
  "video_urls": ["https://assets.jcaigc.cn/video1.mp4", "https://assets.jcaigc.cn/video2.mp4"],
  "timelines": [
    {"start": 0, "end": 3000000},
    {"start": 3000000, "end": 6000000}
  ],
  "height": 1080,
  "width": 1920,
  "mask": "圆形",
  "transition": "叠化",
  "transition_duration": 300000,
  "volume": 1.0
}
```

### 参数说明

| 参数名 | 类型 |必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| video_urls | array[string] |✅ | - |视频文件URL数组 |
| timelines | array[object] |✅ | - | 时间线配置数组 |
| height | integer |❌ | None |视频高度 |
| width | integer |❌ | None |视频宽度 |
| mask | string |❌ | None |遮罩名称：圆形、矩形、爱心、星形；会写入 `video_infos`，但 [add_videos](./add_videos.zh.md) 不会应用——请用 `add_masks` |
| transition | string |❌ | None |转场名称，可用值见 [add_videos](./add_videos.zh.md) |
| transition_duration | integer |❌ | None |转场时长(微秒) |
| volume | number |❌ | 1.0 |音量大小(0-10) |

### 可用转场名称

转场完整可用值清单，请参见 [添加视频（add_videos）](./add_videos.zh.md) 文档中的「支持的转场名称」。画面入场/出场/循环动画请参见 [添加图片（add_images）](./add_images.zh.md)。

##响应格式

### 成功响应 (200)

```json
{
  "code": 0,
  "message": "success",
  "infos": "[{\"video_url\":\"https://assets.jcaigc.cn/video1.mp4\",\"start\":0,\"end\":3000000,\"duration\":3000000,\"height\":1080,\"width\":1920,\"mask\":\"圆形\",\"transition\":\"叠化\",\"transition_duration\":300000,\"volume\":1.0},{\"video_url\":\"https://assets.jcaigc.cn/video2.mp4\",\"start\":3000000,\"end\":6000000,\"duration\":3000000,\"height\":1080,\"width\":1920,\"mask\":\"圆形\",\"transition\":\"叠化\",\"transition_duration\":300000,\"volume\":1.0}]"
}
```

###响应字段说明

| 字段名 | 类型 | 说明 |
|--------|------|------|
| infos | string |视频信息JSON字符串 |

### 错误响应

```json
{
  "code": 1001,
  "message": "参数校验失败"
}
```

## 使用示例

### cURL 示例

#### 1. 基本视频信息生成

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/video_infos \
  -H "Content-Type: application/json" \
  -d '{
    "video_urls": ["https://assets.jcaigc.cn/intro.mp4"],
    "timelines": [{"start": 0, "end": 5000000}],
    "height": 1080,
    "width": 1920
  }'
```

#### 2.带转场的视频信息（其中的 `mask` 不会生效，见 `add_masks`）

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/video_infos \
  -H "Content-Type: application/json" \
  -d '{
    "video_urls": ["https://assets.jcaigc.cn/clip1.mp4", "https://assets.jcaigc.cn/clip2.mp4"],
    "timelines": [{"start": 0, "end": 3000000}, {"start": 3000000, "end": 6000000}],
    "mask": "圆形",
    "transition": "叠化",
    "volume": 0.8
  }'
```

##错误码说明

|错误码 | 错误信息 | 说明 | 解决方案 |
|--------|----------|------|----------|
| 1001 | 参数校验失败 | 请求体未通过字段校验（缺少 `video_urls`/`timelines`、时间线项缺少 `start`/`end`，或类型错误） | 检查参数类型与必填字段 |

## 注意事项

1. **数组匹配**: `video_urls` 与 `timelines` 长度不一致时，按较短长度截断后继续生成（不会直接报错）
2. **时间单位**:所有时间参数使用微秒（1秒 = 1,000,000微秒）
3. **分辨率设置**: height和width参数用于设置视频显示分辨率
4. **遮罩类型**:`mask` 会以圆形、矩形、爱心或星形写入 `video_infos`，但 `add_videos` 不会应用，遮罩请用 `add_masks`
5. **音量范围**: volume值必须在0-10范围内
6. **网络访问**:视频URL必须可以正常访问

##工作流程

1.验证必填参数（video_urls, timelines）
2.按较短长度对齐两个数组
3.验证时间线参数有效性
4. 设置视频分辨率参数
5.应用转场参数并透传 `mask`（`add_videos` 不会应用）
6. 为每个视频URL生成对应的视频信息
7.将信息转换为JSON字符串格式
8. 返回处理结果

##相关接口

- [创建草稿](./create_draft.md)
- [添加视频](./add_videos.md)
- [时间线](./timelines.md)
- [保存草稿](./save_draft.md)

---

<div align="right">

📚 **项目资源**  
**GitHub**: [https://github.com/Hommy-master/capcut-mate](https://github.com/Hommy-master/capcut-mate)  
**Gitee**: [https://gitee.com/taohongmin-gitee/capcut-mate](https://gitee.com/taohongmin-gitee/capcut-mate)

</div>

### 语言切换
[中文版](./video_infos.zh.md) | [English](./video_infos.md)