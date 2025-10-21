# create_draft 接口文档

## 接口概述

创建一个新的剪映草稿项目，支持自定义画布宽度和高度。

---

## 接口信息

### RESTful API 端点

```
POST /create_draft
```

### Content-Type

```
application/json
```

---

## 请求参数

### 请求体 (JSON)

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| width | integer | 否 | 1080 | 画布宽度（像素） |
| height | integer | 否 | 1920 | 画布高度（像素） |

---

## 响应参数

### 响应体 (JSON)

| 参数名 | 类型 | 说明 |
|--------|------|------|
| success | boolean | 请求是否成功 |
| output | object | 成功时返回草稿信息 |
| error | string | 失败时的错误信息 |

### 成功响应的 output 字段

| 参数名 | 类型 | 说明 |
|--------|------|------|
| draft_id | string | 草稿唯一标识符 |
| draft_url | string | 草稿预览 URL |

---

## 请求示例

### 示例 1: 创建默认竖屏草稿（1080x1920）

```bash
curl -X POST http://localhost:9001/create_draft \
  -H "Content-Type: application/json" \
  -d '{}'
```

**请求体 (JSON):**

```json
{}
```

### 示例 2: 创建横屏草稿（1920x1080）

```bash
curl -X POST http://localhost:9001/create_draft \
  -H "Content-Type: application/json" \
  -d '{
    "width": 1920,
    "height": 1080
  }'
```

**请求体 (JSON):**

```json
{
  "width": 1920,
  "height": 1080
}
```

### 示例 3: 创建方形草稿（1080x1080）

```bash
curl -X POST http://localhost:9001/create_draft \
  -H "Content-Type: application/json" \
  -d '{
    "width": 1080,
    "height": 1080
  }'
```

**请求体 (JSON):**

```json
{
  "width": 1080,
  "height": 1080
}
```

### 示例 4: Python 请求示例

```python
import requests

url = "http://localhost:9001/create_draft"
headers = {
    "Content-Type": "application/json"
}
data = {
    "width": 1920,
    "height": 1080
}

response = requests.post(url, json=data, headers=headers)
result = response.json()

print(f"Success: {result['success']}")
if result['success']:
    print(f"Draft ID: {result['output']['draft_id']}")
    print(f"Draft URL: {result['output']['draft_url']}")
else:
    print(f"Error: {result['error']}")
```

---

## 响应示例

### 成功响应

**状态码:** 200 OK

```json
{
  "success": true,
  "output": {
    "draft_id": "dfd_1234567890abcdef",
    "draft_url": "http://example.com/preview?draft_id=dfd_1234567890abcdef"
  },
  "error": ""
}
```

### 失败响应

**状态码:** 200 OK

```json
{
  "success": false,
  "output": "",
  "error": "Error occurred while creating draft: Invalid dimensions."
}
```

---

## 常见画布尺寸

| 类型 | 宽度 | 高度 | 说明 |
|------|------|------|------|
| 竖屏 | 1080 | 1920 | 默认，适合抖音、快手等短视频平台 |
| 横屏 | 1920 | 1080 | 适合 YouTube、B站横屏视频 |
| 方形 | 1080 | 1080 | 适合 Instagram 等社交平台 |
| 4K竖屏 | 2160 | 3840 | 高清竖屏视频 |
| 4K横屏 | 3840 | 2160 | 高清横屏视频 |

---

## 使用场景

### 场景 1: 创建抖音短视频草稿

```json
{
  "width": 1080,
  "height": 1920
}
```

### 场景 2: 创建 YouTube 视频草稿

```json
{
  "width": 1920,
  "height": 1080
}
```

### 场景 3: 创建 Instagram 方形视频

```json
{
  "width": 1080,
  "height": 1080
}
```

---

## 注意事项

1. **默认值**: 如果不提供任何参数，将创建 1080x1920 的竖屏草稿
2. **分辨率**: 建议使用常见的视频分辨率，避免过大或过小的尺寸
3. **草稿 ID**: 返回的 draft_id 需要保存，后续所有操作都需要使用它
4. **预览 URL**: draft_url 可用于在浏览器中预览草稿内容

---

## 工作流程

```
1. 调用 create_draft 创建草稿
   ↓
2. 保存返回的 draft_id
   ↓
3. 使用 draft_id 添加视频、音频、文字等素材
   ↓
4. 调用 save_draft 保存草稿
   ↓
5. 导入剪映或在线预览
```

---

## 相关接口

- `POST /add_video` - 添加视频到草稿
- `POST /add_audio` - 添加音频到草稿
- `POST /add_text` - 添加文字到草稿
- `POST /add_image` - 添加图片到草稿
- `POST /save_draft` - 保存草稿
- `POST /query_script` - 查询草稿脚本

---

## 更新日志

| 版本 | 日期 | 说明 |
|------|------|------|
| 1.0 | 2025-10-21 | 初始版本 |

---

## 技术支持

如有问题，请联系：
- Email: sguann2023@gmail.com
- GitHub Issues: https://github.com/sun-guannan/CapCutAPI/issues
