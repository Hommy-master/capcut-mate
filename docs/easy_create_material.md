# easy_create_material 接口文档

## 接口概述

**接口名称**：easy_create_material  
**接口地址**：`POST /openapi/capcut-mate/v1/easy_create_material`  
**功能描述**：在现有草稿中添加多种类型的素材内容，包括音频、视频、图片和文字。该接口可以一次性向草稿添加多种媒体素材，自动处理素材的时长、尺寸等属性，并智能管理不同类型的媒体轨道。是视频创作的核心接口之一。

## 更多文档

📖 更多详细文档和教程请访问：[https://docs.jcaigc.cn](https://docs.jcaigc.cn)

## 请求参数

### 请求体 (application/json)

| 参数名 | 类型 | 必填 | 默认值 | 描述 |
|--------|------|------|--------|------|
| draft_url | string | 是 | - | 目标草稿的完整URL |
| audio_url | string | 是 | - | 音频文件URL，不能为空或null |
| text | string | 否 | null | 要添加的文字内容 |
| img_url | string | 否 | null | 图片文件URL |
| video_url | string | 否 | null | 视频文件URL |
| text_color | string | 否 | "#ffffff" | 文字颜色（十六进制格式） |
| font_size | integer | 否 | 15 | 字体大小 |
| text_transform_y | integer | 否 | 0 | 文字Y轴位置偏移 |

### 素材类型说明

| 素材类型 | 支持格式 | 自动处理 | 时长设置 |
|----------|----------|----------|----------|
| 音频 | MP3, WAV, AAC | 自动获取时长 | 使用音频原始时长 |
| 视频 | MP4, AVI, MOV | 自动获取属性 | 固定时长5秒 |
| 图片 | JPEG, PNG, GIF | 自动获取尺寸 | 默认时长3秒 |
| 文字 | UTF-8文本 | 支持样式设置 | 默认时长5秒 |

## 请求示例

### 添加所有类型素材

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

### 仅添加音频和文字

```json
{
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
  "audio_url": "https://assets.jcaigc.cn/background_music.mp3",
  "text": "欢迎观看",
  "text_color": "#0066ff",
  "font_size": 18
}
```

### 最简请求（仅音频）

```json
{
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
  "audio_url": "https://assets.jcaigc.cn/audio.wav"
}
```

## 响应格式

### 成功响应

```json
{
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258"
}
```

### 错误响应

#### 400 Bad Request - 参数验证失败

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "请求参数验证失败",
    "details": "audio_url 不能为空"
  }
}
```

#### 404 Not Found - 草稿不存在

```json
{
  "error": {
    "code": "DRAFT_NOT_FOUND", 
    "message": "草稿文件不存在",
    "details": "无法找到指定的草稿文件"
  }
}
```

#### 500 Internal Server Error - 素材创建失败

```json
{
  "error": {
    "code": "MATERIAL_CREATE_FAILED",
    "message": "素材创建失败", 
    "details": "添加音频素材时发生错误"
  }
}
```

## 错误码说明

| 错误码 | HTTP状态码 | 描述 | 解决方案 |
|--------|------------|------|----------|
| VALIDATION_ERROR | 400 | 请求参数验证失败 | 检查必填参数是否提供，参数格式是否正确 |
| DRAFT_NOT_FOUND | 404 | 草稿文件不存在 | 确认草稿URL是否正确，草稿是否已被删除 |
| MATERIAL_CREATE_FAILED | 500 | 素材创建失败 | 检查素材URL是否有效，网络连接是否正常 |
| INVALID_URL | 400 | URL格式无效 | 确认提供的URL格式正确且可访问 |

## 使用说明

### 参数说明

1. **draft_url**：必须是有效的剪映草稿URL，格式为 `https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258
2. **audio_url**：必填参数，必须提供有效的音频文件URL，不接受空字符串或null值
3. **可选素材**：text、img_url、video_url 都是可选参数，可以根据需要选择添加
4. **文字样式**：text_color支持十六进制颜色代码，font_size范围建议10-50
5. **位置偏移**：text_transform_y用于调整文字在画面中的垂直位置

### 素材处理规则

1. **音频处理**：
   - 自动解析音频时长
   - 添加到音频轨道
   - 支持多种音频格式

2. **视频处理**：
   - 固定显示时长5秒
   - 保持原始分辨率比例
   - 添加到视频轨道

3. **图片处理**：
   - 默认显示时长3秒
   - 自动获取图片尺寸
   - 添加到图片轨道

4. **文字处理**：
   - 默认显示时长5秒
   - 支持颜色和字体大小设置
   - 可调整垂直位置

### 注意事项

- 音频是必填参数，其他素材类型都是可选的
- 素材URL必须可公开访问，建议使用HTTPS协议
- 文字颜色使用标准十六进制格式（如 #ffffff、#000000）
- 所有时长都以微秒为单位进行内部计算
- 建议在添加素材前确保网络连接稳定

## 应用场景

1. **快速创建多媒体内容**：一次性添加背景音乐、视频片段、图片和标题文字
2. **批量素材导入**：为新创建的草稿快速添加多种类型的基础素材
3. **模板化创作**：基于固定的素材类型模板快速生成视频草稿
4. **自动化流程**：在自动化视频制作流程中批量添加预设的素材内容

## 相关接口

- [create_draft](./create_draft.md) - 创建新的草稿文件
- [add_audios](./add_audios.md) - 单独添加音频素材
- [add_videos](./add_videos.md) - 单独添加视频素材  
- [add_images](./add_images.md) - 单独添加图片素材
- [save_draft](./save_draft.md) - 保存草稿文件

## 技术实现

### 文件结构

```
src/
├── schemas/easy_create_material.py    # 请求/响应数据模型
├── service/easy_create_material.py    # 业务逻辑实现
└── router/v1.py                       # API路由定义
```

### 核心逻辑

1. **参数验证**：验证草稿URL和音频URL的有效性
2. **草稿加载**：从URL解析并加载草稿文件
3. **素材添加**：按类型分别添加音频、视频、图片、文字素材
4. **轨道管理**：自动管理不同类型素材的轨道分配
5. **文件保存**：保存更新后的草稿文件

### 日志记录

系统会记录以下关键操作的日志：
- 草稿加载成功/失败
- 各类型素材添加的详细过程
- 文件保存结果
- 错误异常信息

---

**版本信息**：v1.0  
**最后更新**：2025-09-24