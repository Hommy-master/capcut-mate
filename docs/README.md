# CapCut Mate API 文档中心

欢迎使用 CapCut Mate API 文档！本文档提供了所有 RESTful API 接口的详细说明。

---

## 📚 文档导航

### 🎬 草稿管理

| 接口 | 文档 | 说明 |
|------|------|------|
| `POST /create_draft` | [create_draft.md](create_draft.md) | 创建新的剪映草稿 |
| `POST /save_draft` | [save_draft.md](save_draft.md) | 保存草稿到本地 |
| `POST /query_script` | - | 查询草稿脚本内容 |
| `POST /generate_draft_url` | - | 生成草稿预览 URL |

### 🎥 媒体素材

| 接口 | 文档 | 说明 |
|------|------|------|
| `POST /add_video` | [add_video.md](add_video.md) | 添加视频到草稿 |
| `POST /add_audio` | [add_audio.md](add_audio.md) | 添加音频到草稿 |
| `POST /add_image` | [add_image.md](add_image.md) | 添加图片到草稿 |
| `POST /add_text` | [add_text.md](add_text.md) | 添加文字到草稿 |
| `POST /add_subtitle` | - | 添加字幕（SRT格式） |
| `POST /add_sticker` | - | 添加贴纸到草稿 |

### 🎨 特效和动画

| 接口 | 文档 | 说明 |
|------|------|------|
| `POST /add_effect` | - | 添加视频特效 |
| `POST /add_video_keyframe` | - | 添加关键帧动画 |
| `GET /get_transition_types` | [get_transition_types.md](get_transition_types.md) | 获取转场类型列表 |
| `GET /get_mask_types` | [get_mask_types.md](get_mask_types.md) | 获取蒙版类型列表 |

### 🎭 动画类型查询

| 接口 | 文档 | 说明 |
|------|------|------|
| `GET /get_intro_animation_types` | - | 获取入场动画类型 |
| `GET /get_outro_animation_types` | - | 获取出场动画类型 |
| `GET /get_combo_animation_types` | - | 获取组合动画类型 |
| `GET /get_text_intro_types` | - | 获取文字入场动画 |
| `GET /get_text_outro_types` | - | 获取文字出场动画 |
| `GET /get_text_loop_anim_types` | - | 获取文字循环动画 |

### 📋 资源查询

| 接口 | 文档 | 说明 |
|------|------|------|
| `GET /get_font_types` | - | 获取可用字体列表 |
| `GET /get_audio_effect_types` | - | 获取音效类型列表 |
| `GET /get_video_scene_effect_types` | - | 获取场景特效类型 |
| `GET /get_video_character_effect_types` | - | 获取人物特效类型 |

### 📊 任务查询

| 接口 | 文档 | 说明 |
|------|------|------|
| `POST /query_draft_status` | - | 查询草稿保存状态 |

---

## 🚀 快速开始

### 1. 创建草稿并添加内容

```python
import requests

base_url = "http://localhost:9001"

# 1. 创建草稿
response = requests.post(f"{base_url}/create_draft", json={
    "width": 1080,
    "height": 1920
})
draft_id = response.json()['output']['draft_id']

# 2. 添加视频
requests.post(f"{base_url}/add_video", json={
    "video_url": "https://example.com/video.mp4",
    "draft_id": draft_id,
    "start": 0,
    "end": 10
})

# 3. 添加文字
requests.post(f"{base_url}/add_text", json={
    "text": "Hello World",
    "start": 0,
    "end": 5,
    "draft_id": draft_id,
    "font_size": 12.0,
    "font_color": "#FFFFFF"
})

# 4. 保存草稿
requests.post(f"{base_url}/save_draft", json={
    "draft_id": draft_id
})
```

---

## 📖 通用说明

### 接口基础信息

- **服务地址**: `http://localhost:9001`
- **Content-Type**: `application/json`
- **字符编码**: UTF-8

### 通用响应格式

所有接口都返回统一的 JSON 格式：

```json
{
  "success": true,        // 请求是否成功
  "output": {},          // 成功时的返回数据
  "error": ""            // 失败时的错误信息
}
```

