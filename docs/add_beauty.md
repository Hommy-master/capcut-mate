# ADD_BEAUTY API Documentation

## 🌐 Language Switch
[中文版](./add_beauty.zh.md) | [English](./add_beauty.md)

## Interface Information

```
POST /openapi/capcut-mate/v1/add_beauty
```

## Function Description

Add beauty adjustments to video segments in an existing draft. Beauty is attached to the segment and stored in `materials.effects` with `type=figure`. It is not a separate effect track.

The 10 parameters from Jianying's beauty panel are supported: even skin (`匀肤`), plump (`丰盈`), smoothing (`磨皮`), nasolabial folds (`祛法令纹`), bright eyes (`亮眼`), dark circles (`祛黑眼圈`), whitening (`美白`), teeth (`白牙`), skin tone (`肤色`), and skin-tone intensity (`肤色强度`). Each parameter has a default. A slider value of 0 or an empty skin tone is not written. Applying any slider also adds one `makeup-root` material. Setting the same slider again updates intensity instead of appending another material.

## More Documentation

📖 For more detailed documentation and tutorials, please visit: [https://docs.jcaigc.cn](https://docs.jcaigc.cn)

## Request Parameters

```json
{
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
  "segment_ids": ["d62994b4-25fe-422a-a123-87ef05038558"],
  "匀肤": 100,
  "丰盈": 100,
  "磨皮": 100,
  "祛法令纹": 100,
  "亮眼": 100,
  "祛黑眼圈": 100,
  "美白": 60,
  "白牙": 100,
  "肤色": "暖白",
  "肤色强度": 60
}
```

### Parameter Description

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| draft_url | string | ✅ | "" | Full URL of the target draft |
| segment_ids | array | ✅ | [] | Video segment IDs to apply beauty to |
| 匀肤 | number | ❌ | 0 | Even-skin intensity, 0–100 |
| 丰盈 | number | ❌ | 0 | Plump intensity, 0–100 |
| 磨皮 | number | ❌ | 0 | Smoothing intensity, 0–100 |
| 祛法令纹 | number | ❌ | 0 | Nasolabial-fold intensity, 0–100 |
| 亮眼 | number | ❌ | 0 | Bright-eye intensity, 0–100 |
| 祛黑眼圈 | number | ❌ | 0 | Dark-circle intensity, 0–100 |
| 美白 | number | ❌ | 0 | Whitening intensity, 0–100 |
| 白牙 | number | ❌ | 0 | Teeth-whitening intensity, 0–100 |
| 肤色 | string | ❌ | "" | Skin-tone preset; empty means off. Currently `暖白` |
| 肤色强度 | number | ❌ | 60 | Skin-tone intensity, 0–100; used only when `肤色` is set |
| beauty_infos | array | ❌ | [] | Legacy slider list; can be combined with the named fields |

### beauty_infos

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| name | string | ✅ | - | Slider name: `匀肤`, `丰盈`, `磨皮`, `祛法令纹`, `亮眼`, `祛黑眼圈`, `美白`, `白牙`, `肤色`/`暖白` |
| intensity | number | ❌ | 0 | Intensity from 0 to 100, matching the Jianying slider |

Intensity is divided by 100 when written. Whitening and smoothing use the material `value` field. Even skin, plump, nasolabial folds, bright eyes, and dark circles use `adjust_params` (`name` is `"0"`). Teeth whitening uses `adjust_params` (`name` is `"1"`). Skin tone is written to `face_adjust_params` and exported as `暖白`.

## Response

```json
{
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
  "affected_segments": ["d62994b4-25fe-422a-a123-87ef05038558"],
  "figure_ids": ["figure-id-1", "makeup-root-id"]
}
```

| Field | Type | Description |
|-------|------|-------------|
| draft_url | string | Draft URL |
| affected_segments | array | Segment IDs that received beauty |
| figure_ids | array | Figure material IDs, including the auto-added makeup-root |

## Notes

- Only segments on a video track are supported (video or image). Captions, audio, and other segment types are rejected.
- Sliders that were not verified in a Jianying draft (face slim, eye enlarge, and so on) are rejected.
- The draft stores `resource_id` and does not embed a local effect-cache path. Jianying downloads the package when the draft is opened.
- Named parameters at 0 (or an empty skin tone) are not written. At least one non-default beauty parameter or `beauty_infos` item is required.
