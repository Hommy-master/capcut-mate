# SAVE_DRAFT API 接口文档

## 接口信息

```
POST /openapi/capcut-mate/v1/save_draft
```

## 功能描述

保存剪映草稿。该接口用于保存当前的草稿状态，确保编辑的内容得到持久化存储。通常在完成一系列编辑操作后调用此接口，以防止编辑内容丢失。

## 请求参数

```json
{
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258"
}
```

### 参数说明

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| draft_url | string | ✅ | - | 要保存的草稿URL |

### 参数详解

#### draft_url

- **类型**: 字符串
- **必填**: 是
- **格式**: 完整的草稿URL，通常由create_draft接口返回
- **示例**: `https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258"draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258"
}
```

### 响应字段说明

| 字段名 | 类型 | 说明 |
|--------|------|------|
| draft_url | string | 保存后的草稿URL，通常与请求中的URL相同 |

### 错误响应 (4xx/5xx)

```json
{
  "detail": "错误信息描述"
}
```

## 使用示例

### cURL 示例

#### 1. 基本保存草稿

```bash
curl -X POST https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/save_draft \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258"
  }'
```

### JavaScript 示例

```javascript
const saveDraft = async (draftUrl) => {
  const response = await fetch('/openapi/capcut-mate/v1/save_draft', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ draft_url: draftUrl })
  });
  return response.json();
};

// 保存草稿
const draftUrl = "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258";
const result = await saveDraft(draftUrl);
console.log('草稿保存成功:', result.draft_url);
```

### 高级JavaScript示例

```javascript
class DraftManager {
  constructor(baseUrl = 'https://capcut-mate.jcaigc.cn') {
    this.baseUrl = baseUrl;
  }

  async saveDraft(draftUrl) {
    const response = await fetch(`${this.baseUrl}/openapi/capcut-mate/v1/save_draft`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ draft_url: draftUrl })
    });
    
    if (!response.ok) {
      throw new Error(`保存草稿失败: ${response.statusText}`);
    }
    
    return response.json();
  }

  // 自动保存功能
  async autoSave(draftUrl, intervalMs = 30000) {
    const saveInterval = setInterval(async () => {
      try {
        await this.saveDraft(draftUrl);
        console.log(`自动保存成功: ${new Date().toLocaleTimeString()}`);
      } catch (error) {
        console.error('自动保存失败:', error);
      }
    }, intervalMs);

    // 返回停止自动保存的函数
    return () => clearInterval(saveInterval);
  }

  // 编辑流程中的保存
  async editWorkflow(draftUrl, operations) {
    const results = [];
    
    for (const operation of operations) {
      try {
        // 执行编辑操作（这里是示例）
        const editResult = await operation();
        results.push(editResult);
        
        // 每次操作后自动保存
        await this.saveDraft(draftUrl);
        console.log(`操作完成并保存: ${operation.name}`);
        
      } catch (error) {
        console.error(`操作失败: ${operation.name}`, error);
        results.push({ error: error.message });
      }
    }
    
    return results;
  }

  // 批量保存多个草稿
  async saveMutipleDrafts(draftUrls) {
    const results = {};
    
    for (const [name, url] of Object.entries(draftUrls)) {
      try {
        const result = await this.saveDraft(url);
        results[name] = result;
        
        // 添加延迟避免请求过快
        await new Promise(resolve => setTimeout(resolve, 100));
      } catch (error) {
        console.error(`保存草稿失败 ${name}:`, error);
        results[name] = { error: error.message };
      }
    }
    
    return results;
  }
}

// 使用示例
const draftManager = new DraftManager();

// 基本保存
const draftUrl = "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258";
await draftManager.saveDraft(draftUrl);

// 启动自动保存（每30秒保存一次）
const stopAutoSave = await draftManager.autoSave(draftUrl, 30000);

// 编辑完成后停止自动保存
setTimeout(() => {
  stopAutoSave();
  console.log('自动保存已停止');
}, 300000); // 5分钟后停止

// 批量保存多个草稿
const multipleDrafts = {
  "project1": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
  "project2": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258"
};
const saveResults = await draftManager.saveMutipleDrafts(multipleDrafts);
```

### Python 示例

