# ADD_CAPTIONS API 接口文档

## 🌐 语言切换
[中文版](./add_captions.zh.md) | [English](./add_captions.md)

## 接口信息

```
POST /openapi/capcut-mate/v1/add_captions
```

## 功能描述

向现有草稿中批量添加字幕。该接口用于在指定的时间段内添加字幕到剪映草稿中，支持丰富的字幕样式设置，包括文本颜色、边框颜色、对齐方式、透明度、字体、字体大小、字间距、行间距、缩放、位置、下划线/斜体/加粗、文本阴影、关键词高亮与关键词阴影、文字动画、花字效果等。

## 请求参数

### 接口级参数说明

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| draft_url | string | ✅ | - | 目标草稿的完整 URL，需包含 `draft_id` 查询参数 |
| captions | string | ✅ | - | 字幕信息列表的 **JSON 字符串**（不是 JSON 数组本身） |
| text_color | string | ❌ | `"#ffffff"` | 普通字幕文本颜色，十六进制，如 `#ffffff` |
| border_color | string | ❌ | `null` | 普通字幕描边颜色，十六进制；`null` 表示无描边 |
| alignment | integer | ❌ | `1` | 文本对齐方式：`0` 左对齐，`1` 居中，`2` 右对齐（横排）；`3` 垂直居中，`4` 垂直左对齐，`5` 垂直右对齐（竖排） |
| alpha | number | ❌ | `1.0` | 文本透明度，取值范围 `[0.0, 1.0]`，`1.0` 为不透明 |
| font | string | ❌ | `null` | 字体名称，须为下方「支持的字体」中的展示名（也支持枚举名/别名）；`null` 使用默认字体 |
| font_size | integer | ❌ | `15` | 接口级默认字号；当 caption 项未指定 `font_size` 时生效，须 `>= 1` |
| letter_spacing | number | ❌ | `null` | 字间距；`null` 表示使用默认值 `0` |
| line_spacing | number | ❌ | `null` | 行间距；`null` 表示使用默认值 `0` |
| line_max_width | number | ❌ | `0.82` | 每行最大行宽占屏幕宽度比例，取值范围 `[0.0, 1.0]`；开启自动换行时生效 |
| scale_x | number | ❌ | `1.0` | 水平缩放，`1.0` 为原始大小 |
| scale_y | number | ❌ | `1.0` | 垂直缩放，`1.0` 为原始大小 |
| transform_x | number | ❌ | `0.0` | 水平位移（像素），正值向右，负值向左，以画布中心为原点 |
| transform_y | number | ❌ | `0.0` | 垂直位移（像素），正值向下，负值向上，以画布中心为原点 |
| style_text | boolean | ❌ | `false` | 是否使用样式文本（预留开关） |
| underline | boolean | ❌ | `false` | 是否开启文字下划线 |
| italic | boolean | ❌ | `false` | 是否开启文字斜体 |
| bold | boolean | ❌ | `false` | 是否开启文字加粗 |
| has_shadow | boolean | ❌ | `false` | 是否启用**整段字幕**文本阴影 |
| shadow_info | object | ❌ | `null` | 整段字幕阴影参数；`has_shadow=true` 且本字段为 `null` 时使用默认阴影 |
| has_background | boolean | ❌ | `false` | 是否启用**整段字幕**文字背景（文字底下的一层纯色底板） |
| background_info | object | ❌ | `null` | 整段字幕背景参数；`has_background=true` 且本字段为 `null` 时使用默认黑色背景。`has_background=false` 时本字段被忽略 |
| text_effect | string | ❌ | `null` | 花字效果名称或 `effect_id`；有效花字会重置颜色/描边/阴影相关效果 |
| text_template | string | ❌ | `null` | 文字模板名称或 `effect_id`（数字 id 可直接透传）；与 `text_effect` 互斥，同时传入时文字模板优先 |
| text_bubble | string | ❌ | `null` | 气泡名称或 `resource_id`/`effect_id`；清单外的气泡传 `"effect_id:resource_id"` 显式 ID 对。优先级：文字模板 > 气泡 > 花字 |
| text_glow | string | ❌ | `null` | 发光预设名称（如 `"外发光"`）或 `resource_id`/`effect_id`；清单外的发光传 `"effect_id:resource_id"` 显式 ID 对。与花字/文字模板/气泡**都不互斥**，可叠加 |

### captions 字段详细说明

`captions` 是一个 JSON 字符串，解析后为字幕对象数组。每个对象字段如下：

