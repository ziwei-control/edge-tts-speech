# ✅ 音频 URL 跨域问题修复

---

## ⚠️ 问题

**错误信息**:
```
HTTPConnectionPool(host='localhost', port=7086): 
Max retries exceeded with url: /speak 
(Caused by NewConnectionError("HTTPConnection(host='localhost', port=7086): 
Failed to establish a new connection: [Errno 111] Connection refused"))
```

**原因分析**:
1. TTS API 服务运行在 `localhost:7086`
2. 返回的音频 URL 是 `http://localhost:7086/audio/xxx.mp3`
3. Localtunnel 是 HTTPS，无法访问 HTTP localhost
4. 浏览器 CORS 策略阻止跨域请求

---

## ✅ 解决方案

### 架构优化

**之前（失败）**:
```
用户浏览器 (HTTPS)
  ↓
Flask 代理 (7091)
  ↓
TTS API (7086) → 返回 http://localhost:7086/audio/xxx.mp3 ❌
  ↓
用户浏览器无法访问 localhost ❌
```

---

**现在（成功）**:
```
用户浏览器 (HTTPS)
  ↓
Flask 代理 (7091)
  ├─ /api/speak → 代理到 TTS API (7086)
  ├─ /api/audio/{file} → 代理音频文件
  └─ 返回 /api/audio/xxx.mp3 (相对路径) ✅
  ↓
用户浏览器访问同域音频 ✅
```

---

### 代码修改

#### 1. 修改 `/api/speak` 端点

**文件**: `flask_voice_server.py`

**修改前**:
```python
@app.route('/api/speak', methods=['POST'])
def speak():
    """代理 TTS 生成"""
    try:
        data = request.get_json()
        resp = requests.post(f"{TTS_API_URL}/speak", json=data, timeout=30)
        return jsonify(resp.json())
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
```

**修改后**:
```python
@app.route('/api/speak', methods=['POST'])
def speak():
    """代理 TTS 生成"""
    try:
        data = request.get_json()
        resp = requests.post(f"{TTS_API_URL}/speak", json=data, timeout=30)
        result = resp.json()
        
        # 修改音频 URL 为当前服务器的路径
        if result.get('success') and result.get('filename'):
            result['url'] = f"/api/audio/{result['filename']}"
        
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
```

**关键改动**:
- 解析 TTS API 返回的 JSON
- 将 `url` 字段改为相对路径 `/api/audio/{filename}`
- 返回修改后的结果

---

#### 2. 优化音频文件端点

**修改前**:
```python
@app.route('/api/audio/<filename>')
def audio(filename):
    """代理音频文件"""
    try:
        filepath = f"output/api/{filename}"
        return send_from_directory("output/api", filename)
    except Exception as e:
        return jsonify({"error": str(e)}), 404
```

**修改后**:
```python
@app.route('/api/audio/<filename>')
def audio(filename):
    """代理音频文件"""
    try:
        return send_from_directory("output/api", filename)
    except Exception as e:
        return jsonify({"error": str(e)}), 404

@app.route('/api/audio_info/<filename>')
def audio_info(filename):
    """获取音频信息（用于调试）"""
    try:
        filepath = f"output/api/{filename}"
        if os.path.exists(filepath):
            size = os.path.getsize(filepath)
            return jsonify({
                "exists": True,
                "size": size,
                "filename": filename
            })
        else:
            return jsonify({"exists": False, "filename": filename}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
```

**关键改动**:
- 简化 `audio()` 函数
- 添加 `audio_info()` 调试端点
- 方便检查音频文件是否存在

---

## 🧪 测试验证

### 测试 1: TTS 生成

**请求**:
```bash
curl -X POST http://localhost:7091/api/speak \
  -H "Content-Type: application/json" \
  -d '{"text":"你好测试","scene":"default","voice":"xiaoxiao"}'
```

**响应**:
```json
{
  "duration_estimate": "1.2 秒",
  "filename": "speech_20260409_172737.mp3",
  "filepath": "output/api/speech_20260409_172737.mp3",
  "scene": "default",
  "success": true,
  "text": "你好测试",
  "url": "/api/audio/speech_20260409_172737.mp3",  ⭐ 相对路径
  "voice": "xiaoxiao"
}
```

**验证**:
- ✅ `url` 字段是相对路径
- ✅ 不再是 `localhost:7086`

---

### 测试 2: 音频文件访问

**请求**:
```bash
curl -I http://localhost:7091/api/audio/speech_20260409_172737.mp3
```

**响应**:
```
HTTP/1.0 200 OK
Content-Type: audio/mpeg
Content-Length: 19234
```

**验证**:
- ✅ HTTP 200 OK
- ✅ 音频文件可访问

---

### 测试 3: 音频信息（调试）

**请求**:
```bash
curl http://localhost:7091/api/audio_info/speech_20260409_172737.mp3
```

**响应**:
```json
{
  "exists": true,
  "filename": "speech_20260409_172737.mp3",
  "size": 19234
}
```

**验证**:
- ✅ 文件存在
- ✅ 显示文件大小

---

### 测试 4: 完整流程（浏览器）

**步骤**:
1. 打开页面
   ```
   https://afraid-ads-kick.loca.lt/voice_chat.html
   ```

2. 选择音色（如 xiaoxiao）

