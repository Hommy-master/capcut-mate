# ADD_MASKS API 接口文档

## 🌐 语言切换
[中文版](./add_audios.zh.md) | [English](./add_audios.md)

## 接口信息

```
POST /openapi/capcut-mate/v1/add_masks
```

## 功能描述

向现有草稿中的指定片段添加遮罩效果。遮罩是视频编辑中的重要功能，通过遮罩可以控制图像的可见区域，创造出各种视觉效果。支持多种遮罩类型（线性、镜面、圆形、矩形、爱心、星形），每种遮罩都可以精确配置位置、大小、羽化、旋转等属性。

## 更多文档

📖 更多详细文档和教程请访问：[https://docs.jcaigc.cn](https://docs.jcaigc.cn)

## 请求参数

```json
{
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
  "segment_ids": ["d62994b4-25fe-422a-a123-87ef05038558"],
  "name": "圆形",
  "X": 100,
  "Y": 200,
  "width": 300,
  "height": 300,
  "feather": 20,
  "rotation": 0,
  "invert": false,
  "roundCorner": 0
}
```

### 参数说明

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| draft_url | string | ✅ | "" | 目标草稿的完整URL |
| segment_ids | array | ✅ | [] | 要应用遮罩的片段ID数组 |
| name | string | ❌ | "线性" | 遮罩类型名称 |
| X | integer | ❌ | 0 | 遮罩中心X坐标（像素） |
| Y | integer | ❌ | 0 | 遮罩中心Y坐标（像素） |
| width | integer | ❌ | 512 | 遮罩宽度（像素） |
| height | integer | ❌ | 512 | 遮罩高度（像素） |
| feather | integer | ❌ | 0 | 羽化程度（0-100） |
| rotation | integer | ❌ | 0 | 旋转角度（度） |
| invert | boolean | ❌ | false | 是否反转遮罩 |
| roundCorner | integer | ❌ | 0 | 圆角半径（0-100） |

### 参数详解

#### 遮罩类型参数

- **name**: 遮罩类型名称
  - 可选值：线性、镜面、圆形、矩形、爱心、星形
  - 默认值：线性

#### 位置参数

- **X**: 遮罩中心X坐标（像素）
  - 正值向右移动
  - 负值向左移动
  - 以素材中心为原点

- **Y**: 遮罩中心Y坐标（像素）
  - 正值向下移动
  - 负值向上移动
  - 以素材中心为原点

#### 尺寸参数

- **width**: 遮罩宽度（像素）
  - 默认值：512
  - 建议范围：1-2048

- **height**: 遮罩高度（像素）
  - 默认值：512
  - 建议范围：1-2048

#### 效果参数

- **feather**: 羽化程度（0-100）
  - 0 = 无羽化（锐利边缘）
  - 100 = 最大羽化（柔和边缘）
  - 默认值：0

- **rotation**: 旋转角度（度）
  - 0-360度范围
  - 默认值：0

- **invert**: 是否反转遮罩
  - true = 反转遮罩效果
  - false = 正常遮罩效果
  - 默认值：false

- **roundCorner**: 圆角半径（0-100）
  - 仅对矩形遮罩有效
  - 0 = 无圆角（直角）
  - 100 = 最大圆角
  - 默认值：0

#### 片段ID参数

- **segment_ids**: 要应用遮罩的片段ID数组
  - 必须是视频片段ID
  - 支持批量处理多个片段
  - 每个片段只能添加一个遮罩

## 响应格式

### 成功响应 (200)

```json
{
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
  "masks_added": 1,
  "affected_segments": ["d62994b4-25fe-422a-a123-87ef05038558"],
  "mask_ids": ["mask_001"]
}
```

### 响应字段说明

| 字段名 | 类型 | 说明 |
|--------|------|------|
| draft_url | string | 更新后的草稿URL |
| masks_added | number | 成功添加的遮罩数量 |
| affected_segments | array | 受影响的片段ID列表 |
| mask_ids | array | 遮罩ID列表 |

### 错误响应 (4xx/5xx)

```json
{
  "detail": "错误信息描述"
}
```

## 使用示例

### cURL 示例

#### 1. 基本遮罩添加

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_masks \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "segment_ids": ["SEGMENT_ID"],
    "name": "圆形"
  }'
