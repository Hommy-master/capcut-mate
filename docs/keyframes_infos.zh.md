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
  "ctype": "position",
  "offsets": [0.0, 0.5, 1.0],
  "values": [0.0, 0.5, 1.0],
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
| ctype | string |✅ | - |关键帧类型 |
| offsets | array[number] |✅ | - | 位置比例数组 |
| values | array[number] |✅ | - |值数组 |
| segment_infos | array[object] |✅ | - |片信息数组 |
| height | number |❌ | 1080 |高度 |
| width | number |❌ | 1920 |宽 |



##响应格式

### 成功响应 (200)

```json
{
  "keyframes_infos": "[{\"ctype\":\"position\",\"offset\":0.0,\"value\":0.0,\"segment_id\":\"segment1\",\"height\":1080,\"width\":1920},{\"ctype\":\"position\",\"offset\":0.5,\"value\":0.5,\"segment_id\":\"segment1\",\"height\":1080,\"width\":1920},{\"ctype\":\"position\",\"offset\":1.0,\"value\":1.0,\"segment_id\":\"segment1\",\"height\":1080,\"width\":1920}]"
}
```

###响应字段说明

| 字段名 | 类型 | 说明 |
|--------|------|------|
| keyframes_infos | string |关键帧信息JSON字符串 |

###错误响应 (4xx/5xx)

```json
{
  "detail": "错误信息描述"
}
```

## 使用示例

### cURL 示例

#### 1.基本关键帧信息生成

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/keyframes_infos \
  -H "Content-Type: application/json" \
  -d '{
    "ctype": "scale",
    "offsets": [0.0, 1.0],
    "values": [0.5, 1.5],
    "segment_infos": [{"id": "segment1", "start": 0, "end": 5000000}]
  }'
```

#### 2.位置关键帧信息

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/keyframes_infos \
  -H "Content-Type: application/json" \
  -d '{
    "ctype": "position",
    "offsets": [0.0, 0.3, 0.7, 1.0],
    "values": [0.0, 0.2, 0.8, 1.0],
    "segment_infos": [{"id": "segment1", "start": 0, "end": 10000000}],
    "height": 1080,
    "width": 1920
  }'
```

##错误码说明

|错误码 | 错误信息 | 说明 | 解决方案 |
|--------|----------|------|----------|
| 400 | ctype是必填项 |缺少关键帧类型参数 | 提供有效的关键帧类型 |
| 400 | offsets是必填项 |缺少位置比例参数 | 提供有效的位置比例数组 |
| 400 | values是必填项 |缺少值参数 | 提供有效的值数组 |
| 400 | segment_infos是必填项 |缺少片段信息参数 | 提供有效的片段信息数组 |
| 400 | 数组长度不匹配 | offsets和values长度不一致 |确保两个数组长度相同 |
| 500 |关键帧信息生成失败 |内部处理错误 |联技术支持 |

## 注意事项

1. **数组匹配**: offsets和values数组长度必须相同
2. **时间单位**:所有时间参数使用微秒（1秒 = 1,000,000微秒）
3. **关键帧类型**:支持position、scale、rotation等类型
4. **位置比例**: offsets值应在0.0-1.0范围内
5. **分辨率设置**: height和width参数用于设置坐标系

##工作流程

1.验证必填参数（ctype, offsets, values, segment_infos）
2. 检查数组长度匹配
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