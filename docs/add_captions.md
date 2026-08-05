# ADD_CAPTIONS API Documentation

## 🌐 Language Switch
[中文版](./add_captions.zh.md) | [English](./add_captions.md)

## Interface Information

```
POST /openapi/capcut-mate/v1/add_captions
```

## Function Description

Batch-add captions to an existing CapCut/Jianying draft. Supports text color, border, alignment, opacity, font, size, letter/line spacing, scale, position, underline/italic/bold, full-text shadow, keyword highlight and keyword shadow, text animations, and text effects (花字).

## More Documentation

📖 For more detailed documentation and tutorials, please visit: [https://docs.jcaigc.cn](https://docs.jcaigc.cn)

## Request Parameters

### Top-level Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| draft_url | string | ✅ | - | Full draft URL including `draft_id` |
| captions | string | ✅ | - | Caption list as a **JSON string** (not a raw JSON array) |
| text_color | string | ❌ | `"#ffffff"` | Normal text color (hex) |
| border_color | string | ❌ | `null` | Normal text stroke color (hex); `null` means no stroke |
| alignment | integer | ❌ | `1` | Alignment: `0` left, `1` center, `2` right (`3`-`5` reserved) |
| alpha | number | ❌ | `1.0` | Opacity in `[0.0, 1.0]` |
| font | string | ❌ | `null` | Font name (enum/display/alias); `null` uses default |
| font_size | integer | ❌ | `15` | Default font size when a caption item omits `font_size`; must be `>= 1` |
| letter_spacing | number | ❌ | `null` | Letter spacing; `null` means `0` |
| line_spacing | number | ❌ | `null` | Line spacing; `null` means `0` |
| scale_x | number | ❌ | `1.0` | Horizontal scale (`1.0` = original) |
| scale_y | number | ❌ | `1.0` | Vertical scale (`1.0` = original) |
| transform_x | number | ❌ | `0.0` | Horizontal offset in pixels (positive = right) |
| transform_y | number | ❌ | `0.0` | Vertical offset in pixels (positive = down) |
| style_text | boolean | ❌ | `false` | Rich-text style switch (reserved) |
| underline | boolean | ❌ | `false` | Underline |
| italic | boolean | ❌ | `false` | Italic |
| bold | boolean | ❌ | `false` | Bold |
| has_shadow | boolean | ❌ | `false` | Enable **full-caption** text shadow |
| shadow_info | object | ❌ | `null` | Full-caption shadow params; defaults apply if `has_shadow=true` and this is `null` |
| text_effect | string | ❌ | `null` | Text effect name or `effect_id`; a valid effect resets color/border/shadow |

### captions Fields

`captions` is a JSON string that parses to an array of caption objects:

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| start | integer | ✅ | - | Start time in microseconds (`1s = 1_000_000µs`), must be `>= 0` |
| end | integer | ✅ | - | End time in microseconds, must be greater than `start` |
| text | string | ✅ | - | Caption text, non-empty |
| keyword | string | ❌ | `null` | Keywords separated by `\|`, e.g. `"Hello\|World"` |
| keyword_color | string | ❌ | `"#ff7100"` | Keyword fill color (hex) |
| keyword_border_color | string | ❌ | `null` | Keyword stroke color; falls back to top-level `border_color` |
| keyword_font_size | integer | ❌ | `15` | Keyword font size, must be `> 0` |
| keyword_has_shadow | boolean | ❌ | `false` | Enable **keyword-range** shadow |
| keyword_shadow_info | object | ❌ | `null` | Keyword shadow params (same fields as `shadow_info`) |
| font_size | integer | ❌ | `null` | Per-caption normal text size; falls back to top-level `font_size` |
| in_animation | string | ❌ | `null` | Intro animation name from `get_text_animations`, e.g. `"向上滑动"` |
| out_animation | string | ❌ | `null` | Outro animation name, e.g. `"向下滑动"` |
| loop_animation | string | ❌ | `null` | Loop animation name, e.g. `"弹幕滚动"` |
| in_animation_duration | integer | ❌ | `null` | Intro duration (µs); omit to use animation default |
| out_animation_duration | integer | ❌ | `null` | Outro duration (µs); omit to use animation default |
| loop_animation_duration | integer | ❌ | `null` | Single loop duration (µs); omit to use animation default |

### shadow_info / keyword_shadow_info Fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| shadow_alpha | number | ❌ | `1.0` | Shadow opacity `[0, 1]` |
| shadow_color | string | ❌ | `"#000000"` | Shadow color (hex) |
| shadow_diffuse | number | ❌ | `15.0` | Diffuse amount `[0, 100]` |
| shadow_distance | number | ❌ | `5.0` | Distance `[0, 100]` |
| shadow_angle | number | ❌ | `-45.0` | Angle `[-180, 180]` |

Default shadow when enabled without `*_shadow_info`:

```json
{
  "shadow_color": "#000000",
  "shadow_alpha": 0.9,
  "shadow_diffuse": 15,
  "shadow_distance": 5,
  "shadow_angle": -45
}
```

### Notes on text_effect vs shadow

If `text_effect` resolves to a valid effect, the API resets `text_color` to `#ffffff`, `border_color` to `null`, `has_shadow` to `false`, and disables keyword shadow. Omit/leave `text_effect` null when you need custom colors or shadows.

### Notes on keyword shadow

`keyword_has_shadow` / `keyword_shadow_info` work like `keyword_color` / `keyword_border_color`: they stay on the **same caption segment** and do not create an extra text line.

When keyword shadow is enabled, the caption is split into non-overlapping `styles` partitions: normal ranges get `shadows: []`, keyword ranges get the shadow params. Without keyword shadow fields, the original base + keyword overlay path is unchanged.

## Fully Annotated Request Example

`//` comments are for documentation only and are **not** valid in a real request body.

```js
{
  // [Required] Draft URL with draft_id
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",

  // [Required] Caption list JSON string (shown as array for readability)
  "captions": [
    {
      "start": 0,                              // [Required] start time (µs)
      "end": 3000000,                          // [Required] end time (µs), must be > start
      "text": "Hello, CapCut captions",        // [Required] caption text
      "keyword": "CapCut|captions",            // [Optional] keywords separated by |
      "keyword_color": "#ff7100",              // [Optional] keyword color
      "keyword_border_color": "#000000",       // [Optional] keyword stroke color
      "keyword_font_size": 22,                 // [Optional] keyword font size
      "keyword_has_shadow": true,              // [Optional] enable keyword shadow
      "keyword_shadow_info": {                 // [Optional] keyword shadow params
        "shadow_alpha": 0.85,
        "shadow_color": "#000000",
        "shadow_diffuse": 18.0,
        "shadow_distance": 6.0,
        "shadow_angle": -45.0
      },
      "font_size": 18,                         // [Optional] this caption's normal font size
      "in_animation": "向上滑动",               // [Optional] intro animation name
      "out_animation": "向下滑动",              // [Optional] outro animation name
      "loop_animation": "弹幕滚动",             // [Optional] loop animation name
      "in_animation_duration": 500000,         // [Optional] intro duration (µs)
      "out_animation_duration": 500000,        // [Optional] outro duration (µs)
      "loop_animation_duration": 1000000       // [Optional] single loop duration (µs)
    }
  ],

  "text_color": "#ffffff",                     // [Optional] normal text color
  "border_color": "#333333",                   // [Optional] normal stroke color
  "alignment": 1,                              // [Optional] 0 left / 1 center / 2 right
  "alpha": 1.0,                                // [Optional] opacity [0,1]
  "font": "思源黑体",                           // [Optional] font name
  "font_size": 15,                             // [Optional] top-level default font size
  "letter_spacing": 0,                         // [Optional] letter spacing
  "line_spacing": 0,                           // [Optional] line spacing
  "scale_x": 1.0,                              // [Optional] horizontal scale
  "scale_y": 1.0,                              // [Optional] vertical scale
  "transform_x": 0.0,                          // [Optional] X offset (px)
  "transform_y": -200.0,                       // [Optional] Y offset (px)
  "style_text": false,                         // [Optional] style-text switch
  "underline": false,                          // [Optional] underline
  "italic": false,                             // [Optional] italic
  "bold": true,                                // [Optional] bold
  "has_shadow": true,                          // [Optional] full-text shadow switch
  "shadow_info": {                             // [Optional] full-text shadow params
    "shadow_alpha": 0.9,
    "shadow_color": "#000000",
    "shadow_diffuse": 15.0,
    "shadow_distance": 5.0,
    "shadow_angle": -45.0
  },
  // [Optional] set null so custom colors/shadows remain effective
  "text_effect": null
}
```

## Response Format

### Success Response (200)

```json
{
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
  "track_id": "caption-track-uuid",
  "text_ids": ["text1-uuid", "text2-uuid"],
  "segment_ids": ["segment1-uuid", "segment2-uuid"],
  "segment_infos": [
    {
      "id": "segment1-uuid",
      "start": 0,
      "end": 3000000
    }
  ]
}
```

### Response Field Description

| Field | Type | Description |
|-------|------|-------------|
| draft_url | string | Updated draft URL |
| track_id | string | Caption track ID |
| text_ids | array | Added text material IDs |
| segment_ids | array | Segment IDs |
| segment_infos | array | Segment info objects (`id` / `start` / `end`) |

### Error Response (4xx/5xx)

```json
{
  "detail": "Error message description"
}
```

## Usage Examples

### cURL Examples

#### 1. Full-parameter request (all required + optional fields)

> Runnable curl with a legal value for every parameter. `captions` must be a JSON string. `text_effect` is `null` so full-text and keyword shadows stay effective.

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_captions \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
    "captions": "[{\"start\":0,\"end\":3000000,\"text\":\"Hello, CapCut captions\",\"keyword\":\"CapCut|captions\",\"keyword_color\":\"#ff7100\",\"keyword_border_color\":\"#000000\",\"keyword_font_size\":22,\"keyword_has_shadow\":true,\"keyword_shadow_info\":{\"shadow_alpha\":0.85,\"shadow_color\":\"#000000\",\"shadow_diffuse\":18.0,\"shadow_distance\":6.0,\"shadow_angle\":-45.0},\"font_size\":18,\"in_animation\":\"向上滑动\",\"out_animation\":\"向下滑动\",\"loop_animation\":\"弹幕滚动\",\"in_animation_duration\":500000,\"out_animation_duration\":500000,\"loop_animation_duration\":1000000},{\"start\":3000000,\"end\":6000000,\"text\":\"Welcome to caption features\",\"keyword\":\"caption\",\"keyword_color\":\"#457616\",\"keyword_border_color\":\"#111111\",\"keyword_font_size\":20,\"keyword_has_shadow\":true,\"keyword_shadow_info\":{\"shadow_alpha\":0.9,\"shadow_color\":\"#000000\",\"shadow_diffuse\":15.0,\"shadow_distance\":5.0,\"shadow_angle\":-45.0},\"font_size\":16,\"in_animation\":\"右上弹入\",\"out_animation\":\"右上弹出\",\"loop_animation\":\"VHS\",\"in_animation_duration\":400000,\"out_animation_duration\":400000,\"loop_animation_duration\":800000}]",
    "text_color": "#ffffff",
    "border_color": "#333333",
    "alignment": 1,
    "alpha": 1.0,
    "font": "思源黑体",
    "font_size": 15,
    "letter_spacing": 0,
    "line_spacing": 0,
    "scale_x": 1.0,
    "scale_y": 1.0,
    "transform_x": 0.0,
    "transform_y": -200.0,
    "style_text": false,
    "underline": false,
    "italic": false,
    "bold": true,
    "has_shadow": true,
    "shadow_info": {
      "shadow_alpha": 0.9,
      "shadow_color": "#000000",
      "shadow_diffuse": 15.0,
      "shadow_distance": 5.0,
      "shadow_angle": -45.0
    },
    "text_effect": null
  }'
