# ADD_FILTERS API Documentation

## 🌐 Language Switch
[中文版](./add_filters.zh.md) | [English](./add_filters.md)

## Interface Information

```
POST /openapi/capcut-mate/v1/add_filters
```

## Function Description

Add video filters to existing drafts. This interface is used to add filter materials to Jianying drafts within specified time periods, supporting various filter types such as vintage, black and white, cinematic, etc. Filters can be used to adjust the color tone and visual style of videos.

## More Documentation

📖 For more detailed documentation and tutorials, please visit: [https://docs.jcaigc.cn](https://docs.jcaigc.cn)

## Request Parameters

```json
{
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
  "filter_infos": "[{\"filter_title\": \"1980\", \"start\": 0, \"end\": 5000000, \"intensity\": 80}, {\"filter_title\": \"森山\", \"start\": 2000000, \"end\": 7000000}]"
}
```

### Parameter Description

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| draft_url | string |✅ | - | Complete URL of the target draft |
| filter_infos | string |✅ | - | JSON string of filter information list |

### Parameter Details

#### filter_infos Array Structure

`filter_infos` is a JSON string containing an array of filter objects, each with the following fields:

```json
[
  {
    "filter_title": "1980",       // Filter name/title, required parameter
    "start": 0,                   // Filter start time (microseconds), required parameter
    "end": 5000000,               // Filter end time (microseconds), required parameter
    "intensity": 80               // Filter intensity (0-100), optional, default 100
  }
]
```

**Field Description**:
- `filter_title`: Filter name; must be one of the Supported Filter Names below
- `start`: Filter start time in microseconds
- `end`: Filter end time in microseconds
- `intensity`: Filter intensity (0-100), controls the strength of the filter effect, default is 100

#### Time Parameters

- **start**: Start time of the filter on the timeline, unit microseconds (1 second = 1,000,000 microseconds)
- **end**: End time of the filter on the timeline, unit microseconds
- **Duration**: Filter duration = end - start

#### Intensity Parameter

- **intensity**: Controls the strength of the filter effect
  - Range: 0-100
  - Default: 100 (full intensity)
  - Lower values result in a more subtle filter effect
  - Example: `intensity: 50` applies the filter at 50% strength

<!-- FILTER_LIST_START -->
### Supported Filter Names (`filter_title` values)

Use the names below directly as `filter_title` (same as CapCut/Jianying display names). Unmatched names will fail.

Total: **1052** filters:

```text
160C
1980
2077
400H
4K画质
4K画质电影
4K高品质
800Z
8K画质
90s
ABG
City Walk
Ditto
EOS3
FXN
GR正片
GR绿
GR蓝
IG白
ins古早味
INS暗
INS暗调
iPhone6s
KE1
KONICA
KU4
KV5D
Lofi II
miu系II
PENTAX
Pocket3
VHS III
Y3K
万圣
三洋VPC
不要抬头
丝滑皮肤
中性
中性II
中性奶杏
乐游
书意
云暖
亢奋
京都
亭竹
亮丽
亮夏
亮肤
人生之事
仲夏夜
仲夏绿光
仿撕拉片
伊豆
伤感故事电影
伤感电影
似锦
低保真
余晖
佳能G12
佳能G7X II
佳能G7X III
佳能清透感
侘寂灰
俏皮萌宠
俱乐部
倾森
假日海滩
假日电影感
偏振镜
傍晚
元宵祈福
元气新年
元气春颜
元气焕肤
元气粉肌
光流
克洛伊
冬日亮肤
冬日清寒
冬日烧烤
冬日物语
冬日胶卷
冬漫
冬禧
冬离
冬绪电影
冬雪电影感
冰夏
冰清玉洁
冰清蓝
冰瀑
冰火
冰肌
冰茶
冰蓝印染
冰雪白
冷叙
冷墨
冷月夜
冷气机
冷白
冷萃
冷蓝
冷调CCD
冷调微曝
冷透
净白
净白肤
净透
凛冬
凛冬电影感
凝黛
初恋
初雪电影感
加州落日
动漫小镇
劲闯
北海道II
千玺IXU
千禧潮酷
千里江山
千金妝
半衫
南法午后
卡露尔
即刻春光
原木
原生肤
原生自然
原野
去灰
去灰II
去灰高清
去雾
去黄
去黄增质
去黄提亮
去黄韩系
反差富士
反差色
发光CCD
叠阳
古早像素
古早回忆
古早回忆录
古早复古
古早宝丽来
古早感胶片
古早时光
古早画质
古早记忆
古早韩系
古早韩风
古早高曝
古罗马
古罗马电影
古都
古风影视
史诗电影
吉宵
向晚
告白
味蕾
和歌山
哈苏I
哈苏II
哈苏蓝
哥谭
喜市
喜庆胶片
喜气新春
四喜
围炉暖食
国民旧照
国风电影
圣善夜
圣诞回忆录
圣诞愿景
圣诞拍立得
圣诞灯光
圣诞灯光II
圣诞灯光III
圣诞胶片
圣诞萌宠
圣诞闪胶II
圣诞闪胶III
城市赏月II
增色
增色II
增质CCD
增质去雾
墨林
墨色胶卷
复古工业
复古电影感
复古蓝调
夏威夷
夏日小美好
夏日清凉
夏日粉
夏日紫霞
夏日辣妹
夏日风吟
多巴胺
夜拍闪曝
夜拍高光
夜景人像增强
夜景去雾
夜景增色II
夜焰
夜雾
大吉岭
大唐盛世
大疆4Pro
大疆电影感
大雪纷飞
奈良
奥本海默
奥林巴斯
奥罗拉
奶呼萌宠
奶昔
奶杏
奶油
奶油II
奶油柔肤
奶油白
奶油白肤
奶油美食
奶油肤
奶油风萌宠
奶绿
好莱坞I
好莱坞II
好莱坞III
好莱坞IV
姜饼红
威尼之都
嬉皮士
子弹列车
安塞尔灰调
安愉
安藤调
安西娅
宝丽来SX70
宫崎漫夏
家宴
宿营
富士CC I
富士CC II
富士NC I
富士NC II
富士NC III
富士NN
富士x100
富士XT5
富士电影
富士蓝
富士蓝II
富士青
富春山居
寻荷
小清新
小美好
小镇
小麦色
尘杏
尘烟
山晴
山本
山海诗篇
山系
岚夏
岩灰
川秋电影感
川野
巧克力
市井
布兰卡
布朗
希望
幽海
幽蓝
底特律
庙会
弥晖
强曝光
彩光
彩果
彩檐
影叙
影忆
影石4k
影部
往事
徕卡I
徕卡II
徕卡Q2
徕卡银盐
微澜
德古拉
心动夏
忆山
忆时
快照I
快照II
忽风
怀旧
怦然心动
恍光
情感故事电影
情感电影
情绪电影
情辉
慕斯
扫街
扬帆远航
拐杖糖
捕风
探店博主III
摩卡灰
摩登
撕拉拍立得
攀岩
敦刻尔克
文艺少女
料理
新中式电影感
新宿
新年喜市
新年欢愉
新年电影
新年电影感
新年红
新年红气
新年顺意
新闪
新颜
日光吻
日出
日出增色
日出时刻
日料寿司
日漫增色
日漫清新
日系增色
日系奶油
日系春和
日落增色
日落时刻
日落晚霞
日落橘
日落飞车
旧乐园
旧时代I
旧时代II
旧时来信
旧曲
旧金山
时尚极简
旷野
旷野自然
旷野蓝
明亮春味
明亮焕晴
明媚春景
明媚春色
明媚自然
明媚透亮
明晰
星云
春和
春喜
春天淡彩
春忆胶卷
春日序
春日樱
春日清晰
春日清透
春日温柔
春日绿妍
春日美食III
春日花田
春日花间
春日韩胶
春桃肤
春橙肤
春游踏青
春禧电影感
春风
昭和
昭和夏
晚宴
晚柠
晚樱
晨旭
普林斯顿
景明
晴冬暖阳
晴天
晴天亮丽
晴天增色
晴天灿烂 
晴好
晴好春日
晴好风光
晴山质感
晴春
晴春奶蓝
晴朗
晴沐
晴海
晴研
晴秋
晴空
晴空漫游
晴肤
晴谷
晴颜
晶莹雪肤
晶透
智能光线
暖晨
暖阳冬日
暖雾晨光
暖食
暖食增色
暖黄
暗光提亮
暗匣
暗夜
暗夜明肤
暗影
暗曛
暗蓝电影
暗蓝电影感
暗调发光
暗调古风
暗调复古电影
暗调氛围
暗调电影
暗调纪实电影
暗调阴郁
暗部漫游
暗金
暗银
暗银II
暗雅
暗黑玫瑰
暮信
暮光
暮川
暮樱
暮涛
暮色
暮色约会
曼波
月升之国
月吟
月夜
月辉
朦胧气质棕
木葵
未央
末世天使
朱栗
杏铃
松果棕
松绿
林间
果酥
柏林
柔光
柔焦
柔雾感
柠檬青
柠青
柯达金200
栖海
栩栩
格金
桃木
桃粉
桐影
梦境
梦幻夏
梦核紫
梨花白
梨花白皙
梵时
棕咖
棕宥
棕榈
棠梨
森山
森林徒步
森秋
森绿
椰林
椿和
椿来
樱晴
樱粉
樱花粉肤
橘光
橘海
橙蓝
欧若淡彩
殷粉
比佛利
毕业胶片
气泡水
气色
气色透亮
氧气春日
氧气甜白
水光红润
水墨意境
江浙沪
沙漫
沙砾
沙龙暖调
治愈奶萌
治愈萌宠
法式少女
法式甜粉
法餐
泥金
洋气新年
洛丽塔粉
活力夏
流光金属
浅岛
浅空
浅绿微曝
浅茶
浅草
浓咖
浓调电影
浓郁增色
浓郁日落
浓郁电影感
浓郁秋意
浓郁胶卷
浪漫烟火
浪漫质感
浪语
浮生
海上冲浪
海山
海松
海水正蓝
海浪梦境
海盐
海盐蓝
海街日记
海边胶片
海雾
海鸥DC
润光
涩谷
淡奶油
深沉
深秋
深蓝电影感
深褐
清冷
清冷冬日
清冷国风
清冷情绪感
清冷暗黑
清冷破碎III
清新
清新感
清新明亮
清新春日
清新晴空
清新暖食
清新氧晴
清新漫和
清新绿妍
清新花妍
清新质感
清新透亮
清新雪肤
清明上河
清晰
清晰ll
清晰严冬
清晰净透
清晰增强
清晰增色
清晰增质
清晰提升
清晰明亮
清晰烟花
清晰电影
清晰画质
清晰自然
清晰花朵
清晰萌宠
清晰质感
清晰透亮
清澈
清透II
清透光感
清透感
清透春日
清透美食
清透自然
清透萌宠
温述
港历
港风
港风复古
港风夜景
港风电影
湖畔
演唱会
漠土
漫夏
漫彩
漫春
漫樱
漫步
漫空
漫荫
漫谷
漫银纪元
漱石
潘多拉
灯会
灯塔
灰芋
灰调中性
灰调日常
灰麻
灿金彩带
炊烟
烈日
烈焰红
烈空
烘培
烘挞
烛光晚餐
烟岚
烟橙
烟火增色
烟火年年
烟火迎春
烟花去雾
烟花增强
烟花灿烂
烟花璀璨
烟花璀璨 II
烟霞
热带季风
热显宝丽来
热气腾腾
焕肤
焰色
熏柏
熔金
燃力
燃空
爱丽丝
爱之城
爱之城II
牙白
牛奶肌
牛皮纸
牧野
独行侠
猎梦
玄影灵
玩趣
珠光蓝
珠落
琥珀
璀璨
甜妹感
甜心芭比
田园野餐
电影光感
电影叙事感
电影境遇
电影增强
电影增质
电影大师
电影往事
电影感增强
电影感大片
电影慢镜
电影慢镜II
电影柔光
电影校正
电影独白
电影画质
电影葡街
电影镜头
画报
画质修复
画质增蓝
画质高清
疼痛文学
病娇
登高
白富美
白瓷亮肤
白皙
白皙丝绸
白皙去黄
百川
盐岚
盐系
石山
矿野
砂红
砂金
破晓
砾绀
硬朗
硬朗男孩
碎芒
碳烤
福桔
福气新年
福气新春
福漫
福运
禾美
私语
秋叶黄
秋季电影感
秋意电影感
秋日物语II
秋日自然
秋池
秋波
秋田胶片
科切拉
科幻星球
空灵
空谷
竹绢
简餐
米棕
粉柔撕拉片
粉橘
粉瓷
粉白
粉白微曝光
粉肤
粉蓝烟花
粉霞
粹光
素净
素简
素肌
紫霞时分
繁花似锦
繁花如梦
繁花璀璨
红绿
红运
纪实电影
纪实电影胶片
纱雾
织乐
经典港风
绝对红
绿妍
绿妍II
绿野
绿野漫旅
缎光肌
美味
美味brunch
美好春日
美好瞬间
美拉德
美食增色
美高
羽梦
老友记
聆时
聚焦
背景增色
胡桃木
胶片微曝
胶片电影
自然
自然增色
自然明亮
自然春色
自然清晰
自由
臻金
艾丽莎
芭比
花园
花容
花椿
花火
花火增色
花火夜焰
花花世界
花间
花食
苍橘
苏打气泡
苦尽柑来
苦檀
英伦复古
茶卡盐湖
茶墨
茶酪
荒原风光
莫吉托
莫奈睡莲
莫奈花园
菁润明肤
萌宠
落日
落日派对
落日海岛
落日电影
落日粉
落日鎏金
落日飞车
落牧
蒸汽机
蒸汽波
蓝梦核
蓝橙II
蓝灰
蓝调
蓝调烟火
蓝调舞曲
蓝都
蓝金
蔚蓝海域
薄绿
薄荷
薄荷奶绿
薰草
藤宅
街头
褪色
褪色胶卷
西冷
西西里
西部峡谷
西野
西雅图
西餐
诗诺
诗野
谧歌
贝松绿
贝果
质感增蓝
质感新中式
质感晴春
质感暗调
质感电影
赏味
赛博朋克
赤陀
赫本
赫石
超清4K
超清电影
超清电影卷
超清画质
超白
超透白皙
超高清
越岭
越野
轻古早
轻氧夏
轻肤III
轻胶少女
轻食
达芬妮
过期电影卷
迈阿密
运动质感
迷幻
迷雾
逆光拯救
逆光提亮
透氧肌肤
通透
通透暖食
通透氧感
邂逅
郁金香
都卡
都城
都市
都市电影II
酚蓝
酷感辣妹
酷白
酷绿
醒春
里昂
野林
野趣
金姜
金属
金粉飘落
铅绿
银蓝
镜粉
闪光灯
闪星
闪耀派对
闪胶回忆
闻香识人
阳光肤
阴天拯救
阿尔菲
陶瓷肌
随性
雀染
雅西卡
雨皂
雨空
雪地胶片
雪地胶片II
雪地胶片III
雪挞
雪白肤III
雪白透亮
雪鹿
雾瓷
雾都
雾野
青提
青春古早
青春照
青春胶片
青森
青橙
青橙电影
青橙电影感
青灰
青红夜
青蒲
青黄
青黄II
韦斯
韩女古早
韩式古早
韩系INS
音乐节
风味
风铃
风铃II
风铃蓝
飒意
食光II
食色
香松
香浓
驮月
高晴画质
高清
高清4K电影
高清4k电影
高清II
高清中性灰
高清亮粉
高清修复
高清修复III
高清冬日
高清冷冬
高清圣诞
高清增强
高清增色
高清增质
高清寒冬
高清影视
高清感
高清感II
高清感III
高清提亮
高清提升
高清明亮
高清春日
高清晴天
高清晴日
高清暖调
高清润白
高清润颜
高清漫晴
高清烟火
高清焕晴
高清电影
高清电影卷
高清画质
高清福气
高清绿妍
高清美食
高清自然
高清质感
高清雪景
高清雪肤
高清鲜明
高清黑白
高清默冬
高级影视
高级质感
高街
高质感电影
高饱和
鬼魅
魅影
魔都
鲜亮
鲜亮食光
鲜明
鲜明II
鲜明增色
鲜美
鲜美年味
鲜艳增色
鲜花增彩
鲜花增色
鲜花增艳
鲜花自然
鲜萃食光
鸿运新春
鹅冠
麋鹿
黄昏
黑冰
黑暗神话
黑曜
黑白记忆
黑胶唱片
黑莓
黑豹
黑金
黑金红
默片
黛瓦
龙舌兰
```
<!-- FILTER_LIST_END -->

## Response Format

### Success Response (200)

```json
{
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
  "track_id": "filter-track-uuid",
  "filter_ids": ["filter1-uuid", "filter2-uuid"],
  "segment_ids": ["segment1-uuid", "segment2-uuid"]
}
```

### Response Field Description

| Field | Type | Description |
|-------|------|-------------|
| draft_url | string | Updated draft URL |
| track_id | string | Filter track ID |
| filter_ids | array | List of added filter IDs |
| segment_ids | array | List of segment IDs |

### Error Response (4xx/5xx)

```json
{
  "detail": "Error message description"
}
```

## Usage Examples

### cURL Examples

#### 1. Basic Filter Addition

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_filters \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "filter_infos": "[{\"filter_title\":\"1980\",\"start\":0,\"end\":10000000}]"
  }'