| 字段名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| start | integer | ✅ | - | 字幕开始时间（微秒），`1 秒 = 1_000_000 微秒`，须 `>= 0` |
| end | integer | ✅ | - | 字幕结束时间（微秒），必须大于 `start` |
| text | string | ✅ | - | 字幕文本内容，不能为空 |
| keyword | string | ❌ | `null` | 关键词，多个用 `\|` 分隔，如 `"剪映\|字幕"` |
| keyword_color | string | ❌ | `"#ff7100"` | 关键词填充颜色（十六进制） |
| keyword_border_color | string | ❌ | `null` | 关键词描边颜色；未指定时回退使用接口级 `border_color` |
| keyword_font | string | ❌ | `null` | 关键词字体（展示名/枚举名/别名，见下方「支持的字体」）；未指定则与主体字幕 `font` 一致 |
| keyword_font_size | integer | ❌ | `null` | 关键词字号，须 `> 0`；未指定则与主体字幕字号一致（本条 `font_size`，否则接口级 `font_size`） |
| keyword_has_shadow | boolean | ❌ | `false` | 是否启用**关键词范围**阴影 |
| keyword_shadow_info | object | ❌ | `null` | 关键词阴影参数，字段同 `shadow_info`；未提供时用默认阴影 |
| font_size | integer | ❌ | `null` | 本条字幕普通文本字号；未指定则使用接口级 `font_size` |
| in_animation | string | ❌ | `null` | 入场动画名称，须为下方「入场动画」列表中的值，如 `"向上滑动"` |
| out_animation | string | ❌ | `null` | 出场动画名称，须为下方「出场动画」列表中的值，如 `"向下滑动"` |
| loop_animation | string | ❌ | `null` | 循环动画名称，须为下方「循环动画」列表中的值，如 `"弹幕滚动"` |
| in_animation_duration | integer | ❌ | `null` | 入场动画时长（微秒）；不填则用动画默认时长 |
| out_animation_duration | integer | ❌ | `null` | 出场动画时长（微秒）；不填则用动画默认时长 |
| loop_animation_duration | integer | ❌ | `null` | 循环动画**单次循环**时长（微秒）；不填则用动画默认时长 |
| text_template | string | ❌ | `null` | 本条字幕的文字模板名称或 `effect_id`；未指定则使用接口级 `text_template` |
| text_bubble | string | ❌ | `null` | 本条字幕的气泡名称、`resource_id`/`effect_id`，或 `"effect_id:resource_id"` 显式 ID 对；未指定则使用接口级 `text_bubble` |

### shadow_info / keyword_shadow_info 字段说明

| 字段名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| shadow_alpha | number | ❌ | `1.0` | 阴影不透明度，取值范围 `[0, 1]` |
| shadow_color | string | ❌ | `"#000000"` | 阴影颜色（十六进制） |
| shadow_diffuse | number | ❌ | `15.0` | 阴影扩散程度，取值范围 `[0, 100]` |
| shadow_distance | number | ❌ | `5.0` | 阴影距离，取值范围 `[0, 100]` |
| shadow_angle | number | ❌ | `-45.0` | 阴影角度，取值范围 `[-180, 180]` |

当 `has_shadow=true`（或 `keyword_has_shadow=true`）且未提供对应 `*_shadow_info` 时，默认阴影为：

```json
{
  "shadow_color": "#000000",
  "shadow_alpha": 0.9,
  "shadow_diffuse": 15,
  "shadow_distance": 5,
  "shadow_angle": -45
}
```

### background_info 字段说明

字段名与剪映草稿 `materials.texts[*]` 的 `background_*` 字段**一一对应**，取值也按草稿语义给出，
从草稿里抄一条带背景的文本素材过来即可直接用。

| 字段名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| background_color | string | ❌ | `"#000000"` | 背景颜色（十六进制）；可省略 `#`，大小写不敏感，输出统一为 `#RRGGBB` |
| background_style | integer | ❌ | `1` | 背景样式，`1`/`2` 分别对应剪映中的两种样式；`0` 表示无背景，**不可传入** |
| background_alpha | number | ❌ | `1.0` | 背景不透明度，取值范围 `[0, 1]` |
| background_round_radius | number | ❌ | `0.0` | 背景圆角半径，取值范围 `[0, 1]` |
| background_height | number | ❌ | `0.14` | 背景高度（相对文字的外扩），取值范围 `[0, 1]` |
| background_width | number | ❌ | `0.14` | 背景宽度（相对文字的外扩），取值范围 `[0, 1]` |
| background_horizontal_offset | number | ❌ | `0.0` | 背景水平偏移，取值范围 `[-1, 1]`，`0` 为居中，负值向左 |
| background_vertical_offset | number | ❌ | `0.0` | 背景竖直偏移，取值范围 `[-1, 1]`，`0` 为居中，负值向上 |

当 `has_background=true` 且未提供 `background_info` 时，使用剪映的默认背景：

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

### 参数详解

#### 对齐方式

| 值 | 说明 |
|---|------|
| 0 | 左对齐（横排） |
| 1 | 居中对齐（横排） |
| 2 | 右对齐（横排） |
| 3 | 垂直居中（竖排 + 居中） |
| 4 | 垂直左对齐（竖排 + 左对齐） |
| 5 | 垂直右对齐（竖排 + 右对齐） |

`alignment` 控制文本框内的排版方向与行对齐，不会改变字幕在画布上的位置。画面位置请使用 `transform_x` / `transform_y`。`3`/`4`/`5` 会将草稿素材的 `typesetting` 设为竖排。

#### 花字与阴影的关系

当 `text_effect` 能解析到有效花字时，系统会将 `text_color` 重置为 `#ffffff`、`border_color` 重置为 `null`、`has_shadow` 重置为 `false`，并禁用关键词阴影（`keyword_has_shadow` 不生效）。若需要自定义颜色/阴影，请不要同时传有效花字。

#### 文字模板

