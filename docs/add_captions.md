# ADD_CAPTIONS API Documentation

## 🌐 Language Switch
[中文版](./add_captions.zh.md) | [English](./add_captions.md)

## Interface Information

```
POST /openapi/capcut-mate/v1/add_captions
```

## Function Description

Batch-add captions to an existing CapCut/Jianying draft. Supports text color, border, alignment, opacity, font, size, letter/line spacing, scale, position, underline/italic/bold, full-text shadow, keyword highlight and keyword shadow, text animations, and text effects (花字).

## Request Parameters

### Top-level Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| draft_url | string | ✅ | - | Full draft URL including `draft_id` |
| captions | string | ✅ | - | Caption list as a **JSON string** (not a raw JSON array) |
| text_color | string | ❌ | `"#ffffff"` | Normal text color (hex) |
| border_color | string | ❌ | `null` | Normal text stroke color (hex); `null` means no stroke |
| alignment | integer | ❌ | `1` | Alignment: `0` left, `1` center, `2` right (horizontal); `3` vertical center, `4` vertical left, `5` vertical right (vertical typesetting) |
| alpha | number | ❌ | `1.0` | Opacity in `[0.0, 1.0]` |
| font | string | ❌ | `null` | Font name from Supported Fonts below (enum/display/alias also ok); `null` uses default |
| font_size | integer | ❌ | `15` | Default font size when a caption item omits `font_size`; must be `>= 1` |
| letter_spacing | number | ❌ | `null` | Letter spacing; `null` means `0` |
| line_spacing | number | ❌ | `null` | Line spacing; `null` means `0` |
| line_max_width | number | ❌ | `0.82` | Max line width as a fraction of screen width, range `[0.0, 1.0]`; used with auto-wrapping |
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
| has_background | boolean | ❌ | `false` | Enable the **full-caption** text background (a solid plate drawn behind the text) |
| background_info | object | ❌ | `null` | Full-caption background params; defaults apply if `has_background=true` and this is `null`. Ignored when `has_background=false` |
| text_effect | string | ❌ | `null` | Text effect name or `effect_id`; a valid effect resets color/border/shadow |
| text_template | string | ❌ | `null` | Text template name or `effect_id` (numeric ids pass through); mutually exclusive with `text_effect`, template wins |
| text_bubble | string | ❌ | `null` | Bubble name or `resource_id`/`effect_id`; for bubbles outside the catalog pass an explicit `"effect_id:resource_id"` pair. Priority: text template > bubble > text effect |
| text_glow | string | ❌ | `null` | Glow preset name (e.g. `"外发光"`) or `resource_id`/`effect_id`; for glows outside the catalog pass an explicit `"effect_id:resource_id"` pair. **Not** mutually exclusive with text effects/templates/bubbles — it stacks with them |

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
| keyword_font | string | ❌ | `null` | Keyword font (display/enum/alias from Supported Fonts); falls back to body caption `font` |
| keyword_font_size | integer | ❌ | `null` | Keyword font size, must be `> 0`; falls back to body size (item `font_size`, else top-level `font_size`) |
| keyword_has_shadow | boolean | ❌ | `false` | Enable **keyword-range** shadow |
| keyword_shadow_info | object | ❌ | `null` | Keyword shadow params (same fields as `shadow_info`) |
| font_size | integer | ❌ | `null` | Per-caption normal text size; falls back to top-level `font_size` |
| in_animation | string | ❌ | `null` | Intro animation name from Intro animations below, e.g. `"向上滑动"` |
| out_animation | string | ❌ | `null` | Outro animation name from Outro animations below, e.g. `"向下滑动"` |
| loop_animation | string | ❌ | `null` | Loop animation name from Loop animations below, e.g. `"弹幕滚动"` |
| in_animation_duration | integer | ❌ | `null` | Intro duration (µs); omit to use animation default |
| out_animation_duration | integer | ❌ | `null` | Outro duration (µs); omit to use animation default |
| loop_animation_duration | integer | ❌ | `null` | Single loop duration (µs); omit to use animation default |
| text_template | string | ❌ | `null` | Text template name or `effect_id` for this caption; falls back to top-level `text_template` |
| text_bubble | string | ❌ | `null` | Bubble name, `resource_id`/`effect_id`, or an explicit `"effect_id:resource_id"` pair for this caption; falls back to top-level `text_bubble` |

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

### background_info Fields

Field names map **one-to-one** onto the `background_*` fields of a JianYing draft's `materials.texts[*]`,
and values use draft semantics too — a background-bearing text material from a real draft can be copied in as-is.

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| background_color | string | ❌ | `"#000000"` | Background color (hex). The leading `#` is optional and case is insensitive; output is normalized to `#RRGGBB` |
| background_style | integer | ❌ | `1` | Background style; `1`/`2` are the two styles offered by JianYing. `0` means "no background" and **must not be passed** |
| background_alpha | number | ❌ | `1.0` | Background opacity `[0, 1]` |
| background_round_radius | number | ❌ | `0.0` | Background corner radius `[0, 1]` |
| background_height | number | ❌ | `0.14` | Background height (padding around the text) `[0, 1]` |
| background_width | number | ❌ | `0.14` | Background width (padding around the text) `[0, 1]` |
| background_horizontal_offset | number | ❌ | `0.0` | Background horizontal offset `[-1, 1]`; `0` is centered, negative moves left |
| background_vertical_offset | number | ❌ | `0.0` | Background vertical offset `[-1, 1]`; `0` is centered, negative moves up |

Default background when `has_background=true` without `background_info`:

```json
{
  "background_color": "#000000",
  "background_style": 1,
  "background_alpha": 1.0,
  "background_round_radius": 0.0,
  "background_height": 0.14,
  "background_width": 0.14,
  "background_horizontal_offset": 0.0,
  "background_vertical_offset": 0.0
}
```

### Notes on alignment

| Value | Meaning |
|---|---|
| 0 | Left (horizontal) |
| 1 | Center (horizontal) |
| 2 | Right (horizontal) |
| 3 | Vertical center (vertical typesetting + center) |
| 4 | Vertical left (vertical typesetting + left) |
| 5 | Vertical right (vertical typesetting + right) |

`alignment` controls in-box typesetting and line alignment, not canvas position. Use `transform_x` / `transform_y` to move captions on screen. Values `3`/`4`/`5` set the draft material `typesetting` to vertical.

