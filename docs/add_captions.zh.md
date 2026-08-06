# ADD_CAPTIONS API 接口文档

## 🌐 语言切换
[中文版](./add_captions.zh.md) | [English](./add_captions.md)

## 接口信息

```
POST /openapi/capcut-mate/v1/add_captions
```

## 功能描述

向现有草稿中批量添加字幕。该接口用于在指定的时间段内添加字幕到剪映草稿中，支持丰富的字幕样式设置，包括文本颜色、边框颜色、对齐方式、透明度、字体、字体大小、字间距、行间距、缩放、位置、下划线/斜体/加粗、文本阴影、关键词高亮与关键词阴影、文字动画、花字效果等。

## 更多文档

📖 更多详细文档和教程请访问：[https://docs.jcaigc.cn](https://docs.jcaigc.cn)

## 请求参数

### 接口级参数说明

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| draft_url | string | ✅ | - | 目标草稿的完整 URL，需包含 `draft_id` 查询参数 |
| captions | string | ✅ | - | 字幕信息列表的 **JSON 字符串**（不是 JSON 数组本身） |
| text_color | string | ❌ | `"#ffffff"` | 普通字幕文本颜色，十六进制，如 `#ffffff` |
| border_color | string | ❌ | `null` | 普通字幕描边颜色，十六进制；`null` 表示无描边 |
| alignment | integer | ❌ | `1` | 文本对齐方式：`0` 左对齐，`1` 居中，`2` 右对齐（`3`-`5` 为预留） |
| alpha | number | ❌ | `1.0` | 文本透明度，取值范围 `[0.0, 1.0]`，`1.0` 为不透明 |
| font | string | ❌ | `null` | 字体名称，须为下方「支持的字体」中的展示名（也支持枚举名/别名）；`null` 使用默认字体 |
| font_size | integer | ❌ | `15` | 接口级默认字号；当 caption 项未指定 `font_size` 时生效，须 `>= 1` |
| letter_spacing | number | ❌ | `null` | 字间距；`null` 表示使用默认值 `0` |
| line_spacing | number | ❌ | `null` | 行间距；`null` 表示使用默认值 `0` |
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
| text_effect | string | ❌ | `null` | 花字效果名称或 `effect_id`；有效花字会重置颜色/描边/阴影相关效果 |

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

### 参数详解

#### 对齐方式

| 值 | 说明 |
|---|------|
| 0 | 左对齐 |
| 1 | 居中对齐 |
| 2 | 右对齐 |
| 3 | 垂直居中（预留） |
| 4 | 垂直左对齐（预留） |
| 5 | 垂直右对齐（预留） |

#### 花字与阴影的关系

当 `text_effect` 能解析到有效花字时，系统会将 `text_color` 重置为 `#ffffff`、`border_color` 重置为 `null`、`has_shadow` 重置为 `false`，并禁用关键词阴影（`keyword_has_shadow` 不生效）。若需要自定义颜色/阴影，请不要同时传有效花字。

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
  "alignment": 1,                              // 【可选】对齐：0左/1中/2右
  "alpha": 1.0,                                // 【可选】透明度 [0,1]
  "font": "得意黑",                           // 【可选】字体名称
  "font_size": 15,                             // 【可选】接口级默认字号
  "letter_spacing": 0,                         // 【可选】字间距
  "line_spacing": 0,                           // 【可选】行间距
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
  // 【可选】花字；与自定义颜色/阴影冲突，完整示例中置为 null 以保留阴影效果
  "text_effect": null
}
```

## 响应格式

### 成功响应 (200)

```json
{
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

### 错误响应 (4xx/5xx)

```json
{
  "detail": "错误信息描述"
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
| scale_x / scale_y | `1.0` | 【可选】不缩放 |
| transform_x | `0.0` | 【可选】水平不偏移 |
| transform_y | `-200.0` | 【可选】向上偏移 200 像素 |
| style_text | `false` | 【可选】不启用样式文本开关 |
| underline / italic | `false` | 【可选】无下划线、无斜体 |
| bold | `true` | 【可选】加粗 |
| has_shadow | `true` | 【可选】启用整段阴影 |
| shadow_info.* | 见上 | 【可选】整段阴影详细参数 |
| text_effect | `null` | 【可选】不使用花字，避免覆盖颜色/阴影 |

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

## 错误码说明

| 错误码 | 错误信息 | 说明 | 解决方案 |
|--------|----------|------|----------|
| 400 | draft_url是必填项 | 缺少草稿 URL | 提供有效的 `draft_url` |
| 400 | captions是必填项 | 缺少字幕信息 | 提供有效的 `captions` |
| 400 | 无效的字幕信息 | captions 校验失败 | 检查 JSON 与必填字段 |
| 400 | 时间范围无效 | end 必须大于 start | 修正起止时间 |
| 404 | 草稿不存在 | draft_id 无效或不在缓存中 | 检查草稿 URL |
| 500 | 字幕添加失败 | 内部处理错误 | 联系技术支持 |

## 注意事项

1. **时间单位**：所有时间参数使用微秒（`1 秒 = 1_000_000 微秒`）
2. **captions 格式**：必须是合法 JSON **字符串**，外层再包一层请求 JSON
3. **颜色格式**：十六进制，如 `#ffffff`、`#ff0000`
4. **动画名称**：请通过 `get_text_animations` 获取可用名称
5. **花字名称**：请通过 `get_text_effects` 获取可用名称或 `effect_id`
6. **坐标系统**：`transform_x` / `transform_y` 使用像素，内部会按画布尺寸换算
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
