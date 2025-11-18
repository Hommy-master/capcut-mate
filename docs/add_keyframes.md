# add_keyframes 接口文档

## 接口描述
向剪映草稿添加关键帧，支持多种动画属性的关键帧设置。

## 更多文档

📖 更多详细文档和教程请访问：[https://docs.jcaigc.cn](https://docs.jcaigc.cn)

## 相关接口

- [create_draft](./create_draft.md) - 创建新的剪映草稿
- [add_videos](./add_videos.md) - 向草稿添加视频内容
- [save_draft](./save_draft.md) - 保存草稿更改

## 接口信息
- **方法**: POST
- **路径**: `/openapi/capcut-mate/v1/add_keyframes`
- **Content-Type**: `application/json`

## 请求参数

### 请求体
```json
{
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
  "keyframes": "[{\"segment_id\":\"d62994b4-25fe-422a-a123-87ef05038558\",\"property\":\"KFTypePositionX\",\"offset\":0.5,\"value\":-0.1}]"
}
```

### 参数说明

| 字段名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| draft_url | string | 是 | 草稿URL |
| keyframes | string | 是 | 关键帧信息列表的JSON字符串 |

### keyframes 字段详细说明
keyframes 是一个JSON字符串，包含关键帧数组，每个关键帧对象包含以下字段：

| 字段名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| segment_id | string | 是 | 目标片段的唯一标识ID |
| property | string | 是 | 动画属性类型，支持的类型见下表 |
| offset | number | 是 | 关键帧在片段中的时间偏移（0-1范围，0表示开始，1表示结束） |
| value | number | 是 | 属性在该时间点的值 |

### 支持的动画属性类型

| 属性类型 | 描述 | 值范围 | 示例 |
|---------|------|--------|------|
| KFTypePositionX | X轴位置 | -1.0 到 1.0 | 0.0 (居中), -0.5 (左移), 0.5 (右移) |
| KFTypePositionY | Y轴位置 | -1.0 到 1.0 | 0.0 (居中), -0.5 (上移), 0.5 (下移) |
| KFTypeScaleX | X轴缩放 | 0.1 到 10.0 | 1.0 (原始), 0.5 (缩小), 2.0 (放大) |
| KFTypeScaleY | Y轴缩放 | 0.1 到 10.0 | 1.0 (原始), 0.5 (缩小), 2.0 (放大) |
| KFTypeRotation | 旋转角度 | -360 到 360 | 0 (无旋转), 90 (顺时针90度) |
| KFTypeAlpha | 透明度 | 0.0 到 1.0 | 1.0 (不透明), 0.5 (半透明), 0.0 (透明) |

## 响应结果

### 成功响应
```json
{
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
  "keyframes_added": 3,
  "affected_segments": ["segment_001", "segment_002"]
}
```

### 响应字段说明

| 字段名 | 类型 | 描述 |
|--------|------|------|
| draft_url | string | 草稿URL |
| keyframes_added | integer | 添加的关键帧数量 |
| affected_segments | array | 受影响的片段ID列表 |

### 错误响应
```json
{
  "code": 2013,
  "message": "无效的关键帧信息，请检查keyframes字段值是否正确"
}
```

## 使用示例

### cURL 示例
```bash
curl -X POST "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_keyframes" \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
    "keyframes": "[{\"segment_id\":\"d62994b4-25fe-422a-a123-87ef05038558\",\"property\":\"KFTypePositionX\",\"offset\":0,\"value\":0},{\"segment_id\":\"d62994b4-25fe-422a-a123-87ef05038558\",\"property\":\"KFTypePositionX\",\"offset\":1,\"value\":-0.5}]"
  }'
```

### Python 示例
```python
import requests
import json

url = "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_keyframes"
keyframes_data = [
    {
        "segment_id": "d62994b4-25fe-422a-a123-87ef05038558",
        "property": "KFTypePositionX",
        "offset": 0,
        "value": 0
    },
    {
        "segment_id": "d62994b4-25fe-422a-a123-87ef05038558", 
        "property": "KFTypePositionX",
        "offset": 1,
        "value": -0.5
    }
]

payload = {
    "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
    "keyframes": json.dumps(keyframes_data)
}

response = requests.post(url, json=payload)
print(response.json())
```

## 注意事项

1. **片段ID验证**: segment_id 必须是草稿中存在的有效片段ID
2. **片段类型限制**: 只有视觉片段（视频、图片、贴纸、文本）支持关键帧
3. **时间偏移范围**: offset 值必须在 0.0-1.0 范围内
4. **属性值范围**: 不同的属性类型有不同的值范围限制
5. **重复关键帧**: 相同片段相同属性的关键帧会被累加，不会覆盖
6. **性能考虑**: 单次请求建议不超过100个关键帧

## 错误码说明

| 错误码 | 错误信息 | 说明 |
|--------|----------|------|
| 2001 | 无效的草稿URL | 草稿URL格式错误或草稿不存在 |
| 2013 | 无效的关键帧信息 | keyframes字段格式错误或包含无效数据 |
| 2014 | 关键帧添加失败 | 添加关键帧过程中发生错误 |
| 2015 | 片段未找到 | 指定的segment_id在草稿中不存在 |
| 2016 | 无效的片段类型 | 该片段不支持关键帧功能 |
| 2017 | 无效的关键帧属性类型 | 指定的property类型不受支持 |

---

## 相关接口

- [create_draft](./create_draft.md) - 创建新的剪映草稿
- [add_videos](./add_videos.md) - 向草稿添加视频内容
- [save_draft](./save_draft.md) - 保存草稿更改
- [get_draft](./get_draft.md) - 获取草稿详情

## 技术实现

### 文件结构
- `src/service/add_keyframes.py` - 关键帧添加服务
- `src/schemas/add_keyframes.py` - 请求响应数据模型
- `src/pyJianYingDraft/keyframe.py` - 关键帧核心实现

### 核心逻辑
1. **参数验证**: 验证草稿URL、关键帧数据格式和属性类型
2. **片段检查**: 确认目标片段存在且支持关键帧功能
3. **关键帧添加**: 将关键帧数据写入草稿文件
4. **结果返回**: 返回添加的关键帧数量和受影响的片段

---

<div align="right">

📚 **项目资源**  
**GitHub**: [https://github.com/Hommy-master/capcut-mate](https://github.com/Hommy-master/capcut-mate)  
**Gitee**: [https://gitee.com/taohongmin-gitee/capcut-mate](https://gitee.com/taohongmin-gitee/capcut-mate)

</div>