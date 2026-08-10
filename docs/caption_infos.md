# CAPTION_INFOS API Documentation

## 🌐 Language Switch
[中文版](./caption_infos.zh.md) | [English](./caption_infos.md)

## Interface Information

```
POST /openapi/capcut-mate/v1/caption_infos
```

## Function Description

Build a caption-info JSON string from text list + timelines. The result can be passed directly to `add_captions` as `captions`. Supports font size, keyword highlight (color/border/size/shadow), intro/loop/outro animations, and transition fields.

## More Documentation

📖 For more detailed documentation and tutorials, please visit: [https://docs.jcaigc.cn](https://docs.jcaigc.cn)

## Request Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| texts | array[string] | ✅ | - | Caption text list; one item per caption |
| timelines | array[object] | ✅ | - | Timeline list, index-aligned with `texts` |
| timelines[].start | integer | ✅ | - | Caption start time (µs), must be `>= 0` |
| timelines[].end | integer | ✅ | - | Caption end time (µs), must be greater than `start` |
| font_size | integer | ❌ | `null` | Normal text size written into each caption; omitted from output if not provided |
| keyword_color | string | ❌ | `null` | Keyword color (hex), written into each caption |
| keyword_border_color | string | ❌ | `null` | Keyword stroke color (hex), written into each caption |
| keyword_font | string | ❌ | `null` | Keyword font name, written into each caption |
| keyword_font_size | integer | ❌ | `null` | Keyword font size, written into each caption |
| keyword_has_shadow | boolean | ❌ | `null` | Whether to enable keyword shadow, written into each caption |
| keyword_shadow_info | object | ❌ | `null` | Keyword shadow params (same fields as `add_captions.shadow_info`) |
| keywords | array[string] | ❌ | `null` | Keyword list assigned by index to `texts[i]`; missing indexes get empty `keyword` |
| in_animation | string | ❌ | `null` | Intro animation name, e.g. `"向上滑动"` |
| in_animation_duration | integer | ❌ | `null` | Intro duration (µs) |
| loop_animation | string | ❌ | `null` | Loop animation name, e.g. `"弹幕滚动"` |
| loop_animation_duration | integer | ❌ | `null` | Single-loop duration (µs) |
| out_animation | string | ❌ | `null` | Outro animation name, e.g. `"向下滑动"` |
| out_animation_duration | integer | ❌ | `null` | Outro duration (µs) |
| transition | string | ❌ | `null` | Transition name written into generated infos |
| transition_duration | integer | ❌ | `null` | Transition duration (µs) |

### keyword_shadow_info Fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| shadow_alpha | number | ❌ | `1.0` | Shadow opacity `[0, 1]` |
| shadow_color | string | ❌ | `"#000000"` | Shadow color (hex) |
| shadow_diffuse | number | ❌ | `15.0` | Diffuse amount `[0, 100]` |
| shadow_distance | number | ❌ | `5.0` | Distance `[0, 100]` |
| shadow_angle | number | ❌ | `-45.0` | Angle `[-180, 180]` |

### Notes

1. If `texts` and `timelines` lengths differ, the shorter length is used (no hard error).
2. `keywords[i]` becomes caption `i`'s `keyword`; shorter `keywords` yields empty string for remaining items.
3. Optional fields are written into output only when not `null`.

## Fully Annotated Request Example

`//` comments are documentation-only and are **not** valid in a real request body.

```js
{
  // [Required] Caption texts, one per item
  "texts": [
    "Welcome to the CapCut tutorial",
    "This is a caption example"
  ],

  // [Required] Timelines, index-aligned with texts
  "timelines": [
    {
      "start": 0,                 // [Required] first caption start (µs)
      "end": 3000000              // [Required] first caption end (µs)
    },
    {
      "start": 3000000,           // [Required] second caption start (µs)
      "end": 6000000              // [Required] second caption end (µs)
    }
  ],

  "font_size": 24,                // [Optional] normal text size
  "keyword_color": "#FF5500",     // [Optional] keyword color
  "keyword_border_color": "#000000", // [Optional] keyword stroke color
  "keyword_font": "思源中宋",          // [Optional] keyword font
  "keyword_font_size": 28,        // [Optional] keyword font size
  "keyword_has_shadow": true,     // [Optional] enable keyword shadow
  "keyword_shadow_info": {        // [Optional] keyword shadow details
    "shadow_alpha": 0.85,         // opacity [0,1]
    "shadow_color": "#000000",    // shadow color
    "shadow_diffuse": 18.0,       // diffuse [0,100]
    "shadow_distance": 6.0,       // distance [0,100]
    "shadow_angle": -45.0         // angle [-180,180]
  },
  "keywords": [                   // [Optional] keywords assigned by index
    "CapCut",
    "caption"
  ],
  "in_animation": "向上滑动",      // [Optional] intro animation
  "in_animation_duration": 500000, // [Optional] intro duration (µs)
  "loop_animation": "弹幕滚动",    // [Optional] loop animation
  "loop_animation_duration": 1000000, // [Optional] single-loop duration (µs)
  "out_animation": "向下滑动",     // [Optional] outro animation
  "out_animation_duration": 500000, // [Optional] outro duration (µs)
  "transition": "淡入淡出",        // [Optional] transition name
  "transition_duration": 300000   // [Optional] transition duration (µs)
}
```

## Response Format

### Success Response (200)

```json
{
  "infos": "[{\"start\":0,\"end\":3000000,\"text\":\"Welcome to the CapCut tutorial\",\"keyword\":\"CapCut\",\"keyword_color\":\"#FF5500\",\"keyword_border_color\":\"#000000\",\"keyword_font\":\"思源中宋\",\"keyword_font_size\":28,\"keyword_has_shadow\":true,\"keyword_shadow_info\":{\"shadow_alpha\":0.85,\"shadow_color\":\"#000000\",\"shadow_diffuse\":18.0,\"shadow_distance\":6.0,\"shadow_angle\":-45.0},\"font_size\":24,\"in_animation\":\"向上滑动\",\"in_animation_duration\":500000,\"loop_animation\":\"弹幕滚动\",\"loop_animation_duration\":1000000,\"out_animation\":\"向下滑动\",\"out_animation_duration\":500000,\"transition\":\"淡入淡出\",\"transition_duration\":300000},{\"start\":3000000,\"end\":6000000,\"text\":\"This is a caption example\",\"keyword\":\"caption\",\"keyword_color\":\"#FF5500\",\"keyword_border_color\":\"#000000\",\"keyword_font\":\"思源中宋\",\"keyword_font_size\":28,\"keyword_has_shadow\":true,\"keyword_shadow_info\":{\"shadow_alpha\":0.85,\"shadow_color\":\"#000000\",\"shadow_diffuse\":18.0,\"shadow_distance\":6.0,\"shadow_angle\":-45.0},\"font_size\":24,\"in_animation\":\"向上滑动\",\"in_animation_duration\":500000,\"loop_animation\":\"弹幕滚动\",\"loop_animation_duration\":1000000,\"out_animation\":\"向下滑动\",\"out_animation_duration\":500000,\"transition\":\"淡入淡出\",\"transition_duration\":300000}]"
}
```

### Response Field Description

| Field | Type | Description |
|-------|------|-------------|
| infos | string | Caption info JSON string; usable as `add_captions.captions` |

### Error Response (4xx/5xx)

```json
{
  "detail": "Error message description"
}
```

## Usage Examples

### cURL Examples

#### 1. Full-parameter request (all required + optional fields)

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/caption_infos \
  -H "Content-Type: application/json" \
  -d '{
    "texts": ["Welcome to the CapCut tutorial", "This is a caption example"],
    "timelines": [
      {"start": 0, "end": 3000000},
      {"start": 3000000, "end": 6000000}
    ],
    "font_size": 24,
    "keyword_color": "#FF5500",
    "keyword_border_color": "#000000",
    "keyword_font": "思源中宋",
    "keyword_font_size": 28,
    "keyword_has_shadow": true,
    "keyword_shadow_info": {
      "shadow_alpha": 0.85,
      "shadow_color": "#000000",
      "shadow_diffuse": 18.0,
      "shadow_distance": 6.0,
      "shadow_angle": -45.0
    },
    "keywords": ["CapCut", "caption"],
    "in_animation": "向上滑动",
    "in_animation_duration": 500000,
    "loop_animation": "弹幕滚动",
    "loop_animation_duration": 1000000,
    "out_animation": "向下滑动",
    "out_animation_duration": 500000,
    "transition": "淡入淡出",
    "transition_duration": 300000
  }'
