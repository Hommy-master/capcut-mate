# ADD_FILTERS API 接口文档

## 🌐 语言切换
[中文版](./add_filters.zh.md) | [English](./add_filters.md)

## 接口信息

```bash
POST /openapi/capcut-mate/v1/add_filters
```

## 功能描述

向现有草稿中添加视频滤镜。该接口用于在指定的时间段内添加滤镜素材到剪映草稿中，支持多种滤镜类型如复古、黑白、电影感等。滤镜可以用于调整视频的色调和视觉风格。

## 更多文档

📖 更多详细文档和教程请访问：[https://docs.jcaigc.cn](https://docs.jcaigc.cn)

## 请求参数

```json
{
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
  "filter_infos": "[{\"filter_title\": \"复古\", \"start\": 0, \"end\": 5000000, \"intensity\": 80}, {\"filter_title\": \"黑白\", \"start\": 2000000, \"end\": 7000000}]"
}
```

### 参数说明

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| draft_url | string | ✅ | - | 目标草稿的完整URL |
| filter_infos | string | ✅ | - | 滤镜信息列表的JSON字符串 |

### 参数详解

#### filter_infos 字段格式

`filter_infos` 是一个JSON字符串，包含滤镜信息数组，每个滤镜对象包含以下字段：

```json
[
    {
        "filter_title": "复古",       // 滤镜名称/标题，必选参数
        "start": 0,                   // 滤镜开始时间（微秒），必选参数
        "end": 5000000,               // 滤镜结束时间（微秒），必选参数
        "intensity": 80               // 滤镜强度(0-100)，可选参数，默认100
    }
]
```

**字段说明**:
- `filter_title`: 滤镜名称，必须是系统中已存在的滤镜名称
- `start`: 滤镜开始时间，单位为微秒，必须大于等于0
- `end`: 滤镜结束时间，单位为微秒，必须大于start
- `intensity`: 滤镜强度(0-100)，控制滤镜效果的强度，默认为100

#### 时间参数

- **start**: 滤镜在时间轴上的开始时间，单位为微秒（1秒 = 1,000,000微秒）
- **end**: 滤镜在时间轴上的结束时间，单位为微秒
- **duration**: 滤镜显示时长 = end - start

#### 强度参数

- **intensity**: 控制滤镜效果的强度
  - 范围：0-100
  - 默认值：100（完全强度）
  - 较低的值会产生更柔和的滤镜效果
  - 示例：`intensity: 50` 表示以50%的强度应用滤镜

#### 滤镜名称说明

- **filter_title**: 滤镜的名称
  - 格式：字符串
  - 示例：`"复古"`、`"黑白"`、`"电影感"`
  - 获取方式：通过剪映滤镜库或相关API获取
  - 常见滤镜名称：
    - 复古风格："复古", "1980", "VHS III"
    - 黑白风格："黑白", "森山"
    - 电影风格："电影感", "好莱坞III"
    - 其他风格："City Walk", "Lofi II"

## 响应格式

### 成功响应 (200)

```json
{
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
  "track_id": "filter_track_123",
  "filter_ids": ["filter_001", "filter_002"],
  "segment_ids": ["seg_001", "seg_002"]
}
```

### 响应字段说明

| 字段名 | 类型 | 说明 |
|--------|------|------|
| draft_url | string | 更新后的草稿URL |
| track_id | string | 滤镜轨道ID |
| filter_ids | array | 添加的滤镜ID列表 |
| segment_ids | array | 创建的滤镜片段ID列表 |

### 错误响应 (4xx/5xx)

```json
{
  "detail": "错误信息描述"
}
```

## 使用示例

### cURL 示例

#### 1. 基本滤镜添加

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_filters \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "filter_infos": "[{\"filter_title\": \"复古\", \"start\": 0, \"end\": 10000000}]"
  }'
```

#### 2. 自定义强度的滤镜

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_filters \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "filter_infos": "[{\"filter_title\": \"黑白\", \"start\": 0, \"end\": 5000000, \"intensity\": 60}]"
  }'
```

#### 3. 批量滤镜添加

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_filters \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "filter_infos": "[{\"filter_title\": \"复古\", \"start\": 0, \"end\": 5000000, \"intensity\": 80}, {\"filter_title\": \"电影感\", \"start\": 3000000, \"end\": 8000000, \"intensity\": 100}]"
  }'
```

## 错误码说明

| 错误码 | 错误信息 | 说明 | 解决方案 |
|--------|----------|------|----------|
| 400 | draft_url是必填项 | 缺少草稿URL参数 | 提供有效的draft_url |
| 400 | filter_infos是必填项 | 缺少滤镜信息参数 | 提供有效的filter_infos |
| 400 | 时间范围无效 | end必须大于start | 确保结束时间大于开始时间 |
| 400 | 强度范围无效 | intensity必须在0-100之间 | 提供有效的强度值 |
| 400 | 无效的滤镜信息，请检查filter_infos字段值是否正确 | 滤镜参数校验失败 | 检查滤镜参数是否符合要求 |
| 404 | 草稿不存在 | 指定的草稿URL无效 | 检查草稿URL是否正确 |
| 404 | 滤镜不存在 | 指定的滤镜名称无效 | 确认滤镜名称是否正确 |
| 500 | 滤镜添加失败 | 内部处理错误 | 联系技术支持 |

## 注意事项

1. **时间单位**: 所有时间参数使用微秒（1秒 = 1,000,000微秒）
2. **滤镜名称**: 确保使用有效的滤镜名称
3. **时间范围**: end必须大于start
4. **强度范围**: intensity必须在0-100之间，默认为100
5. **轨道管理**: 系统自动创建滤镜轨道
6. **性能考虑**: 避免同时添加大量滤镜

## 工作流程

1. 验证必填参数（draft_url, filter_infos）
2. 检查时间范围的有效性
3. 从缓存中获取草稿
4. 创建滤镜轨道（如果不存在）
5. 解析滤镜信息并创建滤镜片段
6. 添加片段到轨道
7. 保存草稿
8. 返回滤镜信息

## 相关接口

- [创建草稿](./create_draft.md)
- [添加视频](./add_videos.md)
- [添加音频](./add_audios.md)
- [添加图片](./add_images.md)
- [添加特效](./add_effects.md)
- [保存草稿](./save_draft.md)
- [生成视频](./gen_video.md)

---

<div align="right">

📚 **项目资源**  
**GitHub**: [https://github.com/Hommy-master/capcut-mate](https://github.com/Hommy-master/capcut-mate)  
**Gitee**: [https://gitee.com/taohongmin-gitee/capcut-mate](https://gitee.com/taohongmin-gitee/capcut-mate)

</div>
