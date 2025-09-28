# add_captions 接口文档

## 接口描述
向剪映草稿批量添加字幕，支持丰富的字幕样式设置，包括关键词高亮、字体样式、边框效果、对齐方式、透明度和动画效果等。

## 接口信息
- **方法**: POST
- **路径**: `/openapi/capcut-mate/v1/add_captions`
- **Content-Type**: `application/json`

## 请求参数

### 请求体
```json
{
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
  "captions": "[{\"start\":0,\"end\":10000000,\"text\":\"你好，剪映\",\"keyword\":\"好\",\"keyword_color\":\"#457616\",\"keyword_font_size\":15,\"font_size\":15}]",
  "text_color": "#ffffff",
  "border_color": null,
  "alignment": 1,
  "alpha": 1.0,
  "font": null,
  "font_size": 15,
  "letter_spacing": null,
  "line_spacing": null,
  "scale_x": 1.0,
  "scale_y": 1.0,
  "transform_x": 0,
  "transform_y": 0,
  "style_text": false
}
```

### 参数说明

| 字段名 | 类型 | 必填 | 默认值 | 描述 |
|--------|------|------|--------|------|
| draft_url | string | 是 | - | 草稿URL |
| captions | string | 是 | - | 字幕信息列表的JSON字符串 |
| text_color | string | 否 | "#ffffff" | 文本颜色（十六进制） |
| border_color | string | 否 | null | 边框颜色（十六进制） |
| alignment | integer | 否 | 1 | 文本对齐方式（0-5） |
| alpha | number | 否 | 1.0 | 文本透明度（0.0-1.0） |
| font | string | 否 | null | 字体名称 |
| font_size | integer | 否 | 15 | 字体大小 |
| letter_spacing | number | 否 | null | 字间距 |
| line_spacing | number | 否 | null | 行间距 |
| scale_x | number | 否 | 1.0 | 水平缩放 |
| scale_y | number | 否 | 1.0 | 垂直缩放 |
| transform_x | integer | 否 | 0 | 水平位移 |
| transform_y | integer | 否 | 0 | 垂直位移 |
| style_text | boolean | 否 | false | 是否使用样式文本 |

### captions 字段详细说明
captions 是一个JSON字符串，包含字幕数组，每个字幕对象包含以下字段：

| 字段名 | 类型 | 必填 | 默认值 | 描述 |
|--------|------|------|--------|------|
| start | integer | 是 | - | 字幕开始时间（微秒） |
| end | integer | 是 | - | 字幕结束时间（微秒） |
| text | string | 是 | - | 字幕文本内容 |
| keyword | string | 否 | null | 关键词（用\|分隔多个关键词） |
| keyword_color | string | 否 | "#ff7100" | 关键词颜色 |
| keyword_font_size | integer | 否 | 15 | 关键词字体大小 |
| font_size | integer | 否 | 15 | 文本字体大小 |
| in_animation | string | 否 | null | 入场动画 |
| out_animation | string | 否 | null | 出场动画 |
| loop_animation | string | 否 | null | 循环动画 |
| in_animation_duration | integer | 否 | null | 入场动画时长 |
| out_animation_duration | integer | 否 | null | 出场动画时长 |
| loop_animation_duration | integer | 否 | null | 循环动画时长 |

### 对齐方式说明

| 值 | 说明 |
|---|------|
| 0 | 左对齐 |
| 1 | 居中对齐 |
| 2 | 右对齐 |
| 3 | 垂直居中 |
| 4 | 垂直左对齐 |
| 5 | 垂直右对齐 |

## 响应结果

### 成功响应
```json
{
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
  "track_id": "text_track_123",
  "text_ids": ["text_001", "text_002"],
  "segment_ids": ["seg_001", "seg_002"]
}
```

### 响应字段说明

| 字段名 | 类型 | 描述 |
|--------|------|------|
| draft_url | string | 草稿URL |
| track_id | string | 字幕轨道ID |
| text_ids | array | 字幕ID列表 |
| segment_ids | array | 字幕片段ID列表 |

### 错误响应
```json
{
  "code": 2018,
  "message": "无效的字幕信息，请检查captions字段值是否正确"
}
```

## 使用示例

### cURL 示例
```bash
curl -X POST "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_captions" \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
    "captions": "[{\"start\":0,\"end\":5000000,\"text\":\"你好，剪映\",\"keyword\":\"好\",\"keyword_color\":\"#ff0000\"}]",
    "text_color": "#ffffff",
    "alignment": 1,
    "alpha": 1.0,
    "font_size": 20
  }'
```

### Python 示例
```python
import requests
import json

url = "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_captions"
captions_data = [
    {
        "start": 0,
        "end": 5000000,
        "text": "你好，剪映",
        "keyword": "好",
        "keyword_color": "#ff0000",
        "font_size": 20
    },
    {
        "start": 5000000,
        "end": 10000000,
        "text": "欢迎使用字幕功能",
        "keyword": "字幕",
        "keyword_color": "#00ff00",
        "font_size": 18
    }
]

payload = {
    "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
    "captions": json.dumps(captions_data),
    "text_color": "#ffffff",
    "alignment": 1,
    "alpha": 1.0,
    "font_size": 16,
    "transform_y": -100
}

response = requests.post(url, json=payload)
print(response.json())
```

### JavaScript 示例
```javascript
const url = "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_captions";
const captionsData = [
  {
    start: 0,
    end: 5000000,
    text: "你好，剪映",
    keyword: "好",
    keyword_color: "#ff0000",
    font_size: 20
  }
];

const payload = {
  draft_url: "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
  captions: JSON.stringify(captionsData),
  text_color: "#ffffff",
  alignment: 1,
  alpha: 1.0,
  font_size: 16
};

fetch(url, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(payload)
})
.then(response => response.json())
.then(data => console.log(data));
```

## 注意事项

1. **时间单位**: 所有时间参数使用微秒为单位（1秒 = 1,000,000微秒）
2. **字幕时长**: end 时间必须大于 start 时间
3. **颜色格式**: 颜色值使用十六进制格式，如 "#ffffff"、"#ff0000"
4. **关键词高亮**: 暂未完全实现，目前为预留功能
5. **动画效果**: 暂未完全实现，目前为预留功能
6. **字体支持**: 字体名称需要系统支持或使用默认字体
7. **对齐方式**: 目前仅支持基础对齐方式（0-2），高级对齐方式（3-5）为预留功能
8. **坐标系统**: transform_x 和 transform_y 使用像素值，会自动转换为草稿相对坐标

## 错误码说明

| 错误码 | 错误信息 | 说明 |
|--------|----------|------|
| 2001 | 无效的草稿URL | 草稿URL格式错误或草稿不存在 |
| 2018 | 无效的字幕信息 | captions字段格式错误或包含无效数据 |
| 2019 | 字幕添加失败 | 添加字幕过程中发生错误 |

## 高级功能（待实现）

1. **关键词高亮**: 支持对指定关键词设置不同颜色和字体大小
2. **入场/出场动画**: 支持字幕的动画效果
3. **循环动画**: 支持字幕的循环动画效果
4. **样式文本**: 支持富文本格式的字幕样式
5. **字体选择**: 支持自定义字体文件
6. **边框和阴影**: 支持字幕边框和阴影效果