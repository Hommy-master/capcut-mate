# GET_DRAFT API 接口文档

## 🌐 语言切换
[中文版](./get_draft.zh.md) | [English](./get_draft.md)

## 接口信息

```
GET /openapi/capcut-mate/v1/get_draft
```

## 功能描述

获取草稿文件列表。该接口用于获取指定草稿ID对应的所有文件列表，可以查看草稿中包含的素材文件、配置文件等信息。通常用于草稿内容的预览、文件管理或状态检查。

## 请求参数

### Query参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| draft_id | string | ✅ | - | 草稿ID，长度为20-32位字符 |

### 参数详解

#### draft_id

- **类型**: 字符串
- **必填**: 是
- **长度**: 20-32位字符
- **格式**: 通常为UUID格式或类似的唯一标识符
- **示例**: `2025092811473036584258`
- **获取方式**: 通常从draft_url中提取或由create_draft接口返回

## 响应格式

### 成功响应 (200)

```json
{
  "code": 0,
  "message": "success",
  "files": [
    "https://capcut-mate.jcaigc.cn/output/draft/2025092811473036584258/draft_info.json",
    "https://capcut-mate.jcaigc.cn/output/draft/2025092811473036584258/draft_content.json",
    "https://capcut-mate.jcaigc.cn/output/draft/2025092811473036584258/draft_meta_info.json"
  ]
}
```

### 响应字段说明

| 字段名 | 类型 | 说明 |
|--------|------|------|
| files | array | 草稿内文件的下载URL列表 |

### 错误响应

```json
{
  "code": 2001,
  "message": "无效的草稿URL"
}
```

## 使用示例

### cURL 示例

#### 1. 基本获取草稿文件列表

```bash
curl -X GET "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258" \
  -H "Content-Type: application/json"
```

#### 2. 使用完整的draft_id

```bash
curl -X GET "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025100512300012345678" \
  -H "Content-Type: application/json"
```

## 错误码说明

| 错误码 | 错误信息 | 说明 | 解决方案 |
|--------|----------|------|----------|
| 1001 | 参数校验失败 | `draft_id` 缺失或长度不在 20-32 位之间 | 传入 20-32 位的 `draft_id` |
| 2001 | 无效的草稿URL | 草稿目录不存在 | 确认 `draft_id` 是否正确且草稿存在 |

## 注意事项

1. **参数格式**: 确保draft_id格式正确且长度在20-32位之间
2. **ID提取**: 从draft_url正确提取draft_id
3. **文件类型**: 返回的文件列表包含多种类型的文件
4. **权限验证**: 确保有权限访问指定的草稿
5. **实时性**: 文件列表可能不是实时更新的，存在一定延迟
6. **文件状态**: 列表中的文件可能处于不同的处理状态

## 工作流程

1. 验证draft_id参数
2. 检查draft_id格式和长度
3. 查找指定的草稿
4. 获取草稿关联的所有文件
5. 返回文件列表

## 相关接口

- [创建草稿](./create_draft.md)
- [保存草稿](./save_draft.md)
- [添加视频](./add_videos.md)
- [添加音频](./add_audios.md)
- [添加图片](./add_images.md)
- [生成视频](./gen_video.md)

---

<div align="right">

📚 **项目资源**  
**GitHub**: [https://github.com/Hommy-master/capcut-mate](https://github.com/Hommy-master/capcut-mate)  
**Gitee**: [https://gitee.com/taohongmin-gitee/capcut-mate](https://gitee.com/taohongmin-gitee/capcut-mate)

</div>

### 语言切换
[中文版](./get_draft.zh.md) | [English](./get_draft.md)