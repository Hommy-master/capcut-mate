# ADD_BEAUTY API Documentation

## 🌐 Language Switch
[中文版](./add_beauty.zh.md) | [English](./add_beauty.md)

## Interface Information

```
POST /openapi/capcut-mate/v1/add_beauty
```

## Function Description

Add portrait beautification to video segments in an existing draft, covering all four JianYing panels:
Skin (`skin`, 美颜), Face Shape (`shape`, 美型), Makeup (`makeup`, 美妆) and Body (`body`, 美体).
Beauty materials are attached to the video segment and written into `materials.effects` (`type=figure`) —
they are not a separate effect track.

The request body has four optional groups: `skin`, `shape`, `makeup`, `body`.
Field names are English; preset **values** keep the JianYing preset names, which are Chinese
(e.g. `skin_tone: "冷白"`, `look: "淡人妆"`).
A slider set to 0 (or an empty preset) is **not written** — matching JianYing's "off" state (material absent).
Whenever any slider is applied, one `makeup-root` material is added to the segment.
Re-applying the same slider updates its intensity in place (the material id is preserved).

## Request Parameters

```json
{
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
  "segment_ids": ["d62994b4-25fe-422a-a123-87ef05038558"],
  "skin": { "smooth": 52, "whitening": 67, "skin_tone": "冷白", "temperature": 11, "intensity": 60 },
  "shape": { "small_face": 19, "slim": 33 },
  "makeup": { "look": "淡人妆", "intensity": 80 },
  "body": { "small_head": 33, "slim_waist": 60, "smooth": 19, "whitening": 26 }
}
```

### Common Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| draft_url | string | ✅ | - | Draft URL |
| segment_ids | array | ✅ | - | Video segment IDs to apply beautification to |
| skin | object | ❌ | - | Skin group (美颜), see below |
| shape | object | ❌ | - | Face-shape group (美型), see below |
| makeup | object | ❌ | - | Makeup group (美妆), see below |
| body | object | ❌ | - | Body group (美体), see below |

### skin (美颜)

| Field | JianYing label | Type | Default | Description |
|-------|----------------|------|---------|-------------|
| even | 匀肤 | number | 0 | Intensity 0-100 |
| plump | 丰盈 | number | 0 | Intensity 0-100 |
| smooth | 磨皮 | number | 0 | Intensity 0-100 (a different material from `body.smooth`) |
| dewrinkle | 祛法令纹 | number | 0 | Intensity 0-100 |
| bright_eye | 亮眼 | number | 0 | Intensity 0-100 |
| dark_circle | 祛黑眼圈 | number | 0 | Intensity 0-100 |
| whitening | 美白 | number | 0 | Intensity 0-100 (a different material from `body.whitening`) |
| white_teeth | 白牙 | number | 0 | Intensity 0-100 |
| skin_tone | 肤色 | string | "" | Skin preset: `冷白` / `暖白`; empty means not applied |
| temperature | 冷暖 | number | 0 | Skin cold/warm 0-99, only used when `skin_tone` is set |
| intensity | 程度 | number | 60 | Skin intensity 0-100, only used when `skin_tone` is set |

### shape (美型) — JianYing "美型 - 面部"

| Field | JianYing label | Type | Default | Description |
|-------|----------------|------|---------|-------------|
| small_face | 小脸 | number | 0 | Intensity 0-100 |
| slim | 瘦脸 | number | 0 | Intensity 0-100 |
| v_shape | V脸 | number | 0 | Intensity 0-100 |
| jaw | 下颌骨 | number | 0 | Intensity 0-100 |
| cheekbone | 颧骨 | number | 0 | Intensity 0-100 |
| shorten | 短脸 | number | 0 | Intensity 0-100 |
| contour_smooth | 流畅脸 | number | 0 | Intensity 0-100 |
| lower | 下庭 | number | 0 | Intensity 0-100 |
| middle | 中庭 | number | 0 | Intensity 0-100 |
| upper | 上庭 | number | 0 | Intensity 0-100 |
| hairline | 发际线 | number | 0 | Intensity 0-100 |
| width | 窄脸 | number | 0 | **Reserved, not supported yet** — must be 0 |
| chin_length | 下巴长短 | number | 0 | **Reserved, not supported yet** — must be 0 |

