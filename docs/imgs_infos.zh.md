# IMGS_INFOS API 接口文档

## 🌐 语言切换
[中文版](./imgs_infos.zh.md) | [English](./imgs_infos.md)

## 接口信息

```
POST /openapi/capcut-mate/v1/imgs_infos
```

## 功能描述

根据图片URL和时间线生成图片信息。该接口将图片文件URL和时间线配置转换为剪映草稿所需的图片信息格式，支持动画效果和转场设置。

## 请求参数

```json
{
  "imgs": ["https://assets.jcaigc.cn/img1.jpg", "https://assets.jcaigc.cn/img2.png"],
  "timelines": [
    {"start": 0, "end": 3000000},
    {"start": 3000000, "end": 6000000}
  ],
  "height": 1080,
  "width": 1920,
  "in_animation": "渐显",
  "in_animation_duration": 500000,
  "loop_animation": "动感摇晃I",
  "loop_animation_duration": 1000000,
  "out_animation": "渐隐",
  "out_animation_duration": 500000,
  "transition": "叠化",
  "transition_duration": 300000
}
```

### 参数说明

| 参数名 | 类型 |必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| imgs | array[string] |✅ | - | 图片文件URL数组 |
| timelines | array[object] |✅ | - | 时间线配置数组 |
| height | integer |❌ | None |图片高度 |
| width | integer |❌ | None |图片宽度 |
| in_animation | string |❌ | None |入场动画名称，可用值见 [add_images](./add_images.zh.md) |
| in_animation_duration | integer |❌ | None |入场动画时长(微秒) |
| loop_animation | string |❌ | None |循环动画名称，可用值见 [add_images](./add_images.zh.md) |
| loop_animation_duration | integer |❌ | None |循环动画时长(微秒) |
| out_animation | string |❌ | None |出场动画名称，可用值见 [add_images](./add_images.zh.md) |
| out_animation_duration | integer |❌ | None |出场动画时长(微秒) |
| transition | string |❌ | None |转场名称，可用值见 [add_images](./add_images.zh.md) / [add_videos](./add_videos.zh.md) |
| transition_duration | integer |❌ | None |转场时长(微秒) |

### 可用转场与动画名称

转场、入场/出场/循环动画的完整可用值清单，请参见 [添加图片（add_images）](./add_images.zh.md) 文档中的「支持的转场与动画名称」。

##响应格式

### 成功响应 (200)

```json
{
  "code": 0,
  "message": "success",
  "infos": "[{\"image_url\":\"https://assets.jcaigc.cn/img1.jpg\",\"start\":0,\"end\":3000000,\"height\":1080,\"width\":1920,\"in_animation\":\"渐显\",\"in_animation_duration\":500000,\"out_animation\":\"渐隐\",\"out_animation_duration\":500000,\"loop_animation\":\"动感摇晃I\",\"loop_animation_duration\":1000000,\"transition\":\"叠化\",\"transition_duration\":300000},{\"image_url\":\"https://assets.jcaigc.cn/img2.png\",\"start\":3000000,\"end\":6000000,\"height\":1080,\"width\":1920,\"in_animation\":\"渐显\",\"in_animation_duration\":500000,\"out_animation\":\"渐隐\",\"out_animation_duration\":500000,\"loop_animation\":\"动感摇晃I\",\"loop_animation_duration\":1000000,\"transition\":\"叠化\",\"transition_duration\":300000}]"
}
```

###响应字段说明

| 字段名 | 类型 | 说明 |
|--------|------|------|
| infos | string | 图片信息JSON字符串 |

### 错误响应

```json
{
  "code": 1001,
  "message": "参数校验失败"
}
```

## 使用示例

### cURL 示例

#### 1.基本图片信息生成

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/imgs_infos \
  -H "Content-Type: application/json" \
  -d '{
    "imgs": ["https://assets.jcaigc.cn/cover.jpg"],
    "timelines": [{"start": 0, "end": 5000000}],
    "height": 1080,
    "width": 1920
  }'
```

#### 2.带动画效果的图片信息

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/imgs_infos \
  -H "Content-Type: application/json" \
  -d '{
    "imgs": ["https://assets.jcaigc.cn/slide1.jpg", "https://assets.jcaigc.cn/slide2.jpg"],
    "timelines": [{"start": 0, "end": 3000000}, {"start": 3000000, "end": 6000000}],
    "in_animation": "渐显",
    "loop_animation": "动感摇晃I",
    "out_animation": "渐隐",
    "transition": "叠化"
  }'
```

##错误码说明

|错误码 | 错误信息 | 说明 | 解决方案 |
|--------|----------|------|----------|
| 1001 | 参数校验失败 | 请求体未通过字段校验（缺少 `imgs`/`timelines`、时间线项缺少 `start`/`end`，或类型错误） | 检查参数类型与必填字段 |

## 注意事项

1. **数组匹配**: `imgs` 与 `timelines` 长度不一致时，按较短长度截断后继续生成（不会直接报错）
2. **时间单位**:所有时间参数使用微秒（1秒 = 1,000,000微秒）
3. **分辨率设置**: height和width参数用于设置图片显示分辨率
4. **动画效果**:支持入动画、循环动画、出动画和转场效果
5. **网络访问**: 图片URL必须可以正常访问
6. **格式支持**:支持常见的图片格式（JPG、PNG、GIF等）

##工作流程

1.验证必填参数（imgs, timelines）
2.按较短长度对齐两个数组
3.验证时间线参数有效性
4. 设置图片分辨率参数
5.应用动画效果参数
6.为每图片URL生成对应的图片信息
7.将信息转换为JSON字符串格式
8.返回处理结果

##相关接口

- [创建草稿](./create_draft.md)
- [添加图片](./add_images.md)
- [时间线](./timelines.md)
- [保存草稿](./save_draft.md)

---

<div align="right">

📚 **项目资源**  
**GitHub**: [https://github.com/Hommy-master/capcut-mate](https://github.com/Hommy-master/capcut-mate)  
**Gitee**: [https://gitee.com/taohongmin-gitee/capcut-mate](https://gitee.com/taohongmin-gitee/capcut-mate)

</div>

### 语言切换
[中文版](./imgs_infos.zh.md) | [English](./imgs_infos.md)