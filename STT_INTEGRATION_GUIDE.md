# 🎤 语音识别（STT）集成指南

---

## 🎯 功能概述

**完整的语音交互流程：**

```
用户说话 → 🎤 录音 → 🔄 语音识别（STT） → 📝 文字
                                        ↓
用户听语音 ← 🔊 播放 ← 🤖 TTS 生成 ← 💬 AI 回复
```

---

## 📦 系统架构

### 服务组成

| 服务 | 端口 | 功能 | 状态 |
|------|------|------|------|
| **Web 服务** | 7091 | 语音交互页面 | ✅ 运行中 |
| **TTS API** | 7086 | 文字转语音 | ✅ 运行中 |
| **STT API** | 5050 | 语音转文字 | ⏳ 待启动 |

---

## 🚀 快速开始

### 步骤 1：安装 Whisper（语音识别引擎）

**Whisper** 是 OpenAI 的开源语音识别模型，支持中文。

```bash
# 安装 Whisper
pip install openai-whisper
```

**或者使用 uv（更快）：**
```bash
uv pip install openai-whisper
```

---

### 步骤 2：启动 STT 服务

```bash
cd /home/admin/projects/live-tts
bash start_stt_service.sh
```

**输出：**
```
======================================
🎤 启动语音识别服务（STT）
======================================
🚀 启动 STT 服务（端口 5050）...
✅ STT 服务已启动
   进程 ID: 123456
   日志：logs/stt_service.log

✅ 服务运行正常
{
    "status": "ok",
    "engine": "whisper",
    "service": "Speech-to-Text API"
}
```

---

### 步骤 3：重启 Web 服务

```bash
# 停止旧服务
pkill -f flask_voice_server

# 启动新服务
cd /home/admin/projects/live-tts
python3 flask_voice_server.py > logs/flask_voice.log 2>&1 &
```

---

### 步骤 4：测试语音输入

**访问：**
```
https://young-lizards-open.loca.lt/voice_chat.html
```

**操作：**
1. 点击"🎤 按住说话"
2. 说话（例如："你好"）
3. 松开结束
4. 等待识别
5. 听语音回复！

---

## 🔧 配置选项

### 语音识别引擎

**编辑 `stt_service.py`：**

```python
# 选择引擎
STT_ENGINE = os.getenv('STT_ENGINE', 'whisper')  # whisper/azure/google/baidu
```

#### 引擎对比

| 引擎 | 成本 | 准确率 | 速度 | 推荐 |
|------|------|--------|------|------|
| **Whisper** | 免费 | ⭐⭐⭐⭐ | 中 | ⭐⭐⭐ 推荐 |
| **Azure Speech** | 付费 | ⭐⭐⭐⭐⭐ | 快 | ⭐⭐⭐⭐ |
| **Google Speech** | 付费 | ⭐⭐⭐⭐⭐ | 快 | ⭐⭐⭐⭐ |
| **百度语音** | 免费/付费 | ⭐⭐⭐⭐ | 快 | ⭐⭐⭐ 国内 |

---

### Azure Speech 配置

**步骤 1：创建 Azure 账号**
```
https://azure.microsoft.com/zh-cn/free/
```

**步骤 2：创建 Speech 资源**
```
Azure 门户 → 创建资源 → AI + 机器学习 → 语音服务
```

**步骤 3：获取 Key 和 Region**
```
密钥和终结点 → KEY1 → 复制
区域 → eastasia（东亚）
```

**步骤 4：配置环境变量**
```bash
export AZURE_SPEECH_KEY="你的密钥"
export AZURE_SPEECH_REGION="eastasia"
```

**步骤 5：安装 SDK**
```bash
pip install azure-cognitiveservices-speech
```

---

### Google Speech 配置

**步骤 1：创建 Google Cloud 项目**
```
https://console.cloud.google.com/
```

**步骤 2：启用 Speech-to-Text API**

**步骤 3：创建服务账号密钥**
```
IAM 和管理 → 服务账号 → 创建服务账号 → JSON
```

**步骤 4：配置环境变量**
```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/key.json"
```

**步骤 5：安装 SDK**
```bash
pip install google-cloud-speech
```

---

## 📊 API 端点

### STT API（5050 端口）

#### 1. 健康检查

```bash
GET http://localhost:5050/health

响应：
{
    "status": "ok",
    "engine": "whisper",
    "service": "Speech-to-Text API"
}
```

---

#### 2. 语音转文字（文件上传）

```bash
POST http://localhost:5050/transcribe
Content-Type: multipart/form-data

参数：
- audio: 音频文件（webm/wav/mp3）

响应：
{
    "text": "你好，世界",
    "success": true,
    "engine": "whisper"
}
```

---

#### 3. 语音转文字（Base64）

```bash
POST http://localhost:5050/transcribe_base64
Content-Type: application/json

{
    "audio": "base64_encoded_audio_data"
}

响应：
{
    "text": "你好，世界",
    "success": true
}
```

