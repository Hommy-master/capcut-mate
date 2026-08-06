# VIDEO_INFOS API 接口文档

## 🌐 语言切换
[中文版](./video_infos.zh.md) | [English](./video_infos.md)

## 接口信息

```
POST /openapi/capcut-mate/v1/video_infos
```

## 功能描述

根据视频URL和时间线生成视频信息。该接口将视频文件URL和时间线配置转换为剪映草稿所需的视频信息格式，支持遮罩和转场设置。

## 更多文档

📖 更多详细文档和教程请访问：[https://docs.jcaigc.cn](https://docs.jcaigc.cn)

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
  "mask": "circle",
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
| height | number |❌ | 1080 |视频高度 |
| width | number |❌ | 1920 |视频宽度 |
| mask | string |❌ | None |遮罩类型 |
| transition | string |❌ | None |转场名称，可用值见 [add_videos](./add_videos.zh.md) |
| transition_duration | number |❌ | 300000 |转场时长(微秒) |
| volume | number |❌ | 1.0 |音量大小(0.0-2.0) |

### 可用转场名称

转场完整可用值清单，请参见 [添加视频（add_videos）](./add_videos.zh.md) 文档中的「支持的转场名称」。画面入场/出场/循环动画请参见 [添加图片（add_images）](./add_images.zh.md)。

##响应格式

### 成功响应 (200)

```json
{
  "infos": "[{\"video_url\":\"https://assets.jcaigc.cn/video1.mp4\",\"start\":0,\"end\":3000000,\"duration\":5000000,\"height\":1080,\"width\":1920,\"mask\":\"circle\",\"transition\":\"叠化\",\"transition_duration\":300000,\"volume\":1.0},{\"video_url\":\"https://assets.jcaigc.cn/video2.mp4\",\"start\":3000000,\"end\":6000000,\"duration\":5000000,\"height\":1080,\"width\":1920,\"mask\":\"circle\",\"transition\":\"叠化\",\"transition_duration\":300000,\"volume\":1.0}]"
}
```

###响应字段说明

| 字段名 | 类型 | 说明 |
|--------|------|------|
| infos | string |视频信息JSON字符串 |

###错误响应 (4xx/5xx)

```json
{
  "detail": "错误信息描述"
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

#### 2.带遮罩和转场的视频信息

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/video_infos \
  -H "Content-Type: application/json" \
  -d '{
    "video_urls": ["https://assets.jcaigc.cn/clip1.mp4", "https://assets.jcaigc.cn/clip2.mp4"],
    "timelines": [{"start": 0, "end": 3000000}, {"start": 3000000, "end": 6000000}],
    "mask": "circle",
    "transition": "叠化",
    "volume": 0.8
  }'
```

##错误码说明

|错误码 | 错误信息 | 说明 | 解决方案 |
|--------|----------|------|----------|
| 400 | video_urls是必填项 |缺少视频URL参数 | 提供有效的视频URL数组 |
| 400 | timelines是必填项 |缺少时间线参数 | 提供有效的时间线数组 |
| 400 | 数组长度不匹配 | video_urls和timelines长度不一致 |确保两个数组长度相同 |
| 400 | volume值无效 |音量不在0.0-2.0范围内 | 使用0.0-2.0之间的音量值 |
| 404 |视频资源不存在 |视频URL无法访问 |检查视频URL是否可访问 |
| 500 |视频信息生成失败 |内部处理错误 |联技术支持 |

## 注意事项

1. **数组匹配**: video_urls和timelines数组长度必须相同
2. **时间单位**:所有时间参数使用微秒（1秒 = 1,000,000微秒）
3. **分辨率设置**: height和width参数用于设置视频显示分辨率
4. **遮罩类型**:支持circle、rectangle等遮罩类型
5. **音量范围**: volume值必须在0.0-2.0范围内
6. **网络访问**:视频URL必须可以正常访问

##工作流程

1.验证必填参数（video_urls, timelines）
2.检查数组长度匹配
3.验证时间线参数有效性
4. 设置视频分辨率参数
5.应用遮罩和转场参数
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