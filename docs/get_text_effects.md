# 获取花字效果列表 API 文档

## 📖 接口说明

获取所有支持的花字效果列表，支持按 VIP/免费进行筛选。

本接口参考 `get_filters` 的实现模式，提供 RESTful 风格的 POST 请求方式。

## 🔗 接口信息

- **路径**: `/get_text_effects`
- **方法**: POST
- **版本**: v1

## 📥 请求参数

### 请求体 (JSON)

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| mode | int | 否 | 0 | 花字效果模式：0=所有，1=VIP，2=免费 |

### 请求示例

#### 1. 获取所有花字效果

```bash
curl -X POST "http://localhost:8000/get_text_effects" \
  -H "Content-Type: application/json" \
  -d '{"mode": 0}'
```

#### 2. 获取 VIP 花字效果

```bash
curl -X POST "http://localhost:8000/get_text_effects" \
  -H "Content-Type: application/json" \
  -d '{"mode": 1}'
```

#### 3. 获取免费花字效果

```bash
curl -X POST "http://localhost:8000/get_text_effects" \
  -H "Content-Type: application/json" \
  -d '{"mode": 2}'
```

## 📤 响应参数

### 响应体 (JSON)

```json
{
  "text_effects": [
    {
      "name": "红黄火焰综艺花字",
      "is_vip": false,
      "resource_id": "7539407429763796249",
      "effect_id": "7539407429763796249"
    },
    {
      "name": "综艺 - 黑暗斑驳红色",
      "is_vip": false,
      "resource_id": "7351316503771368713",
      "effect_id": "7351316503771368713"
    }
    // ... 更多花字效果
  ]
}
```

### 字段说明

#### TextEffectItem 对象

| 字段名 | 类型 | 说明 |
|--------|------|------|
| name | string | 花字效果名称 |
| is_vip | boolean | 是否为 VIP 效果 |
| resource_id | string | 资源 ID |
| effect_id | string | 效果 ID |

## 📊 统计数据

根据当前数据源 (`config\data.ts`) 的统计:

- **总花字数**: 1,673 个
- **VIP 效果**: 0 个
- **免费效果**: 1,673 个
- **提取率**: 100%

## 💡 使用场景

### 1. 在客户端展示花字效果选择器

```javascript
// 获取所有花字效果
const response = await fetch('/get_text_effects', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ mode: 0 })
});

const data = await response.json();

// 渲染花字效果列表
data.text_effects.forEach(effect => {
  console.log(`${effect.name} (ID: ${effect.effect_id})`);
});
```

### 2. 仅展示免费花字效果

```javascript
// 获取免费花字效果
const response = await fetch('/get_text_effects', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ mode: 2 })
});

const data = await response.json();
// data.text_effects 只包含免费花字
```

### 3. 配合 add_captions API 使用

```javascript
// 1. 先获取花字效果列表
const effectsResponse = await fetch('/get_text_effects', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ mode: 0 })
});
const effects = await effectsResponse.json();

// 2. 用户选择一个花字效果
const selectedEffect = effects.text_effects[0];

// 3. 在添加字幕时使用该花字
await fetch('/add_captions', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    draft_id: "your_draft_id",
    captions: [...],
    text_effect: selectedEffect.name  // 或 selectedEffect.effect_id
  })
});
```

## 🔍 错误处理

### 错误码

| 错误码 | 说明 |
|--------|------|
| filter_get_failed | 获取花字效果列表失败 |

### 错误响应示例

```json
{
  "code": "filter_get_failed",
  "message": "获取花字效果列表失败",
  "detail": null
}
```

## ⚙️ 参数模式说明

### mode = 0 (所有)

返回所有花字效果，包括 VIP 和免费效果。

**适用场景**: 
- 完整的花字效果选择器
- 管理后台查看所有效果

### mode = 1 (VIP)

仅返回 VIP 花字效果。

**适用场景**:
- VIP 专属效果展示
- 付费效果推广

### mode = 2 (免费)

仅返回免费花字效果。

**适用场景**:
- 免费版客户端
- 免费效果筛选

## 📝 注意事项

1. **性能考虑**: 首次加载可能需要较长时间（1,673 个效果），建议使用缓存机制
2. **数据更新**: 花字效果数据来自 `config\data.ts`，如需更新请重新运行提取脚本
3. **重名处理**: 部分花字效果因名称重复，在映射表中添加了 `_effect_id` 后缀
4. **兼容性**: 即使没有 VIP 效果，接口也会正常返回空数组，不会报错

## 🛠️ 相关接口

- **添加字幕**: `/add_captions` - 可使用本接口返回的花字效果
- **获取滤镜列表**: `/get_filters` - 类似的滤镜效果列表接口
- **获取特效列表**: `/get_effects` - 视频特效列表接口

## 📦 技术实现

### Service 层

文件：`src/service/get_text_effects.py`

主要函数:
- `get_text_effects(mode: int)` - 主接口函数
- `resolve_text_effect(effect_identifier: str)` - 解析花字效果标识符
- `_get_text_effects_by_mode(mode: int)` - 根据模式获取效果

### Schema 层

文件：`src/schemas/get_text_effects.py`

Pydantic 模型:
- `GetTextEffectsRequest` - 请求参数
- `TextEffectItem` - 单个花字效果项
- `GetTextEffectsResponse` - 响应参数

### Router 层

文件：`src/router/v1.py`

路由定义:
```python
@router.post(path="/get_text_effects", response_model=GetTextEffectsResponse)
def get_text_effects(gter: GetTextEffectsRequest) -> GetTextEffectsResponse:
```

## 🧪 测试

运行测试脚本验证接口功能:

```bash
python tests\test_get_text_effects.py
```

测试覆盖:
- ✅ 获取所有花字效果 (mode=0)
- ✅ 获取 VIP 花字效果 (mode=1)
- ✅ 获取免费花字效果 (mode=2)
- ✅ 无效模式处理 (mode=3)

---

**最后更新**: 2026-03-31  
**API 版本**: v1  
**数据来源**: config\data.ts (1,673 个花字效果)
