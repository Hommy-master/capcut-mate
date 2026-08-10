# ADD_TEXT_STYLE API 接口文档

## 🌐 语言切换
[中文版](./add_audios.zh.md) | [English](./add_audios.md)

## 接口信息

```bash
POST /openapi/capcut-mate/v1/add_text_style
```

## 功能描述

为文本创建富文本样式，支持关键词高亮、颜色设置、字体大小调整等功能。该接口可以将普通文本转换为包含样式信息的富文本格式，实现关键词突出显示、多样化的文本展示效果。

## 更多文档

📖 更多详细文档和教程请访问：[https://docs.jcaigc.cn](https://docs.jcaigc.cn)

## 请求参数

```json
{
  "text": "五个快乐到死的顶级思维",
  "keyword": "快乐|顶级思维",
  "font_size": 12,
  "keyword_color": "#ff7100",
  "keyword_font_size": 15
}
```

### 参数说明

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| text | string | ✅ | - | 要处理的文本内容 |
| keyword | string | ✅ | - | 关键词，多个用 \| 分隔 |
| font_size | number | ❌ | 12 | 普通文本的字体大小 |
| keyword_color | string | ❌ | "#ff7100" | 关键词文本颜色（十六进制） |
| keyword_font_size | number | ❌ | 15 | 关键词字体大小 |

### 参数详解

#### 文本参数

- **text**: 需要进行样式处理的原始文本内容
  - 示例：`"五个快乐到死的顶级思维"`

#### 关键词参数

- **keyword**: 需要高亮显示的关键词，支持多个关键词用竖线（|）分隔
  - 示例：`"快乐|顶级思维"`
  - 注意：系统会按关键词长度优先匹配，避免短关键词覆盖长关键词

#### 字体大小参数

- **font_size**: 普通文本（非关键词）的字体大小
  - 默认值：12
  - 建议范围：8-72

- **keyword_font_size**: 关键词的字体大小
  - 默认值：15
  - 建议范围：8-72

#### 颜色参数

- **keyword_color**: 关键词的文本颜色，使用十六进制格式
  - 默认值：`"#ff7100"` (橙色)
  - 格式：#RRGGBB
  - 示例：`"#ff0000"` (红色), `"#00ff00"` (绿色), `"#0000ff"` (蓝色)

## 响应格式

### 成功响应 (200)

```json
{
  "text_style": "{\"styles\":[{\"fill\":{\"content\":{\"solid\":{\"color\":[1,1,1]}}},\"range\":[0,2],\"size\":12,\"font\":{\"id\":\"\",\"path\":\"\"}},{\"fill\":{\"content\":{\"solid\":{\"color\":[1,0.44313725490196076,0]}}},\"range\":[2,4],\"size\":15,\"font\":{\"id\":\"\",\"path\":\"\"},\"useLetterColor\":true},{\"fill\":{\"content\":{\"solid\":{\"color\":[1,1,1]}}},\"range\":[4,7],\"size\":12,\"font\":{\"id\":\"\",\"path\":\"\"}},{\"fill\":{\"content\":{\"solid\":{\"color\":[1,0.44313725490196076,0]}}},\"range\":[7,11],\"size\":15,\"font\":{\"id\":\"\",\"path\":\"\"},\"useLetterColor\":true}],\"text\":\"五个快乐到死的顶级思维\"}"
}
```

### 响应字段说明

| 字段名 | 类型 | 说明 |
|--------|------|------|
| text_style | string | 文本样式JSON字符串，包含styles数组和text字段 |

### 错误响应 (4xx/5xx)

```json
{
  "code": 2026,
  "message": "无效的文本样式信息，请检查文本或关键词参数"
}
```

## 使用示例

### cURL 示例

#### 1. 基本文本样式创建

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_text_style \
  -H "Content-Type: application/json" \
  -d '{
    "text": "五个快乐到死的顶级思维",
    "keyword": "快乐|顶级思维"
  }'
```

#### 2. 自定义字体大小

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_text_style \
  -H "Content-Type: application/json" \
  -d '{
    "text": "五个快乐到死的顶级思维",
    "keyword": "快乐|顶级思维",
    "font_size": 14,
    "keyword_font_size": 18
  }'
```

#### 3. 自定义关键词颜色

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_text_style \
  -H "Content-Type: application/json" \
  -d '{
    "text": "五个快乐到死的顶级思维",
    "keyword": "快乐|顶级思维",
    "keyword_color": "#ff0000"
  }'
```

## 错误码说明

| 错误码 | 错误信息 | 说明 | 解决方案 |
|--------|----------|------|----------|
| 2026 | 无效的文本样式信息，请检查文本或关键词参数 | 文本或关键词参数格式错误或值无效 | 检查text和keyword参数是否符合要求 |
| 2027 | 文本样式创建失败 | 创建文本样式过程中发生错误 | 联系技术支持 |

## 注意事项

1. **关键词匹配**: 关键词按长度优先匹配，长关键词优先于短关键词
2. **颜色格式**: 使用标准十六进制颜色格式 #RRGGBB
3. **字体大小**: 建议在8-72范围内
4. **关键词分隔**: 多个关键词使用竖线 | 分隔
5. **大小写敏感**: 关键词匹配区分大小写

## 工作流程

1. 验证必填参数（text, keyword）
2. 解析关键词字符串
3. 在文本中查找关键词位置
4. 转换颜色值为RGB格式
5. 生成文本样式数组
6. 构建响应对象
7. 返回文本样式信息

## 相关接口

- [添加字幕](./add_captions.md)
- [创建草稿](./create_draft.md)
- [保存草稿](./save_draft.md)
- [生成视频](./gen_video.md)

---

<div align="right">

📚 **项目资源**  
**GitHub**: [https://github.com/Hommy-master/capcut-mate](https://github.com/Hommy-master/capcut-mate)  
**Gitee**: [https://gitee.com/taohongmin-gitee/capcut-mate](https://gitee.com/taohongmin-gitee/capcut-mate)

</div>