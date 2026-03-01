# CAPTION_INFOS API 接口文档

## 🌐 语言切换
[中文版](./caption_infos.zh.md) | [English](./caption_infos.md)

## 接口信息

```
POST /openapi/capcut-mate/v1/caption_infos
```

## 功能描述

根据文本和时间线生成字幕信息。该接口将文本内容和时间线配置转换为剪映草稿所需的字幕信息格式，支持关键词高亮、动画效果和转场设置。

## 更多文档

📖 更多详细文档和教程请访问：[https://docs.jcaigc.cn](https://docs.jcaigc.cn)

## 请求参数

```json
{
  "texts": ["欢迎观看", "这是一个示例"],
  "timelines": [
    {"start": 0, "end": 3000000},
    {"start": 3000000, "end": 6000000}
  ],
  "font_size": 24,
  "keyword_color": "#FF0000",
  "keyword_font_size": 28,
  "keywords": ["示例"],
  "in_animation": "fade_in",
  "in_animation_duration": 500000,
  "loop_animation": "bounce",
  "loop_animation_duration": 1000000,
  "out_animation": "fade_out",
  "out_animation_duration": 500000,
  "transition": "cross_fade",
  "transition_duration": 300000
}
```

### 参数说明

| 参数名 | 类型 |必 | | 默认值 | 说明 |
|--------|------|------|--------|------|
| texts | array[string] |✅ | - | 文本内容数组 |
| timelines | array[object] |✅ | - | 时间线配置数组 |
| font_size | number |❌ | 24 | 字体大小 |
| keyword_color | string |❌ | "#FF0000" | 关键词颜色 |
| keyword_font_size | number | ❌ | 28 | 关键词字体大小 |
| keywords | array[string] | ❌ | [] | 关键词数组 |
| in_animation | string | ❌ | None |入动画效果 |
| in_animation_duration | number | ❌ | 500000 |入场动画时长(微秒) |
| loop_animation | string | ❌ | None |循动画效果 |
| loop_animation_duration | number | ❌ | 1000000 |循动画动画时长(微秒) |
| out_animation | string | ❌ | None |出场动画效果 |
| out_animation_duration | number | ❌ | 500000 |出场动画时长(微秒) |
| transition | string | ❌ | None |效果 |
| transition_duration | number | ❌ | 300000 |转时长(微秒) |

##响应格式

### 成功响应 (200)

```json
{
  "infos": "[{\"text\":\"欢迎观看\",\"start\":0,\"end\":3000000,\"duration\":5000000,\"font_size\":24,\"keyword_color\":\"#FF0000\",\"keyword_font_size\":28,\"keywords\":[\"观看\"],\"in_animation\":\"fade_in\",\"in_animation_duration\":500000,\"loop_animation\":\"bounce\",\"loop_animation_duration\":1000000,\"out_animation\":\"fade_out\",\"out_animation_duration\":500000,\"transition\":\"cross_fade\",\"transition_duration\":300000},{\"text\":\"这是一个示例\",\"start\":3000000,\"end\":6000000,\"duration\":5000000,\"font_size\":24,\"keyword_color\":\"#FF0000\",\"keyword_font_size\":28,\"keywords\":[\"示例\"],\"in_animation\":\"fade_in\",\"in_animation_duration\":500000,\"loop_animation\":\"bounce\",\"loop_animation_duration\":1000000,\"out_animation\":\"fade_out\",\"out_animation_duration\":500000,\"transition\":\"cross_fade\",\"transition_duration\":300000}]"
}
```

###响应字段说明

| 字段名 | 类型 | 说明 |
|--------|------|------|
| infos | string | 字幕信息JSON字符串 |

###错误响应 (4xx/5xx)

```json
{
  "detail": "错误信息描述"
}
```

## 使用示例

### cURL 示例

#### 1. 基本字幕信息生成

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/caption_infos \
  -H "Content-Type: application/json" \
  -d '{
    "texts": ["Hello World"],
    "timelines": [{"start": 0, "end": 3000000}],
    "font_size": 28
  }'
```

#### 2.带高亮的字幕信息

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/caption_infos \
  -H "Content-Type: application/json" \
  -d '{
    "texts": ["欢迎观看我们的视频", "这是一个精彩示例"],
    "timelines": [{"start": 0, "end": 3000000}, {"start": 3000000, "end": 6000000}],
    "keyword_color": "#FF5500",
    "keywords": ["精彩", "视频"],
    "in_animation": "fade_in",
    "loop_animation": "bounce"
  }'
```

## 错误码说明

| 错误码 | 错误信息 | 说明 | 解决方案 |
|--------|----------|------|----------|
| 400 | texts是必填项 |缺少文本内容参数 | 提供有效的文本内容数组 |
| 400 | timelines是必填项 |缺少时间线参数 | 提供有效的时间线数组 |
| 400 | 数组长度不匹配 | texts和timelines长度不一致 |确保两个数组长度相同 |
| 400 | font_size必须大于0 | 字体大小参数无效 | 使用大于0的字体大小值 |
| 500 | 字幕信息生成失败 |内部处理错误 |联技术支持 |

## 注意事项

1. **数组匹配**: texts和timelines数组长度必须相同
2. **时间单位**:所有时间参数使用微秒（1秒 = 1,000,000微秒）
3. **关键词匹配**: keywords数组中的关键词将在文本中高亮显示
4. **动画效果**:支持入场动画、循环动画、出场动画和转场效果
5. **颜色格式**: keyword_color使用十六进制颜色格式（如"#FF0000"）
6. **字体大小**: 字体大小以像素为单位

##工作流程

1.验证必填参数（texts, timelines）
2. 检查数组长度匹配
3.验证时间线参数有效性
4. 设置字体和颜色参数
5.应用动画效果参数
6. 为每个文本内容生成对应的字幕信息
7. 将信息转换为JSON字符串格式
8. 返回处理结果

##相关接口

- [创建草稿](./create_draft.md)
- [添加字幕](./add_captions.md)
- [时间线](./timelines.md)
- [保存草稿](./save_draft.md)

---

<div align="right">

📚 **项目资源**  
**GitHub**: [https://github.com/Hommy-master/capcut-mate](https://github.com/Hommy-master/capcut-mate)  
**Gitee**: [https://gitee.com/taohongmin-gitee/capcut-mate](https://gitee.com/taohongmin-gitee/capcut-mate)

</div>

### 语言切换
[中文版](./caption_infos.zh.md) | [English](./caption_infos.md)