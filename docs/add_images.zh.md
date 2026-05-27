# ADD_IMAGES API 接口文档

## 🌐 语言切换
[中文版](./add_images.zh.md) | [English](./add_images.md)

## 接口信息

```
POST /openapi/capcut-mate/v1/add_images
```

## 功能描述

向现有草稿中添加图片。该接口用于在指定的时间段内添加图片素材到剪映草稿中，支持图片的透明度、缩放和位置调整。图片可以用于增强视频的视觉效果，如背景图、水印、装饰图等。

## 更多文档

📖 更多详细文档和教程请访问：[https://docs.jcaigc.cn](https://docs.jcaigc.cn)

## 请求参数

```json
{
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
  "image_infos": "[{\"image_url\":\"https://assets.jcaigc.cn/image1.jpg\",\"start\":0,\"end\":5000000}]",
  "alpha": 1.0,
  "scale_x": 1.0,
  "scale_y": 1.0,
  "transform_x": 0,
  "transform_y": 0
}
```

### 参数说明

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| draft_url | string | ✅ | - | 目标草稿的完整URL |
| image_infos | string | ✅ | - | 图片信息数组的JSON字符串 |
| alpha | number | ❌ | 1.0 | 图片透明度，建议范围[0.0, 1.0] |
| scale_x | number | ❌ | 1.0 | 图片X轴缩放比例 |
| scale_y | number | ❌ | 1.0 | 图片Y轴缩放比例 |
| transform_x | number | ❌ | 0 | X轴位置偏移（像素） |
| transform_y | number | ❌ | 0 | Y轴位置偏移（像素） |

### image_infos 数组结构

| 字段名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| image_url | string | ✅ | - | 图片文件的 URL 地址（须以 `http://` 或 `https://` 开头） |
| start | number | ✅ | - | 图片开始显示时间(微秒) |
| end | number | ✅ | - | 图片结束显示时间(微秒) |
| width | number | ❌ | 草稿画布宽度 | 图片宽度(像素)，可选；未传时不校验，片段尺寸以图片文件为准 |
| height | number | ❌ | 草稿画布高度 | 图片高度(像素)，可选；未传时不校验，片段尺寸以图片文件为准 |
| in_animation | string | ❌ | - | 入场动画名称（可选） |
| out_animation | string | ❌ | - | 出场动画名称（可选） |
| loop_animation | string | ❌ | - | 循环动画名称（可选） |
| in_animation_duration | number | ❌ | - | 入场动画时长(微秒，可选) |
| out_animation_duration | number | ❌ | - | 出场动画时长(微秒，可选) |
| loop_animation_duration | number | ❌ | - | 循环动画单次时长(微秒，可选) |
| transition | string | ❌ | - | 转场效果名称（可选） |
| transition_duration | number | ❌ | 500000 | 转场时长(微秒，可选)，范围 100000～2500000 |

### 参数详解

#### 时间参数

- **start**: 图片在时间轴上的开始时间，单位为微秒（1秒 = 1,000,000微秒）
- **end**: 图片在时间轴上的结束时间，单位为微秒
- **duration**: 图片显示时长 = end - start

#### 透明度参数

- **alpha**: 图片的透明度
  - 1.0 = 完全不透明
  - 0.5 = 半透明
  - 0.0 = 完全透明
  - 建议范围：0.0 - 1.0

#### 缩放参数

- **scale_x**: 图片在X轴方向的缩放比例
  - 1.0 = 原始大小
  - 0.5 = 缩小到一半
  - 2.0 = 放大到两倍

- **scale_y**: 图片在Y轴方向的缩放比例
  - 1.0 = 原始大小
  - 0.5 = 缩小到一半
  - 2.0 = 放大到两倍

#### 位置参数

- **transform_x**: 图片在 X 轴方向的位置偏移，单位为像素
  - 正值向右移动，负值向左移动，以画布中心为原点
  - 实际存储时除以**当前草稿画布宽度**（半画布宽单位）

- **transform_y**: 图片在 Y 轴方向的位置偏移，单位为像素
  - 正值向下移动，负值向上移动，以画布中心为原点
  - 实际存储时除以**当前草稿画布高度**（半画布高单位）

#### 图片信息说明

- **image_url**: 图片的 URL 地址
  - 须以 `http://` 或 `https://` 开头
  - 支持 JPG、PNG 等常见图片格式

- **width / height**（可选）
  - **非必填**；未传时接口可正常添加图片
  - 若显式传入，须为大于 0 的整数
  - 片段在剪映中的显示尺寸主要由**图片文件本身**及 `scale_x` / `scale_y` 控制，与这两项无强绑定

## 响应格式

### 成功响应 (200)

```json
{
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
  "track_id": "video-track-uuid",
  "image_ids": ["image1-uuid", "image2-uuid"],
  "segment_ids": ["segment1-uuid", "segment2-uuid"],
  "segment_infos": [
    {
      "id": "segment1-uuid",
      "start": 0,
      "end": 5000000
    }
  ]
}
```

### 响应字段说明

| 字段名 | 类型 | 说明 |
|--------|------|------|
| draft_url | string | 更新后的草稿URL |
| track_id | string | 视频轨道ID |
| image_ids | array | 图片ID列表 |
| segment_ids | array | 片段ID列表 |
| segment_infos | array | 片段信息列表，包含每个片段的ID、开始时间和结束时间 |

### 错误响应 (4xx/5xx)

```json
{
  "detail": "错误信息描述"
}
```

## 使用示例

### cURL 示例

#### 1. 基本图片添加（最小参数）

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_images \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "image_infos": "[{\"image_url\":\"https://assets.jcaigc.cn/photo1.jpg\",\"start\":0,\"end\":5000000}]"
  }'