`text_template` 用于套用剪映的「文字模板」（字体、配色、描边、装饰贴纸、入场动画的成套预设）。取值可以是模板名称（中文）或 `effect_id`；不在已知映射表中的纯数字会被当作 `effect_id` 直接透传。

模板清单维护在 `config/text_template.json`，目前收录 **5166** 个模板（4668 个不重名），字段为 `id`（即 `effect_id`/`resource_id`，两者同值）、`title`、`is_vip`、`category_id`、`category_name`。清单来自第三方整理，可按需增删。

- **接口级与逐条**：接口级 `text_template` 作为整批字幕的默认值，单条字幕（`captions` 数组项）里的 `text_template` 优先。
- **与花字互斥**：同时传入 `text_effect` 与 `text_template` 时，**文字模板优先**，`text_effect` 会被忽略（并记录告警）。模板掌管片段的素材身份，花字掌管 `styles[0].effectStyle`，两者同时生效的渲染结果未定义。
- **颜色/描边/阴影**：文字模板不重置 `text_color` / `border_color` / `has_shadow`（与花字不同）—— 模板的配色由模板自身决定。模板无法解析时，按普通字幕处理并记录告警。
- **草稿结构**：套用模板的字幕，其片段 `material_id` 指向 `materials.text_templates` 中的模板素材，文本素材仍写入 `materials.texts`，由模板的 `text_info_resources[].text_material_id` 反向关联。接口返回的 `text_ids` 仍是**文本素材** id。
- **重名如何处理**：清单里有 498 条重名模板（如「我的水印」重名 41 条），按名称调用时固定命中配置中**靠前的一条**。需要精确定位某个模板时请直接传 `effect_id`。
- **VIP 模板**：5166 个模板中 4735 个为 VIP（`is_vip: true`）。未购买的 VIP 模板在剪映侧可能无法渲染，调用方应自行确保账号有权限；清单中的 `is_vip` 字段可用于筛选。
- **已知限制**：模板资源（本机缓存路径、装饰贴纸等）由剪映按 `effect_id` 自行拉取；目前每个字幕只支持模板的**单个文本槽**。

#### 气泡

`text_bubble` 用于给字幕套用剪映的「气泡」（文字底下的装饰底板，如对话框、标签、印章）。气泡是剪映里独立于花字与文字模板的第三种文字效果，草稿中表现为 `materials.effects` 里一条 `type: "text_shape"` 的素材，由文本片段的 `extra_material_refs` 引用。

**与花字/文字模板最大的差异：气泡的 `effect_id` 与 `resource_id` 不是同一个值。** 例如剪映草稿中的 `effect_id: "716434"` 与 `resource_id: "6821385652727190024"`，两者都需给出，少一个剪映就定位不到气泡资源。因此：

- 清单 `config/bubble.json` 中两者分别记录：`id` 是 **resource_id**，`effect_id` 单独给出（注意与 `text_template.json` 里 `id` 兼作 `effect_id` 的约定不同）。
- 清单外的任意气泡，用 `"effect_id:resource_id"` 显式 ID 对传入，如 `"716434:6821385652727190024"`。
- **只传一个纯数字不会被透传**（这点与 `text_template` 相反），因为无法补全另一个 id，会按未找到处理并回退为普通字幕。

取值方式与优先级：

- **四种写法**：气泡名称（如 `"背景装饰54"`）、`resource_id`、`effect_id`，或 `"effect_id:resource_id"` 显式 ID 对。
- **接口级与逐条**：接口级 `text_bubble` 作为整批字幕的默认值，单条字幕里的 `text_bubble` 优先。
- **优先级为 文字模板 > 气泡 > 花字**：气泡与花字同属文字效果且互斥，同时传入时**气泡优先**，`text_effect` 被忽略并告警；与 `text_template` 同时传入时**文字模板优先**，气泡被忽略并告警。
- **颜色/描边/阴影**：气泡只负责文字底下的装饰底板，**不重置** `text_color` / `border_color` / `has_shadow`（这点与花字相反，与文字模板一致）。气泡无法解析时，按普通字幕处理并记录告警。
- **已知限制**：气泡素材的 `path`、`request_id` 等取决于创建者本机剪映缓存，本服务不导出，由剪映按 `effect_id`/`resource_id` 自行拉取（与花字相同的做法）。需要原样覆写这些字段时，可在 `config/bubble.json` 的 `material` 字段中提供，会原样写入气泡素材。
- **未经实测**：`气泡1` 草稿只证明了**草稿结构**（素材字段与片段引用关系逐项对齐），气泡在剪映里的**实际渲染**尚未验证。花字发同样的最小字段集且工作正常，但气泡是不同素材类型（`text_shape`）与渲染路径，属推断而非实测——上线前请在剪映里实跑一次。
- **清单规模**：当前只收录 `气泡1` 草稿实证过的 **1** 个气泡（`背景装饰54`），故**按名称只能在清单内用这 1 个**；其余气泡请用显式 ID 对传入，或按同样字段格式向 `config/bubble.json` 增补（`id` 为 resource_id，`effect_id` 单独给出，两者缺一不可）。
- **关于批量导入**：速创小助手的气泡页收录了 326 个气泡的名称与预览图（名称即剪映气泡名，如 `情绪07`/`会话105`），但**不提供 `effect_id`/`resource_id`**（该站的「特效」页才提供 id 对），因此无法直接批量导入，补齐 id 需在剪映「气泡」面板逐个确认。

