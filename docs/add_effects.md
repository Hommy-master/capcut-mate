# 添加特效接口文档

## 接口概述
向现有剪映草稿中添加视频特效轨道和特效片段。支持批量添加多种视频特效，包括边框特效、滤镜特效、动态特效等，为视频内容增加丰富的视觉效果。

## 更多文档

📖 更多详细文档和教程请访问：[https://docs.jcaigc.cn](https://docs.jcaigc.cn)

## 接口信息
- **请求方式**: POST
- **接口路径**: `/openapi/capcut-mate/v1/add_effects`
- **Content-Type**: `application/json`

## 请求参数

### 请求体 (Body)

| 参数名 | 类型 | 必填 | 默认值 | 描述 |
|--------|------|------|--------|------|
| draft_url | string | 是 | "" | 目标草稿的完整URL |
| effect_infos | string | 是 | "" | JSON字符串格式的特效信息数组 |

#### effect_infos 字段格式

`effect_infos` 是一个JSON字符串，包含特效信息数组，每个特效对象包含以下字段：

```json
[
    {
        "effect_title": "录制边框 III",  // 特效名称/标题，必选参数
        "start": 0,                     // 特效开始时间（微秒），必选参数  
        "end": 5000000                  // 特效结束时间（微秒），必选参数
    }
]
```

**字段说明**:
- `effect_title`: 特效名称，必须是系统中已存在的特效名称
- `start`: 特效开始时间，单位为微秒，必须大于等于0
- `end`: 特效结束时间，单位为微秒，必须大于start

### 常见特效名称

| 特效类型 | 特效名称示例 |
|----------|--------------|
| 边框特效 | "录制边框 III", "简约边框", "霓虹边框" |
| 滤镜特效 | "复古滤镜", "黑白滤镜", "暖色调" |
| 动态特效 | "粒子效果", "光晕效果", "闪烁特效" |
| 转场特效 | "淡入淡出", "推拉门", "马赛克转场" |

## 请求示例

```bash
curl -X POST "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_effects" \
-H "Content-Type: application/json" \
-d '{
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
  "effect_infos": "[{\"effect_title\": \"录制边框 III\", \"start\": 0, \"end\": 5000000}, {\"effect_title\": \"复古滤镜\", \"start\": 2000000, \"end\": 7000000}]"
}'
```

## 响应格式

### 成功响应

```json
{
  "code": 0,
  "message": "Success",
  "data": {
    "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
    "track_id": "effect_track_123",
    "effect_ids": ["effect_001", "effect_002"],
    "segment_ids": ["seg_001", "seg_002"]
  }
}
```

**响应字段说明**:
- `draft_url`: 草稿URL
- `track_id`: 创建的特效轨道ID
- `effect_ids`: 添加的特效ID列表
- `segment_ids`: 创建的特效片段ID列表

### 错误响应

```json
{
  "code": 2020,
  "message": "无效的特效信息，请检查effect_infos字段值是否正确"
}
```

## 错误码说明

| 错误码 | 错误信息 | 描述 |
|--------|----------|------|
| 2001 | 无效的草稿URL | 草稿URL格式错误或草稿不存在 |
| 2020 | 无效的特效信息 | effect_infos格式错误或字段值无效 |
| 2021 | 特效添加失败 | 添加特效过程中发生错误 |
| 2022 | 特效未找到 | 指定的特效名称不存在 |

## 使用说明

1. **时间单位**: 所有时间参数使用微秒（μs）为单位，1秒 = 1,000,000微秒
2. **时间范围**: 确保 `start < end`，且时间范围合理
3. **特效名称**: 特效名称必须完全匹配系统中预定义的特效名称，区分大小写
4. **批量添加**: 支持一次添加多个特效，按数组顺序依次处理
5. **轨道管理**: 系统会自动创建特效轨道，无需手动管理

## 注意事项

- 特效会按照指定的时间范围添加到视频中
- 如果特效名称不存在，会返回特效未找到错误
- 特效的时间范围不能超出视频总时长
- 建议在添加特效前确保草稿中已有视频内容
- 特效效果可能因版本差异而有所不同

## 相关接口

- [创建草稿](./create_draft.md) - 创建新的剪映草稿
- [添加视频](./add_videos.md) - 向草稿添加视频内容
- [保存草稿](./save_draft.md) - 保存草稿更改