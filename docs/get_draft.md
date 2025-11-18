# GET_DRAFT API 接口文档

## 📋 目录

- [🔧 接口信息](#-接口信息)
- [🎯 功能描述](#-功能描述)
- [📖 更多文档](#-更多文档)
- [📥 请求参数](#-请求参数)
- [📤 响应格式](#-响应格式)
- [💻 使用示例](#-使用示例)
- [❌ 错误码说明](#-错误码说明)
- [⚠️ 注意事项](#️-注意事项)
- [🔗 相关接口](#-相关接口)

## 🔧 接口信息

```
GET /openapi/capcut-mate/v1/get_draft
```

## 功能描述

获取草稿文件列表。该接口用于获取指定草稿ID对应的所有文件列表，可以查看草稿中包含的素材文件、配置文件等信息。通常用于草稿内容的预览、文件管理或状态检查。

## 更多文档

📖 更多详细文档和教程请访问：[https://docs.jcaigc.cn](https://docs.jcaigc.cn)

## 请求参数

### Query参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| draft_id | string | ✅ | - | 草稿ID，长度为20-32位字符 |

### 参数详解

#### draft_id

- **类型**: 字符串
- **必填**: 是
- **长度**: 20-32位字符
- **格式**: 通常为UUID格式或类似的唯一标识符
- **示例**: `2f52a63b-8c6a-4417-8b01-1b2a569ccb6c`
- **获取方式**: 通常从draft_url中提取或由create_draft接口返回

#### draft_id提取方法

从draft_url中提取draft_id：
```javascript
// 示例draft_url:
// https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258"2f52a63b-8c6a-4417-8b01-1b2a569ccb6c"
```

## 响应格式

### 成功响应 (200)

```json
{
  "files": [
    "2f52a63b-8c6a-4417-8b01-1b2a569ccb6c.json",
    "video_123456789.mp4",
    "audio_987654321.mp3",
    "image_555666777.jpg",
    "thumbnail_888999000.png"
  ]
}
```

### 响应字段说明

| 字段名 | 类型 | 说明 |
|--------|------|------|
| files | array | 草稿相关的文件列表 |

### 文件类型说明

返回的文件列表可能包含以下类型：

| 文件类型 | 扩展名 | 说明 |
|----------|--------|------|
| 草稿配置文件 | .json | 草稿的主要配置文件，包含所有编辑信息 |
| 视频文件 | .mp4, .avi, .mov | 草稿中使用的视频素材 |
| 音频文件 | .mp3, .wav, .aac | 草稿中使用的音频素材 |
| 图片文件 | .jpg, .png, .gif | 草稿中使用的图片素材 |
| 缩略图文件 | .png, .jpg | 素材的缩略图文件 |
| 临时文件 | .tmp | 处理过程中的临时文件 |

### 错误响应 (4xx/5xx)

```json
{
  "detail": "错误信息描述"
}
```

## 使用示例

### cURL 示例

#### 1. 基本获取草稿文件列表

```bash
curl -X GET "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2f52a63b-8c6a-4417-8b01-1b2a569ccb6c" \
  -H "Content-Type: application/json"
```

#### 2. 使用完整的draft_id

```bash
curl -X GET "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=7e8f9a0b-1c2d-3e4f-5g6h-7i8j9k0l1m2n" \
  -H "Content-Type: application/json"
```

### JavaScript 示例

```javascript
const getDraft = async (draftId) => {
  const response = await fetch(`/v1/get_draft?draft_id=${draftId}`, {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' }
  });
  return response.json();
};

// 使用示例
const draftId = "2f52a63b-8c6a-4417-8b01-1b2a569ccb6c";
const result = await getDraft(draftId);
console.log('草稿文件列表:', result.files);

// 从draft_url提取draft_id
function extractDraftId(draftUrl) {
  const match = draftUrl.match(/\/([^\/]+)\.json$/);
  return match ? match[1] : null;
}

const draftUrl = "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258";
const extractedId = extractDraftId(draftUrl);

if (extractedId) {
  const files = await getDraft(extractedId);
  console.log('文件列表:', files);
}
```

### 高级JavaScript示例

```javascript
class DraftManager {
  constructor(baseUrl = 'https://capcut-mate.jcaigc.cn') {
    this.baseUrl = baseUrl;
  }

  async getDraft(draftId) {
    const response = await fetch(`${this.baseUrl}/v1/get_draft?draft_id=${draftId}`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' }
    });
    
    if (!response.ok) {
      throw new Error(`获取草稿失败: ${response.statusText}`);
    }
    
    return response.json();
  }

  // 从draft_url提取draft_id
  extractDraftId(draftUrl) {
    try {
      const url = new URL(draftUrl);
      const draftIdParam = url.searchParams.get('drafId');
      if (draftIdParam) {
        const match = draftIdParam.match(/\/([^\/]+)\.json$/);
        return match ? match[1] : null;
      }
      return null;
    } catch (error) {
      console.error('URL解析失败:', error);
      return null;
    }
  }

  // 分析文件类型
  analyzeFiles(files) {
    const analysis = {
      total: files.length,
      types: {
        config: [],
        video: [],
        audio: [],
        image: [],
        thumbnail: [],
        other: []
      }
    };

    files.forEach(file => {
      const ext = file.split('.').pop()?.toLowerCase();
      
      switch (ext) {
        case 'json':
          analysis.types.config.push(file);
          break;
        case 'mp4':
        case 'avi':
        case 'mov':
        case 'mkv':
          analysis.types.video.push(file);
          break;
        case 'mp3':
        case 'wav':
        case 'aac':
        case 'flac':
          analysis.types.audio.push(file);
          break;
        case 'jpg':
        case 'jpeg':
        case 'png':
        case 'gif':
        case 'bmp':
          if (file.includes('thumbnail')) {
            analysis.types.thumbnail.push(file);
          } else {
            analysis.types.image.push(file);
          }
          break;
        default:
          analysis.types.other.push(file);
      }
    });

    return analysis;
  }

  // 获取草稿详细信息
  async getDraftDetails(draftUrl) {
    const draftId = this.extractDraftId(draftUrl);
    if (!draftId) {
      throw new Error('无法从URL中提取草稿ID');
    }

    const result = await this.getDraft(draftId);
    const analysis = this.analyzeFiles(result.files);

    return {
      draftId,
      draftUrl,
      files: result.files,
      analysis
    };
  }

  // 批量获取多个草稿信息
  async getBatchDrafts(draftUrls) {
    const results = {};
    
    for (const [name, url] of Object.entries(draftUrls)) {
      try {
        const details = await this.getDraftDetails(url);
        results[name] = details;
        
        // 添加延迟避免请求过快
        await new Promise(resolve => setTimeout(resolve, 100));
      } catch (error) {
        console.error(`获取草稿失败 ${name}:`, error);
        results[name] = { error: error.message };
      }
    }
    
    return results;
  }

  // 监控草稿文件变化
  async monitorDraftChanges(draftId, callback, intervalMs = 5000) {
    let lastFileList = [];
    
    const checkChanges = async () => {
      try {
        const result = await this.getDraft(draftId);
        const currentFiles = result.files.sort();
        
        // 检查文件列表是否发生变化
        if (JSON.stringify(currentFiles) !== JSON.stringify(lastFileList)) {
          const changes = {
            added: currentFiles.filter(f => !lastFileList.includes(f)),
            removed: lastFileList.filter(f => !currentFiles.includes(f)),
            current: currentFiles
          };
          
          callback(changes);
          lastFileList = currentFiles;
        }
      } catch (error) {
        console.error('监控草稿变化失败:', error);
      }
    };

    // 初始检查
    await checkChanges();
    
    // 定期检查
    const interval = setInterval(checkChanges, intervalMs);
    
    // 返回停止监控的函数
    return () => clearInterval(interval);
  }
}

// 使用示例
const draftManager = new DraftManager();

// 获取单个草稿详情
const draftUrl = "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258";
const details = await draftManager.getDraftDetails(draftUrl);

console.log('草稿详情:', {
  id: details.draftId,
  totalFiles: details.analysis.total,
  videoCount: details.analysis.types.video.length,
  audioCount: details.analysis.types.audio.length,
  imageCount: details.analysis.types.image.length
});

// 批量获取草稿信息
const multipleDrafts = {
  "project1": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
  "project2": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258"
};

const batchResults = await draftManager.getBatchDrafts(multipleDrafts);
console.log('批量草稿信息:', batchResults);

// 监控草稿文件变化
const draftId = "2f52a63b-8c6a-4417-8b01-1b2a569ccb6c";
const stopMonitoring = await draftManager.monitorDraftChanges(draftId, (changes) => {
  console.log('草稿文件发生变化:', changes);
  if (changes.added.length > 0) {
    console.log('新增文件:', changes.added);
  }
  if (changes.removed.length > 0) {
    console.log('删除文件:', changes.removed);
  }
});

// 30秒后停止监控
setTimeout(() => {
  stopMonitoring();
  console.log('停止监控草稿变化');
}, 30000);
```

### Python 示例

```python
import requests
import re
import time
import threading
from urllib.parse import urlparse, parse_qs
from typing import Dict, List, Optional, Callable

class DraftManager:
    def __init__(self, base_url: str = "https://api.assets.jcaigc.cn"):
        self.base_url = base_url

    def get_draft(self, draft_id: str) -> Dict:
        """获取草稿文件列表"""
        response = requests.get(
            f'{self.base_url}/openapi/capcut-mate/v1/get_draft',
            params={'draft_id': draft_id},
            headers={'Content-Type': 'application/json'}
        )
        response.raise_for_status()
        return response.json()

    def extract_draft_id(self, draft_url: str) -> Optional[str]:
        """从draft_url提取draft_id"""
        try:
            parsed_url = urlparse(draft_url)
            query_params = parse_qs(parsed_url.fragment.split('?')[1] if '?' in parsed_url.fragment else '')
            
            draft_id_param = query_params.get('drafId', [None])[0]
            if draft_id_param:
                match = re.search(r'/([^/]+)\.json$', draft_id_param)
                return match.group(1) if match else None
            return None
        except Exception as e:
            print(f"URL解析失败: {e}")
            return None

    def analyze_files(self, files: List[str]) -> Dict:
        """分析文件类型"""
        analysis = {
            'total': len(files),
            'types': {
                'config': [],
                'video': [],
                'audio': [],
                'image': [],
                'thumbnail': [],
                'other': []
            }
        }

        for file in files:
            ext = file.split('.')[-1].lower() if '.' in file else ''
            
            if ext == 'json':
                analysis['types']['config'].append(file)
            elif ext in ['mp4', 'avi', 'mov', 'mkv']:
                analysis['types']['video'].append(file)
            elif ext in ['mp3', 'wav', 'aac', 'flac']:
                analysis['types']['audio'].append(file)
            elif ext in ['jpg', 'jpeg', 'png', 'gif', 'bmp']:
                if 'thumbnail' in file:
                    analysis['types']['thumbnail'].append(file)
                else:
                    analysis['types']['image'].append(file)
            else:
                analysis['types']['other'].append(file)

        return analysis

    def get_draft_details(self, draft_url: str) -> Dict:
        """获取草稿详细信息"""
        draft_id = self.extract_draft_id(draft_url)
        if not draft_id:
            raise ValueError('无法从URL中提取草稿ID')

        result = self.get_draft(draft_id)
        analysis = self.analyze_files(result['files'])

        return {
            'draft_id': draft_id,
            'draft_url': draft_url,
            'files': result['files'],
            'analysis': analysis
        }

    def get_batch_drafts(self, draft_urls: Dict[str, str]) -> Dict:
        """批量获取草稿信息"""
        results = {}
        
        for name, url in draft_urls.items():
            try:
                details = self.get_draft_details(url)
                results[name] = details
                time.sleep(0.1)  # 避免请求过快
            except Exception as e:
                print(f"获取草稿失败 {name}: {e}")
                results[name] = {'error': str(e)}
        
        return results

    def monitor_draft_changes(self, draft_id: str, callback: Callable, interval_seconds: int = 5) -> str:
        """监控草稿文件变化"""
        last_file_list = []
        stop_event = threading.Event()
        
        def check_changes():
            nonlocal last_file_list
            while not stop_event.is_set():
                try:
                    result = self.get_draft(draft_id)
                    current_files = sorted(result['files'])
                    
                    if current_files != last_file_list:
                        changes = {
                            'added': [f for f in current_files if f not in last_file_list],
                            'removed': [f for f in last_file_list if f not in current_files],
                            'current': current_files
                        }
                        
                        callback(changes)
                        last_file_list = current_files
                        
                except Exception as e:
                    print(f"监控草稿变化失败: {e}")
                
                stop_event.wait(interval_seconds)
        
        # 初始检查
        try:
            result = self.get_draft(draft_id)
            last_file_list = sorted(result['files'])
        except Exception as e:
            print(f"初始检查失败: {e}")
        
        # 启动监控线程
        thread = threading.Thread(target=check_changes, daemon=True)
        thread.start()
        
        # 返回停止函数
        def stop_monitoring():
            stop_event.set()
            thread.join(timeout=1)
        
        return stop_monitoring

# 使用示例
manager = DraftManager()

# 获取单个草稿
draft_url = "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258"
details = manager.get_draft_details(draft_url)

print(f"草稿ID: {details['draft_id']}")
print(f"文件总数: {details['analysis']['total']}")
print(f"视频文件: {len(details['analysis']['types']['video'])}个")
print(f"音频文件: {len(details['analysis']['types']['audio'])}个")
print(f"图片文件: {len(details['analysis']['types']['image'])}个")

# 批量获取草稿
multiple_drafts = {
    "project1": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
    "project2": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258"
}

batch_results = manager.get_batch_drafts(multiple_drafts)
for name, result in batch_results.items():
    if 'error' not in result:
        print(f"{name}: {result['analysis']['total']} 个文件")

# 监控草稿变化
def on_change(changes):
    print(f"草稿文件发生变化:")
    if changes['added']:
        print(f"新增: {changes['added']}")
    if changes['removed']:
        print(f"删除: {changes['removed']}")

draft_id = "2f52a63b-8c6a-4417-8b01-1b2a569ccb6c"
stop_monitoring = manager.monitor_draft_changes(draft_id, on_change)

# 30秒后停止监控
time.sleep(30)
stop_monitoring()
print("停止监控")
```

## 错误码说明

| 错误码 | 错误信息 | 说明 | 解决方案 |
|--------|----------|------|----------|
| 400 | draft_id是必填项 | 缺少draft_id参数 | 提供有效的draft_id |
| 400 | draft_id长度无效 | draft_id长度不在20-32位范围内 | 检查draft_id格式是否正确 |
| 400 | draft_id格式无效 | draft_id格式不正确 | 确保使用正确的草稿ID格式 |
| 404 | 草稿不存在 | 指定的草稿ID无法找到 | 确认草稿ID是否正确且存在 |
| 500 | 获取文件列表失败 | 内部服务错误 | 联系技术支持或稍后重试 |
| 503 | 服务不可用 | 系统维护中 | 稍后重试 |

## 注意事项

1. **参数格式**: 确保draft_id格式正确且长度在20-32位之间
2. **ID提取**: 从draft_url正确提取draft_id
3. **文件类型**: 返回的文件列表包含多种类型的文件
4. **权限验证**: 确保有权限访问指定的草稿
5. **实时性**: 文件列表可能不是实时更新的，存在一定延迟
6. **文件状态**: 列表中的文件可能处于不同的处理状态

## 工作流程

1. 验证draft_id参数
2. 检查draft_id格式和长度
3. 查找指定的草稿
4. 获取草稿关联的所有文件
5. 返回文件列表

## 最佳实践

1. **ID验证**: 在调用前验证draft_id的有效性
2. **错误处理**: 妥善处理草稿不存在的情况
3. **文件分析**: 对返回的文件列表进行分类分析
4. **缓存策略**: 对于频繁查询的草稿，考虑适当缓存
5. **监控变化**: 对于需要实时更新的场景，实现变化监控

## 相关接口

- [创建草稿](./create_draft.md)
- [保存草稿](./save_draft.md)
- [添加视频](./add_videos.md)
- [添加音频](./add_audios.md)
- [添加图片](./add_images.md)
- [生成视频](./gen_video.md)

---

<div align="right">

**📚 项目资源**: [GitHub](https://github.com/Hommy-master/capcut-mate) | [Gitee](https://gitee.com/taohongmin-gitee/capcut-mate)

</div>
