# CREATE_DRAFT API Documentation

### 🌐 Language Switch
[中文版](./create_draft.zh.md) | [English](./create_draft.md)

## Interface Information

```
POST /openapi/capcut-mate/v1/create_draft
```

## Function Description

Create a Jianying draft. This interface is used to create a new Jianying draft project, allowing customization of video width and height. After successful creation, it returns the draft URL and help document URL, providing the foundation for subsequent video editing operations.

## More Documentation

📖 For more detailed documentation and tutorials, please visit: [https://docs.jcaigc.cn](https://docs.jcaigc.cn)

## Request Parameters

```json
{
  "width": 1920,
  "height": 1080
}
```

### Parameter Description

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| width | number | ❌ | 1920 | Video width (pixels), must be greater than or equal to 1 |
| height | number | ❌ | 1080 | Video height (pixels), must be greater than or equal to 1 |

### Parameter Details

#### Size Parameters

- **width**: Width of the draft video
  - Minimum: 1 pixel
  - Recommended common values: 1920, 1280, 720
  - Supports custom sizes

- **height**: Height of the draft video
  - Minimum: 1 pixel
  - Recommended common values: 1080, 720, 480
  - Supports custom sizes

#### Common Resolutions

| Resolution Name | Width | Height | Application Scenario |
|-----------------|-------|--------|---------------------|
| 1080P | 1920 | 1080 | HD video production |
| 720P | 1280 | 720 | SD video production |
| 4K | 3840 | 2160 | Ultra HD video production |
| Vertical Short Video | 1080 | 1920 | Mobile short videos |
| Square | 1080 | 1080 | Social media content |

## Response Format

### Success Response (200)

```json
{
  "draft_url": "https://cm.jcaigc.cn/openapi/v1/get_draft?draft_id=2025092811473036584258",
  "tip_url": "https://help.assets.jcaigc.cn/draft-usage"
}
```

### Response Field Description

| Field | Type | Description |
|-------|------|-------------|
| draft_url | string | Newly created draft URL, used for subsequent editing operations |
| tip_url | string | Draft usage help documentation URL |

### Error Response (4xx/5xx)

```json
{
  "detail": "Error message description"
}
```

## 💻 Usage Examples

### cURL Examples

#### 1. Create Draft with Default Resolution

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/create_draft \
  -H "Content-Type: application/json" \
  -d '{}'
```

#### 2. Create Draft with Custom Resolution

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/create_draft \
  -H "Content-Type: application/json" \
  -d '{
    "width": 1280,
    "height": 720
  }'
```

#### 3. Create Vertical Short Video Draft

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/create_draft \
  -H "Content-Type: application/json" \
  -d '{
    "width": 1080,
    "height": 1920
  }'
```


## Error Code Description

| Error Code | Error Message | Description | Solution |
|------------|---------------|-------------|----------|
| 400 | width must be greater than or equal to 1 | Invalid width parameter | Provide a width value greater than or equal to 1 |
| 400 | height must be greater than or equal to 1 | Invalid height parameter | Provide a height value greater than or equal to 1 |
| 400 | Parameter type error | Parameter type is incorrect | Ensure width and height are numeric types |
| 500 | Draft creation failed | Internal service error | Contact technical support |
| 503 | Service unavailable | System maintenance | Retry later |

## Notes

1. **Parameter Validation**: width and height must be positive integers
2. **Resolution Recommendation**: Suggest using common video resolutions to ensure compatibility
3. **Performance Consideration**: Ultra-high resolution may affect subsequent processing performance
4. **Storage Usage**: High-resolution drafts will occupy more storage space
5. **URL Validity**: The returned draft_url has a certain validity period

## Workflow

1. Receive and validate request parameters
2. Create draft basic structure
3. Set canvas size
4. Generate draft URL
5. Return draft information and help document link

## Related Interfaces

- [Add Videos](./add_videos.md)
- [Add Audios](./add_audios.md)
- [Add Images](./add_images.md)
- [Save Draft](./save_draft.md)
- [Generate Video](./gen_video.md)

---

<div align="right">

📚 **Project Resources**  
**GitHub**: [https://github.com/Hommy-master/capcut-mate](https://github.com/Hommy-master/capcut-mate)  
**Gitee**: [https://gitee.com/taohongmin-gitee/capcut-mate](https://gitee.com/taohongmin-gitee/capcut-mate)

</div>

---