```

**Top-level parameter meanings:**

| Parameter | Example | Meaning |
|-----------|---------|---------|
| draft_url | `...draft_id=2025092811473036584258` | [Required] Target draft URL |
| captions | JSON string with 2 captions | [Required] Caption content + per-item style/animation/keyword config |
| text_color | `#ffffff` | [Optional] Normal text color |
| border_color | `#333333` | [Optional] Normal stroke color |
| alignment | `1` | [Optional] Center align |
| alpha | `1.0` | [Optional] Fully opaque |
| font | `思源黑体` | [Optional] Font name |
| font_size | `15` | [Optional] Top-level default size |
| letter_spacing / line_spacing | `0` | [Optional] Spacing |
| scale_x / scale_y | `1.0` | [Optional] No scaling |
| transform_x | `0.0` | [Optional] No horizontal offset |
| transform_y | `-200.0` | [Optional] Move up 200 px |
| style_text | `false` | [Optional] Style-text switch off |
| underline / italic | `false` | [Optional] No underline / italic |
| bold | `true` | [Optional] Bold on |
| has_shadow | `true` | [Optional] Full-text shadow on |
| shadow_info.* | see above | [Optional] Full-text shadow details |
| text_effect | `null` | [Optional] No 花字, keep colors/shadows |

**Per-caption field meanings:**