```

#### 2. 带透明度的图片

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_images \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "image_infos": "[{\"image_url\":\"https://assets.jcaigc.cn/logo.png\",\"width\":800,\"height\":600,\"start\":1000000,\"end\":6000000}]",
    "alpha": 0.8
  }'
```

#### 3. 带缩放和位置偏移的图片

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_images \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "image_infos": "[{\"image_url\":\"https://assets.jcaigc.cn/watermark.png\",\"width\":300,\"height\":100,\"start\":2000000,\"end\":7000000}]",
    "scale_x": 0.5,
    "scale_y": 0.5,
    "transform_x": 700,
    "transform_y": -400
  }'
```

## 错误码说明

| 错误码 | 错误信息 | 说明 | 解决方案 |
|--------|----------|------|----------|
| 400 | draft_url是必填项 | 缺少草稿URL参数 | 提供有效的draft_url |
| 400 | image_infos是必填项 | 缺少图片信息参数 | 提供有效的image_infos |
| 400 | image_url是必填项 | 图片URL缺失 | 为每个图片提供URL |
| 400 | 图片尺寸无效 | 显式传入的 width 或 height ≤ 0 | 不传宽高即可；若传入须为正整数 |
| 400 | 时间范围无效 | end必须大于start | 确保结束时间大于开始时间 |
| 400 | 透明度无效 | alpha超出建议范围 | 使用0.0-1.0范围内的透明度值 |
| 404 | 草稿不存在 | 指定的草稿URL无效 | 检查草稿URL是否正确 |
| 404 | 图片不存在 | 指定的图片URL无效 | 确认图片URL是否正确 |
| 500 | 图片添加失败 | 内部处理错误 | 联系技术支持 |

## 注意事项

1. **时间单位**: 所有时间参数使用微秒（1秒 = 1,000,000微秒）
2. **必填字段**: `image_infos` 每项至少包含 `image_url`、`start`、`end`
3. **宽高可选**: `width`、`height` 可不传；传入时须为正整数
4. **图片 URL**: 须以 `http://` 或 `https://` 开头
5. **时间范围**: `end` 必须大于 `start`
6. **透明度范围**: `alpha` 建议在 0.0～1.0 范围内
7. **位置参数**: `transform_x` / `transform_y` 单位为像素，内部按**草稿画布宽高**转换为半画布单位
8. **轨道管理**: 系统自动创建视频轨道（图片以 `VideoSegment` 形式添加）
9. **性能考虑**: 避免同时添加大量图片

## 工作流程

1. 验证必填参数（draft_url, image_infos）
2. 检查时间范围的有效性
3. 从缓存中获取草稿
4. 创建视频轨道（图片作为VideoSegment）
5. 创建图像调节设置
6. 创建图片片段
7. 添加片段到轨道
8. 保存草稿
9. 返回图片信息

## 相关接口

- [创建草稿](./create_draft.md)
- [添加视频](./add_videos.md)
- [添加音频](./add_audios.md)
- [添加贴纸](./add_sticker.md)
- [保存草稿](./save_draft.md)
- [生成视频](./gen_video.md)

---

<div align="right">

📚 **项目资源**  
**GitHub**: [https://github.com/Hommy-master/capcut-mate](https://github.com/Hommy-master/capcut-mate)  
**Gitee**: [https://gitee.com/taohongmin-gitee/capcut-mate](https://gitee.com/taohongmin-gitee/capcut-mate)

</div>

### 语言切换
[中文版](./add_images.zh.md) | [English](./add_images.md)