### Notes on text_effect vs shadow

If `text_effect` resolves to a valid effect, the API resets `text_color` to `#ffffff`, `border_color` to `null`, `has_shadow` to `false`, and disables keyword shadow. Omit/leave `text_effect` null when you need custom colors or shadows.

### Notes on text_template

`text_template` applies a JianYing 文字模板 (a bundled preset of font, colors, stroke, decorative stickers and intro animation). The value is either the template name (Chinese) or its `effect_id`; a numeric value not present in the mapping table is passed through as an `effect_id`.

The catalog lives in `config/text_template.json` and currently holds **5166** templates (4668 distinct names), with fields `id` (the `effect_id`/`resource_id` — the same value), `title`, `is_vip`, `category_id` and `category_name`, plus two optional fields: `resources` (the template resource manifest) and `animation` (the template's built-in intro animation). The list is community-sourced and can be edited freely.

- **Top-level vs per-caption**: the top-level `text_template` is the default for the whole batch; a per-caption `text_template` takes precedence.
- **Mutually exclusive with text effects**: when both `text_effect` and `text_template` are supplied, the **template wins** and `text_effect` is ignored (a warning is logged). The template owns the segment's material identity while the effect owns `styles[0].effectStyle`, so applying both has undefined rendering.
- **Colors / stroke / shadow**: unlike text effects, a template does **not** reset `text_color` / `border_color` / `has_shadow` — the template supplies its own colors. An unresolvable template falls back to a plain caption with a warning.
- **Draft structure**: for a templated caption the segment's `material_id` points at the template material in `materials.text_templates`, while the text material is still written to `materials.texts` and linked back via the template's `text_info_resources[].text_material_id`. The returned `text_ids` remain **text material** ids.
- **Duplicate names**: the catalog contains 498 duplicate names (e.g. 41 templates called `我的水印`). A name lookup always resolves to the **first matching entry** in the config; pass the `effect_id` when you need an exact template.
- **VIP templates**: 4735 of the 5166 templates are VIP (`is_vip: true`). A VIP template the account has not purchased may not render in JianYing — callers should ensure entitlement; the `is_vip` field is available for filtering.
- **Intro animation and resource manifest**: a template's built-in intro animation does not appear from `effect_id` alone. Add `resources` (including the `panel: "text"` animation resource) and `animation` (`type`/`duration`/`resource_id`) to the catalog entry; the generator then writes it into the segment's `sticker_animation` material. `path` may be left empty — JianYing fetches by `resource_id`. Templates without these fields still render text, but without the template animation. Only a template's **single text slot** is supported for now.

### Notes on text_bubble

`text_bubble` applies a JianYing 气泡 — the decorative plate drawn behind the text (speech bubbles, labels, stamps). A bubble is the third kind of text effect, separate from text effects and templates: in the draft it is one entry in `materials.effects` with `type: "text_shape"`, referenced by the text segment's `extra_material_refs`.

**The key difference from effects/templates: a bubble's `effect_id` and `resource_id` are not the same value.** In a real draft they look like `effect_id: "716434"` and `resource_id: "6821385652727190024"`. Both are required — with only one, JianYing cannot locate the resource. Therefore:

- The catalog `config/bubble.json` stores them separately: `id` is the **resource_id** and `effect_id` is given on its own (note this differs from `text_template.json`, where `id` doubles as the `effect_id`).
- For any bubble outside the catalog, pass an explicit `"effect_id:resource_id"` pair, e.g. `"716434:6821385652727190024"`.
- **A single numeric value is not passed through** (the opposite of `text_template`), because the other id cannot be inferred; it is treated as not found and the caption falls back to a plain one.

Accepted forms and priority:

- **Four forms**: bubble name (e.g. `"背景装饰54"`), `resource_id`, `effect_id`, or an explicit `"effect_id:resource_id"` pair.
- **Top-level vs per-caption**: the top-level `text_bubble` is the default for the whole batch; a per-caption `text_bubble` takes precedence.
- **Priority is text template > bubble > text effect**: a bubble and a text effect are both text effects and are mutually exclusive, so **the bubble wins** over `text_effect` (which is ignored with a warning); when combined with `text_template` the **template wins** and the bubble is ignored with a warning.
- **Colors / stroke / shadow**: a bubble only draws a decorative plate behind the text and does **not** reset `text_color` / `border_color` / `has_shadow` (unlike a text effect, matching a template). An unresolvable bubble falls back to a plain caption with a warning.
- **Known limitations**: bubble material fields such as `path` and `request_id` depend on the creator's local JianYing cache and are not emitted by this service — JianYing fetches them by `effect_id`/`resource_id` (the same approach used for text effects). To pin such fields verbatim, put them in the `material` field of the `config/bubble.json` entry; they are written into the bubble material as-is.
- **Not verified in JianYing**: the `气泡1` draft only proves the **draft structure** (material fields and segment references match item by item); the bubble's **actual rendering** has not been verified. Text effects emit the same minimal field set and work, but a bubble is a different material type (`text_shape`) on a different render path, so this is inferred rather than measured — run it once in JianYing before shipping.
- **Catalog size**: only **1** bubble verified against a real draft (`背景装饰54`) is included, so a **name lookup only resolves within the catalog**. Use the explicit id pair for any other bubble, or extend `config/bubble.json` with the same field shape (`id` is the resource_id, `effect_id` is given separately, both required).
- **On bulk import**: 速创小助手's bubble page lists 326 bubbles with names and preview images (its names are the JianYing bubble names, e.g. `情绪07` / `会话105`), but it **does not expose `effect_id`/`resource_id`** (only that site's 特效 page carries id pairs), so they cannot be imported in bulk — filling in ids requires confirming each bubble in JianYing's 气泡 panel.

### Notes on text background

`has_background` / `background_info` apply a JianYing 背景 — a solid plate drawn behind the text, commonly used to keep captions readable over busy footage. In the draft it is a group of `background_*` fields on the text material `materials.texts[*]`, plus bit 16 set in `check_flag` (`7 → 23`).