| Field | Example | Meaning |
|-------|---------|---------|
| start / end | `0` / `3000000` | [Required] Time range (µs) |
| text | `Hello, CapCut captions` | [Required] Caption text |
| keyword | `CapCut\|captions` | [Optional] Highlight keywords |
| keyword_color | `#ff7100` | [Optional] Keyword color |
| keyword_border_color | `#000000` | [Optional] Keyword stroke |
| keyword_font_size | `22` | [Optional] Keyword size |
| keyword_has_shadow | `true` | [Optional] Keyword shadow on |
| keyword_shadow_info.* | see above | [Optional] Keyword shadow params |
| font_size | `18` | [Optional] This caption's normal size |
| in/out/loop_animation | names above | [Optional] Animation names |
| *_animation_duration | `500000` etc. | [Optional] Animation durations (µs) |

#### 2. Required parameters only

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_captions \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
    "captions": "[{\"start\":0,\"end\":5000000,\"text\":\"Hello, CapCut\"}]"
  }'
```

#### 3. Keyword highlight + keyword shadow

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_captions \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
    "captions": "[{\"start\":0,\"end\":5000000,\"text\":\"Hello CapCut\",\"keyword\":\"CapCut\",\"keyword_color\":\"#ff0000\",\"keyword_font_size\":22,\"keyword_has_shadow\":true,\"keyword_shadow_info\":{\"shadow_alpha\":0.8,\"shadow_color\":\"#000000\",\"shadow_diffuse\":20.0,\"shadow_distance\":8.0,\"shadow_angle\":-45.0}}]",
    "text_color": "#ffffff",
    "font_size": 16,
    "alignment": 1
  }'
```

