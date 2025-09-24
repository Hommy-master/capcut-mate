# GEN_VIDEO API 接口文档

## 接口信息

```
POST /v1/gen_video
```

## 功能描述

生成视频 - 根据草稿URL，导出视频。该接口用于将编辑完成的草稿导出为最终的视频文件。接口会处理草稿中的所有素材、效果、转场等，生成一个完整的视频文件供下载或进一步使用。

## 请求参数

```json
{
  "draft_url": "https://ts.fyshark.com/#/cozeToJianyin?drafId=https://video-snot-12220.oss-cn-shanghai.aliyuncs.com/2025-05-28/draft/2f52a63b-8c6a-4417-8b01-1b2a569ccb6c.json"
}
```

### 参数说明

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| draft_url | string | ✅ | - | 要导出的草稿URL |

### 参数详解

#### draft_url

- **类型**: 字符串
- **必填**: 是
- **格式**: 完整的草稿URL，包含草稿ID信息
- **示例**: `https://ts.fyshark.com/#/cozeToJianyin?drafId=https://video-snot-12220.oss-cn-shanghai.aliyuncs.com/...`
- **要求**: 必须是有效的、存在的草稿URL

#### 导出流程说明

视频生成过程包括以下步骤：
1. **草稿解析**: 解析草稿配置文件，获取所有素材和效果信息
2. **素材下载**: 下载所有必需的视频、音频、图片素材
3. **时间轴处理**: 按照时间轴顺序排列所有素材
4. **效果渲染**: 应用透明度、缩放、位置变换等效果
5. **转场处理**: 添加视频间的转场效果
6. **音频混合**: 混合多个音频轨道
7. **视频编码**: 将处理后的内容编码为最终视频
8. **文件上传**: 将生成的视频上传到存储服务

## 响应格式

### 成功响应 (200)

```json
{
  "message": "视频生成成功",
  "video_url": "https://video-output.example.com/generated/2f52a63b-8c6a-4417-8b01-1b2a569ccb6c_final.mp4"
}
```

### 响应字段说明

| 字段名 | 类型 | 说明 |
|--------|------|------|
| message | string | 处理结果消息 |
| video_url | string | 生成的视频文件URL |

#### video_url说明

- **格式**: 完整的视频文件URL
- **有效期**: 通常具有一定的有效期限制
- **下载**: 可以直接通过URL下载视频文件
- **格式**: 通常为MP4格式，具有良好的兼容性

### 错误响应 (4xx/5xx)

```json
{
  "detail": "错误信息描述"
}
```

### 处理状态说明

视频生成是一个相对耗时的过程，可能的状态包括：

| 状态 | 说明 | 预期时间 |
|------|------|----------|
| 开始处理 | 接收请求，开始解析草稿 | 1-2秒 |
| 素材下载 | 下载所有必需的素材文件 | 5-30秒 |
| 视频渲染 | 处理视频效果和转场 | 10秒-数分钟 |
| 音频处理 | 混合和同步音频 | 5-20秒 |
| 最终编码 | 生成最终视频文件 | 10秒-数分钟 |
| 上传完成 | 视频上传到存储服务 | 5-30秒 |

## 使用示例

### cURL 示例

#### 1. 基本视频生成

```bash
curl -X POST https://api.example.com/v1/gen_video \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "https://ts.fyshark.com/#/cozeToJianyin?drafId=https://video-snot-12220.oss-cn-shanghai.aliyuncs.com/2025-05-28/draft/example.json"
  }'
```

#### 2. 带超时设置的请求

```bash
curl -X POST https://api.example.com/v1/gen_video \
  -H "Content-Type: application/json" \
  -d '{
    "draft_url": "YOUR_DRAFT_URL"
  }' \
  --max-time 300
```

### JavaScript 示例

```javascript
const generateVideo = async (draftUrl) => {
  const response = await fetch('/v1/gen_video', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ draft_url: draftUrl })
  });
  return response.json();
};

// 基本使用
const draftUrl = "https://ts.fyshark.com/#/cozeToJianyin?drafId=...";
const result = await generateVideo(draftUrl);

if (result.video_url) {
  console.log('视频生成成功:', result.video_url);
  
  // 创建下载链接
  const downloadLink = document.createElement('a');
  downloadLink.href = result.video_url;
  downloadLink.download = 'generated_video.mp4';
  downloadLink.click();
} else {
  console.error('视频生成失败:', result.message);
}
```