- **Switch semantics**: it only takes effect when `has_background=true`; passing `background_info` alone is **silently ignored** (same as `has_shadow` / `shadow_info`). With `has_background=true` and no `background_info`, the default black background is used.
- **Values are draft values**: `background_info` field names and values map **one-to-one** onto the draft, with no unit conversion — the one exception is that the color is normalized to uppercase `#RRGGBB`. Note `background_style` only accepts `1`/`2`; the draft's `0` (meaning "no background") **cannot be passed** — just omit `has_background` instead.
- **The color is not RGB-converted**: border and shadow colors go through `hex_to_rgb` and become `[r, g, b]`, but the background color **does not** — the draft stores the `"#RRGGBB"` string verbatim. So an invalid color **falls back to black with a warning**, rather than to white like `text_color`.
- **With text effects**: an effect resets `text_color` / `border_color` / `has_shadow` to their defaults but **does not reset the background** (the background is outside the effect's `effectStyle`, matching how bubbles behave). Using both stacks them visually, and the service logs a warning.
- **With templates**: the background lives on the text material, while the template material (`materials.text_templates`) is a **separate entry** carrying no `background_*` fields, so it is not applied twice. The template's own decoration may still clash visually — verify by running it.
- **With keyword highlighting**: highlighting uses `content.styles` partitions while the background sits on the material, so the two do not interact.
- **Not verified in JianYing**: the `背景` draft proves the **draft structure** (all 8 `background_*` fields and `check_flag: 23` match item by item, and the defaults are exactly the values of the background-bearing caption in that draft), but the **actual rendering** of a draft generated by this service has not been verified. `background_style: 2` and every non-default value have no verified sample at all — run it once in JianYing before shipping.
- **Offset pitfall**: `background_horizontal_offset` / `background_vertical_offset` use **draft coordinates** `[-1, 1]` where `0` is centered — not the `[0, 1]` coordinates some internal APIs use. Copying values straight from a draft is the safe route.

### Notes on text glow

`text_glow` applies a JianYing 发光 — a halo around the text edges. It is the fourth kind of text effect, separate from text effects, templates and bubbles: in the draft it is one entry in `materials.effects` with `type: "bloom"`, referenced by the text segment's `extra_material_refs` (appended after `sticker_animation`), and the text material gets bit 64 set in `check_flag` (`7 → 71`). Apart from `check_flag`, **a glowing text material is field-for-field identical to a plain caption** — the glow does not touch the fill/stroke/shadow.

**As with bubbles, a glow's `effect_id` and `resource_id` are not the same value** (`effect_id: "9762443"`, `resource_id: "7202576698775179837"`). Both are required — with only one, JianYing cannot locate the resource. Therefore:

- The catalog `config/glow.json` stores them separately: `id` is the **resource_id** and `effect_id` is given on its own.
- For any glow outside the catalog, pass an explicit `"effect_id:resource_id"` pair.
- **A single numeric value is not passed through** (the opposite of `text_template`); it is treated as not found and the caption falls back to a plain one.

Accepted forms and priority:

- **Four forms**: preset name (e.g. `"外发光"`, `"轮廓光"`), `resource_id`, `effect_id`, or an explicit `"effect_id:resource_id"` pair.
- **No mutual exclusion**: a glow neither owns the segment's material identity (that is the template's job) nor changes the text styling (that is the effect's job) — it just adds one more material, so it **can be combined** with a text effect, a template and a bubble. There is no precedence between them. A text effect does not reset the glow (matching how it treats the background), and the service logs a warning that the two stack visually.
- **`bloom_params` differ per preset**: the glow's color/strength/range/direction live in the material's `bloom_params`, supplied by the catalog per preset (外发光 `range 0.2, strength 0.3`; 轮廓光 `range 0.4, strength 0.5`). **An out-of-catalog glow has no verified values** — the service falls back to the 外发光 values with a warning. JianYing does not re-derive these from `resource_id`, so add the preset to `config/glow.json` to reproduce it exactly.
- **Top-level only**: `text_glow` applies to the whole batch and is **not settable per caption**. Mixing two presets in one draft (e.g. 默认文本2 with 外发光, 默认文本3 with 轮廓光) requires two `add_captions` calls.
- **Not verified in JianYing**: the `发光` draft proves the **draft structure** (both presets' material fields and `check_flag: 71` match item by item), but the **actual rendering** of a draft generated by this service has not been verified — including whether `bloom_params` is required, whether the out-of-catalog fallback values work, and how a glow actually looks stacked with a text effect or background. Run it once in JianYing before shipping.
- **Catalog size**: only the **2** presets verified against the `发光` draft (`外发光`, `轮廓光`) are included. Use an explicit id pair for any other glow, or extend `config/glow.json` with the same field shape.

### Notes on keyword shadow

`keyword_has_shadow` / `keyword_shadow_info` work like `keyword_color` / `keyword_border_color`: they stay on the **same caption segment** and do not create an extra text line.

When keyword shadow is enabled, the caption is split into non-overlapping `styles` partitions: normal ranges get `shadows: []`, keyword ranges get the shadow params. Without keyword shadow fields, the original base + keyword overlay path is unchanged.

<!-- FONT_LIST_START -->
### Supported Fonts (`font` values)

You can set `font` to any of the following **display names** (same as CapCut/Jianying font names). Enum names and the aliases below are also accepted. If unresolved, the default font is used.

Total: **798** fonts:

```
3D 만화
A1明朝
Aa之云体
Aa乌日莫
Aa人间蹉跎
Aa全息黑体
Aa刃黑体
Aa剑豪体
Aa动员宋
Aa勘亭流
Aa厚底黑
Aa古线体
Aa台灣漢字心動信號（简繁）
Aa封神榜书
Aa小星星
Aa居酒屋
Aa巴洛克
Aa幻想
Aa德古拉简
Aa放放隶书
Aa新华墨竹体
Aa新华惊马体
Aa新怪谈
Aa方块黑
Aa未央宫词
Aa杜康手书
Aa欢乐堡
Aa水玉圆体
Aa浮梦体
Aa海豹体
Aa清欢圆体
Aa漆书
Aa烈焰隶书
Aa狂派手书
Aa疏漫宋
Aa百物语
Aa祝融隶
Aa简正隶黑
Aa芥末墩
Aa菊花体
Aa融融宋
Aa西风手书
Aa跃然体
Aa醒狮体
Aa金石体
Aa锐智体
Aa锐甲黑
Aa锐雅体
Aa镁宋
Aa闲云体
Aa霸道楷
Aa顽宋
Aa鲸潮体
Aa鹅卵石
Aa麟兰宋
Aa龙象体
AlexBrush
Alice-Regular
Alike-Regular
Allura-Regular
Amble-Regular
Amigate
Anson
Anton
Arizonia-Regular
Arvo
Atomic-Marker
Awelier
Ballet
Barrio-Regular
Belleza-Regular
Bevan-Regular
Bilbo-Regular
BlackMango-Regular
Blinker-Thin
Boxing
Bungee-Regular
Caladea-Regular
Calfine
Candal-Regular
Candice
Carattere-Regular
Cardo-Regular
Caveat-Bold
Caveat-Regular
CC-Captial
CC-Chubby
CC-Decocut
CC-DerStil
CC-Element
CC-Fluffy
CC-Fusion
CC-Glee
CC-lemon
CC-Loopy Letters
CC-Manga
CC-Moderno
CC-MonoCut
CC-Piston
CC-Rapid
CC-UltraMass
CC-Vita
Chonburi-Regular
Cinzel-Regular
Clostan
Coda-Heavy
Coiny-Regular
Cola
Cookie-Regular
Cormorant Garamond-Medium
Coustard-Regular
Crimson-SemiboldItalic
Dynalight-Regular
Exo
Facon
FiraSans-Book
Fraunces-Black
Fulbo-Argenta
Gallery
GenWanMinJP-Light（源云明体）
GenWanMinJP-Medium（源云明体）
GenWanMinJP-Regular（源云明体）
GenWanMinJP-SB（源云明体）
Gildan
Gildan-It
Giveny
Great Vibes-Regular
Grenze-Thin
HarmonyOS_Sans_SC_Bold
HarmonyOS_Sans_SC_Light
HarmonyOS_Sans_SC_Medium
HarmonyOS_Sans_SC_Regular
HarmonyOS_Sans_TC_Bold
HarmonyOS_Sans_TC_Light
HarmonyOS_Sans_TC_Medium
HarmonyOS_Sans_TC_Regular
HarmonyOSCn-Ltlt
HeptaSlab-Light
HG行書体
Inter-SemiBold
Italianno
Jellee-Bold
JYruantang
JYshiduo
JYzhuqingting
Kanit-ExtraBoldItalic
Kanit-Regular
KaushanScript
Koulen-Regular
Letter
Lexend Tera-Regular
Lora-Regular
Love
Luxury
LXGWWenKai-Bold
LXGWWenKai-Light
LXGWWenKai-Regular
Maler
Marker
Mellow
Merry Christmas
Mirza-Regular
Misto
Modern
Mokgech
Montserrat-Black
Montserrat-Thin
Morska
MyFont凌渡哥哥简
MyFont凌渡猪猪简
Nunito
OldStandardTT-Regular
Parisienne-Regular
Playfair Display SC-Re
PlayfairDisplay-Italic
Plunct
Polly
Poppins-Bold
Poppins-Regular
Prata
Quattrocento-Regular
Railway-Gank
RedHatDisplay-BoldItalic
RedHatDisplay-Light
ReenieBeanie-Regular
ResourceHanRoundedCN-Bold
ResourceHanRoundedCN-Lt
ResourceHanRoundedCN-Md
ResourceHanRoundedCN-Nl
Rix독도
Romantic
Rubik
SansitaSwashed-Regular
SecularOne-Regular
Serrat
Signature
Soap
SourceHanSansCN-Bold
SourceHanSansCN-Light
SourceHanSansCN-Medium
SourceHanSansCN-Normal
SourceHanSansCN-Regular
SourceHanSansTW-Bold
SourceHanSansTW-Light
SourceHanSansTW-Medium
SourceHanSansTW-Normal
SourceHanSansTW-Regular
SourceHanSerifCN-Bold
SourceHanSerifCN-Light
SourceHanSerifCN-Medium
SourceHanSerifCN-Regular
SourceHanSerifCN-SemiBold
SourceHanSerifTW-Bold
SourceHanSerifTW-Light
SourceHanSerifTW-Medium
SourceHanSerifTW-Regular
SourceHanSerifTW-SemiBold
SourceSansPro-Regular
Specta
Spicy Rice-Regular
Staatliches-Regular
Sugary
Sugary-Dreams-Italic
Sunset
Thinker-Alt1
Thrive
Thunder
Ugly-Dave-Alternates
Vogue
Work Sans-ExtraBoldItalic
WorkSans-BlackItalic
WorkSans-Regular
Zapfino
ZEN丸ゴシック
ZEN紅道
ZY Alluring-Regular
ZY Amity
ZY Azure
ZY Balloonbillow
ZY Bless
ZY Blossom
ZY Brief
ZY Classical
ZY Coconut-Regular
ZY Concise
ZY Coruscant
ZY Courage
ZY Daisy
ZY Dexterous
ZY Diligent
ZY Dots Art
ZY Elegant-Black
ZY Elixir
ZY Etiquette
ZY Fabulous
ZY Fantasy
ZY Fervent
ZY Flexible
ZY Flourishing-Italic
ZY Fortitude
ZY Genial
ZY Harmony
ZY Heaven
ZY Hope
ZY Ingenious
ZY Innocent
ZY Kindly Breeze
ZY Loose
ZY Loyalty
ZY Majestic
ZY Modern
ZY Modest
ZY Multiplicity
ZY Oliver
ZY Pace
ZY Panacea
ZY Panorama
ZY Radiance
ZY Rainbow
ZY Relax
ZY Resolve
ZY Rhythm
ZY Slender
ZY Spunk
ZY Squiggle
ZY Starry
ZY Steady
ZY Superb-Regular
ZY Tactful
ZY Timing
ZY Trend
ZY Upright
ZY Vibrant
ZY Vigour
ZY Vision
ZY Wonder
ZYCherish
ZYLAA Demure
ZYLAA Flechazo
ZYLAA Gambol
ZYLAA Infinity
ZYLAA lavender
ZYLAA Serein
いろは角クラシックE
いろは角クラシックM
きざはし金陵
くり抜く
しっぽりアンチック
すずむし
だるまどろっぷ
つきみ丸ゴかな B
つきみ丸ゴかな R
はちきるポップ
ひな明朝
ぽってり
オとマのペ
ギガ丸
キャビン
クレー One
ゴシック
コスギ
ゴシック
タイムマシンわ号
チェリーボム
デラゴシック
ドットゴシック 16
ニューテゴミン
ビジネス
ブロック
ペンレタ
ポッタ
ポジティブ
ミンサン書体B
ミンサン書体R
メモ
メモ帳
モッチーポップ
ランパート
レゲエ One
ロックンロール
ローマ
一笔壹画加油体
一笔壹画潮黑体
三极云隶体中
三极力量体简-粗
三极古拙楷书
三极妙漫体
三极宋黑体超粗
三极拙墨体
三极拙隶简体
三极极宋超粗
三极榜楷简体
三极欢乐体
三极正雅黑粗
三极气泡体
三极泼墨体
三极活力黑简体 粗
三极浓密仙粗
三极湘乡体
三极纯真体粗
三极罗丽黑简体-粗
三极萌喵简体
三极行楷简体-粗
三极铿锵体
三极黑宋体中粗
中秀体
书南体
云书法三行魏碑体
云书法手书建刚静心楷简
云书法生如夏花简
云书法罗西硬笔楷书体
云书法萨瓦迪卡简
云魅手书
亦然体
今宋体
仓耳与墨W05
仓耳丝柔体
仓耳丰黑
仓耳体
仓耳力士
仓耳周珂正大榜书
仓耳小丸子
仓耳明黑
仓耳曙黑
仓耳榜黑
仓耳状元楷
仓耳舒圆体W02
仓耳视频体
仓耳趣黑
仓耳酷黑
仓耳非白W02
仓耳非白W04
以梦为马
优设书华体
优设好身体
优设字由棒棒体
优设字美体
优设招牌体
优设标题圆
优设标题黑
伯兮体
佑字 朴
佑字 舞
佳妙体
俊雅体
俪金黑
修羽体
像素体
元也
元气泡泡体
元瑶体
先锋体
光远体
兰亭圆
凌东齐伋体-combo
凌东齐伋体-fallback
凌丝体
凝琴体
刘炳森
初尘体
利飞体
剪映专辑
剪映云迹
剪映半山海
剪映印章
剪映团子
剪映圆隶
剪映手书
剪映新年体
剪映春日部
剪映狗爬体
剪映细毛笔
剪映香蕉
励字俊林简
励字勇敢黑简 大黑
励字大黑简繁
励字姚体简繁
励字小怪兽简
励字志向黑简 特粗
励字憨憨简
励字敲可爱简 中粗
励字星宜简
励字玉树临风简
励字行楷简繁
励字趣石简
励字趣黑简繁
励字逆反差圆舞简 超级黑
励字造梦简 特粗
励字隶书简繁
匹喏曹
半梦体
华书体
南廱明體
卡酷体
古典体
古印宋简
古雅体
古风小楷
台北黑体-Bold
台北黑体-Light
台北黑体-Regular
后现代体
听露体
启功行楷
吹き出し
唐瑜体
唧唧国王
喜悦体
喜鹊万人造字
喜鹊梅花楷
喵魂体
嘉木体
圆体
基础像素
墩墩体
壮楷体
大字报
天云体
妙如体
妙松体
妙黑体
子どもたち
字制区喜脉体
字制区喜脉喜欢体
字由爱驾公路体
字语云黑宋
字语俊言体
字语叙黑体
字语叙黑体-中粗
字语叙黑体-常规
字语叙黑体-粗体
字语叙黑体-细体
字语叙黑体-超粗
字语古兰体
字语古映体
字语咏宋体
字语咏宏体
字语咏楷体
字语嘟嘟体
字语圆体
字语康宋体
字语康宋体繁体
字语文乐体
字语文乐体-粗体
字语文乐体-细体
字语文刻体
字语文熙体
字语文酷体
字语文雅体
字语文韬体
字语文韵体
字语漫雅手书
字语萌酱体
字语软糖体
字语颖黑体
孤月体
宋体
宜宋
小可爱体
小杉ｺﾞｼｯｸ
小薇体
少年南波万
尔雅新大黑
居酒屋
山林体
山雁体
岩柚体
峰骨体
幸せ
幼萱体
幽梦体
庞门正道标题体
庞门正道粗书体
庞门正道轻松体
张子山体
归雁体
彼岸体
得意黑
德古拉
快乐体
快速体
怜秋体
思源中宋
思源粗宋
悠悠然
悠然体
悦妍体
惊鸿体
手書
承英体
抖音美好体
招牌体
拼音体
挥墨体
教科書
文研体
文艺繁体
文轩体
文雅体
新青年体
方正王铎行草
方糖体
无界黑
日式标题
星光体
星汉宋
晨风体
景天体
景曜体
晴雪体
書道
月亮供电不足
有猫在
未光体
未来黑
本黑体
李李体
极简拼音
柏青体
柳公权
梅雨煎茶
梦寒体
梦想家
梦桃体
梦槐体
棘薔薇ボールド
棘薔薇ライト
楚辰体
楷書MCBK1
欣然体
正奇体
毛体行楷
毛体行草
毛笔行楷
毡笔体
汇文明朝体
汉仪英雄体
汉仪贤二体
汉字之美棒棒糖粗简
汉字之美玉龙简
汉字之美郝刚牡丹体简
江户招牌
江湖体
沈尹默
油性マジック
油漆体
流苏体
海岛森林-全字符
清刻本悦
清酒体
渊亭体
温宁体
温柔体
港风繁体
游乐体
游园体
游思体
源ノ角ゴシック
漫语体
澄月
瀞ノクーゲル明朝
点字佳楷
点字奇巧
点字小隶书
点字玄真宋
点字王者风范
点字艺圆
点字青花楷
点字青花隶
点宋体
烈金体
烟客体
烟波宋
爨宝子碑
爱你是无解命题
爱民小楷
特黑体
玄鸟体
玉轩体
玩童体
琉璃宋
瑞意宋
瑶蝶体
甜甜圈
白舟武骨
目光体
真言体
知夏森林
知新体
研宋体
研月体
禅影体
秀英四号太かな
站酷仓耳渔阳体-W02
站酷仓耳渔阳体-W03
站酷仓耳渔阳体-W04
站酷文艺体
站酷酷黑体
章鱼小丸子
童趣体
竹柏体
竹言体
竹风体
简中圆
糯米团
結月
纯真体
细体
经典雅黑
综艺体
综艺字
美佳体
聚珍体
胡晓波男神体
胡晓波真帅体
胡晓波骚包体
芋圆体
花语手书
花锦体
芷云体
若烟体
荔枝体
莫雪体
萌趣体
萧疏体
蒹葭体
蕴行体
薯条少年
蜡笔体
蝉影隶书
蝶汐体
装甲明朝
解星デコール
谷槐体
谷秋体
超级战甲
超重要体
轻吟体
轻烟体
追光体
造字侠今朝醉简
造字侠寻味江湖简
造字侠昊仔简繁
造字侠永刚漆书简繁
造字侠陈坤风行简繁
造字工房朴月体
逸致拼音
醉冬体
醉山体
金陵体
钟隶体
锋舞九天
锦瑟体
闘龍
阳华体
阳煦体
陈森田
雁兰体
雅月体
雅酷黑简
雅韵体
霸燃手书
青印体
青春加糖体
青松体
青禾体
青翼体
青鸟华光中长宋
青鸟华光书宋2
青鸟华光仿宋2
青鸟华光大标宋
青鸟华光报宋2
青鸟华光标题黑
青鸟华光楷体2
青鸟华光粗黑
青鸟华光细黑
青鸟华光细黑1
青鸟华光美黑
青鸟华光黑体
青鸟华光黑变
风铃悠悠
风雅宋
飒爽手写
飞扬行书
飞驰体
飞鸟集
高字标志圆
高字标志黑
高字湘黑体
魏碑体
鱼太闲躺平体
鲁迅行书
鸣翠体
鸿朗体
鸿潮榜书
鹿鸣体
黄令东齐伋复刻体
黄油体
黄金时代
黎首体
黑糖体
黒明朝
默陌手写
검
검은 고딕체
고딕
고딕체
귀염
나눔 명조체
낭만
로맨틱가이
로봇
룬
버터
성냥개비
소나무
시트콤
십대
아기
아이
유행
이야기
전통
초승달
추사체
커피
필기
한드
행복
흑백만
ｱﾄﾞｺﾞｯｼｸ
ｵｰﾊﾞｰﾗｯﾌﾟ
ｽｸﾘﾌﾟﾄ
ｾﾘﾌ太字
ｾﾘﾌﾗｲﾄ
ﾓｰﾀﾞ太字
ﾓｰﾀﾞﾗｲﾄ
ﾚｷﾞｭﾗｰ
```

#### Font aliases

These aliases are also valid `font` values:

- `志向黑` → `励字志向黑简 特粗`
- `励字志向黑` → `励字志向黑简 特粗`
- `励字志向黑简` → `励字志向黑简 特粗`
<!-- FONT_LIST_END -->

<!-- ANIMATION_LIST_START -->
### Supported Text Animations (in / out / loop)

Use the names below directly as in_animation, out_animation, or loop_animation (same as CapCut/Jianying titles and get_text_animations.name). Unmatched names are ignored.

#### Intro animations (in_animation, 145 total)

```text
乱码故障
二段缩放
便利贴
倒数
兔子弹跳
冰雪飘动
冲屏位移
卡拉OK
发光模糊
发光闪入
变色输入
叠影并入
右上弹入
右下擦开
向上弹入
向上擦除
向上滑动
向上翻转
向上重叠
向上露出
向下擦除
向下溶解
向下滑动
向下露出
向下飞入
向右擦除
向右模糊 II
向右滑动
向右缓入
向右集合
向右露出
向左擦除
向左模糊
向左滑动
向左露出
吸入
呐喊声波
喷绘
圆形扫描
圆柱体滚动
圣诞帽弹跳
圣诞树弹跳II
复古打字机
居中打字
左上弹入
左移弹动
开幕
弹入
弹入跳动
弹弓
弹性伸缩
弹性伸缩 II
弹簧
彩色映射
心动瞬间
慢速放大
打字光标
打字机 I
打字机 II
打字机 III
打字机IV
扭曲模糊
抖动甩入
折叠
拖尾
描边填充
收拢
放大
放大震动
故障打字机
故障闪动
新年打字机
旋入
旋转缩放
旋转飞入
日出
星光闪闪
星光闪闪 II
星星弹跳
晕开
模糊
模糊发光
模糊滚动
模糊缩小
水墨晕开
水平翻转
汇聚
波浪弹入
波浪弹跳
流光扩散
渐显
溶解
滑动上升
滚入
激光雕刻
爱心弹跳
玩雪
环绕滑入
生长
生长 II
甩出
电光
电光 II
碰碰车
空翻
站起
缤纷冲屏
缩小
缩小 II
缩放 III
羽化向右擦开
羽化向左擦开
翻动
翻页II
背景滑入
色散拖影
螺旋上升
跃进
跳跳捣蛋鬼
跳跳糖
轻微放大
辉光
辉光扫描
逐字弹跳
逐字旋入
逐字旋转
逐字显影
逐字翻转
金粉飘落
镂空跳入
闪动
闪烁集合
随机上升
随机弹跳
随机弹跳 II
随机打字机
随机落下
随机集合
随机飞入
雪光模糊
音符弹跳
顶出
预览打字
飞入
鼠标点击
```

#### Outro animations (out_animation, 97 total)

```text
二段缩放
发光闪出
叠影并出
右上弹出
右下擦除
向上擦除
向上溶解
向上滑动
向上飞出
向下弹出
向下擦除
向下滑动
向下翻转
向右擦除
向右滑动
向右缓出
向左擦除
向左模糊
向左模糊 II
向左滑动
向左解散
吸出
喷绘
圆形扫描
复古打字机
居中打字
展开
左上弹出
左移弹动
弹出
弹出跳动
弹弓
弹性伸缩
弹性伸缩 II
弹簧
打字光标
打字机 I
打字机 II
打字机 III
打字机IV
扭曲模糊
折叠
拖尾
描边填充
收缩震动
放大
放大 II
故障
故障打字机
故障闪动
旋出
旋转缩放
旋转飞出
日落
晕开
模糊
模糊发光
模糊滚动
水墨晕开
水平翻转
波浪弹出
波浪弹跳
消散
渐隐
溶解
滑动下落
滚出
激光雕刻
炸开
炸开 II
炸开 Ⅲ
环绕滑出
生长
甩回
空翻
缩小
羽化向右擦除
羽化向左擦除
翻动
螺旋下降
躺下
轻微放大
逐字旋出
逐字旋转
逐字翻转
逐字虚影
镂空跳出
闪动
闪烁散开
闭幕
随机弹跳
随机弹跳 II
随机打字机
随机飞出
顶出
预览打字
飞出
```

#### Loop animations (loop_animation, 93 total)

```text
VHS
上弧
刷屏
加字符
发光模糊多行
吹泡泡
吹泡泡 II
呐喊
喷涌
喷绘
圆形涂鸦
声波震动
复古涂鸦
字体变换
字幕滚动
尾巴摇摆
弹幕
弹幕 II
弹幕滚动
强调三遍
彩色切换
彩色火焰
彩虹
彩虹-情人节
彩虹-新年
彩虹-马卡龙
影像叠加
心跳
急了
悸动
情绪加载
扩音器
扫光
扭动
投影颤抖
投影颤抖 II
抖动故障
折叠
拉住
拉开
拼贴纹理
排队入场
描边粉笔
摇摆
摇摆 I
摇荡
放大缩小
放大镜
故障闪动
文字泛光
旋转
晃动
波浪
波浪 II
波浪 III
流光
涂鸦手绘
涂鸦手绘 II
渐变拖尾
漂浮
漩涡
爆闪
环形滚动
环绕
环绕 II
甜甜圈
福袋炸开
空间翻转 I
空间翻转 II
空间翻转 III
竖向渐变
翻转
翻页I
色差故障
蓝黄滑动
调皮
超强晃动
超强晃动 II
超强波浪
超强波浪 II
跳动
轻微跳动
逐字放大
钟摆
错位
闪烁
随机弹跳
雨刷
频闪边框
颤抖
颤抖 II
颤抖 III
飘起
```
<!-- ANIMATION_LIST_END -->

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
      "keyword_font": "思源中宋",               // [Optional] keyword font; falls back to body caption font
      "keyword_font_size": 22,                 // [Optional] keyword font size; falls back to body size
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
  "alignment": 1,                              // [Optional] 0 left / 1 center / 2 right (horizontal); 3/4/5 vertical center/left/right
  "alpha": 1.0,                                // [Optional] opacity [0,1]
  "font": "得意黑",                           // [Optional] font name
  "font_size": 15,                             // [Optional] top-level default font size
  "letter_spacing": 0,                         // [Optional] letter spacing
  "line_spacing": 0,                           // [Optional] line spacing
  "line_max_width": 0.82,                      // [Optional] max line width as fraction of screen width [0,1]
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
  "has_background": true,                      // [Optional] full-caption text background switch
  "background_info": {                         // [Optional] full-caption text background params
    "background_color": "#000000",
    "background_style": 1,
    "background_alpha": 1.0,
    "background_round_radius": 0.0,
    "background_height": 0.14,
    "background_width": 0.14,
    "background_horizontal_offset": 0.0,
    "background_vertical_offset": 0.0
  },
  // [Optional] set null so custom colors/shadows remain effective
  "text_effect": null,
  // [Optional] text template; mutually exclusive with text_effect and wins; null here
  "text_template": null,
  // [Optional] bubble; for bubbles outside the catalog use an "effect_id:resource_id" pair
  "text_bubble": null,
  // [Optional] glow; preset name or an "effect_id:resource_id" pair; not mutually exclusive with other text effects
  "text_glow": null
}
```

## Response Format

### Success Response (200)

```json
{
  "code": 0,
  "message": "success",
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

### Error Response

```json
{
  "code": 2018,
  "message": "Invalid caption information, please check if the value of the captions field is correct."
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
    "captions": "[{\"start\":0,\"end\":3000000,\"text\":\"Hello, CapCut captions\",\"keyword\":\"CapCut|captions\",\"keyword_color\":\"#ff7100\",\"keyword_border_color\":\"#000000\",\"keyword_font\":\"思源中宋\",\"keyword_font_size\":22,\"keyword_has_shadow\":true,\"keyword_shadow_info\":{\"shadow_alpha\":0.85,\"shadow_color\":\"#000000\",\"shadow_diffuse\":18.0,\"shadow_distance\":6.0,\"shadow_angle\":-45.0},\"font_size\":18,\"in_animation\":\"向上滑动\",\"out_animation\":\"向下滑动\",\"loop_animation\":\"弹幕滚动\",\"in_animation_duration\":500000,\"out_animation_duration\":500000,\"loop_animation_duration\":1000000},{\"start\":3000000,\"end\":6000000,\"text\":\"Welcome to caption features\",\"keyword\":\"caption\",\"keyword_color\":\"#457616\",\"keyword_border_color\":\"#111111\",\"keyword_font_size\":20,\"keyword_has_shadow\":true,\"keyword_shadow_info\":{\"shadow_alpha\":0.9,\"shadow_color\":\"#000000\",\"shadow_diffuse\":15.0,\"shadow_distance\":5.0,\"shadow_angle\":-45.0},\"font_size\":16,\"in_animation\":\"右上弹入\",\"out_animation\":\"右上弹出\",\"loop_animation\":\"VHS\",\"in_animation_duration\":400000,\"out_animation_duration\":400000,\"loop_animation_duration\":800000}]",
    "text_color": "#ffffff",
    "border_color": "#333333",
    "alignment": 1,
    "alpha": 1.0,
    "font": "得意黑",
    "font_size": 15,
    "letter_spacing": 0,
    "line_spacing": 0,
    "line_max_width": 0.82,
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
    "text_effect": null,
    "text_template": null,
    "text_bubble": null
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
| font | `得意黑` | [Optional] Font name |
| font_size | `15` | [Optional] Top-level default size |
| letter_spacing / line_spacing | `0` | [Optional] Spacing |
| line_max_width | `0.82` | [Optional] Max line width as fraction of screen width |
| scale_x / scale_y | `1.0` | [Optional] No scaling |
| transform_x | `0.0` | [Optional] No horizontal offset |
| transform_y | `-200.0` | [Optional] Move up 200 px |
| style_text | `false` | [Optional] Style-text switch off |
| underline / italic | `false` | [Optional] No underline / italic |
| bold | `true` | [Optional] Bold on |
| has_shadow | `true` | [Optional] Full-text shadow on |
| shadow_info.* | see above | [Optional] Full-text shadow details |
| has_background | `true` | [Optional] Full-caption text background on |
| background_info.* | see above | [Optional] Full-caption text background details |
| text_effect | `null` | [Optional] No 花字, keep colors/shadows |
| text_template | `null` | [Optional] No text template; mutually exclusive with text_effect and wins |
| text_bubble | `null` | [Optional] No bubble. Pass a name or an `"effect_id:resource_id"` pair to use one; priority is text template > bubble > text effect |
| text_glow | `null` | [Optional] No glow. Pass a preset name or an `"effect_id:resource_id"` pair to use one; not mutually exclusive with other text effects |

**Per-caption field meanings:**

| Field | Example | Meaning |
|-------|---------|---------|
| start / end | `0` / `3000000` | [Required] Time range (µs) |
| text | `Hello, CapCut captions` | [Required] Caption text |
| keyword | `CapCut\|captions` | [Optional] Highlight keywords |
| keyword_color | `#ff7100` | [Optional] Keyword color |
| keyword_border_color | `#000000` | [Optional] Keyword stroke |
| keyword_font | `思源中宋` | [Optional] Keyword font |
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

#### 6. Text template (文字模板)

Top-level template applied to the whole batch:

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_captions \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
    "captions": "[{\"start\":0,\"end\":5000000,\"text\":\"Template demo\"}]",
    "text_template": "嘎嘎香！红色 简约 美食 情绪表达 字幕"
  }'
```

Per-caption template (mixable with plain captions, which are unaffected):

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_captions \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
    "captions": "[{\"start\":0,\"end\":5000000,\"text\":\"Plain caption\"},{\"start\":5000000,\"end\":10000000,\"text\":\"Templated caption\",\"text_template\":\"7383613902744980770\"}]"
  }'
```

#### 7. Using a bubble

By name, using a bubble from the catalog (`config/bubble.json`):

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_captions \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
    "captions": "[{\"start\":0,\"end\":5000000,\"text\":\"Bubble caption\"}]",
    "text_bubble": "背景装饰54"
  }'