```

#### 2. 带位置和尺寸的遮罩

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_masks \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "segment_ids": ["SEGMENT_ID"],
    "name": "矩形",
    "X": 100,
    "Y": 50,
    "width": 400,
    "height": 300
  }'
```

#### 3. 带效果参数的遮罩

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_masks \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "segment_ids": ["SEGMENT_ID"],
    "name": "线性",
    "feather": 30,
    "rotation": 45,
    "invert": true
  }'
```

#### 4. 矩形遮罩带圆角

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/add_masks \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL",
    "segment_ids": ["SEGMENT_ID"],
    "name": "矩形",
    "roundCorner": 50
  }'
```

## 错误码说明

| 错误码 | 错误信息 | 说明 | 解决方案 |
|--------|----------|------|----------|
| 400 | draft_url是必填项 | 缺少草稿URL参数 | 提供有效的draft_url |
| 400 | segment_ids是必填项 | 缺少片段ID参数 | 提供有效的segment_ids数组 |
| 400 | 无效的遮罩信息，请检查遮罩参数是否正确 | 遮罩参数校验失败 | 检查遮罩参数是否符合要求 |
| 400 | 羽化程度无效 | feather超出范围 | 使用0-100范围内的羽化值 |
| 400 | 旋转角度无效 | rotation超出范围 | 使用0-360范围内的角度值 |
| 400 | 圆角半径无效 | roundCorner超出范围 | 使用0-100范围内的圆角值 |
| 404 | 草稿不存在 | 指定的草稿URL无效 | 检查草稿URL是否正确 |
| 404 | 片段未找到 | 指定的片段ID不存在 | 确认片段ID是否正确 |
| 400 | 无效的片段类型 | 片段类型不支持添加遮罩 | 确保使用视频片段ID |
| 404 | 遮罩类型未找到 | 指定的遮罩名称不存在 | 使用有效的遮罩类型名称 |
| 500 | 遮罩添加失败 | 内部处理错误 | 联系技术支持 |

## 注意事项

1. **片段要求**: 只有视频片段（VideoSegment）支持添加遮罩
2. **遮罩限制**: 每个片段只能添加一个遮罩，重复添加不会报错，会返回现有遮罩信息
3. **坐标系统**: X、Y坐标以像素为单位，原点位于素材中心
4. **参数范围**: 
   - feather: 0-100，羽化程度
   - rotation: 0-360度，旋转角度
   - roundCorner: 0-100，圆角半径（仅矩形遮罩有效）
5. **批量处理**: 支持同时为多个片段添加相同配置的遮罩
6. **遮罩类型**: 支持线性、镜面、圆形、矩形、爱心、星形六种遮罩类型
7. **性能考虑**: 避免同时添加大量遮罩

## 工作流程

1. 验证必填参数（draft_url, segment_ids）
2. 检查片段ID的有效性
3. 从缓存中获取草稿
4. 查找并验证遮罩类型
5. 为每个片段添加遮罩
6. 保存草稿
7. 返回遮罩信息

## 相关接口

- [创建草稿](./create_draft.md)
- [添加视频](./add_videos.md)
- [添加音频](./add_audios.md)
- [添加图片](./add_images.md)
- [添加蒙版关键帧](./add_mask_keyframes.zh.md)
- [保存草稿](./save_draft.md)
- [生成视频](./gen_video.md)

---

<div align="right">

📚 **项目资源**  
**GitHub**: [https://github.com/Hommy-master/capcut-mate](https://github.com/Hommy-master/capcut-mate)  
**Gitee**: [https://gitee.com/taohongmin-gitee/capcut-mate](https://gitee.com/taohongmin-gitee/capcut-mate)

</div>