```

**Full-parameter meanings:**

| Parameter | Example | Meaning |
|-----------|---------|---------|
| texts | `["Welcome to the CapCut tutorial", "This is a caption example"]` | [Required] Two caption texts |
| timelines[0].start / end | `0` / `3000000` | [Required] First caption time range (µs) |
| timelines[1].start / end | `3000000` / `6000000` | [Required] Second caption time range (µs) |
| font_size | `24` | [Optional] Normal text size |
| keyword_color | `#FF5500` | [Optional] Keyword color |
| keyword_border_color | `#000000` | [Optional] Keyword stroke color |
| keyword_font | `思源中宋` | [Optional] Keyword font |
| keyword_font_size | `28` | [Optional] Keyword font size |
| keyword_has_shadow | `true` | [Optional] Enable keyword shadow |
| keyword_shadow_info.shadow_alpha | `0.85` | [Optional] Keyword shadow opacity |
| keyword_shadow_info.shadow_color | `#000000` | [Optional] Keyword shadow color |
| keyword_shadow_info.shadow_diffuse | `18.0` | [Optional] Keyword shadow diffuse |
| keyword_shadow_info.shadow_distance | `6.0` | [Optional] Keyword shadow distance |
| keyword_shadow_info.shadow_angle | `-45.0` | [Optional] Keyword shadow angle |
| keywords | `["CapCut", "caption"]` | [Optional] Keywords assigned by index |
| in_animation | `向上滑动` | [Optional] Intro animation |
| in_animation_duration | `500000` | [Optional] Intro duration (µs) |
| loop_animation | `弹幕滚动` | [Optional] Loop animation |
| loop_animation_duration | `1000000` | [Optional] Single-loop duration (µs) |
| out_animation | `向下滑动` | [Optional] Outro animation |
| out_animation_duration | `500000` | [Optional] Outro duration (µs) |
| transition | `淡入淡出` | [Optional] Transition name |
| transition_duration | `300000` | [Optional] Transition duration (µs) |

