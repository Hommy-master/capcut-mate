# KEYFRAMES_INFOS API 接口文档

## 🌐 语言切换
[中文版](./keyframes_infos.zh.md) | [English](./keyframes_infos.md)

## 接口信息

```
POST /openapi/capcut-mate/v1/keyframes_infos
```

## 功能描述

根据关键帧类型、位置比例和值生成关键帧信息。该接口将关键帧配置转换为剪映草稿所需的关键帧信息格式。

## 更多文档

📖 更多详细文档和教程请访问：[https://docs.jcaigc.cn](https://docs.jcaigc.cn)

## 请求参数

```json
{
  "ctype": "KFTypePositionX",
  "offsets": "0|50|100",
  "values": "0|960|1920",
  "segment_infos": [
    {"id": "segment1", "start": 0, "end": 5000000}
  ],
  "height": 1080,
  "width": 1920
}
```

### 参数说明

| 参数名 | 类型 |必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| ctype | string |✅ | - |关键帧类型：`KFTypePositionX`（X轴移动，需要 `width`）、`KFTypePositionY`（Y轴移动，需要 `height`）、`KFTypeRotation`（0-360）、`UNIFORM_SCALE`（0.01-5）、`KFTypeAlpha`（0-1） |
| offsets | string |✅ | - | 位置比例，用 `\|` 分隔，如 `"0\|100"`（开头和结尾）、`"0\|50\|100"`（开头、中间、结尾） |
| values | string |✅ | - | 对应 offsets 的值，用 `\|` 分隔，元素个数须与 offsets 一致，如 `"1\|2"`、`"1\|2\|1"` |
| segment_infos | array[object] |✅ | - |轨道数据（片段对象数组），每项含 `id`、`start`、`end`（微秒） |
| height | integer |❌ | None |高度，用于 `KFTypePositionY` 值的归一化 |
| width | integer |❌ | None |宽，用于 `KFTypePositionX` 值的归一化 |



##响应格式

### 成功响应 (200)

```json
{
  "code": 0,
  "message": "success",
  "keyframes_infos": "[{\"offset\":0,\"property\":\"KFTypePositionX\",\"segment_id\":\"segment1\",\"value\":0.0},{\"offset\":2500000,\"property\":\"KFTypePositionX\",\"segment_id\":\"segment1\",\"value\":0.5},{\"offset\":5000000,\"property\":\"KFTypePositionX\",\"segment_id\":\"segment1\",\"value\":1.0}]"
}
```

###响应字段说明

| 字段名 | 类型 | 说明 |
|--------|------|------|
| keyframes_infos | string |关键帧信息JSON字符串 |

### 错误响应

```json
{
  "code": 1001,
  "message": "参数校验失败"
}
```

## 使用示例

### cURL 示例

#### 1.基本关键帧信息生成

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/keyframes_infos \
  -H "Content-Type: application/json" \
  -d '{
    "ctype": "UNIFORM_SCALE",
    "offsets": "0|100",
    "values": "0.5|1.5",
    "segment_infos": [{"id": "segment1", "start": 0, "end": 5000000}]
  }'
```

#### 2.位置关键帧信息

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/keyframes_infos \
  -H "Content-Type: application/json" \
  -d '{
    "ctype": "KFTypePositionX",
    "offsets": "0|30|70|100",
    "values": "0|384|1536|1920",
    "segment_infos": [{"id": "segment1", "start": 0, "end": 10000000}],
    "height": 1080,
    "width": 1920
  }'
```

##错误码说明

|错误码 | 错误信息 | 说明 | 解决方案 |
|--------|----------|------|----------|
| 1001 | 参数校验失败 | 请求体未通过字段校验（缺少 `ctype`/`offsets`/`values`/`segment_infos`，或 `offsets`/`values` 不是字符串） | 检查参数类型与必填字段 |
| 9998 | 系统内部错误 | `offsets` 与 `values` 用 `\|` 分隔的元素个数不一致 | 保证 `offsets` 与 `values` 的元素个数一致 |

## 注意事项

1. **元素数量匹配**: offsets和values用 `|` 分隔的元素个数必须相同
2. **时间单位**:所有时间参数使用微秒（1秒 = 1,000,000微秒）
3. **关键帧类型**:支持 KFTypePositionX、KFTypePositionY、KFTypeRotation、UNIFORM_SCALE、KFTypeAlpha
4. **位置比例**: offsets值为 0-100 的百分比，关键帧的 offset 相对片段起点计算
5. **分辨率设置**: KFTypePositionX/KFTypePositionY 的值会除以 width/height 进行归一化

##工作流程

1.验证必填参数（ctype, offsets, values, segment_infos）
2. 检查 offsets 与 values 的元素个数是否一致
3.验证参数有效性
4. 为每个offset生成对应的关键帧信息
5.应用分辨率参数
6.将信息转换为JSON字符串格式
7. 返回处理结果

##相关接口

- [创建草稿](./create_draft.md)
- [添加关键帧](./add_keyframes.md)
- [保存草稿](./save_draft.md)

---

<div align="right">

📚 **项目资源**  
**GitHub**: [https://github.com/Hommy-master/capcut-mate](https://github.com/Hommy-master/capcut-mate)  
**Gitee**: [https://gitee.com/taohongmin-gitee/capcut-mate](https://gitee.com/taohongmin-gitee/capcut-mate)

</div>

### 语言切换
[中文版](./keyframes_infos.zh.md) | [English](./keyframes_infos.md)