```python
import requests
import time
import threading
from typing import Dict, List, Callable

class DraftSaver:
    def __init__(self, base_url: str = "https://api.example.com"):
        self.base_url = base_url
        self._auto_save_threads = {}

    def save_draft(self, draft_url: str) -> Dict:
        """保存草稿"""
        response = requests.post(
            f'{self.base_url}/openapi/capcut-mate/v1/save_draft',
            headers={'Content-Type': 'application/json'},
            json={"draft_url": draft_url}
        )
        response.raise_for_status()
        return response.json()

    def auto_save(self, draft_url: str, interval_seconds: int = 30) -> str:
        """启动自动保存，返回线程ID用于停止"""
        def save_loop():
            while True:
                try:
                    self.save_draft(draft_url)
                    print(f"自动保存成功: {time.strftime('%H:%M:%S')}")
                    time.sleep(interval_seconds)
                except Exception as e:
                    print(f"自动保存失败: {e}")
                    time.sleep(5)  # 出错后等待5秒再重试

        thread_id = f"auto_save_{int(time.time())}"
        thread = threading.Thread(target=save_loop, daemon=True)
        thread.start()
        self._auto_save_threads[thread_id] = thread
        
        return thread_id

    def stop_auto_save(self, thread_id: str):
        """停止自动保存"""
        if thread_id in self._auto_save_threads:
            # 线程设为daemon，程序结束时会自动停止
            del self._auto_save_threads[thread_id]
            print(f"自动保存线程 {thread_id} 已标记停止")

    def save_with_retry(self, draft_url: str, max_retries: int = 3) -> Dict:
        """带重试机制的保存"""
        for attempt in range(max_retries):
            try:
                return self.save_draft(draft_url)
            except Exception as e:
                if attempt == max_retries - 1:
                    raise e
                print(f"保存失败，第{attempt + 1}次重试: {e}")
                time.sleep(2 ** attempt)  # 指数退避

# 使用示例
saver = DraftSaver()

# 基本保存
draft_url = "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258"
result = saver.save_draft(draft_url)
print(f"草稿保存成功: {result['draft_url']}")

# 带重试的保存
try:
    result = saver.save_with_retry(draft_url, max_retries=3)
    print("保存成功（带重试机制）")
except Exception as e:
    print(f"保存最终失败: {e}")

# 启动自动保存
auto_save_id = saver.auto_save(draft_url, interval_seconds=30)
print(f"自动保存已启动，ID: {auto_save_id}")

# 10分钟后停止自动保存
time.sleep(600)
saver.stop_auto_save(auto_save_id)
```

## 错误码说明

| 错误码 | 错误信息 | 说明 | 解决方案 |
|--------|----------|------|----------|
| 400 | draft_url是必填项 | 缺少草稿URL参数 | 提供有效的draft_url |
| 400 | draft_url格式无效 | URL格式不正确 | 检查URL格式是否正确 |
| 404 | 草稿不存在 | 指定的草稿无法找到 | 确认草稿URL是否正确且存在 |
| 500 | 保存失败 | 内部服务错误 | 联系技术支持或稍后重试 |
| 503 | 服务不可用 | 系统维护中 | 稍后重试 |

## 注意事项

1. **URL有效性**: 确保传入的draft_url是有效且存在的
2. **网络稳定性**: 保存操作需要稳定的网络连接
3. **频率控制**: 避免过于频繁的保存操作
4. **自动保存**: 建议在长时间编辑时启用自动保存功能
5. **错误处理**: 保存失败时应该有重试机制
6. **并发安全**: 同一草稿的并发保存可能导致冲突

## 工作流程

1. 验证draft_url参数
2. 检查草稿是否存在
3. 获取当前草稿状态
4. 持久化保存草稿数据
5. 返回保存结果

## 最佳实践

1. **定期保存**: 在重要操作后及时保存
2. **自动保存**: 为长时间编辑设置自动保存
3. **错误恢复**: 保存失败时提供重试机制
4. **状态提示**: 向用户显示保存状态
5. **备份策略**: 考虑多版本备份机制

## 相关接口

- [创建草稿](./create_draft.md)
- [添加视频](./add_videos.md)
- [添加音频](./add_audios.md)
- [添加图片](./add_images.md)
- [生成视频](./gen_video.md)