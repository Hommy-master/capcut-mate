# UPLOAD_FILE API 接口文档

## 🌐 语言切换
[中文版](./upload_file.zh.md) | [English](./upload_file.md)

## 接口信息

```
POST /openapi/capcut-mate/v1/upload_file
Content-Type: multipart/form-data
```

## 功能描述

上传文件到对象存储（服务端中转）。客户端把文件字节提交到本服务，服务端转发上传到对象存储，
上传成功后按文件实际体积计费（0.0005 元/MB），并返回带签名的下载 URL。
对象存储密钥全程留在服务端，不会下发给客户端。

## 更多文档

📖 更多详细文档和教程请访问：[https://docs.jcaigc.cn](https://docs.jcaigc.cn)

## 请求参数

以 `multipart/form-data` 提交：文件放在 `file` 字段，密钥放在 `apiKey` 字段。

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/upload_file \
  -F "file=@demo.mp4" \
  -F "apiKey=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
```

### 参数说明

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| file | file | ✅ | - | 待上传文件，单文件最大 500MB |
| apiKey | string | 按服务端配置 | - | 合法的 UUID；`ENABLE_APIKEY=true` 时必填，可登录 https://jcaigc.cn 获取 |

### 参数详解

#### file

- **类型**: 文件（multipart/form-data）
- **说明**: 支持常见音视频/图片格式：mp4、mov、m4v、avi、mkv、flv、webm、wmv、mp3、wav、m4a、aac、flac、ogg、jpg、jpeg、png、gif、webp、bmp
- **限制**: 单文件最大 500MB，空文件会被拒绝

#### apiKey

- **类型**: string
- **说明**: 必须是合法的 UUID 格式；服务端开启 apiKey 校验时必填，且账户余额需大于 1 才可上传

## 响应格式

### 成功响应 (200)

```json
{
  "code": 0,
  "message": "success",
  "url": "https://bucket.oss-cn-hangzhou.aliyuncs.com/jianchuang/2026-10-06/8f3a1c2d5e6b7a90_demo.mp4?OSSAccessKeyId=xxx&Expires=xxx&Signature=xxx",
  "key": "jianchuang/2026-10-06/8f3a1c2d5e6b7a90_demo.mp4",
  "size": 10485760,
  "size_mb": 10.0,
  "cost": 0.005,
  "url_expire_days": 7
}
```

### 响应字段说明

| 字段名 | 类型 | 说明 |
|--------|------|------|
| url | string | 对象存储带签名的临时下载地址，可直接传给 add_videos / add_images / add_audios 等接口 |
| key | string | 对象存储 object key |
| size | int | 文件实际字节数 |
| size_mb | float | 文件体积（MB，保留 3 位小数） |
| cost | float | 本次上传费用（元）；未启用计费时为 0 |
| url_expire_days | int | url 有效期（天），取 `VIDEO_GEN_RETENTION_DAYS`（默认 7 天） |

### 错误响应

```json
{
  "code": 2050,
  "message": "不支持的文件类型，请上传受支持格式的文件"
}
```

## 使用示例

### cURL 示例

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/upload_file \
  -F "file=@demo.mp4" \
  -F "apiKey=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
```

### Python 示例

```python
import requests

with open("demo.mp4", "rb") as f:
    resp = requests.post(
        "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/upload_file",
        files={"file": ("demo.mp4", f, "video/mp4")},
        data={"apiKey": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"},
        timeout=600,
    )

result = resp.json()
video_url = result["url"]  # 可直接传给 add_videos / add_images / add_audios
print("体积:", result["size_mb"], "MB", "费用:", result["cost"], "元")
```

## 错误码说明

| 错误码 | 错误信息 | 说明 | 解决方案 |
|--------|----------|------|----------|
| 1001 | 参数校验失败 | 缺少 file 字段、apiKey 不是合法 UUID，或上传了空文件 | 检查请求参数 |
| 2004 | 文件大小超出限制 | 文件超过 500MB | 压缩或切分文件后重试 |
| 2035 | 账户余额不足 | 账户积分需大于 1 才可继续使用服务 | 完成充值后重试 |
| 2036 | 无效的 apiKey | `ENABLE_APIKEY=true` 且 apiKey 缺失或非法 | 登录 https://jcaigc.cn 获取 apiKey |
| 2049 | 无效的文件名 | 文件名为空或清洗后没有可用字符 | 提供合法的文件名 |
| 2050 | 不支持的文件类型 | 扩展名不在内置白名单内 | 改用受支持的格式 |
| 9998 | 系统内部错误 | 未配置任何对象存储或上传失败 | 检查服务端对象存储配置 |

## 注意事项

1. **服务端中转**：文件先上传到本服务，再由服务端上传到对象存储；对象存储密钥不会下发给客户端
2. **计费规则**：0.0005 元/MB，按文件实际字节数计算（保留 6 位小数），仅在对象存储上传成功后才扣费
3. **大小限制**：单文件最大 500MB；若部署在 nginx 之后，需同时放开 `client_max_body_size`（默认 1MB 会直接返回 413）
4. **有效期**：返回的 `url` 为带签名的临时地址，有效期由 `VIDEO_GEN_RETENTION_DAYS` 控制（默认 7 天）
5. **上传完成即可用**：`url` 可直接传给 add_videos / add_images / add_audios 等接口使用

## 工作流程

1. 校验 apiKey（`ENABLE_APIKEY=true` 时）与账户余额（需大于 1）
2. 清洗文件名并校验扩展名白名单
3. 流式落盘并统计文件体积（超过 500MB 或为空则拒绝）
4. 上传文件到对象存储（COS / OSS / TOS）
5. 上传成功后按体积扣费
6. 返回带签名的下载 URL

## 相关接口

- [创建草稿](./create_draft.zh.md)
- [添加视频](./add_videos.zh.md)

---

<div align="right">

📚 **项目资源**  
**GitHub**: [https://github.com/Hommy-master/capcut-mate](https://github.com/Hommy-master/capcut-mate)  
**Gitee**: [https://gitee.com/taohongmin-gitee/capcut-mate](https://gitee.com/taohongmin-gitee/capcut-mate)

</div>