```

#### 2. Filter with Custom Intensity

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_filters \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "filter_infos": "[{\"filter_title\":\"森山\",\"start\":0,\"end\":5000000,\"intensity\":60}]"
  }'
```

#### 3. Multiple Filters

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_filters \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "filter_infos": "[{\"filter_title\":\"1980\",\"start\":0,\"end\":5000000,\"intensity\":80},{\"filter_title\":\"City Walk\",\"start\":3000000,\"end\":8000000,\"intensity\":100}]"
  }'
```

## Error Code Description

| Error Code | Error Message | Description | Solution |
|------------|---------------|-------------|----------|
| 400 | draft_url is required | Missing draft URL parameter | Provide a valid draft URL |
| 400 | filter_infos is required | Missing filter information parameter | Provide valid filter information JSON |
| 400 | filter_infos format error | JSON format is incorrect | Check JSON string format |
| 400 | Filter configuration validation failed | Filter parameters do not meet requirements | Check parameters for each filter |
| 400 | filter_title is required | Filter title missing | Provide title for each filter |
| 400 | start is required | Filter start time missing | Provide start time for each filter |
| 400 | end is required | Filter end time missing | Provide end time for each filter |
| 400 | Time range invalid | end must be greater than start | Ensure end time is greater than start time |
| 400 | Intensity out of range | Intensity must be between 0-100 | Provide valid intensity value |
| 404 | Draft does not exist | Specified draft URL invalid | Check if draft URL is correct |
| 404 | Filter not found | Specified filter does not exist | Check if filter title is valid |
| 500 | Filter addition failed | Internal processing error | Contact technical support |

## Notes

1. **JSON Format**: filter_infos must be a valid JSON string
2. **Time Unit**: All time parameters use microseconds (1 second = 1,000,000 microseconds)
3. **Filter Names**: Filter titles must match exactly with system filter names
4. **Intensity Range**: Intensity must be between 0-100, default is 100
5. **Time Overlap**: Multiple filters can be applied to the same time period
6. **Filter Priority**: Filters are applied in the order they appear in the array
7. **Performance**: Complex filters may affect video processing performance

## Workflow

1. Validate required parameters (draft_url, filter_infos)
2. Parse filter_infos JSON string
3. Validate parameter configuration for each filter
4. Obtain and decrypt draft content
5. Create filter track
6. Add filter segments to track
7. Save and encrypt draft
8. Return processing result

## Related Interfaces

- [Create Draft](./create_draft.md)
- [Add Videos](./add_videos.md)
- [Add Images](./add_images.md)
- [Add Effects](./add_effects.md)
- [Save Draft](./save_draft.md)
- [Generate Video](./gen_video.md)

---

<div align="right">

📚 **Project Resources**  
**GitHub**: [https://github.com/Hommy-master/capcut-mate](https://github.com/Hommy-master/capcut-mate)  
**Gitee**: [https://gitee.com/taohongmin-gitee/capcut-mate](https://gitee.com/taohongmin-gitee/capcut-mate)

</div>
