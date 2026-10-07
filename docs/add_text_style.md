# ADD_TEXT_STYLE API Documentation

## 🌐 Language Switch
[中文版](./add_text_style.zh.md) | [English](./add_text_style.md)

## Interface Information

```bash
POST /openapi/capcut-mate/v1/add_text_style
```

## Function Description

Create rich text styles for text, supporting keyword highlighting, color settings, font size adjustments, and other functions. This interface can convert plain text into rich text format containing style information, achieving keyword highlighting and diverse text display effects.

## More Documentation

📖 For more detailed documentation and tutorials, please visit: [https://docs.jcaigc.cn](https://docs.jcaigc.cn)

## Request Parameters

```json
{
  "text": "五个快乐到死的顶级思维",
  "keyword": "快乐|顶级思维",
  "font_size": 12,
  "keyword_color": "#ff7100",
  "keyword_font_size": 15
}
```

### Parameter Description

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| text | string |✅ | - | Text content to process |
| keyword | string |✅ | - | Keywords, multiple separated by \| |
| font_size | integer |❌ | 12 | Font size of plain text |
| keyword_color | string |❌ | "#ff7100" | Keyword text color (hexadecimal) |
| keyword_font_size | integer |❌ | 15 | Keyword font size |

### Parameter Details

#### Text Parameters

- **text**: Original text content to be processed for styling
  - Example: `"五个快乐到死的顶级思维"`

#### Keyword Parameters

- **keyword**: Keywords to be highlighted, support multiple keywords separated by vertical bar (|)
  - Example: `"快乐|顶级思维"`
  - Note: System matches keywords by length priority to avoid short keywords overriding long keywords

#### Font Size Parameters

- **font_size**: Font size of plain text (non-keywords)
  - Default: 12
  - Recommended range: 8-72

- **keyword_font_size**: Font size of keywords
  - Default: 15
  - Recommended range: 8-72

#### Color Parameters

- **keyword_color**: Text color of keywords, using hexadecimal format
  - Default: `"#ff7100"` (orange)
  - Format: #RRGGBB
  - Examples: `"#ff0000"` (red), `"#00ff00"` (green), `"#0000ff"` (blue)

## Response Format

### Success Response (200)

```json
{
  "code": 0,
  "message": "success",
  "text_style": "{\"styles\":[{\"fill\":{\"content\":{\"solid\":{\"color\":[1,1,1]}}},\"range\":[0,2],\"size\":12,\"font\":{\"id\":\"\",\"path\":\"D:\"}},{\"fill\":{\"content\":{\"solid\":{\"color\":[1,0.44313725490196076,0]}}},\"range\":[2,4],\"size\":15,\"font\":{\"id\":\"\",\"path\":\"D:\"},\"useLetterColor\":true},{\"fill\":{\"content\":{\"solid\":{\"color\":[1,1,1]}}},\"range\":[4,7],\"size\":12,\"font\":{\"id\":\"\",\"path\":\"D:\"}},{\"fill\":{\"content\":{\"solid\":{\"color\":[1,0.44313725490196076,0]}}},\"range\":[7,11],\"size\":15,\"font\":{\"id\":\"\",\"path\":\"D:\"},\"useLetterColor\":true}],\"text\":\"五个快乐到死的顶级思维\"}"
}
```

### Response Field Description

| Field | Type | Description |
|-------|------|-------------|
| text_style | string | Text style JSON string, containing styles array and text field |

### Error Response

```json
{
  "code": 2026,
  "message": "Invalid text style information, please check text or keyword parameters"
}
```

## Usage Examples

### cURL Examples

#### 1. Basic Text Style Creation

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_text_style \
  -H "Content-Type: application/json" \
  -d '{
    "text": "五个快乐到死的顶级思维",
    "keyword": "快乐|顶级思维"
  }'
```

#### 2. Custom Font Sizes

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

#### 3. Custom Keyword Color

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_text_style \
  -H "Content-Type: application/json" \
  -d '{
    "text": "五个快乐到死的顶级思维",
    "keyword": "快乐|顶级思维",
    "keyword_color": "#ff0000"
  }'
```

## Error Code Description

| Error Code | Error Message | Description | Solution |
|------------|---------------|-------------|----------|
| 2026 | Invalid text style information | Text or keyword parameter format error or invalid value | Check if text and keyword parameters meet requirements |
| 2027 | Text style creation failed | Error occurred during text style creation | Contact technical support |

## Notes

1. **Keyword Matching**: Keywords are matched by length priority, longer keywords take precedence over shorter ones
2. **Color Format**: Use standard hexadecimal color format #RRGGBB
3. **Font Size**: Recommended within 8-72 range
4. **Keyword Separation**: Multiple keywords separated by vertical bar |
5. **Case Sensitivity**: Keyword matching is case-sensitive

## Workflow

1. Validate required parameters (text, keyword)
2. Parse keyword string
3. Find keyword positions in text
4. Convert color values to RGB format
5. Generate text style array
6. Build response object
7. Return text style information

## Related Interfaces

- [Add Captions](./add_captions.md)
- [Create Draft](./create_draft.md)
- [Save Draft](./save_draft.md)
- [Generate Video](./gen_video.md)

---

<div align="right">

📚 **Project Resources**  
**GitHub**: [https://github.com/Hommy-master/capcut-mate](https://github.com/Hommy-master/capcut-mate)  
**Gitee**: [https://gitee.com/taohongmin-gitee/capcut-mate](https://gitee.com/taohongmin-gitee/capcut-mate)

</div>