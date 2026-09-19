# ADD_BEAUTY API Documentation

## 🌐 Language Switch
[中文版](./add_beauty.zh.md) | [English](./add_beauty.md)

## Interface Information

```
POST /openapi/capcut-mate/v1/add_beauty
```

## Function Description

Add beauty adjustments to video segments in an existing draft. Beauty is attached to the segment and stored in `materials.effects` with `type=figure`. It is not a separate effect track.

Supported sliders, verified against Jianying drafts: whitening (`美白`), skin smoothing (`磨皮`), and teeth whitening (`白牙`). Applying any slider also adds one `makeup-root` material to that segment. Setting the same slider again updates intensity instead of appending another material.

## More Documentation

📖 For more detailed documentation and tutorials, please visit: [https://docs.jcaigc.cn](https://docs.jcaigc.cn)

## Request Parameters

```json
{
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
  "segment_ids": ["d62994b4-25fe-422a-a123-87ef05038558"],
  "beauty_infos": [
    {"name": "美白", "intensity": 60},
    {"name": "磨皮", "intensity": 20},
    {"name": "白牙", "intensity": 17}
  ]
}
```

### Parameter Description

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| draft_url | string | ✅ | "" | Full URL of the target draft |
| segment_ids | array | ✅ | [] | Video segment IDs to apply beauty to |
| beauty_infos | array | ✅ | [] | Beauty slider list |

### beauty_infos

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | ✅ | Slider name: `美白`, `磨皮`, or `白牙` |
| intensity | number | ✅ | Intensity from 0 to 100, matching the Jianying slider |

Intensity is divided by 100 when written. Whitening and smoothing use the material `value` field. Teeth whitening uses `adjust_params` (`name` is `"1"`) and keeps the top-level `value` at 0.

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
