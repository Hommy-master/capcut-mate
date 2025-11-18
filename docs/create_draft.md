# CREATE_DRAFT API 接口文档

## 📋 目录

- [🔧 接口信息](#-接口信息)
- [🎯 功能描述](#-功能描述)
- [📖 更多文档](#-更多文档)
- [📥 请求参数](#-请求参数)
- [📤 响应格式](#-响应格式)
- [💻 使用示例](#-使用示例)
- [❌ 错误码说明](#-错误码说明)
- [⚠️ 注意事项](#️-注意事项)
- [🔄 工作流程](#-工作流程)
- [➡️ 下一步操作](#️-下一步操作)
- [🔗 相关接口](#-相关接口)

## 🔧 接口信息

```
POST /openapi/capcut-mate/v1/create_draft
```

## 功能描述

创建剪映草稿。该接口用于创建一个新的剪映草稿项目，可以自定义视频的宽度和高度。创建成功后会返回草稿URL和帮助文档URL，为后续的视频编辑操作提供基础。

## 更多文档

📖 更多详细文档和教程请访问：[https://docs.jcaigc.cn](https://docs.jcaigc.cn)

## 请求参数

```json
{
  "width": 1920,
  "height": 1080
}
```

### 参数说明

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| width | number | ❌ | 1920 | 视频宽度(像素)，必须大于等于1 |
| height | number | ❌ | 1080 | 视频高度(像素)，必须大于等于1 |

### 参数详解

#### 尺寸参数

- **width**: 草稿视频的宽度
  - 最小值：1像素
  - 建议常用值：1920、1280、720
  - 支持自定义尺寸

- **height**: 草稿视频的高度
  - 最小值：1像素
  - 建议常用值：1080、720、480
  - 支持自定义尺寸

#### 常用分辨率

| 分辨率名称 | 宽度 | 高度 | 适用场景 |
|------------|------|------|----------|
| 1080P | 1920 | 1080 | 高清视频制作 |
| 720P | 1280 | 720 | 标清视频制作 |
| 4K | 3840 | 2160 | 超高清视频制作 |
| 竖屏短视频 | 1080 | 1920 | 手机短视频 |
| 正方形 | 1080 | 1080 | 社交媒体内容 |

## 响应格式

### 成功响应 (200)

```json
{
  "draft_url": "https://cm.jcaigc.cn/openapi/v1/get_draft?draft_id=2025092811473036584258",
  "tip_url": "https://help.assets.jcaigc.cn/draft-usage"
}
```

### 响应字段说明

| 字段名 | 类型 | 说明 |
|--------|------|------|
| draft_url | string | 新创建的草稿URL，用于后续的编辑操作 |
| tip_url | string | 草稿使用帮助文档URL |

### 错误响应 (4xx/5xx)

```json
{
  "detail": "错误信息描述"
}
```

## 💻 使用示例

### cURL 示例

#### 1. 创建默认分辨率草稿

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/create_draft \
  -H "Content-Type: application/json" \
  -d '{}'
```

#### 2. 创建自定义分辨率草稿

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/create_draft \
  -H "Content-Type: application/json" \
  -d '{
    "width": 1280,
    "height": 720
  }'
```

#### 3. 创建竖屏短视频草稿

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/create_draft \
  -H "Content-Type: application/json" \
  -d '{
    "width": 1080,
    "height": 1920
  }'
```

### JavaScript 示例

#### 基础使用

```javascript
// 创建草稿函数
const createDraft = async (width = 1920, height = 1080) => {
  const response = await fetch('/openapi/capcut-mate/v1/create_draft', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ width, height })
  });
  return response.json();
};

// 使用示例
(async () => {
  // 创建默认分辨率草稿
  const defaultDraft = await createDraft();
  
  // 创建720P草稿
  const hdDraft = await createDraft(1280, 720);
  
  // 创建正方形草稿
  const squareDraft = await createDraft(1080, 1080);
  
  console.log('草稿创建成功:', {
    default: defaultDraft.draft_url,
    hd: hdDraft.draft_url,
    square: squareDraft.draft_url
  });
})();
```

#### 高级封装类

```javascript
class DraftManager {
  constructor(baseUrl = 'https://capcut-mate.jcaigc.cn') {
    this.baseUrl = baseUrl;
  }

  async createDraft(config = {}) {
    const { width = 1920, height = 1080 } = config;
    
    const response = await fetch(`${this.baseUrl}/openapi/capcut-mate/v1/create_draft`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ width, height })
    });
    
    if (!response.ok) {
      throw new Error(`创建草稿失败: ${response.statusText}`);
    }
    
    return response.json();
  }

  // 预设分辨率创建方法
  async create1080p() {
    return this.createDraft({ width: 1920, height: 1080 });
  }

  async create720p() {
    return this.createDraft({ width: 1280, height: 720 });
  }

  async create4K() {
    return this.createDraft({ width: 3840, height: 2160 });
  }

  async createVertical() {
    return this.createDraft({ width: 1080, height: 1920 });
  }

  async createSquare() {
    return this.createDraft({ width: 1080, height: 1080 });
  }

  // 批量创建多种规格草稿
  async createMultipleFormats() {
    const formats = [
      { name: '1080P', width: 1920, height: 1080 },
      { name: '720P', width: 1280, height: 720 },
      { name: '竖屏', width: 1080, height: 1920 },
      { name: '正方形', width: 1080, height: 1080 }
    ];

    const results = {};
    
    for (const format of formats) {
      try {
        const draft = await this.createDraft({
          width: format.width,
          height: format.height
        });
        results[format.name] = draft;
        
        // 添加延迟避免请求过快
        await new Promise(resolve => setTimeout(resolve, 100));
      } catch (error) {
        console.error(`创建${format.name}草稿失败:`, error);
        results[format.name] = { error: error.message };
      }
    }
    
    return results;
  }
}

// 使用示例
const draftManager = new DraftManager();

// 创建单个草稿
draftManager.create1080p().then(draft => {
  console.log('草稿URL:', draft.draft_url);
});

// 批量创建多种格式
draftManager.createMultipleFormats().then(results => {
  console.log('多种格式草稿:', results);
});
```

### Python 示例

```python
import requests
from typing import Optional, Dict

class DraftCreator:
    def __init__(self, base_url: str = "https://api.assets.jcaigc.cn"):
        self.base_url = base_url

    def create_draft(self, width: int = 1920, height: int = 1080) -> Dict:
        """创建草稿"""
        response = requests.post(
            f'{self.base_url}/openapi/capcut-mate/v1/create_draft',
            headers={'Content-Type': 'application/json'},
            json={
                "width": width,
                "height": height
            }
        )
        response.raise_for_status()
        return response.json()

    # 预设分辨率方法
    def create_1080p(self) -> Dict:
        return self.create_draft(1920, 1080)

    def create_720p(self) -> Dict:
        return self.create_draft(1280, 720)

    def create_4k(self) -> Dict:
        return self.create_draft(3840, 2160)

    def create_vertical(self) -> Dict:
        return self.create_draft(1080, 1920)

    def create_square(self) -> Dict:
        return self.create_draft(1080, 1080)

# 使用示例
creator = DraftCreator()

# 创建不同分辨率的草稿
drafts = {
    "1080p": creator.create_1080p(),
    "720p": creator.create_720p(),
    "vertical": creator.create_vertical(),
    "square": creator.create_square()
}

for name, draft in drafts.items():
    print(f"{name} 草稿URL: {draft['draft_url']}")
```

## 错误码说明

| 错误码 | 错误信息 | 说明 | 解决方案 |
|--------|----------|------|----------|
| 400 | width必须大于等于1 | 宽度参数无效 | 提供大于等于1的宽度值 |
| 400 | height必须大于等于1 | 高度参数无效 | 提供大于等于1的高度值 |
| 400 | 参数类型错误 | 参数类型不正确 | 确保width和height为数字类型 |
| 500 | 草稿创建失败 | 内部服务错误 | 联系技术支持 |
| 503 | 服务不可用 | 系统维护中 | 稍后重试 |

## 注意事项

1. **参数验证**: width和height必须为正整数
2. **分辨率建议**: 建议使用常见的视频分辨率以确保兼容性
3. **性能考虑**: 超高分辨率可能影响后续处理性能
4. **存储占用**: 高分辨率草稿会占用更多存储空间
5. **URL有效期**: 返回的draft_url具有一定的有效期

## 工作流程

1. 接收并验证请求参数
2. 创建草稿基础结构
3. 设置画布尺寸
4. 生成草稿URL
5. 返回草稿信息和帮助文档链接

## 下一步操作

创建草稿后，您可以使用以下接口继续编辑：

- **add_videos**: 添加视频素材
- **add_audios**: 添加音频素材  
- **add_images**: 添加图片素材
- **save_draft**: 保存草稿
- **gen_video**: 导出视频

## 🔗 相关接口

<div align="center">

### 📚 导航指南

**🎯 新手路径**: [首页文档](./index.md) ← 当前位置 → [添加视频](./add_videos.md)

**🔄 工作流程**: 创建草稿 → **当前: CREATE_DRAFT** → [添加素材](./add_videos.md) → [生成视频](./gen_video.md)

**📖 相关文档**:
- [项目概览](./index.md) - 了解完整功能
- [添加视频](./add_videos.md) - 添加视频素材
- [保存草稿](./save_draft.md) - 保存草稿更改

</div>

---

<div align="right">

**📚 项目资源**: [GitHub](https://github.com/Hommy-master/capcut-mate) | [Gitee](https://gitee.com/taohongmin-gitee/capcut-mate)

</div>