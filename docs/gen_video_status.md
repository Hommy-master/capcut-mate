# gen_video_status 接口文档

## 接口概述

**接口名称**：gen_video_status  
**接口地址**：`POST /openapi/capcut-mate/v1/gen_video_status`  
**功能描述**：查询视频生成任务的状态和进度。配合 gen_video 接口使用，用于实时跟踪视频生成任务的执行情况，包括任务状态、进度百分比、完成结果等信息。

## 更多文档

📖 更多详细文档和教程请访问：[https://docs.jcaigc.cn](https://docs.jcaigc.cn)

## 请求参数

### 请求体 (application/json)

| 参数名 | 类型 | 必填 | 默认值 | 描述 |
|--------|------|------|--------|------|
| draft_url | string | 是 | - | 草稿URL，与提交任务时使用的URL相同 |

## 请求示例

```json
{
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258"
}
```

## 响应格式

### 成功响应

#### 任务等待中

```json
{
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
  "status": "pending",
  "progress": 0,
  "video_url": "",
  "error_message": "",
  "created_at": "2024-09-24T10:30:00.000Z",
  "started_at": null,
  "completed_at": null
}
```

#### 任务处理中

```json
{
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258", 
  "status": "processing",
  "progress": 65,
  "video_url": "",
  "error_message": "",
  "created_at": "2024-09-24T10:30:00.000Z",
  "started_at": "2024-09-24T10:30:05.000Z",
  "completed_at": null
}
```

#### 任务已完成

```json
{
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
  "status": "completed",
  "progress": 100,
  "video_url": "https://video-output.assets.jcaigc.cn/generated/video_abc123def456ghi789.mp4",
  "error_message": "",
  "created_at": "2024-09-24T10:30:00.000Z",
  "started_at": "2024-09-24T10:30:05.000Z",
  "completed_at": "2024-09-24T10:35:30.000Z"
}
```

#### 任务失败

```json
{
  "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258",
  "status": "failed",
  "progress": 0,
  "video_url": "",
  "error_message": "导出草稿失败: 剪映导出结束但目标文件未生成，请检查磁盘空间或剪映版本",
  "created_at": "2024-09-24T10:30:00.000Z",
  "started_at": "2024-09-24T10:30:05.000Z",
  "completed_at": "2024-09-24T10:32:15.000Z"
}
```

### 响应字段说明

| 字段名 | 类型 | 描述 |
|--------|------|------|
| draft_url | string | 草稿URL |
| status | string | 任务状态：pending/processing/completed/failed |
| progress | integer | 任务进度（0-100） |
| video_url | string | 生成的视频URL（仅在completed状态时有值） |
| error_message | string | 错误信息（仅在failed状态时有值） |
| created_at | string | 任务创建时间（ISO格式） |
| started_at | string\|null | 任务开始时间（ISO格式） |
| completed_at | string\|null | 任务完成时间（ISO格式） |

### 任务状态说明

| 状态值 | 状态名称 | 描述 | 进度范围 |
|--------|----------|------|----------|
| pending | 等待中 | 任务已提交，等待处理 | 0 |
| processing | 处理中 | 任务正在执行中 | 10-90 |
| completed | 已完成 | 任务成功完成 | 100 |
| failed | 失败 | 任务执行失败 | 0 |

### 进度说明

进度百分比对应的处理阶段：

| 进度范围 | 处理阶段 | 说明 |
|----------|----------|------|
| 0% | 等待中 | 任务在队列中等待 |
| 10% | 开始处理 | 任务开始执行 |
| 20% | 草稿解析 | 解析草稿配置 |
| 30% | 准备环境 | 初始化剪映环境 |
| 50% | 素材处理 | 处理素材和效果 |
| 70% | 导出控制 | 控制剪映导出 |
| 90% | 文件生成 | 生成视频文件 |
| 100% | 完成 | 任务完成 |

### 错误响应

#### 404 Not Found - 任务不存在

```json
{
  "error": {
    "code": "VIDEO_TASK_NOT_FOUND",
    "message": "视频生成任务未找到",
    "details": "指定的草稿URL没有对应的视频生成任务"
  }
}
```

#### 500 Internal Server Error - 查询失败

```json
{
  "error": {
    "code": "VIDEO_STATUS_QUERY_FAILED",
    "message": "视频任务状态查询失败",
    "details": "系统内部错误"
  }
}
```

## 错误码说明

| 错误码 | HTTP状态码 | 描述 | 解决方案 |
|--------|------------|------|----------|
| VALIDATION_ERROR | 400 | 请求参数验证失败 | 检查draft_url参数格式是否正确 |
| VIDEO_TASK_NOT_FOUND | 404 | 视频生成任务未找到 | 确认是否已通过gen_video接口提交任务 |
| VIDEO_STATUS_QUERY_FAILED | 500 | 状态查询失败 | 稍后重试或联系技术支持 |

## 使用说明

### 轮询查询

建议使用轮询方式查询任务状态：

1. **轮询间隔**：建议每5-10秒查询一次
2. **超时设置**：建议设置总超时时间（如10分钟）
3. **错误处理**：处理网络错误和任务失败情况

### 最佳实践

1. **及时查询**：任务提交后立即开始查询
2. **进度显示**：利用progress字段显示进度条
3. **状态处理**：根据不同状态提供不同的用户反馈
4. **错误处理**：妥善处理任务失败情况

## 示例代码

### JavaScript 轮询示例

```javascript
async function pollVideoStatus(draftUrl, maxAttempts = 120) {
  let attempts = 0;
  const pollInterval = 5000; // 5秒间隔
  
  while (attempts < maxAttempts) {
    try {
      const response = await fetch('/openapi/capcut-mate/v1/gen_video_status', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ draft_url: draftUrl })
      });
      
      const status = await response.json();
      
      console.log(`任务状态: ${status.status}, 进度: ${status.progress}%`);
      
      if (status.status === 'completed') {
        console.log('视频生成完成:', status.video_url);
        return status;
      }
      
      if (status.status === 'failed') {
        throw new Error(`任务失败: ${status.error_message}`);
      }
      
      // 等待后继续轮询
      await new Promise(resolve => setTimeout(resolve, pollInterval));
      attempts++;
      
    } catch (error) {
      console.error('查询状态失败:', error);
      attempts++;
      await new Promise(resolve => setTimeout(resolve, pollInterval));
    }
  }
  
  throw new Error('任务超时');
}

// 使用示例
const draftUrl = "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258";

try {
  const result = await pollVideoStatus(draftUrl);
  console.log('视频生成成功:', result.video_url);
} catch (error) {
  console.error('视频生成失败:', error);
}
```

### Python 轮询示例

```python
import requests
import time
import json

def poll_video_status(draft_url, max_attempts=120, poll_interval=5):
    """轮询查询视频生成状态"""
    url = 'http://localhost:8000/v1/gen_video_status'
    
    for attempt in range(max_attempts):
        try:
            response = requests.post(url, json={'draft_url': draft_url})
            if response.status_code == 200:
                status = response.json()
                
                print(f"任务状态: {status['status']}, 进度: {status['progress']}%")
                
                if status['status'] == 'completed':
                    print(f"视频生成完成: {status['video_url']}")
                    return status
                
                if status['status'] == 'failed':
                    raise Exception(f"任务失败: {status['error_message']}")
                
            else:
                print(f"查询失败: {response.status_code}")
            
        except requests.RequestException as e:
            print(f"网络错误: {e}")
        
        # 等待后继续轮询
        time.sleep(poll_interval)
    
    raise Exception("任务超时")

# 使用示例
if __name__ == "__main__":
    draft_url = "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2025092811473036584258"
    
    try:
        result = poll_video_status(draft_url)
        print(f"视频生成成功: {result['video_url']}")
    except Exception as e:
        print(f"视频生成失败: {e}")
```

### 完整工作流程

```javascript
// 完整的视频生成工作流程
async function generateVideoWorkflow(draftUrl) {
  try {
    // 1. 提交视频生成任务
    console.log('提交视频生成任务...');
    const submitResponse = await fetch('/v1/gen_video', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ draft_url: draftUrl })
    });
    
    const submitResult = await submitResponse.json();
    console.log(`任务已提交: ${submitResult.message}`);
    
    // 2. 轮询查询任务状态
    console.log('开始查询任务状态...');
    const finalResult = await pollVideoStatus(draftUrl);
    
    // 3. 处理完成结果
    if (finalResult.video_url) {
      console.log('视频生成成功！');
      
      // 可以进行后续操作，如下载视频
      const downloadLink = document.createElement('a');
      downloadLink.href = finalResult.video_url;
      downloadLink.download = 'generated_video.mp4';
      downloadLink.click();
      
      return finalResult.video_url;
    }
    
  } catch (error) {
    console.error('视频生成工作流程失败:', error);
    throw error;
  }
}
```

## 相关接口

- [gen_video](./gen_video.md) - 提交视频生成任务
- [create_draft](./create_draft.md) - 创建新的草稿文件
- [save_draft](./save_draft.md) - 保存草稿文件

## 技术实现

### 文件结构

```
src/
├── schemas/gen_video_status.py       # 请求/响应数据模型
├── service/gen_video.py              # 业务逻辑实现
├── utils/video_task_manager.py       # 任务队列管理
└── router/v1.py                      # API路由定义
```

### 核心逻辑

1. **参数验证**：验证草稿URL的有效性
2. **任务查询**：从任务管理器中查询任务状态
3. **状态转换**：将内部状态转换为API响应格式
4. **错误处理**：处理任务不存在和查询失败的情况

---

**版本信息**：v1.0  
**最后更新**：2024-09-24