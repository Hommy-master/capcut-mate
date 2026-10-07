# EASY_CREATE_MATERIAL API 接口文档

## 🌐 语言切换
[中文版](./easy_create_material.zh.md) | [English](./easy_create_material.md)

## 接口信息

```
POST /openapi/capcut-mate/v1/easy_create_material
```

## 功能描述

在现有草稿中添加多种类型的素材内容，包括音频、视频、图片和文字。该接口可以一次性向草稿添加多种媒体素材，自动处理素材的时长、尺寸等属性，并智能管理不同类型的媒体轨道。是视频创作的核心接口之一。

## 请求参数

```json
{
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
  "audio_url": "https://assets.jcaigc.cn/audio.mp3",
  "text": "Hello World",
  "img_url": "https://s.coze.cn/t/JTa5Ne6_liY/",
  "video_url": "https://assets.jcaigc.cn/video.mp4",
  "text_color": "#ff0000",
  "font_size": 20,
  "text_transform_y": 100
}
```

### 参数说明

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| draft_url | string | ✅ | - | 目标草稿的完整URL |
| audio_url | string | ✅ | - | 音频文件URL，不能为空或null |
| text | string | ❌ | null | 要添加的文字内容 |
| img_url | string | ❌ | null | 图片文件URL |
| video_url | string | ❌ | null | 视频文件URL |
| text_color | string | ❌ | "#ffffff" | 文字颜色（十六进制格式） |
| font_size | integer | ❌ | 15 | 字体大小 |
| text_transform_y | integer | ❌ | 0 | 文字Y轴位置偏移 |

### 参数详解

#### 必填参数

- **draft_url**: 目标草稿的完整URL
  - 格式：必须是有效的剪映草稿URL
  - 示例：`"https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258"`

- **audio_url**: 音频文件URL
  - 必填参数，不能为空或"null"
  - 支持格式：MP3, WAV, AAC等常见音频格式
  - 说明：音频是必填参数，其他素材类型都是可选的

#### 可选参数

- **text**: 要添加的文字内容
  - 类型：UTF-8文本
  - 默认值：null（不添加文字）
  - 说明：如果提供，将添加文字素材到草稿中

- **img_url**: 图片文件URL
  - 类型：有效的图片URL
  - 默认值：null（不添加图片）
  - 支持格式：JPEG, PNG, GIF等常见图片格式
  - 说明：如果提供，将添加图片素材到草稿中

- **video_url**: 视频文件URL
  - 类型：有效的视频URL
  - 默认值：null（不添加视频）
  - 支持格式：MP4, AVI, MOV等常见视频格式
  - 说明：如果提供，将添加视频素材到草稿中

- **text_color**: 文字颜色
  - 类型：十六进制颜色代码
  - 默认值：`"#ffffff"`（白色）
  - 说明：设置文字颜色，使用标准十六进制格式（如 #ffffff、#000000）

- **font_size**: 字体大小
  - 类型：整数
  - 默认值：15
  - 说明：设置文字字体大小，建议范围10-50

- **text_transform_y**: 文字Y轴位置偏移
  - 类型：整数
  - 默认值：0
  - 说明：调整文字在画面中的垂直位置，单位为像素

#### 素材处理规则

- **音频处理**：
  - 固定 5 秒时长（音频实际更短时取实际时长）
  - 添加到音频轨道
  - 支持多种音频格式

- **视频处理**：
  - 固定显示时长5秒
  - 保持原始分辨率比例
  - 添加到视频轨道

- **图片处理**：
  - 默认显示时长3秒
  - 自动获取图片尺寸
  - 添加到图片轨道

- **文字处理**：
  - 默认显示时长5秒
  - 支持颜色和字体大小设置
  - 可调整垂直位置

## 响应格式

### 成功响应 (200)

```json
{
  "code": 0,
  "message": "success",
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258"
}
```

### 响应字段说明

| 字段名 | 类型 | 说明 |
|--------|------|------|
| draft_url | string | 更新后的草稿URL |

### 错误响应

```json
{
  "code": 2028,
  "message": "素材创建失败"
}
```

## 使用示例

### cURL 示例

#### 1. 添加所有类型素材

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/easy_create_material \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "audio_url": "https://assets.jcaigc.cn/audio.mp3",
    "text": "Hello World",
    "img_url": "https://s.coze.cn/t/JTa5Ne6_liY/",
    "video_url": "https://assets.jcaigc.cn/video.mp4",
    "text_color": "#ff0000",
    "font_size": 20,
    "text_transform_y": 100
  }'
```

#### 2. 仅添加音频和文字

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/easy_create_material \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "audio_url": "https://assets.jcaigc.cn/background_music.mp3",
    "text": "欢迎观看",
    "text_color": "#0066ff",
    "font_size": 18
  }'
```

#### 3. 最简请求（仅音频）

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/easy_create_material \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "audio_url": "https://assets.jcaigc.cn/audio.wav"
  }'
```

## 错误码说明

| 错误码 | 错误信息 | 说明 | 解决方案 |
|--------|----------|------|----------|
| 1001 | 参数校验失败 | `draft_url` 或 `audio_url` 缺失，或素材 URL 不是以 `http://` / `https://` 开头 | 检查参数类型与必填字段 |
| 2001 | 无效的草稿URL | `draft_url` 缺少 `draft_id`，或草稿不在缓存中 | 传入 `create_draft` 返回的 `draft_url` |
| 2028 | 素材创建失败 | 写入草稿过程出错 | 检查草稿状态与素材 URL 后重试 |
| 2042 | 草稿锁获取超时 | 同一草稿正在被其他操作占用（超时 30 秒） | 稍后重试 |

## 注意事项

1. **音频必填**: audio_url是必填参数，不能为空或null
2. **素材URL**: 素材URL必须可公开访问，建议使用HTTPS协议
3. **文字颜色**: text_color使用标准十六进制格式（如 #ffffff、#000000）
4. **字体大小**: font_size建议范围10-50
5. **位置偏移**: text_transform_y用于调整文字在画面中的垂直位置
6. **时长设置**: 不同素材类型有不同的默认显示时长
   - 音频：固定 5 秒（音频实际更短时取实际时长）
   - 视频：固定5秒
   - 图片：默认3秒
   - 文字：默认5秒
7. **轨道管理**: 系统自动创建不同类型素材的轨道
8. **性能考虑**: 避免同时添加大量素材

## 工作流程

1. 验证必填参数（draft_url, audio_url）
2. 从缓存中获取草稿
3. 创建音频轨道并添加音频素材
4. 如果提供，创建视频轨道并添加视频素材
5. 如果提供，创建图片轨道并添加图片素材
6. 如果提供，创建文字轨道并添加文字素材
7. 保存草稿
8. 返回更新后的草稿URL

## 相关接口

- [创建草稿](./create_draft.md)
- [添加视频](./add_videos.md)
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