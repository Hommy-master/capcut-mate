# TIMELINES API 接口文档

## 🌐 语言切换
[中文版](./timelines.zh.md) | [English](./timelines.md)

## 接口信息

```
POST /openapi/capcut-mate/v1/timelines
```

## 功能描述

根据指定的时长和数量创建时间线。该接口用于生成视频编辑所需的时间线配置，支持多种时间线类型和起始时间设置，为后续的素材添加和编辑提供时间参考。

## 更多文档

📖 更多详细文档和教程请访问：[https://docs.jcaigc.cn](https://docs.jcaigc.cn)

## 请求参数

```json
{
  "duration": 10000000,
  "num": 3,
  "start": 0,
  "type": 0
}
```

### 参数说明

| 参数名 | 类型 |必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| duration | integer |✅ | - |总时长(微秒) |
| num | integer |✅ | - | 时间段数量 |
| start | integer |✅ | - |时间(微秒) |
| type | integer |✅ | - | 时间线类型：0 平均分，1 随机 |

### 参数详解

#### duration
- **类型**: integer
- **说明**:总时长，单位为微秒（1秒 = 1,000,000微秒）
- **示例**: 10000000 (10秒)

#### num
- **类型**: integer
- **说明**:需要创建的时间段数量
- **示例**: 3 (创建3个时间段)

#### start
- **类型**: integer
- **说明**: 时间线的起始时间，单位为微秒
- **示例**: 2000000 (从2秒开始)

#### type
- **类型**: integer
- **说明**: 时间线分割类型
- **可选值**: 
  - 0 - 平均分时间线
  - 1 - 随机时间线
- **示例**: 0

## 响应格式

### 成功响应 (200)

```json
{
  "code": 0,
  "message": "success",
  "timelines": [
    {
      "start": 0,
      "end": 3333333
    },
    {
      "start": 3333333,
      "end": 6666666
    },
    {
      "start": 6666666,
      "end": 10000000
    }
  ],
  "all_timelines": [
    {
      "start": 0,
      "end": 10000000
    }
  ]
}
```

###响应字段说明

| 字段名 | 类型 | 说明 |
|--------|------|------|
| timelines | array | 分段时间线数组 |
| all_timelines | array |完整时间线数组 |
| start | number | 时间段开始时间(微秒) |
| end | number | 时间段结束时间(微秒) |

### 错误响应

```json
{
  "code": 1001,
  "message": "参数校验失败"
}
```

## 使用示例

### cURL 示例

#### 1.基本时间线创建

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/timelines \
  -H "Content-Type: application/json" \
  -d '{
    "duration": 15000000,
    "num": 5,
    "start": 0,
    "type": 0
  }'
```

#### 2.带始时间的时间线

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/timelines \
  -H "Content-Type: application/json" \
  -d '{
    "duration": 20000000,
    "num": 4,
    "start": 5000000,
    "type": 0
  }'
```

##错误码说明

| 错误码 |错误信息 | 说明 | 解决方案 |
|--------|----------|------|----------|
| 1001 | 参数校验失败 | 请求体未通过字段校验（`duration`/`num`/`start`/`type` 缺失或不是整数） | 检查参数类型与必填字段 |

## 注意事项

1. **时间单位**:所有时间参数使用微秒（1秒 = 1,000,000微秒）
2. **参数要求**: duration、num、start、type 均为必填参数
3. **时间范围**: `all_timelines` 覆盖 `start` 到 `start + duration`，分段时间线均在该范围内生成
4. **类型选择**:根据实际需求选择合适的时间线类型
5. **精度考虑**:微秒级别的时间精度适合精确的视频编辑

##工作流程

1.验证必填参数（duration, num, start, type）
2.检查参数类型（整数）
3.根据type类型计算时间线分割方式
4. 生成分段时间线数组
5. 生成完整时间线数组
6. 返回时间线配置结果

##相关接口

- [创建草稿](./create_draft.md)
- [音频时间线](./audio_timelines.md)
- [视频信息](./video_infos.md)
- [图片信息](./imgs_infos.md)

---

<div align="right">

📚 **项目资源**  
**GitHub**: [https://github.com/Hommy-master/capcut-mate](https://github.com/Hommy-master/capcut-mate)  
**Gitee**: [https://gitee.com/taohongmin-gitee/capcut-mate](https://gitee.com/taohongmin-gitee/capcut-mate)

</div>

### 语言切换
[中文版](./timelines.zh.md) | [English](./timelines.md)