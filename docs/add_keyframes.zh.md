# ADD_KEYFRAMES API 接口文档

## 🌐 语言切换
[中文版](./add_keyframes.zh.md) | [English](./add_keyframes.md)

## 接口信息

``` 
POST /openapi/capcut-mate/v1/add_keyframes
```

## 功能描述

向现有草稿中添加关键帧。该接口用于在指定的片段上添加关键帧动画，支持多种属性类型的关键帧设置，如位置、缩放、旋转、透明度等。关键帧可以用于创建复杂的动画效果，增强视频的视觉表现力。

## 请求参数

```json
{
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
  "keyframes": "[{\"segment_id\":\"d62994b4-25fe-422a-a123-87ef05038558\",\"property\":\"KFTypePositionX\",\"offset\":5000000,\"value\":-0.1}]"
}
```

### 参数说明

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| draft_url | string | ✅ | - | 目标草稿的完整URL |
| keyframes | string | ✅ | - | 关键帧信息列表的JSON字符串 |

### keyframes 参数详解

#### 基本结构
keyframes 是一个JSON字符串，包含关键帧数组，每个关键帧对象包含以下字段：

| 字段名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| segment_id | string | ✅ | 目标片段的唯一标识ID |
| property | string | ✅ | 动画属性类型，支持的类型见下表 |
| offset | number | ✅ | 关键帧在片段中的时间偏移（微秒绝对时间） |
| value | number | ✅ | 属性在该时间点的值 |

#### offset 参数说明

offset 参数只支持微秒绝对时间格式：
- 以微秒为单位的数值，如 5000000 表示片段开始后5秒的位置
- 系统会自动将微秒值转换为相对时间比例

#### 支持的动画属性类型

| 属性类型 | 描述 | 值范围 | 示例 |
|---------|------|--------|------|
| KFTypePositionX | X轴位置 | -1.0 到 1.0 | 0.0 (居中), -0.5 (左移), 0.5 (右移) |
| KFTypePositionY | Y轴位置 | -1.0 到 1.0 | 0.0 (居中), 0.5 (上移), -0.5 (下移) |
| KFTypeScaleX | X轴缩放 | 0.1 到 10.0 | 1.0 (原始), 0.5 (缩小), 2.0 (放大) |
| KFTypeScaleY | Y轴缩放 | 0.1 到 10.0 | 1.0 (原始), 0.5 (缩小), 2.0 (放大) |
| KFTypeRotation | 旋转角度 | -360 到 360 | 0 (无旋转), 90 (顺时针90度) |
| KFTypeAlpha | 透明度 | 0.0 到 1.0 | 1.0 (不透明), 0.5 (半透明), 0.0 (透明) |
| UNIFORM_SCALE | 统一缩放 | 0.1 到 10.0 | 1.0 (原始), 0.5 (缩小), 2.0 (放大) |
| KFTypeSaturation | 饱和度 | -1.0 到 1.0 | 0.0 (原始), -0.5 (降低), 0.5 (增强) |
| KFTypeContrast | 对比度 | -1.0 到 1.0 | 0.0 (原始), -0.5 (降低), 0.5 (增强) |
| KFTypeBrightness | 亮度 | -1.0 到 1.0 | 0.0 (原始), -0.5 (变暗), 0.5 (变亮) |
| KFTypeVolume | 音量 | 0.0 到 2.0 | 1.0 (原始), 0.5 (降低), 2.0 (增强) |

## 响应格式

### 成功响应 (200)

```json
{
  "code": 0,
  "message": "success",
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
  "keyframes_added": 3,
  "affected_segments": ["segment_001", "segment_002"]
}
```

### 响应字段说明

| 字段名 | 类型 | 说明 |
|--------|------|------|
| draft_url | string | 更新后的草稿URL |
| keyframes_added | integer | 添加的关键帧数量 |
| affected_segments | array | 受影响的片段ID列表 |

### 错误响应

```json
{
  "code": 2013,
  "message": "无效的关键帧信息，请检查keyframes字段值是否正确"
}
```

## 使用示例

### cURL 示例

#### 1. 基本关键帧添加（使用微秒时间）

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_keyframes \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "keyframes": "[{\"segment_id\":\"segment-id\",\"property\":\"UNIFORM_SCALE\",\"offset\":0,\"value\":1},{\"segment_id\":\"segment-id\",\"property\":\"UNIFORM_SCALE\",\"offset\":5000000,\"value\":1.3}]"
  }'
```

#### 2. 多属性关键帧

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_keyframes \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "keyframes": "[{\"segment_id\":\"segment-uuid\",\"property\":\"KFTypePositionX\",\"offset\":0,\"value\":0},{\"segment_id\":\"segment-uuid\",\"property\":\"KFTypePositionY\",\"offset\":0,\"value\":0},{\"segment_id\":\"segment-uuid\",\"property\":\"KFTypeRotation\",\"offset\":2500000,\"value\":90},{\"segment_id\":\"segment-uuid\",\"property\":\"KFTypeAlpha\",\"offset\":5000000,\"value\":0}]"
  }'
```

## 错误码说明

| 错误码 | 错误信息 | 说明 | 解决方案 |
|--------|----------|------|----------|
| 2001 | 无效的草稿URL | 草稿缺失或不在缓存中 | 检查 `draft_url` |
| 2013 | 无效的关键帧信息 | JSON 非法、不是数组、缺少字段、property 不受支持，或 offset/value 类型不正确 | 修正 `keyframes` JSON |
| 2014 | 关键帧添加失败 | 保存草稿失败 | 重试或联系技术支持 |
| 2042 | 草稿锁获取超时 | 另一个写操作正持有草稿锁 | 稍后重试 |

## 注意事项

1. **片段ID验证**: segment_id 必须是草稿中存在的有效片段ID
2. **片段类型限制**: 只有视觉片段（视频、图片、贴纸、文本）支持关键帧
3. **时间偏移范围**: offset 值必须是非负数（微秒）
4. **属性值范围**: 不同的属性类型有不同的值范围限制
5. **重复关键帧**: 相同片段相同属性的关键帧会被累加，不会覆盖
6. **性能考虑**: 单次请求建议不超过100个关键帧
7. **缩放属性**: 设置KFTypeScaleX或KFTypeScaleY会自动取消锁定XY轴缩放比例

## 工作流程

1. 验证必填参数（draft_url, keyframes）
2. 解析关键帧数据JSON字符串
3. 从缓存中获取草稿
4. 验证每个关键帧数据的有效性
5. 查找目标片段并验证片段类型
6. 为每个关键帧创建关键帧列表并添加到片段
7. 保存草稿
8. 返回添加结果信息

## 相关接口

- [创建草稿](./create_draft.md)
- [添加视频](./add_videos.md)
- [添加音频](./add_audios.md)
- [添加图片](./add_images.md)
- [保存草稿](./save_draft.md)
- [生成视频](./gen_video.md)

---

<div align="right">

📚 **项目资源**  
**GitHub**: [https://github.com/Hommy-master/capcut-mate](https://github.com/Hommy-master/capcut-mate)  
**Gitee**: [https://gitee.com/taohongmin-gitee/capcut-mate](https://gitee.com/taohongmin-gitee/capcut-mate)

</div>