### makeup (美妆)

| Field | JianYing label | Type | Default | Description |
|-------|----------------|------|---------|-------------|
| look | 套装 | string | "" | Makeup preset, the Chinese name shown in JianYing's 美妆 - 套装 panel (54 in total, see below); empty means not applied |
| intensity | 程度 | number | 80 | Preset intensity 0-100, only used when `look` is set |
| face_id | 人脸 | string | "-1" | Which face the look applies to: `-1` means all faces (same as JianYing's "apply globally"); or a detected face index `0` / `1` / `2`… |

### body (美体)

| Field | JianYing label | Type | Default | Description |
|-------|----------------|------|---------|-------------|
| small_head | 小头 | number | 0 | Intensity 0-100 |
| swan_neck | 天鹅颈 | number | 0 | Intensity 0-100 |
| slim_arm | 瘦手臂 | number | 0 | Intensity 0-100 |
| straight_shoulder | 直角肩 | number | 0 | Intensity 0-100 |
| slim_body | 瘦身 | number | 0 | Intensity 0-100 |
| slim_waist | 瘦腰 | number | 0 | Intensity 0-100 |
| long_leg | 长腿 | number | 0 | Intensity 0-100 |
| plump_breast | 丰胸 | number | 0 | Intensity 0-100 |
| slim_hip | 美胯 | number | 0 | Intensity 0-100 |
| smooth | 磨皮 | number | 0 | Body smoothing 0-100 (a different material from `skin.smooth`) |
| whitening | 美白 | number | 0 | Body whitening 0-100 (a different material from `skin.whitening`) |
| wide_shoulder | 宽肩 | number | 0 | **Reserved, not supported yet** — must be 0 |

## How Values Are Written

| Group | category_id | Intensity location | Normalization |
|-------|-------------|--------------------|---------------|
| skin sliders | auto-beauty2 | `smooth`/`whitening` in top-level `value`, others in `adjust_params` | ÷100 |
| skin tone | auto-beauty2 | `face_adjust_params` (ColdWarm + Intensity) | temperature ÷99, intensity ÷100 |
| shape | auto-beauty | `adjust_params` (name is always "0") | ÷100 |
| makeup | makeup | `face_adjust_params` (face_adjust_whole) | ÷100 |
| body | auto-beauty3 | top-level `value` | ÷100 |

- skin, shape and makeup sliders carry an `algorithm_artifact_path`; `whitening`, all body sliders and skin tone do not.
- Makeup writes a fixed 11-item `exclusion_group` so it never stacks with other makeup parts.
- `face_id` is the **index of a detected face** (JianYing numbers faces in detection order, starting at 0), not a slot belonging to the look; `-1` (the default) means all faces. Hard-coding one index makes the look land on a non-existent face — and render nothing — as soon as the clip has fewer faces or a different detection order.
- Materials are written by `resource_id`; no local effect-cache path is written — JianYing downloads resources on open.
- The `name` field written into the draft keeps the JianYing Chinese label (e.g. `"name": "磨皮"`), not the English API field name.

### Presets

| Preset | resource_id | Notes |
|--------|-------------|-------|
| `skin_tone: 冷白` | 7148720872105185800 | temperature ÷99, intensity ÷100 |
| `skin_tone: 暖白` | 7148720647714116132 | temperature defaults to 0 |
| `look: <name>` | see below | all faces by default (face_id "-1") |

All 54 looks accepted by `look` (the value is the name itself, same as the JianYing panel):

> 90年代、doll感、上镜韩妹、中国妆、人形电脑、元气、兔兔妆、冬日白开水、冷感、减龄妆、初恋、原生、古早韩妆、夏日桃桃、夏日清透感、夏日白开水、奶杏、学姐妆、小烟熏、小魔女、微醺、心动、拜年妆、新年开运妆、无花果、春日樱花妆、柿柿如意、橘子汽水、氧气感、派对微醺、淡人妆、淡妆公式、淡盐系、清透感、热红酒、猫系女友、甜心芭比、甜系白开水、男友、男生、白开水、白鹿好运妆、盐系、纯欲蝴蝶兰、腮红大法、芋泥啵啵、芭蕾少女、英气、落日、裸妆、郁金香、雀斑自由、韩国学妹、韩系蜜桃

The name → `resource_id` table is exported from the JianYing panel cache by `tools/extract_makeup_looks.py` into `src/pyJianYingDraft/metadata/makeup_looks_generated.py`; re-run the script after JianYing ships new looks.

## Response Format

### Success Response (200)

```json
{
  "code": 0,
  "message": "success",
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
  "affected_segments": ["d62994b4-25fe-422a-a123-87ef05038558"],
  "figure_ids": ["figure-id-1", "makeup-root-id"]
}
```

| Field | Type | Description |
|-------|------|-------------|
| draft_url | string | Draft URL |
| affected_segments | array | Segment IDs the beautification was applied to |
| figure_ids | array | Beautification material IDs, including the auto-added makeup-root |

## Usage Example

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_beauty \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
    "segment_ids": ["d62994b4-25fe-422a-a123-87ef05038558"],
    "skin": { "smooth": 52, "whitening": 67, "skin_tone": "冷白", "temperature": 11, "intensity": 60 },
    "shape": { "small_face": 19, "slim": 33 },
    "makeup": { "look": "淡人妆", "intensity": 80 },
    "body": { "small_head": 33, "slim_waist": 60, "smooth": 19, "whitening": 26 }
  }'
