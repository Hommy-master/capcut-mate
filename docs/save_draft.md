# save_draft 接口文档

## 接口概述

保存草稿项目到本地文件，生成可导入剪映的草稿文件夹。

---

## 接口信息

### RESTful API 端点

```
POST /save_draft
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
| **draft_id** | string | **是** | - | 草稿唯一标识符（必需参数） |
| draft_folder | string | 否 | null | 草稿保存的文件夹路径 |

---

## 响应参数

### 响应体 (JSON)

| 参数名 | 类型 | 说明 |
|--------|------|------|
| success | boolean | 请求是否成功 |
| output | object/string | 成功时返回任务信息 |
| error | string | 失败时的错误信息 |

### 成功响应的 output 字段

| 参数名 | 类型 | 说明 |
|--------|------|------|
| task_id | string | 保存任务的唯一标识符 |
| status | string | 任务状态（pending/processing/completed/failed） |
| draft_folder | string | 草稿保存的文件夹路径 |

---

## 请求示例

### 示例 1: 基础保存草稿

```bash
curl -X POST http://localhost:9001/save_draft \
  -H "Content-Type: application/json" \
  -d '{
    "draft_id": "dfd_1234567890abcdef"
  }'
```

**请求体 (JSON):**

```json
{
  "draft_id": "dfd_1234567890abcdef"
}
```

### 示例 2: 指定保存路径

```bash
curl -X POST http://localhost:9001/save_draft \
  -H "Content-Type: application/json" \
  -d '{
    "draft_id": "dfd_1234567890abcdef",
    "draft_folder": "/path/to/save/folder"
  }'
```

**请求体 (JSON):**

```json
{
  "draft_id": "dfd_1234567890abcdef",
  "draft_folder": "/path/to/save/folder"
}
```

### 示例 3: Python 请求示例

```python
import requests

url = "http://localhost:9001/save_draft"
headers = {
    "Content-Type": "application/json"
}
data = {
    "draft_id": "dfd_1234567890abcdef"
}

response = requests.post(url, json=data, headers=headers)
result = response.json()

print(f"Success: {result['success']}")
if result['success']:
    print(f"Task ID: {result['output']['task_id']}")
    print(f"Status: {result['output']['status']}")
    print(f"Draft Folder: {result['output']['draft_folder']}")
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
    "task_id": "task_abc123",
    "status": "processing",
    "draft_folder": "/output/draft/dfd_1234567890abcdef"
  },
  "error": ""
}
```

### 失败响应 - 缺少必需参数

**状态码:** 200 OK

```json
{
  "success": false,
  "output": "",
  "error": "Hi, the required parameter 'draft_id' is missing. Please add it and try again."
}
```

### 失败响应 - 保存错误

**状态码:** 200 OK

```json
{
  "success": false,
  "output": "",
  "error": "Error occurred while saving draft: Draft not found."
}
```

---

## 错误码说明

| 错误信息 | 说明 | 解决方案 |
|---------|------|---------|
| "Hi, the required parameter 'draft_id' is missing." | 缺少必需的 draft_id 参数 | 请在请求体中提供 draft_id 参数 |
| "Error occurred while saving draft: Draft not found." | 草稿不存在 | 检查 draft_id 是否正确，或先创建草稿 |
| "Error occurred while saving draft: ..." | 保存过程中出错 | 检查错误详情，确认权限和磁盘空间 |

---

## 使用场景

### 场景 1: 保存草稿到默认位置

```json
{
  "draft_id": "dfd_abc123"
}
```

### 场景 2: 查询保存状态

首先保存草稿获取 task_id：

```json
{
  "draft_id": "dfd_abc123"
}
```

然后使用 `/query_draft_status` 查询进度：

```json
{
  "task_id": "task_abc123"
}
```

---

## 保存后的文件结构

保存成功后，会在指定位置或默认位置生成以下文件结构：

```
dfd_1234567890abcdef/
├── draft_content.json          # 草稿内容
├── draft_info.json             # 草稿信息
├── draft_meta_info.json        # 草稿元信息
└── assets/                     # 资源文件夹
    ├── video/                  # 视频文件
    ├── audio/                  # 音频文件
    └── image/                  # 图片文件
```

---

## 导入剪映

保存后的草稿可以直接导入剪映：

1. **Windows 剪映**
   - 复制草稿文件夹到：`C:\Users\[用户名]\AppData\Local\JianyingPro\User Data\Projects\com.lveditor.draft\`

2. **macOS 剪映**
   - 复制草稿文件夹到：`~/Library/Containers/com.lveditor.LveDitor/Data/Movies/JianyingPro/User Data/Projects/com.lveditor.draft/`

3. **剪映国际版 (CapCut)**
   - 复制草稿文件夹到对应的 CapCut 草稿目录

---

## 注意事项

1. **必需参数**: draft_id 是必需的
2. **异步处理**: 保存操作是异步的，返回 task_id 后可以查询状态
3. **文件夹权限**: 确保有写入权限到指定的 draft_folder
4. **草稿存在性**: 保存前确保草稿已创建并添加了内容
5. **覆盖警告**: 如果目标位置已存在同名草稿，可能会被覆盖
6. **资源文件**: 会自动下载和保存所有引用的远程资源

---

## 工作流程

```
1. 创建草稿 (create_draft)
   ↓
2. 添加各种素材 (add_video/audio/text/image)
   ↓
3. 保存草稿 (save_draft) ← 当前接口
   ↓
4. 查询保存状态 (query_draft_status)
   ↓
5. 导入剪映进行编辑
```

---

## 相关接口

- `POST /create_draft` - 创建新草稿
- `POST /query_draft_status` - 查询保存状态
- `POST /query_script` - 查询草稿脚本
- `POST /generate_draft_url` - 生成草稿预览 URL

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