#### 文字背景

`has_background` / `background_info` 用于给字幕加剪映的「背景」——文字底下的一层纯色底板，
常用来压住花哨画面、提高字幕可读性。草稿中表现为文本素材 `materials.texts[*]` 上的一组
`background_*` 字段，同时 `check_flag` 置上第 16 位（`7 → 23`）。

- **开关语义**：必须传 `has_background=true` 才会生效；只传 `background_info` 不开开关时**静默忽略**
  （与 `has_shadow` / `shadow_info` 一致）。`has_background=true` 且不给 `background_info` 时用默认黑色背景。
- **取值即草稿值**：`background_info` 的字段名与取值**与草稿一一对应**，没有单位换算；
  唯一例外是颜色会归一为 `#RRGGBB` 大写形式。注意 `background_style` 只接受 `1`/`2`，
  草稿里表示「无背景」的 `0` **不能传入**（无背景请直接不传 `has_background`）。
- **颜色不做 RGB 转换**：描边/阴影的颜色会经 `hex_to_rgb` 转成 `[r, g, b]`，背景色**不走这条路**，
  草稿里存的就是 `"#RRGGBB"` 字符串。因此颜色非法时会**回退为黑色并记录告警**，
  而不是像 `text_color` 那样回退白色。
- **与花字共存**：花字把 `text_color` / `border_color` / `has_shadow` 重置为默认值，
  但**不重置背景**（背景不在花字的 `effectStyle` 管辖范围内，这点与气泡一致）。
  两者同时使用时画面会叠加，服务会记录一条告警提醒。
- **与文字模板共存**：背景写在文本素材上，模板素材（`materials.text_templates`）是**另一条独立素材**，
  不含 `background_*`，不会被重复套用。模板自带的装饰可能与背景视觉冲突，需自行实跑确认。
- **与关键词高亮共存**：关键词高亮走 `content.styles` 分区，背景挂在素材侧，两者互不影响。
- **未经实测**：`背景` 草稿证明了**草稿结构**（8 个 `background_*` 字段与 `check_flag: 23`
  逐项对齐，默认值即该草稿里带背景那条字幕的原值），但**本服务生成的草稿在剪映里的实际渲染尚未验证**——
  且 `background_style: 2` 及各类非默认取值均无实证样本。上线前请在剪映里实跑一次。
- **偏移量的坑**：`background_horizontal_offset` / `background_vertical_offset` 用的是**草稿坐标**
  `[-1, 1]`、`0` 为居中，不是某些内部 API 的 `[0, 1]` 坐标——照抄草稿最稳妥。

#### 发光

`text_glow` 用于给字幕加剪映的「发光」（文字边缘的一层辉光）。发光是剪映里独立于花字、
文字模板、气泡的第四种文字效果，草稿中表现为 `materials.effects` 里一条 `type: "bloom"`
的素材，由文本片段的 `extra_material_refs` 引用（追加在 `sticker_animation` 之后），
同时文本素材的 `check_flag` 置上第 64 位（`7 → 71`）。除 `check_flag` 外，
**带发光的文本素材与普通字幕逐字段完全相同**——发光不碰文字的填充/描边/阴影。

**与气泡一样，发光的 `effect_id` 与 `resource_id` 不是同一个值**（如 `effect_id: "9762443"`、
`resource_id: "7202576698775179837"`），两者都需给出，少一个剪映就定位不到发光资源。因此：

- 清单 `config/glow.json` 中两者分别记录：`id` 是 **resource_id**，`effect_id` 单独给出。
- 清单外的任意发光，用 `"effect_id:resource_id"` 显式 ID 对传入。
- **只传一个纯数字不会被透传**（这点与 `text_template` 相反），会按未找到处理并回退为普通字幕。

取值方式与优先级：

- **四种写法**：预设名称（如 `"外发光"`、`"轮廓光"`）、`resource_id`、`effect_id`，
  或 `"effect_id:resource_id"` 显式 ID 对。
- **不互斥**：发光既不掌管片段的素材身份（那是文字模板的事），也不改动文字样式
  （那是花字的事），只是再挂一条素材，因此与花字 / 文字模板 / 气泡**可以同时使用**，
  没有优先级关系。花字也不重置发光（与背景一致），服务会记录一条告警提醒两者会视觉叠加。
- **`bloom_params` 各预设不同**：发光的颜色/强度/范围/方向存在素材的 `bloom_params` 里，
  由清单按预设给出（外发光 `range 0.2, strength 0.3`；轮廓光 `range 0.4, strength 0.5`）。
  **清单外的发光没有实证取值**，服务会落到外发光的默认值并告警——剪映不会按 `resource_id`
  重新推导这些数值，需要精确复刻请把该预设加入 `config/glow.json`。
- **接口级**：`text_glow` 只作用于整批字幕，**不支持逐条指定**。想在一次草稿里混用两种预设
  （如「默认文本2 用外发光、默认文本3 用轮廓光」），需分两次调用 `add_captions`。