### 通用参数说明

#### 画布尺寸

| 类型 | 宽度 | 高度 | 说明 |
|------|------|------|------|
| 竖屏 | 1080 | 1920 | 抖音、快手等短视频 |
| 横屏 | 1920 | 1080 | YouTube、B站横屏 |
| 方形 | 1080 | 1080 | Instagram 等 |

#### 坐标系统

- **transform_x/y**: 相对坐标，范围 -1.0 到 1.0
  - `0` 表示中心位置
  - `transform_y = -1.0` 表示顶部
  - `transform_y = 1.0` 表示底部
  - `transform_x = -1.0` 表示左侧
  - `transform_x = 1.0` 表示右侧

#### 时间参数

- **start**: 素材开始时间（秒）
- **end**: 素材结束时间（秒）
- **target_start**: 素材在时间轴上的起始位置（秒）
- **duration**: 素材显示时长（秒）

#### 颜色格式

使用 16 进制颜色码，格式为 `#RRGGBB`，例如：
- `#FF0000` - 红色
- `#00FF00` - 绿色
- `#0000FF` - 蓝色
- `#FFFFFF` - 白色
- `#000000` - 黑色

---

## 🔧 常见问题

### Q: 如何获取 draft_id？

A: 调用 `/create_draft` 接口会返回 draft_id，保存它用于后续操作。

### Q: 如何预览草稿？

A: 使用返回的 `draft_url` 在浏览器中预览，或调用 `/generate_draft_url` 生成预览链接。

### Q: 如何导入剪映？

A: 调用 `/save_draft` 保存草稿后，将生成的文件夹复制到剪映的草稿目录。

### Q: 支持哪些媒体格式？

A: 
- **视频**: MP4, MOV, AVI, MKV 等
- **音频**: MP3, WAV, AAC, M4A 等
- **图片**: JPG, PNG, GIF, WebP 等

### Q: 如何添加转场效果？

A: 在 `add_video` 或 `add_image` 时设置 `transition` 和 `transition_duration` 参数。

### Q: 如何使用蒙版？

A: 先调用 `/get_mask_types` 获取可用蒙版，然后在 `add_video` 或 `add_image` 时设置蒙版参数。

---

## 📝 注意事项

1. **草稿 ID**: 创建草稿后务必保存返回的 draft_id
2. **URL 格式**: 所有媒体 URL 必须是可访问的完整地址
3. **参数验证**: 注意必填参数和参数类型
4. **时间重叠**: 注意不同素材的时间轴不要冲突
5. **性能考虑**: 大文件和复杂效果会影响处理速度

---

## 🌟 最佳实践

### 1. 错误处理

```python
response = requests.post(url, json=data)
result = response.json()

if result['success']:
    print(f"Success: {result['output']}")
else:
    print(f"Error: {result['error']}")
```

### 2. 批量操作

```python
draft_id = create_draft()

# 添加多个视频
for video_url in video_list:
    add_video(video_url, draft_id)

# 最后保存
save_draft(draft_id)
```

### 3. 动画效果组合

```python
# 先获取可用动画
intro_types = get_intro_animation_types()
transition_types = get_transition_types()

# 使用动画
add_image(
    image_url=url,
    intro_animation=intro_types[0]['name'],
    transition=transition_types[0]['name']
)
```

---

## 🔗 相关资源

- [GitHub 仓库](https://github.com/sun-guannan/CapCutAPI)
- [在线体验](https://www.capcutapi.top)
- [问题反馈](https://github.com/sun-guannan/CapCutAPI/issues)

---

## 📧 技术支持

如有问题，请联系：
- **Email**: sguann2023@gmail.com
- **GitHub Issues**: https://github.com/sun-guannan/CapCutAPI/issues

---

## 📅 更新日志

| 版本 | 日期 | 说明 |
|------|------|------|
| 1.0 | 2025-10-21 | 初始版本，包含主要接口文档 |

---

**© 2025 CapCut Mate - 让视频编辑更简单**