3. 输入文字："你好"

4. 点击"发送"

5. **预期结果**:
   - ✅ 显示机器人回复
   - ✅ 自动播放音频
   - ✅ 无 CORS 错误

---

## 📊 数据流对比

### 之前（失败）

```
1. 用户发送文字
   ↓
2. Flask 代理 → TTS API (7086)
   ↓
3. TTS API 返回: {"url": "http://localhost:7086/audio/xxx.mp3"}
   ↓
4. 浏览器尝试访问 localhost:7086
   ↓
5. ❌ 失败（HTTPS 无法访问 HTTP localhost）
```

---

### 现在（成功）

```
1. 用户发送文字
   ↓
2. Flask 代理 → TTS API (7086)
   ↓
3. Flask 修改 URL: {"url": "/api/audio/xxx.mp3"}
   ↓
4. 浏览器访问同域 /api/audio/xxx.mp3
   ↓
5. Flask 代理音频文件 → 返回 MP3
   ↓
6. ✅ 成功播放
```

---

## 🔧 服务状态

### 运行中的服务

| 服务 | 端口 | 状态 | 说明 |
|------|------|------|------|
| **TTS API** | 7086 | ✅ 运行中 | 文字转语音 |
| **Flask 代理** | 7091 | ✅ 运行中 | Web+API 代理 |
| **STT API** | 5050 | ✅ 运行中 | 语音识别 |
| **Localtunnel** | - | ✅ 运行中 | HTTPS 隧道 |

---

### 检查命令

**检查 TTS API**:
```bash
curl http://localhost:7086/health
# 应返回：{"status":"ok",...}
```

**检查 Flask 代理**:
```bash
curl http://localhost:7091/api/health
# 应返回：{"status":"ok",...}
```

**检查 STT API**:
```bash
curl http://localhost:5050/health
# 应返回：{"status":"ok",...}
```

---

## 🎯 完整测试流程

### 1. 检查所有服务

```bash
# TTS API
curl http://localhost:7086/health

# Flask 代理
curl http://localhost:7091/api/health

# STT API (如果已安装)
curl http://localhost:5050/health
```

---

### 2. 测试 TTS 生成

```bash
curl -X POST http://localhost:7091/api/speak \
  -H "Content-Type: application/json" \
  -d '{"text":"测试音频","scene":"default","voice":"xiaoxiao"}'
```

**应返回**:
```json
{
  "success": true,
  "url": "/api/audio/speech_xxx.mp3",
  ...
}
```

---

### 3. 测试音频播放

```bash
# 获取文件名（从上一步）
curl -I http://localhost:7091/api/audio/speech_xxx.mp3
```

**应返回**:
```
HTTP/1.0 200 OK
Content-Type: audio/mpeg
```

---

### 4. 浏览器测试

**访问**:
```
https://afraid-ads-kick.loca.lt/voice_chat.html
```

**操作**:
1. 选择音色
2. 输入文字
3. 发送
4. 听语音回复

**预期**:
- ✅ 无错误
- ✅ 自动播放

---

## 📖 相关文件

| 文件 | 说明 | 状态 |
|------|------|------|
| **flask_voice_server.py** | Flask 代理服务器 | ✅ 已修复 |
| **agent_tts_api.py** | TTS API 服务 | ✅ 运行中 |
| **voice_chat.html** | 语音对话页面 | ✅ 已更新 |
| **AUDIO_URL_FIX.md** | 本文档 | ✅ 新增 |

---

## 🚀 未来优化

### 1. 音频缓存

**添加缓存头**:
```python
@app.route('/api/audio/<filename>')
def audio(filename):
    response = send_from_directory("output/api", filename)
    response.headers['Cache-Control'] = 'public, max-age=3600'
    return response
```

**效果**: 浏览器缓存 1 小时，减少重复请求

---

### 2. 音频流式传输

**支持 Range 请求**:
```python
from flask import send_file, request

@app.route('/api/audio/<filename>')
def audio(filename):
    filepath = f"output/api/{filename}"
    return send_file(
        filepath,
        mimetype='audio/mpeg',
        conditional=True  # 支持 Range
    )
```

**效果**: 支持拖拽进度条

---

### 3. 音频清理

**定时清理旧音频**:
```python
import time
from datetime import datetime, timedelta

def cleanup_old_audio():
    """清理 24 小时前的音频"""
    cutoff = datetime.now() - timedelta(hours=24)
    for filename in os.listdir('output/api'):
        filepath = f'output/api/{filename}'
        mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
        if mtime < cutoff:
            os.remove(filepath)
```

**效果**: 节省磁盘空间

---

## ✅ 总结

**问题**: TTS API 返回 localhost URL，Localtunnel 无法访问  
**解决**: Flask 代理音频文件，返回相对路径  
**状态**: ✅ 已修复  

**关键改动**:
- ✅ `/api/speak` 修改 URL 为相对路径
- ✅ `/api/audio/{file}` 代理音频文件
- ✅ `/api/audio_info/{file}` 调试端点

**立即测试**:
```
https://afraid-ads-kick.loca.lt/voice_chat.html
```

**应该可以正常播放语音了！** 🎵✨

---

**修复时间**: 2026-04-09 17:27  
**提交**: 2031de2  
**状态**: ✅ 运行正常