- **未经实测**：`发光` 草稿证明了**草稿结构**（两个预设的素材字段与 `check_flag: 71` 逐项对齐），
  但**本服务生成的草稿在剪映里的实际渲染尚未验证**——包括 `bloom_params` 是否必需、
  清单外的兜底值是否可用、以及与花字/背景叠加时的实际效果。上线前请在剪映里实跑一次。
- **清单规模**：当前只收录 `发光` 草稿实证过的 **2** 个预设（`外发光`、`轮廓光`）；
  其余发光请用显式 ID 对传入，或按同样字段格式向 `config/glow.json` 增补。

#### 关键词阴影如何生效

`keyword_has_shadow` / `keyword_shadow_info` 与 `keyword_color` / `keyword_border_color` 一样，都作用在**同一条字幕**内，不会新建额外字幕行。

实现上会把字幕拆成互不重叠的 `styles` 分区：普通文字分区 `shadows: []`，关键词分区写入阴影参数，从而尽量只让关键词带阴影。不传阴影相关字段时，仍走原来的「base + 关键词叠加样式」路径，行为与增加阴影功能前一致。

<!-- FONT_LIST_START -->
### 支持的字体（font 可用值）

`font` 可直接填写下列**展示名**（与剪映字体名一致）。也支持对应的枚举名，以及下方别名。未匹配到时将回退默认字体。

当前共 **798** 种字体：

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

#### 字体别名

下列别名也可作为 `font` 的值：

- `志向黑` → `励字志向黑简 特粗`
- `励字志向黑` → `励字志向黑简 特粗`
- `励字志向黑简` → `励字志向黑简 特粗`
<!-- FONT_LIST_END -->

<!-- ANIMATION_LIST_START -->
### 支持的文字动画（in / out / loop）

下列名称可直接作为字段 in_animation、out_animation、loop_animation 的值（与 get_text_animations 返回的 name、以及剪映动画标题一致）。未匹配到时该动画不会生效。

#### 入场动画（in_animation，共 145 种）

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

#### 出场动画（out_animation，共 97 种）

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

#### 循环动画（loop_animation，共 93 种）

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

## 完整参数请求示例（含注释）

下列为**全部接口级参数 + captions 全部字段**的示意；`//` 注释仅用于说明，不能直接作为请求体。

```js
{
  // 【必填】目标草稿 URL，必须带 draft_id
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",

  // 【必填】字幕列表 JSON 字符串（下方用数组展示结构，实际请求需序列化为字符串）
  "captions": [
    {
      "start": 0,                              // 【必填】开始时间（微秒）
      "end": 3000000,                          // 【必填】结束时间（微秒），须 > start
      "text": "你好，剪映字幕",                 // 【必填】字幕文本
      "keyword": "剪映|字幕",                   // 【可选】关键词，多个用 | 分隔
      "keyword_color": "#ff7100",              // 【可选】关键词颜色
      "keyword_border_color": "#000000",       // 【可选】关键词描边颜色
      "keyword_font": "思源中宋",               // 【可选】关键词字体；未指定则同主体字幕 font
      "keyword_font_size": 22,                 // 【可选】关键词字号；未指定则同主体字幕字号
      "keyword_has_shadow": true,              // 【可选】是否启用关键词阴影
      "keyword_shadow_info": {                 // 【可选】关键词阴影参数
        "shadow_alpha": 0.85,                  // 阴影不透明度 [0,1]
        "shadow_color": "#000000",             // 阴影颜色
        "shadow_diffuse": 18.0,                // 阴影扩散 [0,100]
        "shadow_distance": 6.0,                // 阴影距离 [0,100]
        "shadow_angle": -45.0                  // 阴影角度 [-180,180]
      },
      "font_size": 18,                         // 【可选】本条普通文本字号
      "in_animation": "向上滑动",               // 【可选】入场动画名称
      "out_animation": "向下滑动",              // 【可选】出场动画名称
      "loop_animation": "弹幕滚动",             // 【可选】循环动画名称
      "in_animation_duration": 500000,         // 【可选】入场动画时长（微秒）
      "out_animation_duration": 500000,        // 【可选】出场动画时长（微秒）
      "loop_animation_duration": 1000000       // 【可选】循环动画单次时长（微秒）
    }
  ],

  "text_color": "#ffffff",                     // 【可选】普通文本颜色
  "border_color": "#333333",                   // 【可选】普通文本描边颜色
  "alignment": 1,                              // 【可选】对齐：0左/1中/2右（横排），3垂直居中/4垂直左/5垂直右（竖排）
  "alpha": 1.0,                                // 【可选】透明度 [0,1]
  "font": "得意黑",                           // 【可选】字体名称
  "font_size": 15,                             // 【可选】接口级默认字号
  "letter_spacing": 0,                         // 【可选】字间距
  "line_spacing": 0,                           // 【可选】行间距
  "line_max_width": 0.82,                      // 【可选】每行最大行宽占屏幕宽度比例 [0,1]
  "scale_x": 1.0,                              // 【可选】水平缩放
  "scale_y": 1.0,                              // 【可选】垂直缩放
  "transform_x": 0.0,                          // 【可选】水平位移（像素）
  "transform_y": -200.0,                       // 【可选】垂直位移（像素）
  "style_text": false,                         // 【可选】样式文本开关
  "underline": false,                          // 【可选】下划线
  "italic": false,                             // 【可选】斜体
  "bold": true,                                // 【可选】加粗
  "has_shadow": true,                          // 【可选】整段文本阴影开关
  "shadow_info": {                             // 【可选】整段文本阴影参数
    "shadow_alpha": 0.9,
    "shadow_color": "#000000",
    "shadow_diffuse": 15.0,
    "shadow_distance": 5.0,
    "shadow_angle": -45.0
  },
  "has_background": true,                      // 【可选】整段文字背景开关
  "background_info": {                         // 【可选】整段文字背景参数
    "background_color": "#000000",
    "background_style": 1,
    "background_alpha": 1.0,
    "background_round_radius": 0.0,
    "background_height": 0.14,
    "background_width": 0.14,
    "background_horizontal_offset": 0.0,
    "background_vertical_offset": 0.0
  },
  // 【可选】花字；与自定义颜色/阴影冲突，完整示例中置为 null 以保留阴影效果
  "text_effect": null,
  // 【可选】文字模板；与花字互斥且优先，完整示例中置为 null
  "text_template": null,
  // 【可选】气泡；清单外的气泡用 "effect_id:resource_id" 显式 ID 对
  "text_bubble": null,
  // 【可选】发光；预设名称或 "effect_id:resource_id" 显式 ID 对，与其它文字效果不互斥
  "text_glow": null
}
```