#### 4. Full-text shadow with default shadow_info

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_captions \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
    "captions": "[{\"start\":0,\"end\":5000000,\"text\":\"Hello, CapCut\"}]",
    "text_color": "#ffffff",
    "font_size": 20,
    "has_shadow": true
  }'
```

#### 5. Text effect (花字)

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_captions \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
    "captions": "[{\"start\":0,\"end\":5000000,\"text\":\"Effect demo\"}]",
    "text_effect": "白字橘色发光花字"
  }'
```

## Error Code Description

| Error Code | Error Message | Description | Solution |
|------------|---------------|-------------|----------|
| 400 | draft_url is required | Missing draft URL | Provide a valid `draft_url` |
| 400 | captions is required | Missing captions | Provide valid `captions` |
| 400 | captions format error | Invalid JSON | Fix JSON string format |
| 400 | Time range invalid | end must be > start | Fix start/end |
| 404 | Draft does not exist | Invalid/missing draft | Check draft URL |
| 500 | Caption processing failed | Internal error | Contact support |

## Notes

1. **Time unit**: microseconds (`1s = 1_000_000µs`)
2. **captions format**: must be a valid JSON **string** inside the request JSON
3. **Color format**: hex, e.g. `#ffffff`
4. **Animation names**: from `get_text_animations`
5. **Text effect names**: from `get_text_effects`
6. **Coordinates**: `transform_x` / `transform_y` are pixels, converted internally by canvas size
7. **Keyword shadow**: applies only to keyword ranges; full-text shadow uses `has_shadow` / `shadow_info`

## Related Interfaces

- [Create Draft](./create_draft.md)
- [Caption Infos](./caption_infos.md)
- [Get Text Animations](./get_text_animations.md)
- [Get Text Effects](./get_text_effects.md)
- [Save Draft](./save_draft.md)

---

<div align="right">

📚 **Project Resources**  
**GitHub**: [https://github.com/Hommy-master/capcut-mate](https://github.com/Hommy-master/capcut-mate)  
**Gitee**: [https://gitee.com/taohongmin-gitee/capcut-mate](https://gitee.com/taohongmin-gitee/capcut-mate)

</div>