```

For a bubble outside the catalog use the explicit `"effect_id:resource_id"` pair; it can also be set per caption, mixed with plain captions:

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_captions \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
    "captions": "[{\"start\":0,\"end\":5000000,\"text\":\"Plain caption\"},{\"start\":5000000,\"end\":10000000,\"text\":\"Bubble caption\",\"text_bubble\":\"716434:6821385652727190024\"}]"
  }'
```

#### 8. Using a text background

Flip the switch only, for JianYing's default black background:

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_captions \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
    "captions": "[{\"start\":0,\"end\":5000000,\"text\":\"Default text 1\"},{\"start\":5000000,\"end\":10000000,\"text\":\"Default text 2\"}]",
    "has_background": true
  }'
```

A custom color with rounded corners (a semi-transparent orange plate):

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_captions \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
    "captions": "[{\"start\":0,\"end\":5000000,\"text\":\"Caption with background\"}]",
    "text_color": "#ffffff",
    "has_background": true,
    "background_info": {
      "background_color": "#ff7100",
      "background_alpha": 0.8,
      "background_round_radius": 0.3,
      "background_width": 0.2
    }
  }'
```

#### 9. Using a glow

By preset name, using a glow from the catalog (`config/glow.json`):

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_captions \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
    "captions": "[{\"start\":0,\"end\":5000000,\"text\":\"Glowing caption\"}]",
    "text_glow": "外发光"
  }'