## 响应格式

### 成功响应 (200)

```json
{
  "code": 0,
  "message": "success",
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
  "track_id": "text_track_123",
  "text_ids": ["text_001", "text_002"],
  "segment_ids": ["seg_001", "seg_002"],
  "segment_infos": [
    {
      "id": "seg_001",
      "start": 0,
      "end": 3000000
    },
    {
      "id": "seg_002",
      "start": 3000000,
      "end": 6000000
    }
  ]
}
```

### 响应字段说明

| 字段名 | 类型 | 说明 |
|--------|------|------|
| draft_url | string | 更新后的草稿 URL |
| track_id | string | 字幕轨道 ID |
| text_ids | array | 字幕素材 ID 列表 |
| segment_ids | array | 字幕片段 ID 列表 |
| segment_infos | array | 片段信息列表（含 `id`/`start`/`end`） |

### 错误响应

```json
{
  "code": 2018,
  "message": "无效的字幕信息，请检查captions字段值是否正确"
}
```

## 使用示例

### cURL 示例

#### 1. 完整参数请求（全部必填 + 可选参数）

> 下列 curl 可直接执行：每个参数都给出了合法值。`captions` 必须是 JSON 字符串。本示例将 `text_effect` 设为 `null`，以便整段阴影与关键词阴影生效。

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_captions \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
    "captions": "[{\"start\":0,\"end\":3000000,\"text\":\"你好，剪映字幕\",\"keyword\":\"剪映|字幕\",\"keyword_color\":\"#ff7100\",\"keyword_border_color\":\"#000000\",\"keyword_font\":\"思源中宋\",\"keyword_font_size\":22,\"keyword_has_shadow\":true,\"keyword_shadow_info\":{\"shadow_alpha\":0.85,\"shadow_color\":\"#000000\",\"shadow_diffuse\":18.0,\"shadow_distance\":6.0,\"shadow_angle\":-45.0},\"font_size\":18,\"in_animation\":\"向上滑动\",\"out_animation\":\"向下滑动\",\"loop_animation\":\"弹幕滚动\",\"in_animation_duration\":500000,\"out_animation_duration\":500000,\"loop_animation_duration\":1000000},{\"start\":3000000,\"end\":6000000,\"text\":\"欢迎使用字幕功能\",\"keyword\":\"字幕\",\"keyword_color\":\"#457616\",\"keyword_border_color\":\"#111111\",\"keyword_font_size\":20,\"keyword_has_shadow\":true,\"keyword_shadow_info\":{\"shadow_alpha\":0.9,\"shadow_color\":\"#000000\",\"shadow_diffuse\":15.0,\"shadow_distance\":5.0,\"shadow_angle\":-45.0},\"font_size\":16,\"in_animation\":\"右上弹入\",\"out_animation\":\"右上弹出\",\"loop_animation\":\"VHS\",\"in_animation_duration\":400000,\"out_animation_duration\":400000,\"loop_animation_duration\":800000}]",
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

**上述完整请求参数含义速查：**