#### 2. Required parameters only

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/caption_infos \
  -H "Content-Type: application/json" \
  -d '{
    "texts": ["Hello World"],
    "timelines": [{"start": 0, "end": 3000000}]
  }'
```

#### 3. Keyword highlight + keyword shadow

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/caption_infos \
  -H "Content-Type: application/json" \
  -d '{
    "texts": ["Welcome to watch our video", "This is a wonderful example"],
    "timelines": [
      {"start": 0, "end": 3000000},
      {"start": 3000000, "end": 6000000}
    ],
    "font_size": 24,
    "keyword_color": "#FF5500",
    "keyword_border_color": "#111111",
    "keyword_font": "思源中宋",
    "keyword_font_size": 28,
    "keyword_has_shadow": true,
    "keyword_shadow_info": {
      "shadow_alpha": 0.9,
      "shadow_color": "#000000",
      "shadow_diffuse": 15.0,
      "shadow_distance": 5.0,
      "shadow_angle": -45.0
    },
    "keywords": ["video", "wonderful"]
  }'
```

#### 4. Use with add_captions

1. Call `caption_infos` and read `infos` from the response.
2. Pass that string unchanged as `add_captions.captions`.

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_captions \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
    "captions": "[{\"start\":0,\"end\":3000000,\"text\":\"Welcome to the CapCut tutorial\",\"keyword\":\"CapCut\",\"keyword_color\":\"#FF5500\",\"keyword_has_shadow\":true,\"font_size\":24}]",
    "text_color": "#ffffff",
    "alignment": 1
  }'
```

## Error Code Description

| Error Code | Error Message | Description | Solution |
|------------|---------------|-------------|----------|
| 400 | texts is required | Missing texts | Provide non-empty `texts` |
| 400 | timelines is required | Missing timelines | Provide valid `timelines` |
| 500 | Caption information generation failed | Internal error | Contact support |

## Notes

1. **Time unit**: microseconds (`1s = 1_000_000µs`)
2. **Color format**: hex, e.g. `#FF0000`
3. **Animation names**: prefer names from `get_text_animations`
4. **Output usage**: response `infos` can be used as `add_captions.captions`
5. **Keyword shadow**: this API only writes fields; rendering happens in `add_captions`

## Workflow

1. Validate `texts` / `timelines`
2. Align arrays by shorter length
3. Build each caption object (keywords + optional style/animation fields)
4. Serialize to JSON string and return

## Related Interfaces

- [Create Draft](./create_draft.md)
- [Add Captions](./add_captions.md)
- [Get Text Animations](./get_text_animations.md)
- [Save Draft](./save_draft.md)

---

<div align="right">

📚 **Project Resources**  
**GitHub**: [https://github.com/Hommy-master/capcut-mate](https://github.com/Hommy-master/capcut-mate)  
**Gitee**: [https://gitee.com/taohongmin-gitee/capcut-mate](https://gitee.com/taohongmin-gitee/capcut-mate)

</div>
