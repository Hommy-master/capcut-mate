# 剪映草稿创建 API 接口文档

## 目录

- [1. 草稿管理核心接口](#1-草稿管理核心接口)
  - [1.1 创建草稿 (create_draft)](#11-创建草稿-create_draft)
  - [1.2 保存草稿 (save_draft)](#12-保存草稿-save_draft)
  - [1.3 获取草稿 (get_draft)](#13-获取草稿-get_draft)
- [2. 素材添加接口](#2-素材添加接口)
- [3. 完整接口列表](#3-完整接口列表)

---

## 1. 草稿管理核心接口

### 1.1 创建草稿 (create_draft)

创建一个新的剪映草稿项目，设置画布尺寸。这是所有视频编辑操作的起点。

#### 接口信息

- **接口路径**: `/openapi/capcut-mate/v1/create_draft`
- **请求方法**: `POST`
- **Content-Type**: `application/json`

#### 请求参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| width | integer | 否 | 1920 | 视频宽度（像素），必须 ≥ 1 |
| height | integer | 否 | 1080 | 视频高度（像素），必须 ≥ 1 |

#### 常用分辨率

| 视频类型 | width | height | 说明 |
|----------|-------|--------|------|
| 横屏视频（16:9） | 1920 | 1080 | 标准高清横屏 |
| 竖屏视频（9:16） | 1080 | 1920 | 抖音/快手竖屏 |
| 方形视频（1:1） | 1080 | 1080 | 社交媒体方形 |
| 4K横屏 | 3840 | 2160 | 超高清横屏 |

#### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| draft_url | string | 草稿URL，用于后续所有操作 |
| tip_url | string | 帮助文档链接 |

#### 请求示例

```bash
curl -X POST "http://localhost:30000/openapi/capcut-mate/v1/create_draft" \
  -H "Content-Type: application/json" \
  -d '{
    "width": 1080,
    "height": 1920
  }'
```

#### 响应示例

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "draft_url": "http://localhost:30000/openapi/capcut-mate/v1/get_draft?draft_id=20231215123456abcd1234",
    "tip_url": "https://example.com/help"
  }
}
```

#### 业务逻辑

1. 生成唯一的草稿ID（格式：`时间戳(14位) + UUID前8位`）
2. 从模板目录复制默认模板到新草稿目录
3. 根据传入的宽高参数修改画布配置
4. 创建空的主轨道（main_track）
5. 保存草稿文件（同时生成 `draft_info.json` 和 `draft_content.json`）
6. 将草稿对象缓存到内存中
7. 返回草稿访问URL

#### 注意事项

- 创建的草稿会自动启用双文件兼容模式
- 草稿ID在服务器重启后依然有效（持久化存储）
- 返回的 `draft_url` 必须保存，用于后续所有编辑操作

---

### 1.2 保存草稿 (save_draft)

保存当前草稿的所有修改，确保编辑内容持久化到文件系统。

#### 接口信息

- **接口路径**: `/openapi/capcut-mate/v1/save_draft`
- **请求方法**: `POST`
- **Content-Type**: `application/json`

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| draft_url | string | 是 | 草稿URL（create_draft 返回的 draft_url） |

#### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| draft_url | string | 草稿URL |

#### 请求示例

```bash
curl -X POST "http://localhost:30000/openapi/capcut-mate/v1/save_draft" \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "http://localhost:30000/openapi/capcut-mate/v1/get_draft?draft_id=20231215123456abcd1234"
  }'
```

#### 响应示例

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "draft_url": "http://localhost:30000/openapi/capcut-mate/v1/get_draft?draft_id=20231215123456abcd1234"
  }
}
```

#### 业务逻辑

1. 从 draft_url 中解析出 draft_id
2. 验证 draft_id 是否在缓存中存在
3. 从缓存获取草稿对象
4. 调用草稿对象的 save() 方法，将内存中的修改写入文件
5. 返回草稿URL

#### 并发保护机制

接口使用异步锁机制防止并发写入冲突：
- **锁超时时间**: 30秒
- **锁粒度**: 每个草稿ID独立加锁
- **自动释放**: 无论成功或失败都会自动释放锁

#### 注意事项

- 每次调用 add_videos、add_audios 等编辑接口后，建议调用此接口保存
- 如果草稿URL无效或草稿不在缓存中，会抛出异常
- 支持高并发场景，同一草稿的多个请求会排队处理

---

### 1.3 获取草稿 (get_draft)

获取指定草稿的所有文件列表，用于下载或查看草稿内容。

#### 接口信息

- **接口路径**: `/openapi/capcut-mate/v1/get_draft`
- **请求方法**: `GET`
- **Content-Type**: `application/json`

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| draft_id | string | 是 | 草稿ID（长度 20-32 字符） |

#### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| files | array[string] | 草稿文件下载URL列表 |

#### 请求示例

```bash
curl -X GET "http://localhost:30000/openapi/capcut-mate/v1/get_draft?draft_id=20231215123456abcd1234"
```

#### 响应示例

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "files": [
      "http://localhost:30000/drafts/20231215123456abcd1234/draft_info.json",
      "http://localhost:30000/drafts/20231215123456abcd1234/draft_content.json",
      "http://localhost:30000/drafts/20231215123456abcd1234/draft_meta_info.json"
    ]
  }
}
```

#### 业务逻辑

1. 验证 draft_id 参数是否为空
2. 检查草稿目录是否存在
3. 遍历草稿目录，获取所有文件路径
4. 将文件路径转换为可下载的HTTP URL
5. 返回文件URL列表

#### 注意事项

- draft_id 可以从 draft_url 中提取（URL参数中的 draft_id）
- 返回的文件URL可以直接通过浏览器或HTTP客户端下载
- 如果草稿目录不存在，会抛出异常

---

## 2. 素材添加接口

在创建草稿后，可以使用以下接口添加各种素材：

### 2.1 添加视频 (add_videos)

向草稿添加视频素材。

- **接口路径**: `/openapi/capcut-mate/v1/add_videos`
- **请求方法**: `POST`
- **核心参数**: 
  - `draft_url`: 草稿URL
  - `video_infos`: 视频信息列表（JSON字符串）
  - `alpha`: 透明度 (0.0-1.0)
  - `scale_x`, `scale_y`: 缩放比例
  - `transform_x`, `transform_y`: 位置偏移

### 2.2 添加音频 (add_audios)

向草稿批量添加音频。

- **接口路径**: `/openapi/capcut-mate/v1/add_audios`
- **请求方法**: `POST`
- **核心参数**:
  - `draft_url`: 草稿URL
  - `audio_infos`: 音频信息列表（JSON字符串）

### 2.3 添加图片 (add_images)

向草稿批量添加图片素材。

- **接口路径**: `/openapi/capcut-mate/v1/add_images`
- **请求方法**: `POST`
- **核心参数**:
  - `draft_url`: 草稿URL
  - `image_infos`: 图片信息列表（JSON字符串）
  - 支持动画、转场效果

### 2.4 添加字幕 (add_captions)

向草稿批量添加字幕。

- **接口路径**: `/openapi/capcut-mate/v1/add_captions`
- **请求方法**: `POST`
- **核心参数**:
  - `draft_url`: 草稿URL
  - `captions`: 字幕信息列表
  - `text_color`: 文字颜色
  - `font_size`: 字体大小
  - 支持关键词高亮、样式设置

### 2.5 添加贴纸 (add_sticker)

向草稿添加贴纸素材。

- **接口路径**: `/openapi/capcut-mate/v1/add_sticker`
- **请求方法**: `POST`
- **核心参数**:
  - `draft_url`: 草稿URL
  - `sticker_id`: 贴纸ID
  - `start`, `end`: 时间范围
  - `scale`: 缩放比例
  - `transform_x`, `transform_y`: 位置

### 2.6 添加特效 (add_effects)

向草稿添加视觉特效。

- **接口路径**: `/openapi/capcut-mate/v1/add_effects`
- **请求方法**: `POST`
- **核心参数**:
  - `draft_url`: 草稿URL
  - `effect_infos`: 特效信息列表（JSON字符串）

### 2.7 添加滤镜 (add_filters)

向草稿添加滤镜效果。

- **接口路径**: `/openapi/capcut-mate/v1/add_filters`
- **请求方法**: `POST`
- **核心参数**:
  - `draft_url`: 草稿URL
  - `filter_infos`: 滤镜信息列表（JSON字符串）

### 2.8 添加遮罩 (add_masks)

向草稿添加遮罩效果。

- **接口路径**: `/openapi/capcut-mate/v1/add_masks`
- **请求方法**: `POST`
- **核心参数**:
  - `draft_url`: 草稿URL
  - `segment_ids`: 目标片段ID列表
  - `name`: 遮罩类型
  - `width`, `height`: 遮罩尺寸

### 2.9 添加关键帧 (add_keyframes)

添加关键帧动画。

- **接口路径**: `/openapi/capcut-mate/v1/add_keyframes`
- **请求方法**: `POST`
- **核心参数**:
  - `draft_url`: 草稿URL
  - `keyframes`: 关键帧信息列表

---

## 3. 完整接口列表

### 3.1 草稿管理
| 接口 | 路径 | 方法 | 说明 |
|------|------|------|------|
| create_draft | /v1/create_draft | POST | 创建草稿 |
| save_draft | /v1/save_draft | POST | 保存草稿 |
| get_draft | /v1/get_draft | GET | 获取草稿文件列表 |

### 3.2 素材添加
| 接口 | 路径 | 方法 | 说明 |
|------|------|------|------|
| add_videos | /v1/add_videos | POST | 添加视频 |
| add_audios | /v1/add_audios | POST | 添加音频 |
| add_images | /v1/add_images | POST | 添加图片 |
| add_sticker | /v1/add_sticker | POST | 添加贴纸 |
| add_captions | /v1/add_captions | POST | 添加字幕 |
| add_effects | /v1/add_effects | POST | 添加特效 |
| add_filters | /v1/add_filters | POST | 添加滤镜 |
| add_masks | /v1/add_masks | POST | 添加遮罩 |
| add_keyframes | /v1/add_keyframes | POST | 添加关键帧 |
| add_text_style | /v1/add_text_style | POST | 创建富文本样式 |

### 3.3 资源查询
| 接口 | 路径 | 方法 | 说明 |
|------|------|------|------|
| get_text_animations | /v1/get_text_animations | POST | 获取文字动画列表 |
| get_image_animations | /v1/get_image_animations | POST | 获取图片动画列表 |
| get_effects | /v1/get_effects | POST | 获取特效列表 |
| get_filters | /v1/get_filters | POST | 获取滤镜列表 |
| get_text_effects | /v1/get_text_effects | POST | 获取花字效果列表 |
| search_sticker | /v1/search_sticker | POST | 搜索贴纸 |
| get_audio_duration | /v1/get_audio_duration | POST | 获取音频时长 |

### 3.4 视频生成
| 接口 | 路径 | 方法 | 说明 |
|------|------|------|------|
| gen_video | /v1/gen_video | POST | 生成视频（云渲染） |
| gen_video_status | /v1/gen_video_status | POST | 查询视频生成状态 |
| gen_video_active_count | /v1/gen_video_active_count | GET | 查询活跃渲染任务数 |

### 3.5 快速工具
| 接口 | 路径 | 方法 | 说明 |
|------|------|------|------|
| easy_create_material | /v1/easy_create_material | POST | 快速创建素材（一次性添加多种素材） |

### 3.6 辅助工具
| 接口 | 路径 | 方法 | 说明 |
|------|------|------|------|
| timelines | /v1/timelines | POST | 创建时间线 |
| audio_timelines | /v1/audio_timelines | POST | 基于音频计算时间线 |
| audio_infos | /v1/audio_infos | POST | 生成音频信息JSON |
| imgs_infos | /v1/imgs_infos | POST | 生成图片信息JSON |
| caption_infos | /v1/caption_infos | POST | 生成字幕信息JSON |
| srt_infos | /v1/srt_infos | POST | 解析SRT文件生成字幕信息JSON |
| effect_infos | /v1/effect_infos | POST | 生成特效信息JSON |
| filter_infos | /v1/filter_infos | POST | 生成滤镜信息JSON |
| keyframes_infos | /v1/keyframes_infos | POST | 生成关键帧信息JSON |
| video_infos | /v1/video_infos | POST | 生成视频信息JSON |
| get_url | /v1/get_url | POST | 提取URL |
| str_list_to_objs | /v1/str_list_to_objs | POST | 字符串列表转对象 |
| str_to_list | /v1/str_to_list | POST | 字符串转列表 |
| objs_to_str_list | /v1/objs_to_str_list | POST | 对象列表转字符串 |

---

## 4. 典型工作流程

### 4.1 基础视频创建流程

```
1. create_draft (创建草稿)
   ↓
2. add_videos (添加视频素材)
   ↓
3. add_audios (添加背景音乐)
   ↓
4. add_captions (添加字幕)
   ↓
5. save_draft (保存草稿)
   ↓
6. gen_video (生成最终视频)
```

### 4.2 完整编辑流程

```
1. create_draft (创建草稿，设置分辨率)
   ↓
2. add_videos (添加视频片段)
   ↓
3. add_images (添加图片素材)
   ↓
4. add_filters (添加滤镜)
   ↓
5. add_effects (添加特效)
   ↓
6. add_captions (添加字幕)
   ↓
7. add_keyframes (添加关键帧动画)
   ↓
8. add_audios (添加背景音乐)
   ↓
9. add_sticker (添加贴纸装饰)
   ↓
10. save_draft (保存草稿)
   ↓
11. gen_video (生成视频)
   ↓
12. gen_video_status (查询渲染进度)
```

---

## 5. 错误码说明

| 错误码 | 说明 | 解决方案 |
|--------|------|----------|
| INVALID_DRAFT_URL | 无效的草稿URL | 检查draft_url参数是否正确 |
| DRAFT_CREATE_FAILED | 草稿创建失败 | 检查服务器文件系统权限 |
| DRAFT_LOCK_TIMEOUT | 获取草稿锁超时 | 等待当前操作完成或增加超时时间 |

---

## 6. 注意事项

### 6.1 并发安全
- 所有编辑操作（add_videos、add_audios等）都使用了异步锁机制
- 同一草稿的并发请求会自动排队，避免数据冲突
- 默认锁超时时间为30秒

### 6.2 性能优化
- 草稿对象会缓存在内存中，提高访问速度
- 建议批量操作时使用 `easy_create_material` 接口
- 大量素材添加后及时调用 `save_draft` 持久化

### 6.3 URL格式
- draft_url 格式: `http://host:port/openapi/capcut-mate/v1/get_draft?draft_id=xxx`
- 所有素材URL必须是可访问的HTTP/HTTPS地址
- 本地文件需要先上传到服务器或使用文件服务

### 6.4 文件兼容性
- 系统自动维护 `draft_info.json` 和 `draft_content.json` 两个文件
- 支持剪映PC版和移动版的草稿格式
- 草稿可以直接导入剪映客户端编辑

---

## 7. 相关文档链接

- [添加视频详细文档](./add_videos.md)
- [添加音频详细文档](./add_audios.md)
- [添加字幕详细文档](./add_captions.md)
- [生成视频详细文档](./gen_video.md)
- [快速创建素材文档](./easy_create_material.md)

---

## 8. API 调试

### 8.1 在线文档
启动服务后访问：
- Swagger UI: http://localhost:30000/docs
- ReDoc: http://localhost:30000/redoc

### 8.2 Postman 集合
项目提供了完整的 Postman Collection，可以导入 `openapi.yaml` 文件进行测试。

---

**文档版本**: v1.0  
**最后更新**: 2024-12-15  
**维护者**: CapCut Mate Team