| 参数 | 示例值 | 含义 |
|------|--------|------|
| draft_url | `...draft_id=2025092811473036584258` | 【必填】目标草稿地址 |
| captions | JSON 字符串（含 2 条字幕） | 【必填】字幕内容与每条字幕的样式/动画/关键词配置 |
| text_color | `#ffffff` | 【可选】普通文本白色 |
| border_color | `#333333` | 【可选】普通文本深灰描边 |
| alignment | `1` | 【可选】居中对齐 |
| alpha | `1.0` | 【可选】完全不透明 |
| font | `得意黑` | 【可选】字体名称 |
| font_size | `15` | 【可选】接口级默认字号 |
| letter_spacing | `0` | 【可选】字间距 |
| line_spacing | `0` | 【可选】行间距 |
| line_max_width | `0.82` | 【可选】每行最大行宽占屏幕宽度比例 |
| scale_x / scale_y | `1.0` | 【可选】不缩放 |
| transform_x | `0.0` | 【可选】水平不偏移 |
| transform_y | `-200.0` | 【可选】向上偏移 200 像素 |
| style_text | `false` | 【可选】不启用样式文本开关 |
| underline / italic | `false` | 【可选】无下划线、无斜体 |
| bold | `true` | 【可选】加粗 |
| has_shadow | `true` | 【可选】启用整段阴影 |
| shadow_info.* | 见上 | 【可选】整段阴影详细参数 |
| has_background | `true` | 【可选】启用整段文字背景 |
| background_info.* | 见上 | 【可选】整段文字背景详细参数 |
| text_effect | `null` | 【可选】不使用花字，避免覆盖颜色/阴影 |
| text_template | `null` | 【可选】不使用文字模板；与花字互斥且优先 |
| text_bubble | `null` | 【可选】不使用气泡。需要时传名称或 `"effect_id:resource_id"`；优先级 文字模板 > 气泡 > 花字 |
| text_glow | `null` | 【可选】不使用发光。需要时传预设名称或 `"effect_id:resource_id"`；与其它文字效果不互斥 |

**captions 内每条字幕字段含义速查：**

| 字段 | 示例值 | 含义 |
|------|--------|------|
| start / end | `0` / `3000000` | 【必填】起止时间（微秒） |
| text | `你好，剪映字幕` | 【必填】字幕文本 |
| keyword | `剪映\|字幕` | 【可选】高亮关键词 |
| keyword_color | `#ff7100` | 【可选】关键词颜色 |
| keyword_border_color | `#000000` | 【可选】关键词描边 |
| keyword_font | `思源中宋` | 【可选】关键词字体 |
| keyword_font_size | `22` | 【可选】关键词字号 |
| keyword_has_shadow | `true` | 【可选】启用关键词阴影 |
| keyword_shadow_info.* | 见上 | 【可选】关键词阴影参数 |
| font_size | `18` | 【可选】本条普通文本字号 |
| in_animation | `向上滑动` | 【可选】入场动画 |
| out_animation | `向下滑动` | 【可选】出场动画 |
| loop_animation | `弹幕滚动` | 【可选】循环动画 |
| *_animation_duration | `500000` 等 | 【可选】对应动画时长（微秒） |
| text_template | `嘎嘎香！红色 简约 美食 情绪表达 字幕` | 【可选】本条字幕的文字模板；优先于接口级 |
| text_bubble | `背景装饰54` / `716434:6821385652727190024` | 【可选】本条字幕的气泡；优先于接口级 |

#### 2. 仅必填参数

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_captions \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
    "captions": "[{\"start\":0,\"end\":5000000,\"text\":\"你好，剪映\"}]"
  }'
```

#### 3. 关键词高亮 + 关键词阴影

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_captions \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
    "captions": "[{\"start\":0,\"end\":5000000,\"text\":\"你好，剪映\",\"keyword\":\"剪映\",\"keyword_color\":\"#ff0000\",\"keyword_font_size\":22,\"keyword_has_shadow\":true,\"keyword_shadow_info\":{\"shadow_alpha\":0.8,\"shadow_color\":\"#000000\",\"shadow_diffuse\":20.0,\"shadow_distance\":8.0,\"shadow_angle\":-45.0}}]",
    "text_color": "#ffffff",
    "font_size": 16,
    "alignment": 1
  }'
```

#### 4. 整段文本阴影（使用默认 shadow_info）

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_captions \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
    "captions": "[{\"start\":0,\"end\":5000000,\"text\":\"你好，剪映\"}]",
    "text_color": "#ffffff",
    "font_size": 20,
    "has_shadow": true
  }'
```

#### 5. 使用花字效果

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_captions \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
    "captions": "[{\"start\":0,\"end\":5000000,\"text\":\"花字演示\"}]",
    "text_effect": "白字橘色发光花字"
  }'
```

#### 6. 使用文字模板

接口级模板（整批字幕套用同一个模板）：

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_captions \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
    "captions": "[{\"start\":0,\"end\":5000000,\"text\":\"文字模板演示\"}]",
    "text_template": "嘎嘎香！红色 简约 美食 情绪表达 字幕"
  }'
```

逐条指定模板（可与普通字幕混合，普通字幕不受影响）：

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_captions \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
    "captions": "[{\"start\":0,\"end\":5000000,\"text\":\"普通字幕\"},{\"start\":5000000,\"end\":10000000,\"text\":\"模板字幕\",\"text_template\":\"7383613902744980770\"}]"
  }'
```

#### 7. 使用气泡

按名称使用清单内的气泡（`config/bubble.json`）：

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_captions \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
    "captions": "[{\"start\":0,\"end\":5000000,\"text\":\"气泡字幕\"}]",
    "text_bubble": "背景装饰54"
  }'
```

清单外的气泡用 `"effect_id:resource_id"` 显式 ID 对；也可逐条指定，与普通字幕混合：

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_captions \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
    "captions": "[{\"start\":0,\"end\":5000000,\"text\":\"普通字幕\"},{\"start\":5000000,\"end\":10000000,\"text\":\"气泡字幕\",\"text_bubble\":\"716434:6821385652727190024\"}]"
  }'
```

#### 8. 使用文字背景