### 高级JavaScript示例

```javascript
class VideoGenerator {
  constructor(baseUrl = 'https://api.example.com') {
    this.baseUrl = baseUrl;
  }

  async generateVideo(draftUrl, options = {}) {
    const {
      timeout = 300000, // 5分钟超时
      onProgress = null
    } = options;

    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), timeout);

    try {
      const response = await fetch(`${this.baseUrl}/v1/gen_video`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ draft_url: draftUrl }),
        signal: controller.signal
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        throw new Error(`视频生成失败: ${response.statusText}`);
      }

      return response.json();
    } catch (error) {
      clearTimeout(timeoutId);
      if (error.name === 'AbortError') {
        throw new Error('视频生成超时');
      }
      throw error;
    }
  }

  // 轮询式视频生成（适用于长时间处理）
  async generateVideoWithPolling(draftUrl, options = {}) {
    const {
      pollInterval = 5000, // 5秒轮询间隔
      maxAttempts = 60, // 最大尝试次数（5分钟）
      onProgress = null
    } = options;

    // 启动生成请求
    let attempt = 0;
    
    while (attempt < maxAttempts) {
      try {
        const result = await this.generateVideo(draftUrl, { timeout: 30000 });
        
        if (result.video_url) {
          if (onProgress) onProgress({ status: 'completed', result });
          return result;
        }
        
        if (onProgress) {
          onProgress({ 
            status: 'processing', 
            attempt: attempt + 1, 
            maxAttempts,
            message: result.message 
          });
        }
        
        // 等待下次轮询
        await new Promise(resolve => setTimeout(resolve, pollInterval));
        attempt++;
        
      } catch (error) {
        if (error.message.includes('超时')) {
          // 超时不算失败，继续轮询
          if (onProgress) {
            onProgress({ 
              status: 'processing', 
              attempt: attempt + 1, 
              maxAttempts,
              message: '处理中...' 
            });
          }
          await new Promise(resolve => setTimeout(resolve, pollInterval));
          attempt++;
        } else {
          throw error;
        }
      }
    }
    
    throw new Error('视频生成超时，请稍后重试');
  }

  // 批量生成视频
  async generateBatchVideos(draftUrls, options = {}) {
    const {
      concurrent = 2, // 并发数量
      onProgress = null
    } = options;

    const results = {};
    const entries = Object.entries(draftUrls);
    
    // 分批处理
    for (let i = 0; i < entries.length; i += concurrent) {
      const batch = entries.slice(i, i + concurrent);
      
      const batchPromises = batch.map(async ([name, url]) => {
        try {
          if (onProgress) {
            onProgress({ name, status: 'starting', url });
          }
          
          const result = await this.generateVideoWithPolling(url, {
            onProgress: (progress) => {
              if (onProgress) {
                onProgress({ name, ...progress, url });
              }
            }
          });
          
          results[name] = result;
          
          if (onProgress) {
            onProgress({ name, status: 'completed', result, url });
          }
          
        } catch (error) {
          console.error(`生成视频失败 ${name}:`, error);
          results[name] = { error: error.message };
          
          if (onProgress) {
            onProgress({ name, status: 'failed', error: error.message, url });
          }
        }
      });
      
      await Promise.all(batchPromises);
      
      // 批次间添加延迟
      if (i + concurrent < entries.length) {
        await new Promise(resolve => setTimeout(resolve, 1000));
      }
    }
    
    return results;
  }

  // 下载生成的视频
  async downloadVideo(videoUrl, filename = 'generated_video.mp4') {
    try {
      const response = await fetch(videoUrl);
      const blob = await response.blob();
      
      const downloadUrl = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = downloadUrl;
      link.download = filename;
      
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      
      window.URL.revokeObjectURL(downloadUrl);
      
      return true;
    } catch (error) {
      console.error('下载视频失败:', error);
      return false;
    }
  }
}

// 使用示例
const videoGenerator = new VideoGenerator();

// 单个视频生成
const draftUrl = "https://ts.fyshark.com/#/cozeToJianyin?drafId=...";

try {
  const result = await videoGenerator.generateVideoWithPolling(draftUrl, {
    onProgress: (progress) => {
      console.log(`生成进度: ${progress.status}`, progress);
      
      if (progress.status === 'processing') {
        console.log(`正在处理... (${progress.attempt}/${progress.maxAttempts})`);
      }
    }
  });
  
  console.log('视频生成成功:', result.video_url);
  
  // 下载视频
  await videoGenerator.downloadVideo(result.video_url, 'my_video.mp4');
  
} catch (error) {
  console.error('生成失败:', error);
}

// 批量生成视频
const multipleDrafts = {
  "video1": "https://ts.fyshark.com/#/cozeToJianyin?drafId=...draft1.json",
  "video2": "https://ts.fyshark.com/#/cozeToJianyin?drafId=...draft2.json",
  "video3": "https://ts.fyshark.com/#/cozeToJianyin?drafId=...draft3.json"
};

const batchResults = await videoGenerator.generateBatchVideos(multipleDrafts, {
  concurrent: 2,
  onProgress: (progress) => {
    console.log(`${progress.name}: ${progress.status}`);
  }
});

console.log('批量生成结果:', batchResults);

// 下载所有成功的视频
for (const [name, result] of Object.entries(batchResults)) {
  if (result.video_url && !result.error) {
    await videoGenerator.downloadVideo(result.video_url, `${name}.mp4`);
  }
}
```

