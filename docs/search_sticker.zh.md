# SEARCH_STICKER API 接口文档

## 🌐 语言切换
[中文版](./search_sticker.zh.md) | [English](./search_sticker.md)

## 接口信息

```
POST /openapi/capcut-mate/v1/search_sticker
```

## 功能描述

根据关键词搜索贴纸。该接口用于根据用户提供的关键词搜索相关的贴纸素材，返回匹配的贴纸列表，包括贴纸的详细信息如图片URL、尺寸、类型等。

## 请求参数

```json
{
  "keyword": "人"
}
```

### 参数说明

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| keyword | string | ✅ | - | 搜索关键词 |

### 参数详解

#### keyword

- **类型**: string
- **说明**: 搜索贴纸的关键词
- **示例**: "人", "花", "动物"

## 响应格式

### 成功响应 (200)

```json
{
  "code": 0,
  "message": "success",
  "data": [
    {
      "sticker": {
        "large_image": {
          "image_url": "https://p3-heycan-jy-sign.byteimg.com/tos-cn-i-3jr8j4ixpe/29351205dbd943658d94c8feb17e5ed4~tplv-3jr8j4ixpe-resize:1920:1920.png?x-expires=1797257777&x-signature=r18I9uLQzgm%2FcvF8WNLbgw8BRwg%3D"
        },
        "preview_cover": "",
        "sticker_package": {
          "height_per_frame": 540,
          "size": 305932,
          "width_per_frame": 540
        },
        "sticker_type": 1,
        "track_thumbnail": "https://p3-heycan-jy-sign.byteimg.com/tos-cn-i-3jr8j4ixpe/29351205dbd943658d94c8feb17e5ed4~tplv-3jr8j4ixpe-resize:120:120.png?x-expires=1797257777&x-signature=NqeKYGyeqIjCzF0Ls07ctnP%2BehI%3D&format=.png"
      },
      "sticker_id": "7521200021564427545",
      "title": "大笑"
    }
  ]
}
```

### 响应字段说明

| 字段名 | 类型 | 说明 |
|--------|------|------|
| data | array | 贴纸数据列表 |
| sticker | object | 贴纸详细信息 |
| large_image | object | 大图信息 |
| image_url | string | 图片URL |
| preview_cover | string | 预览封面 |
| sticker_package | object | 贴纸包信息 |
| height_per_frame | number | 每帧高度 |
| size | number | 贴纸包大小 |
| width_per_frame | number | 每帧宽度 |
| sticker_type | number | 贴纸类型 |
| track_thumbnail | string | 轨道缩略图 |
| sticker_id | string | 贴纸ID |
| title | string | 贴纸标题 |

### 错误响应

```json
{
  "code": 1001,
  "message": "参数校验失败"
}
```

## 使用示例

### cURL 示例

#### 1. 搜索关键词为"人"的贴纸

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/search_sticker \
  -H "Content-Type: application/json" \
  -d '{
    "keyword": "人"
  }'
```

#### 2. 搜索关键词为"动物"的贴纸

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/search_sticker \
  -H "Content-Type: application/json" \
  -d '{
    "keyword": "动物"
  }'
```

## 错误码说明

| 错误码 | 错误信息 | 说明 | 解决方案 |
|--------|----------|------|----------|
| 1001 | 参数校验失败 | 缺少 keyword 参数（请求体未通过参数校验） | 提供有效的keyword参数 |

## 注意事项

1. **关键词匹配**: 当前实现为简单的标题匹配，实际应用中可以扩展为全文搜索
2. **数据来源**: 当前返回的是模拟数据，实际应用中应该连接贴纸数据库或调用外部API
3. **性能考虑**: 对于大量贴纸数据，应考虑分页和缓存机制

## 工作流程

1. 验证必填参数（keyword）
2. 调用服务层搜索贴纸
3. 返回匹配的贴纸列表

## 相关接口

- [添加贴纸](./add_sticker.md)
- [创建草稿](./create_draft.md)

---

<div align="right">

📚 **项目资源**  
**GitHub**: [https://github.com/Hommy-master/capcut-mate](https://github.com/Hommy-master/capcut-mate)  
**Gitee**: [https://gitee.com/taohongmin-gitee/capcut-mate](https://gitee.com/taohongmin-gitee/capcut-mate)

</div>