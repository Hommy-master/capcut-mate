# FILTER_INFOS API 接口文档

## 🌐 语言切换
[中文版](./filter_infos.zh.md) | [English](./filter_infos.md)

## 接口信息

```
POST /openapi/capcut-mate/v1/filter_infos
```

## 功能描述

根据滤镜名称、时间线和强度生成滤镜信息。该接口将滤镜名称和时间线配置转换为剪映草稿所需的滤镜信息格式。

## 更多文档

📖 更多详细文档和教程请访问：[https://docs.jcaigc.cn](https://docs.jcaigc.cn)

## 请求参数

```json
{
  "filters": ["复古", "黑白"],
  "timelines": [
    {"start": 0, "end": 3000000},
    {"start": 3000000, "end": 6000000}
  ],
  "intensities": [80, 100]
}
```

### 参数说明

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| filters | array[string] | ✅ | - | 滤镜名称数组 |
| timelines | array[object] | ✅ | - | 时间线配置数组 |
| intensities | array[number] | ❌ | 100 | 滤镜强度数组(0-100)，可选，默认全部为100 |

## 响应格式

### 成功响应 (200)

```json
{
  "infos": "[{\"filter_title\":\"复古\",\"start\":0,\"end\":3000000,\"intensity\":80},{\"filter_title\":\"黑白\",\"start\":3000000,\"end\":6000000,\"intensity\":100}]"
}
```

### 响应字段说明

| 字段名 | 类型 | 说明 |
|--------|------|------|
| infos | string | 滤镜信息JSON字符串 |

### 错误响应 (4xx/5xx)

```json
{
  "detail": "错误信息描述"
}
```

## 使用示例

### cURL 示例

#### 1. 基本滤镜信息生成

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/filter_infos \
  -H "Content-Type: application/json" \
  -d '{
    "filters": ["复古"],
    "timelines": [{"start": 0, "end": 5000000}]
  }'
```

#### 2. 自定义强度的滤镜信息生成

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/filter_infos \
  -H "Content-Type: application/json" \
  -d '{
    "filters": ["黑白"],
    "timelines": [{"start": 0, "end": 5000000}],
    "intensities": [60]
  }'
```

#### 3. 多滤镜信息生成

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/filter_infos \
  -H "Content-Type: application/json" \
  -d '{
    "filters": ["复古", "黑白", "电影感"],
    "timelines": [{"start": 0, "end": 2000000}, {"start": 2000000, "end": 4000000}, {"start": 4000000, "end": 6000000}],
    "intensities": [80, 100, 90]
  }'
```

## 错误码说明

| 错误码 | 错误信息 | 说明 | 解决方案 |
|--------|----------|------|----------|
| 400 | filters是必填项 | 缺少滤镜名称参数 | 提供有效的滤镜名称数组 |
| 400 | timelines是必填项 | 缺少时间线参数 | 提供有效的时间线数组 |
| 400 | 数组长度不匹配 | filters、timelines、intensities长度不一致 | 确保所有数组长度相同 |
| 400 | 强度范围无效 | intensity必须在0-100之间 | 提供有效的强度值 |
| 500 | 滤镜信息生成失败 | 内部处理错误 | 联系技术支持 |

## 注意事项

1. **数组匹配**: filters和timelines数组长度必须相同；如果提供intensities，长度也应相同
2. **时间单位**: 所有时间参数使用微秒（1秒 = 1,000,000微秒）
3. **滤镜名称**: 需要使用系统支持的滤镜名称
4. **强度范围**: 强度值必须在0-100之间，默认为100
5. **连续性**: 滤镜按时间线顺序应用

## 工作流程

1. 验证必填参数（filters, timelines）
2. 检查数组长度匹配
3. 验证时间线参数有效性
4. 验证强度范围（如果提供）
5. 为每个滤镜名称生成对应的滤镜信息
6. 将信息转换为JSON字符串格式
7. 返回处理结果

## 相关接口

- [创建草稿](./create_draft.md)
- [添加滤镜](./add_filters.md)
- [时间线](./timelines.md)
- [保存草稿](./save_draft.md)

---

<div align="right">

📚 **项目资源**  
**GitHub**: [https://github.com/Hommy-master/capcut-mate](https://github.com/Hommy-master/capcut-mate)  
**Gitee**: [https://gitee.com/taohongmin-gitee/capcut-mate](https://gitee.com/taohongmin-gitee/capcut-mate)

</div>

### 语言切换
[中文版](./filter_infos.zh.md) | [English](./filter_infos.md)
