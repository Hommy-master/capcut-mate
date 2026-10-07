# AUDIO_TIMELINES API 接口文档

## 🌐 语言切换
[中文版](./audio_timelines.zh.md) | [English](./audio_timelines.md)

## 接口信息

```
POST /openapi/capcut-mate/v1/audio_timelines
```

## 功能描述

根据音频文件时长计算时间线。该接口通过分析输入音频文件的时长信息，自动计算并生成合适的时间线配置，用于视频编辑中音频素材的精确时间安排。

## 请求参数

```json
{
  "links": [
    "https://assets.jcaigc.cn/audio1.mp3",
    "https://assets.jcaigc.cn/audio2.mp3"
  ]
}
```

### 参数说明

| 参数名 | 类型 |必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| links | array[string] |✅ | - | 音频文件URL数组 |

### links 数组结构

每个links数组元素为一个音频文件URL字符串：

| 字段名 | 类型 |必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| links[] | string |✅ | - | 音频文件URL地址 |

### 参数详解

#### links[]
- **类型**: string
- **说明**: 音频文件的完整URL地址；时长由服务端从下载的文件中测量，不在请求中传入
- **示例**: "https://assets.jcaigc.cn/background.mp3"

##响应格式

### 成功响应 (200)

```json
{
  "code": 0,
  "message": "success",
  "timelines": [
    {
      "start": 0,
      "end": 5000000
    },
    {
      "start": 5000000,
      "end": 8000000
    }
  ],
  "all_timelines": [
    {
      "start": 0,
      "end": 8000000
    }
  ]
}
```

###响应字段说明

| 字段名 | 类型 | 说明 |
|--------|------|------|
| timelines | array | 分段音频时间线数组 |
| all_timelines | array |完整音频时间线数组 |
| start | number | 时间段开始时间(微秒) |
| end | number | 时间段结束时间(微秒) |

### 错误响应

```json
{
  "code": 2034,
  "message": "获取音频时长失败"
}
```

## 使用示例

### cURL 示例

#### 1. 基本音频时间线计算

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/audio_timelines \
  -H "Content-Type: application/json" \
  -d '{
    "links": [
      "https://assets.jcaigc.cn/intro.mp3",
      "https://assets.jcaigc.cn/bgm.mp3"
    ]
  }'
```

#### 2.多音频时间线计算

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/audio_timelines \
  -H "Content-Type: application/json" \
  -d '{
    "links": [
      "https://assets.jcaigc.cn/opening.mp3",
      "https://assets.jcaigc.cn/content.mp3",
      "https://assets.jcaigc.cn/ending.mp3"
    ]
  }'
```

##错误码说明

| 错误码 | 错误信息 | 说明 | 解决方案 |
|--------|----------|------|----------|
| 1001 | 参数校验失败 | `links` 缺失，或不是字符串数组 | 提供有效的音频文件URL数组 |
| 2004 | 文件大小超出限制 | 下载的音频超过下载大小限制 | 使用更小的音频文件 |
| 2005 | 下载文件失败 | 音频文件下载失败 | 检查音频URL是否可公网访问 |
| 2034 | 获取音频时长失败 | 无法读取已下载音频文件的时长 | 使用合法、可正常播放的音频文件 |

## 注意事项

1. **时间单位**:所有时间参数使用微秒（1秒 = 1,000,000微秒）
2. **参数要求**: links数组为必填参数，且每个元素为音频文件URL字符串
3. **时长来源**: 每个音频的时长由服务端从下载的文件中测得（微秒），不在请求中传入
4. **网络访问**: 音频URL必须可以正常访问，因为需要下载文件来测量时长
5. **连续性**: 时间线按音频顺序连续排列，无间隔
6. **总时长**:完整时间线的end值等于所有音频时长之和

##工作流程

1.验证必填参数（links）
2. 下载每个音频文件并获取其时长
3. 无法获取时长时以错误码 2034 返回
4.按顺序计算每个音频的时间段
5. 生成分段音频时间线数组
6. 生成完整音频时间线数组
7. 返回时间线配置结果

##相关接口

- [创建草稿](./create_draft.md)
- [创建时间线](./timelines.md)
- [音频信息](./audio_infos.md)
- [生成视频](./gen_video.md)

---

<div align="right">

📚 **项目资源**  
**GitHub**: [https://github.com/Hommy-master/capcut-mate](https://github.com/Hommy-master/capcut-mate)  
**Gitee**: [https://gitee.com/taohongmin-gitee/capcut-mate](https://gitee.com/taohongmin-gitee/capcut-mate)

</div>

### 语言切换
[中文版](./audio_timelines.zh.md) | [English](./audio_timelines.md)