```

## Error Codes

| Code | Message | Description | Solution |
|------|---------|-------------|----------|
| 1001 | Parameter validation failed | Slider out of range (0-100, temperature 0-99) or an unknown field in a group | Check the request payload |
| 2043 | Invalid beauty information | No effective parameter provided, or an invalid value type | Provide at least one non-zero slider or a valid preset |
| 2044 | Beauty type not found | A reserved field was set to non-zero, an unsupported preset was used, or an unknown key was passed on a direct call | Use a supported name, or pass 0 for reserved fields |
| 2045 | Beauty addition failed | Error while writing the draft | Retry or check the draft state |
| 2001 | Invalid draft URL | draft_url is invalid or the draft is not cached | Create or download the draft first |
| 2015 | Segment not found | segment_id does not exist | Check the segment ID |
| 2016 | Invalid segment type | Target segment is not a video/image segment | Apply only to video-track segments |
| 2042 | Draft lock timeout | Concurrent operation on the same draft | Retry later |

## Notes

1. **Video-track segments only** (video or image); text/audio segments will fail.
2. **0 means "not written"** — matching JianYing's "off" state (material absent). An applied slider can only be changed, not removed yet.
3. **Reserved fields**: `width` (窄脸), `chin_length` (下巴长短), `wide_shoulder` (宽肩) have no material in the JianYing draft format; passing a non-zero value returns 2044 — pass 0.
4. **Duplicate names across groups**: `smooth` and `whitening` under `skin` and `body` are different materials (different resource_ids).
5. **Repeated calls** update intensity in place and keep the material id.
6. **Resources**: the draft only stores resource_ids, no local cache paths; JianYing downloads them on first open.
7. **Hand-drawn face shaping** (`manual_deformations`) is out of scope for this API.

## Workflow

1. Collect and validate all sliders per group (zeros skipped, reserved fields rejected, presets looked up)
2. Validate the draft and segments
3. Write `materials.effects` per segment and attach them to `extra_material_refs`
4. Add one `makeup-root` per segment
5. Save the draft and return the material ids

## Related Interfaces

- [Create Draft](./create_draft.md)
- [Add Videos](./add_videos.md)

---

<div align="right">

📚 **Project Resources**  
**GitHub**: [https://github.com/Hommy-master/capcut-mate](https://github.com/Hommy-master/capcut-mate)  
**Gitee**: [https://gitee.com/taohongmin-gitee/capcut-mate](https://gitee.com/taohongmin-gitee/capcut-mate)

</div>
