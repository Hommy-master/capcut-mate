# AUDIO_INFOS API 接口文档

## 🌐 语言切换
[中文版](./audio_infos.zh.md) | [English](./audio_infos.md)

## 接口信息

```
POST /openapi/capcut-mate/v1/audio_infos
```

## 功能描述

根据音频URL和时间线生成音频信息。该接口将音频文件URL和时间线配置转换为剪映草稿所需的音频信息格式，支持音量控制和音频效果设置。

## 请求参数

```json
{
  "mp3_urls": ["https://assets.jcaigc.cn/audio1.mp3", "https://assets.jcaigc.cn/audio2.mp3"],
  "timelines": [
    {"start": 0, "end": 3000000},
    {"start": 3000000, "end": 8000000}
  ],
  "audio_effect": "reverb",
  "volume": 0.8
}
```

### 参数说明

| 参数名 | 类型 |必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| mp3_urls | array[string] |✅ | - | 音频文件URL数组 |
| timelines | array[object] |✅ | - | 时间线配置数组 |
| audio_effect | string |❌ | None | 音频效果名称 |
| volume | number |❌ | None |音量大小(0.0-2.0) |

### 参数详解

#### mp3_urls
- **类型**: array[string]
- **说明**: 音频文件URL地址数组
- **示例**: ["https://assets.jcaigc.cn/bgm.mp3", "https://assets.jcaigc.cn/sfx.mp3"]

#### timelines
- **类型**: array[object]
- **说明**: 时间线配置数组，每个元素包含start和end字段
- **示例**: [{"start": 0, "end": 5000000}, {"start": 5000000, "end": 10000000}]

#### audio_effect
- **类型**: string
- **说明**: 音频效果名称
- **默认值**: None
- **示例**: "reverb", "echo", "bass_boost"

#### volume
- **类型**: number
- **说明**: 音频音量大小
- **默认值**: None
- **范围**: 0.0 - 2.0
- **示例**: 0.8 (80%音量)

##响应格式

### 成功响应 (200)

```json
{
  "code": 0,
  "message": "success",
  "infos": "[{\"audio_url\":\"https://assets.jcaigc.cn/audio1.mp3\",\"start\":0,\"end\":3000000,\"audio_effect\":\"reverb\",\"volume\":0.8},{\"audio_url\":\"https://assets.jcaigc.cn/audio2.mp3\",\"start\":3000000,\"end\":8000000,\"audio_effect\":\"reverb\",\"volume\":0.8}]"
}
```

###响应字段说明

| 字段名 | 类型 | 说明 |
|--------|------|------|
| infos | string |音信息JSON字符串 |

### 错误响应

```json
{
  "code": 1001,
  "message": "参数校验失败"
}
```

## 使用示例

### cURL 示例

#### 1.基本音频信息生成

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/audio_infos \
  -H "Content-Type: application/json" \
  -d '{
    "mp3_urls": ["https://assets.jcaigc.cn/bgm.mp3"],
    "timelines": [{"start": 0, "end": 10000000}],
    "volume": 0.7
  }'
```

#### 2.效果的音频信息

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/audio_infos \
  -H "Content-Type: application/json" \
  -d '{
    "mp3_urls": ["https://assets.jcaigc.cn/intro.mp3", "https://assets.jcaigc.cn/content.mp3"],
    "timelines": [{"start": 0, "end": 2000000}, {"start": 2000000, "end": 12000000}],
    "audio_effect": "reverb",
    "volume": 0.9
  }'
```

##错误码说明

|错误码 | 错误信息 | 说明 | 解决方案 |
|--------|----------|------|----------|
| 1001 | 参数校验失败 | 请求体未通过字段校验（缺少 `mp3_urls`/`timelines`、时间线项缺少 `start`/`end`，或类型错误） | 检查参数类型与必填字段 |

## 注意事项

1. **数组匹配**: `mp3_urls` 与 `timelines` 长度不一致时，按较短长度截断后继续生成（不会直接报错）
2. **时间单位**:所有时间参数使用微秒（1秒 = 1,000,000微秒）
3. **音量范围**: volume值必须在0.0-2.0范围内
4. **效果支持**: audio_effect需要是系统支持的音频效果名称
5. **JSON格式**: 返回的infos是JSON字符串，需要解析后使用
6. **网络访问**: 音频URL必须可以正常访问

##工作流程

1.验证必填参数（mp3_urls, timelines）
2.按较短长度对齐两个数组
3.验证时间线参数有效性
4. 读取可选的 volume 和 audio_effect 参数
5. 为每个音频URL生成对应的音频信息
6.应用音量和音频效果设置
7.将信息转换为JSON字符串格式
8. 返回处理结果

##相关接口

- [创建草稿](./create_draft.md)
- [添加音频](./add_audios.md)
- [音频时间线](./audio_timelines.md)
- [保存草稿](./save_draft.md)

---

<div align="right">

📚 **项目资源**  
**GitHub**: [https://github.com/Hommy-master/capcut-mate](https://github.com/Hommy-master/capcut-mate)  
**Gitee**: [https://gitee.com/taohongmin-gitee/capcut-mate](https://gitee.com/taohongmin-gitee/capcut-mate)

</div>

### 语言切换
[中文版](./audio_infos.zh.md) | [English](./audio_infos.md)