### Python 示例

```python
import requests
import time
import asyncio
import aiohttp
from typing import Dict, Optional, Callable

class VideoGenerator:
    def __init__(self, base_url: str = "https://api.example.com"):
        self.base_url = base_url

    def generate_video(self, draft_url: str, timeout: int = 300) -> Dict:
        """生成视频"""
        response = requests.post(
            f'{self.base_url}/v1/gen_video',
            headers={'Content-Type': 'application/json'},
            json={"draft_url": draft_url},
            timeout=timeout
        )
        response.raise_for_status()
        return response.json()

    def generate_video_with_polling(self, draft_url: str, 
                                  poll_interval: int = 5, 
                                  max_attempts: int = 60,
                                  on_progress: Optional[Callable] = None) -> Dict:
        """轮询式视频生成"""
        attempt = 0
        
        while attempt < max_attempts:
            try:
                result = self.generate_video(draft_url, timeout=30)
                
                if result.get('video_url'):
                    if on_progress:
                        on_progress({'status': 'completed', 'result': result})
                    return result
                
                if on_progress:
                    on_progress({
                        'status': 'processing',
                        'attempt': attempt + 1,
                        'max_attempts': max_attempts,
                        'message': result.get('message', '处理中...')
                    })
                
                time.sleep(poll_interval)
                attempt += 1
                
            except requests.exceptions.Timeout:
                if on_progress:
                    on_progress({
                        'status': 'processing',
                        'attempt': attempt + 1,
                        'max_attempts': max_attempts,
                        'message': '处理中...'
                    })
                time.sleep(poll_interval)
                attempt += 1
            except Exception as e:
                raise e
        
        raise Exception('视频生成超时，请稍后重试')

    def generate_batch_videos(self, draft_urls: Dict[str, str], 
                            concurrent: int = 2,
                            on_progress: Optional[Callable] = None) -> Dict:
        """批量生成视频"""
        results = {}
        entries = list(draft_urls.items())
        
        # 分批处理
        for i in range(0, len(entries), concurrent):
            batch = entries[i:i + concurrent]
            batch_results = {}
            
            for name, url in batch:
                try:
                    if on_progress:
                        on_progress({'name': name, 'status': 'starting', 'url': url})
                    
                    def progress_callback(progress):
                        if on_progress:
                            on_progress({'name': name, **progress, 'url': url})
                    
                    result = self.generate_video_with_polling(
                        url, 
                        on_progress=progress_callback
                    )
                    
                    batch_results[name] = result
                    
                    if on_progress:
                        on_progress({'name': name, 'status': 'completed', 'result': result, 'url': url})
                        
                except Exception as e:
                    print(f"生成视频失败 {name}: {e}")
                    batch_results[name] = {'error': str(e)}
                    
                    if on_progress:
                        on_progress({'name': name, 'status': 'failed', 'error': str(e), 'url': url})
            
            results.update(batch_results)
            
            # 批次间延迟
            if i + concurrent < len(entries):
                time.sleep(1)
        
        return results

    def download_video(self, video_url: str, filename: str = "generated_video.mp4") -> bool:
        """下载视频"""
        try:
            response = requests.get(video_url, stream=True)
            response.raise_for_status()
            
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"视频已下载到: {filename}")
            return True
            
        except Exception as e:
            print(f"下载视频失败: {e}")
            return False

# 使用示例
generator = VideoGenerator()

# 单个视频生成
draft_url = "https://ts.fyshark.com/#/cozeToJianyin?drafId=example.json"

def on_progress(progress):
    print(f"生成进度: {progress['status']}")
    if progress['status'] == 'processing':
        print(f"正在处理... ({progress['attempt']}/{progress['max_attempts']})")

try:
    result = generator.generate_video_with_polling(
        draft_url, 
        on_progress=on_progress
    )
    
    print(f"视频生成成功: {result['video_url']}")
    
    # 下载视频
    generator.download_video(result['video_url'], 'my_video.mp4')
    
except Exception as e:
    print(f"生成失败: {e}")

# 批量生成
multiple_drafts = {
    "video1": "https://ts.fyshark.com/#/cozeToJianyin?drafId=draft1.json",
    "video2": "https://ts.fyshark.com/#/cozeToJianyin?drafId=draft2.json"
}

def batch_progress(progress):
    print(f"{progress['name']}: {progress['status']}")

batch_results = generator.generate_batch_videos(
    multiple_drafts,
    concurrent=2,
    on_progress=batch_progress
)

# 下载所有成功的视频
for name, result in batch_results.items():
    if 'video_url' in result and 'error' not in result:
        generator.download_video(result['video_url'], f'{name}.mp4')
```