```

For a glow outside the catalog use the explicit `"effect_id:resource_id"` pair; a glow also stacks with the background, a bubble, and so on:

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_captions \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
    "captions": "[{\"start\":0,\"end\":5000000,\"text\":\"Glowing caption\"}]",
    "text_glow": "9762443:7202576698775179837",
    "has_background": true
  }'
```

## Error Code Description

| Error Code | Error Message | Description | Solution |
|------------|---------------|-------------|----------|
| 1001 | Parameter validation failed | Request body failed schema validation | Check parameter types and required fields |
| 2001 | Invalid draft URL | `draft_url` is missing, malformed, or the draft is not in the cache | Pass the `draft_url` returned by `create_draft` |
| 2018 | Invalid caption information | `captions` is not valid JSON, an item is missing `start`/`end`/`text`, `end` is not greater than `start`, or the text is empty | Fix the JSON string and the required fields |
| 2019 | Caption addition failed | Failed while writing captions into the draft | Check the draft state and retry |
| 2042 | Draft lock acquisition timeout | Only one operation is allowed on a draft at a time | Retry later |

## Notes

1. **Time unit**: microseconds (`1s = 1_000_000µs`)
2. **captions format**: must be a valid JSON **string** inside the request JSON
3. **Color format**: hex, e.g. `#ffffff`
4. **Animation names**: from `get_text_animations`
5. **Text effect names**: from `get_text_effects`
5.1. **Text template**: pass a template name or a numeric `effect_id`; mutually exclusive with `text_effect` and wins. The catalog lives in `config/text_template.json` (5166 templates); duplicate names resolve to the first entry, so use the `effect_id` for an exact match. Numeric ids absent from the table pass straight through
5.2. **Bubble**: pass a bubble name, `resource_id` or `effect_id`; a bubble's `effect_id` and `resource_id` are **not the same value**, so for bubbles outside the catalog pass an explicit `"effect_id:resource_id"` pair (e.g. `"716434:6821385652727190024"`) — a lone numeric value is not passed through. Priority is text template > bubble > text effect; a bubble does not reset colors/stroke/shadow
5.3. **Text background**: only takes effect with `has_background=true` — passing `background_info` alone is ignored; without `background_info` the default black background is used. The `background_info` fields map one-to-one onto the draft's `background_*`, `background_style` accepts only `1`/`2`, and an invalid color falls back to black with a warning. A text effect does not reset the background, so the two stack visually
5.4. **Glow**: pass a preset name (`外发光`/`轮廓光`) or `resource_id`/`effect_id`; as with bubbles the `effect_id` and `resource_id` are **not the same value**, so for glows outside the catalog pass an explicit `"effect_id:resource_id"` pair (e.g. `"9762443:7202576698775179837"`) — a lone numeric value is not passed through. A glow is **not mutually exclusive** with text effects/templates/bubbles (it does not reset colors/stroke/shadow), but it is **top-level only**, so mixing two presets needs two calls; an out-of-catalog glow falls back to the default `bloom_params` with a warning
6. **Coordinates**: `transform_x` / `transform_y` are pixels, converted internally by canvas size; `background_horizontal_offset` / `background_vertical_offset` instead use draft coordinates `[-1, 1]` where `0` is centered
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