---

### TTS API（7086 端口）

#### 文字转语音

```bash
POST http://localhost:7086/speak
Content-Type: application/json

{
    "text": "你好",
    "scene": "default"
}

响应：
{
    "success": true,
    "filename": "speech_20260409_150000.mp3"
}
```

---

## 🎨 前端集成

### 语音识别流程

```javascript
async function processAudio(audioBlob) {
    // 步骤 1：语音识别（STT）
    const sttFormData = new FormData();
    sttFormData.append('audio', audioBlob);
    
    const sttResponse = await fetch('/api/transcribe', {
        method: 'POST',
        body: sttFormData
    });
    const sttData = await sttResponse.json();
    
    const recognizedText = sttData.text;
    
    // 步骤 2：调用 TTS 生成语音回复
    const response = await fetch('/api/speak', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: recognizedText, scene: 'default' })
    });
    const data = await response.json();
    
    // 步骤 3：播放语音
    const audio = new Audio(`/api/audio/${data.filename}`);
    audio.play();
}
```

---

## 🔍 故障排查

### 问题 1：Whisper 安装失败

**错误：**
```
ERROR: Could not find a version that satisfies the requirement openai-whisper
```

**解决：**
```bash
# 升级 pip
pip install --upgrade pip

# 安装 PyTorch（依赖）
pip install torch torchaudio

# 重新安装 Whisper
pip install openai-whisper
```

---

### 问题 2：STT 服务启动失败

**检查日志：**
```bash
tail -f logs/stt_service.log
```

**常见错误：**
```
ModuleNotFoundError: No module named 'whisper'
```

**解决：**
```bash
pip install openai-whisper
```

---

### 问题 3：语音识别超时

**错误：**
```
错误：语音识别超时
```

**原因：** Whisper 模型较大，首次运行需要下载

**解决：**
```bash
# 预下载模型
python3 -c "import whisper; whisper.load_model('base')"
```

---

### 问题 4：识别结果不准确

**优化方法：**

1. **使用更大的模型**
   ```python
   # 编辑 stt_service.py
   ['whisper', audio_file, '--model', 'large', ...]
   ```
   
   模型大小：tiny < base < small < medium < large

2. **提高录音质量**
   - 使用更好的麦克风
   - 减少环境噪音
   - 说话清晰

3. **切换引擎**
   - Azure Speech（准确率最高）
   - Google Speech（多语言支持好）

---

## 📈 性能优化

### 1. 使用 GPU 加速

**安装 CUDA 版本：**
```bash
pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu118
pip install openai-whisper
```

**速度提升：**
- CPU: ~10 秒/分钟音频
- GPU: ~1 秒/分钟音频（10 倍提升）

---

### 2. 缓存常用识别结果

```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def transcribe_cached(audio_hash: str) -> str:
    # 缓存识别结果
    pass
```

---

### 3. 流式识别

**实时识别（边说边识别）：**
```python
# 使用 Azure 流式 API
recognizer.recognize_continuous()
```

---

## 🎊 完整测试流程

### 测试脚本

```bash
#!/bin/bash
# test_stt.sh

echo "🎤 测试语音识别..."

# 1. 检查服务
curl http://localhost:5050/health

# 2. 测试识别
curl -X POST http://localhost:5050/transcribe \
  -F "audio=@test_audio.webm"

# 3. 检查响应时间
time curl -X POST http://localhost:5050/transcribe \
  -F "audio=@test_audio.webm"
```

---

### 手动测试

**步骤 1：录制测试音频**
```bash
# 使用 arecord（Linux）
arecord -f cd -t wav -d 5 test.wav
```

**步骤 2：识别**
```bash
curl -X POST http://localhost:5050/transcribe \
  -F "audio=@test.wav"
```

**步骤 3：验证**
```json
{
    "text": "测试音频内容",
    "success": true
}
```

---

## 📖 相关文档

| 文档 | 说明 |
|------|------|
| `stt_service.py` | STT 服务代码（7.9KB） |
| `start_stt_service.sh` | 启动脚本 |
| `ENABLE_HTTPS_GUIDE.md` | HTTPS 配置指南 |
| `TEXT_INPUT_GUIDE.md` | 文字输入指南 |

---

## 🎯 下一步

### 已完成
- ✅ STT 服务代码
- ✅ Flask 代理集成
- ✅ 前端语音识别流程
- ✅ 多引擎支持

### 待完成
- ⏳ 安装 Whisper
- ⏳ 启动 STT 服务
- ⏳ 完整测试

---

**更新时间**: 2026-04-09  
**STT 服务**: `/home/admin/projects/live-tts/stt_service.py`  
**启动脚本**: `/home/admin/projects/live-tts/start_stt_service.sh`  
**推荐引擎**: Whisper（免费，本地，中文支持好）