只开开关，用剪映默认的黑色背景：

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_captions \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
    "captions": "[{\"start\":0,\"end\":5000000,\"text\":\"默认文本1\"},{\"start\":5000000,\"end\":10000000,\"text\":\"默认文本2\"}]",
    "has_background": true
  }'
```

自定义背景色与圆角（半透明橙色底板）：

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_captions \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
    "captions": "[{\"start\":0,\"end\":5000000,\"text\":\"带背景的字幕\"}]",
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

#### 9. 使用发光

按预设名称使用清单内的发光（`config/glow.json`）：

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_captions \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
    "captions": "[{\"start\":0,\"end\":5000000,\"text\":\"外发光字幕\"}]",
    "text_glow": "外发光"
  }'
```

清单外的发光用 `"effect_id:resource_id"` 显式 ID 对；发光与背景/气泡等可同时叠加：

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_captions \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
    "captions": "[{\"start\":0,\"end\":5000000,\"text\":\"发光字幕\"}]",
    "text_glow": "9762443:7202576698775179837",
    "has_background": true
  }'
```

## 错误码说明

| 错误码 | 错误信息 | 说明 | 解决方案 |
|--------|----------|------|----------|
| 1001 | 参数校验失败 | 请求体未通过字段校验 | 检查参数类型与必填字段 |
| 2001 | 无效的草稿URL | `draft_url` 缺失、格式错误，或草稿不在缓存中 | 传入 `create_draft` 返回的 `draft_url` |
| 2018 | 无效的字幕信息 | `captions` 不是合法 JSON、某项缺少 `start`/`end`/`text`、`end` 不大于 `start`，或文本为空 | 修正 JSON 字符串与必填字段 |
| 2019 | 字幕添加失败 | 写入草稿过程出错 | 检查草稿状态后重试 |
| 2042 | 草稿锁获取超时 | 同一时间只允许一个操作，草稿正被占用 | 稍后重试 |

## 注意事项

1. **时间单位**：所有时间参数使用微秒（`1 秒 = 1_000_000 微秒`）
2. **captions 格式**：必须是合法 JSON **字符串**，外层再包一层请求 JSON
3. **颜色格式**：十六进制，如 `#ffffff`、`#ff0000`
4. **动画名称**：请通过 `get_text_animations` 获取可用名称
5. **花字名称**：请通过 `get_text_effects` 获取可用名称或 `effect_id`
5.1. **文字模板**：传模板名称或数字 `effect_id`；与 `text_effect` 互斥且优先。模板清单见 `config/text_template.json`（5166 个），名称重名时命中靠前一条，精确定位请用 `effect_id`；不在表中的纯数字 id 会直接透传
5.2. **气泡**：传气泡名称、`resource_id` 或 `effect_id`；气泡的 `effect_id` 与 `resource_id` **不是同一个值**，清单外的气泡请传 `"effect_id:resource_id"` 显式 ID 对（如 `"716434:6821385652727190024"`），只传单个数字不会透传。优先级为 文字模板 > 气泡 > 花字；气泡不重置颜色/描边/阴影
5.3. **文字背景**：`has_background=true` 才生效，只传 `background_info` 会被忽略；不给 `background_info` 时用剪映默认黑色背景。`background_info` 字段与草稿 `background_*` 一一对应，`background_style` 只能传 `1`/`2`，颜色非法会回退黑色并告警。花字不重置背景，两者会视觉叠加
5.4. **发光**：传预设名称（`外发光`/`轮廓光`）或 `resource_id`/`effect_id`；与气泡一样 `effect_id` 与 `resource_id` **不是同一个值**，清单外的发光请传 `"effect_id:resource_id"` 显式 ID 对（如 `"9762443:7202576698775179837"`），只传单个数字不会透传。发光**与花字/文字模板/气泡都不互斥**（不重置颜色/描边/阴影），但**只支持接口级**，混用两种预设需分两次调用；清单外的发光其 `bloom_params` 会落到默认值并告警
6. **坐标系统**：`transform_x` / `transform_y` 使用像素，内部会按画布尺寸换算；`background_horizontal_offset` / `background_vertical_offset` 则是 `[-1, 1]` 的草稿坐标，`0` 为居中
7. **关键词阴影**：与关键词颜色/描边一样写在同一字幕的 styles 分区内，不另建字幕行；整段阴影仍由 `has_shadow` / `shadow_info` 控制

## 工作流程

1. 验证必填参数（`draft_url`, `captions`）
2. 解析并校验每条字幕
3. 从缓存获取草稿
4. 创建字幕轨道
5. 创建文本片段并应用样式/关键词/动画/花字
6. 保存草稿并返回结果

## 相关接口

- [创建草稿](./create_draft.md)
- [生成字幕信息](./caption_infos.md)
- [获取文字动画](./get_text_animations.md)
- [获取花字效果](./get_text_effects.md)
- [保存草稿](./save_draft.md)
- [生成视频](./gen_video.md)

---
<div align="right">

📚 **项目资源**  
**GitHub**: [https://github.com/Hommy-master/capcut-mate](https://github.com/Hommy-master/capcut-mate)  
**Gitee**: [https://gitee.com/taohongmin-gitee/capcut-mate](https://gitee.com/taohongmin-gitee/capcut-mate)

</div>