## 错误码说明

| 错误码 | 错误信息 | 说明 | 解决方案 |
|--------|----------|------|----------|
| 400 | draft_url是必填项 | 缺少草稿URL参数 | 提供有效的draft_url |
| 400 | draft_url格式无效 | URL格式不正确 | 检查URL格式是否正确 |
| 404 | 草稿不存在 | 指定的草稿无法找到 | 确认草稿URL是否正确且存在 |
| 400 | 草稿内容为空 | 草稿中没有可导出的内容 | 确保草稿包含视频、音频或图片素材 |
| 400 | 素材无法访问 | 草稿中的素材文件无法下载 | 检查素材URL是否有效 |
| 500 | 视频渲染失败 | 视频处理过程中出错 | 检查草稿内容或联系技术支持 |
| 500 | 音频处理失败 | 音频混合过程中出错 | 检查音频格式或联系技术支持 |
| 500 | 编码失败 | 最终视频编码失败 | 联系技术支持 |
| 503 | 服务繁忙 | 渲染服务器负载过高 | 稍后重试 |
| 504 | 处理超时 | 视频生成超时 | 简化草稿内容或稍后重试 |

## 注意事项

1. **处理时间**: 视频生成是耗时操作，可能需要几分钟到几十分钟
2. **文件大小**: 草稿复杂度和素材数量会影响处理时间
3. **网络稳定**: 确保素材URL可以稳定访问
4. **超时设置**: 建议设置较长的超时时间或使用轮询机制
5. **并发限制**: 避免同时生成大量视频
6. **存储空间**: 生成的视频文件可能很大，注意存储空间
7. **URL有效期**: 生成的video_url可能有时效性限制

## 工作流程

1. 验证draft_url参数
2. 解析草稿配置文件
3. 下载所有必需的素材文件
4. 按时间轴排列和处理素材
5. 应用视觉效果和转场
6. 混合音频轨道
7. 渲染最终视频
8. 编码并上传视频文件
9. 返回视频URL

## 最佳实践

1. **轮询检查**: 对于长时间处理，使用轮询机制
2. **错误重试**: 实现自动重试机制
3. **进度反馈**: 向用户显示处理进度
4. **批量处理**: 合理控制并发数量
5. **资源清理**: 及时清理临时文件
6. **质量控制**: 生成前验证草稿内容的完整性

## 相关接口

- [创建草稿](./create_draft.md)
- [保存草稿](./save_draft.md)
- [添加视频](./add_videos.md)
- [添加音频](./add_audios.md)
- [添加图片](./add_images.md)
- [获取草稿](./get_draft.md)