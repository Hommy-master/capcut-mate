# GET_POINTS API 接口文档

## 🌐 语言切换
[中文版](./get_points.zh.md) | [English](./get_points.md)

## 接口信息

```
GET https://jcaigc.cn/openapi/v1/user/points
```

## 功能描述

查询指定 apiKey 对应账户的充值余额（单位：元）。接口由简创开放平台（jcaigc.cn）直接提供，
与 `gen_video`、`upload_file` 扣费使用的是同一份充值余额；请求不经过剪映小助手服务端。
可在调用计费接口前先查余额，避免因余额不足导致任务被拒绝。

## 请求参数

参数放在 URL 查询串中，没有请求体。

```bash
curl -X GET "https://jcaigc.cn/openapi/v1/user/points?apiKey=123e4567-e89b-12d3-a456-426614174000"
```

### 参数说明

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| apiKey | string | ✅ | - | 账户的 API Key，固定为 36 位 UUID，可在 https://jcaigc.cn/user-info 查看 |

### 参数详解

#### apiKey

- **类型**: string
- **说明**: 必须是完整的 36 位 UUID（含连字符）；缺省或长度不是 36 位都会返回 10002
- **获取方式**: 登录 https://jcaigc.cn/user-info 查看或重新生成

## 响应格式

### 成功响应 (200)

```json
{
  "code": 0,
  "message": "success",
  "traceid": "067b0e601f4a4784afe4068da658e555",
  "data": {
    "points": 12.34
  }
}
```

### 响应字段说明

| 字段名 | 类型 | 说明 |
|--------|------|------|
| code | int | 业务状态码，0 表示成功 |
| message | string | 状态描述；中文请求返回「成功」，英文请求返回「success」 |
| traceid | string | 本次请求的链路追踪 ID，排查问题时提供给技术支持 |
| data | object | 业务数据 |
| data.points | float | 账户充值余额，单位：元；字段名沿用网关的 `points` |

### 错误响应

```json
{
  "code": 10007,
  "message": "API密钥无效",
  "traceid": "845b5403cd8a999ad7df7b6c4649336d",
  "data": null
}
```

## 使用示例

### cURL 示例

#### 1. 查询账户余额

```bash
curl -X GET "https://jcaigc.cn/openapi/v1/user/points?apiKey=123e4567-e89b-12d3-a456-426614174000"
```

#### 2. 指定中文错误信息

```bash
curl -X GET "https://jcaigc.cn/openapi/v1/user/points?apiKey=123e4567-e89b-12d3-a456-426614174000" \
  -H "Accept-Language: zh-CN"
```

### Python 示例

```python
import requests

resp = requests.get(
    "https://jcaigc.cn/openapi/v1/user/points",
    params={"apiKey": "123e4567-e89b-12d3-a456-426614174000"},
    headers={"Accept-Language": "zh-CN"},
    timeout=10,
)
result = resp.json()

if result["code"] == 0:
    print("账户余额:", result["data"]["points"], "元")
else:
    print("查询失败:", result["code"], result["message"], result["traceid"])
```

## 错误码说明

| 错误码 | 错误信息 | 说明 | 解决方案 |
|--------|----------|------|----------|
| 10002 | 参数无效 | 未传 apiKey，或 apiKey 长度不是 36 位 | 传入完整的 36 位 UUID |
| 10007 | API密钥无效 | apiKey 格式正确，但账户不存在 | 核对 API Key，或登录 https://jcaigc.cn/user-info 重新获取 |
| 10001 | 服务器内部错误 | 网关内部异常 | 稍后重试；持续失败请携带 traceid 联系技术支持 |

## 注意事项

1. **接口归属**：本接口由简创开放平台（jcaigc.cn）提供，不是剪映小助手的服务地址；剪映小助手的 `gen_video`、`upload_file` 内部也调用同一接口查询余额
2. **免费**：查询余额不扣费
3. **余额单位**：`points` 是网关沿用的字段名，实际值是充值余额，单位：元
4. **apiKey 在 URL 中**：请使用 HTTPS 调用，不要把带 apiKey 的完整 URL 写入日志或公开分享
5. **会员折扣**：本接口返回扣费前的账户余额；实际扣费时按会员等级打折（SVIP 6 折、VIP 8 折）

## 工作流程

1. 校验 apiKey：缺省或长度不是 36 位返回 10002
2. 按 apiKey 查找账户：账户不存在返回 10007
3. 返回账户当前的充值余额

## 相关接口

- [生成视频](./gen_video.zh.md)
- [上传文件](./upload_file.zh.md)

---

<div align="right">

📚 **项目资源**  
**GitHub**: [https://github.com/Hommy-master/capcut-mate](https://github.com/Hommy-master/capcut-mate)  
**Gitee**: [https://gitee.com/taohongmin-gitee/capcut-mate](https://gitee.com/taohongmin-gitee/capcut-mate)

</div>
