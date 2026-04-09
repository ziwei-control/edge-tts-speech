# ✅ STT 语音识别服务修复

---

## ⚠️ 问题

**错误信息**:
```
识别失败：HTTPConnectionPool(host='localhost', port=5050): 
Max retries exceeded with url: /transcribe 
(Caused by NewConnectionError("HTTPConnection(host='localhost', port=5050): 
Failed to establish a new connection: [Errno 111] Connection refused"))
```

**原因**:
- STT 语音识别服务未运行
- 端口 5050 没有服务监听
- 导致语音识别请求失败

---

## ✅ 解决方案

### 1. 启动 STT 服务

**命令**:
```bash
cd /home/admin/projects/live-tts
python3 stt_service.py > /tmp/stt.log 2>&1 &
```

**验证**:
```bash
curl http://localhost:5050/health
```

**应返回**:
```json
{
  "engine": "whisper",
  "service": "Speech-to-Text API",
  "status": "ok"
}
```

---

### 2. 更新一键启动脚本

**文件**: `start_everything_v2.sh`

**新增内容**:
```bash
# 2. 启动 STT 服务
echo "🎤 启动 STT 语音识别服务 (5050)..."
cd /home/admin/projects/live-tts
nohup python3 stt_service.py > /tmp/stt.log 2>&1 &
sleep 3

# 检查 STT
if curl -s http://localhost:5050/health > /dev/null 2>&1; then
    echo "✅ STT 服务启动成功"
else
    echo "❌ STT 服务启动失败，检查日志：/tmp/stt.log"
fi
```

**功能**:
- ✅ 自动启动 STT 服务
- ✅ 健康检查验证
- ✅ 错误日志记录

---

## 📊 完整服务架构

### 语音对话流程

```
1. 用户按住说话 → 录音（前端浏览器）
   ↓
2. 上传音频 → /api/transcribe（Flask 代理 7091）
   ↓
3. 代理转发 → STT 服务（5050 端口）
   ↓
4. 语音识别 → Whisper 引擎
   ↓
5. 返回文字 → Flask 代理
   ↓
6. 显示文字消息 → 调用 TTS API（7086 端口）
   ↓
7. 生成语音 → Edge TTS
   ↓
8. 返回音频 → 自动播放
```

---

## 🔧 服务状态

### 运行中的服务

| 服务 | 端口 | 进程 | 状态 | 功能 |
|------|------|------|------|------|
| **STT** | 5050 | stt_service.py | ✅ 运行中 | 语音识别 |
| **TTS API** | 7086 | agent_tts_api.py | ✅ 运行中 | 文字转语音 |
| **Flask 代理** | 7091 | flask_voice_server.py | ✅ 运行中 | Web+API 代理 |
| **Localtunnel** | - | lt --port 7091 | ✅ 运行中 | HTTPS 隧道 |

---

### 检查命令

**检查 STT 服务**:
```bash
ps aux | grep "stt_service.py" | grep -v grep
curl http://localhost:5050/health
```

**检查 TTS API**:
```bash
ps aux | grep "agent_tts_api.py" | grep -v grep
curl http://localhost:7086/health
```

**检查 Flask 代理**:
```bash
ps aux | grep "flask_voice_server.py" | grep -v grep
curl http://localhost:7091/api/health
```

**检查 Localtunnel**:
```bash
ps aux | grep "lt --port" | grep -v grep
cat /tmp/lt.log
```

---

##  完整测试流程

### 测试 1: STT 服务健康检查

**命令**:
```bash
curl http://localhost:5050/health
```

**预期**:
```json
{"engine":"whisper","service":"Speech-to-Text API","status":"ok"}
```

---

### 测试 2: 语音识别 API

**准备音频文件** (测试用):
```bash
# 录制 3 秒音频（需要麦克风）
# 或使用现有音频文件
```

**请求**:
```bash
curl -X POST http://localhost:5050/transcribe \
  -F "audio=@test_audio.wav"
```

**预期**:
```json
{
  "success": true,
  "text": "你好测试"
}
```

---

### 测试 3: 完整语音对话（浏览器）

**步骤**:
1. 打开页面
   ```
   https://fast-items-clean.loca.lt/voice_chat.html
   ```

2. 点击"高级 → 继续访问"（首次）

3. ✅ 点击"按住说话"按钮

4. ✅ 说话（如"你好"）

5. ✅ 松开按钮

6. **预期结果**:
   - ✅ 显示"正在识别..."
   - ✅ 显示识别的文字
   - ✅ 生成语音回复
   - ✅ 自动播放语音

---

## 📖 STT 引擎说明

### Whisper（本地免费）

**优点**:
- ✅ 免费开源
- ✅ 本地运行，无需网络
- ✅ 支持多语言
- ✅ 准确率高

**缺点**:
- ⚠️ 需要 GPU 加速（CPU 也可但较慢）
- ⚠️ 首次加载模型需要时间
- ⚠️ 占用内存较大（~500MB）

**安装**:
```bash
pip install openai-whisper
```

---

### Azure Speech（备选）

**优点**:
- ✅ 准确率高
- ✅ 响应快
- ✅ 支持实时识别

**缺点**:
- ⚠️ 需要 API Key
- ⚠️ 按调用次数收费

**配置**:
在 `stt_service.py` 中设置：
```python
AZURE_SPEECH_KEY = "your_key"
AZURE_SPEECH_REGION = "eastasia"
```

---

### Google Cloud Speech（备选）

**优点**:
- ✅ 准确率最高
- ✅ 支持多语言
- ✅ 实时识别

**缺点**:
- ⚠️ 需要 API Key
- ⚠️ 需要信用卡

---

### 百度语音（备选）

**优点**:
- ✅ 中文识别好
- ✅ 免费额度
- ✅ 国内访问快

**缺点**:
- ⚠️ 需要 API Key
- ⚠️ 需要实名认证

---

## 🔧 故障排查

### 问题 1: STT 服务无法启动

**检查日志**:
```bash
cat /tmp/stt.log
```

**常见错误**:
- `ModuleNotFoundError: No module named 'whisper'`
  - 解决：`pip install openai-whisper`
- `Port 5050 already in use`
  - 解决：`pkill -f stt_service.py` 然后重启

---

### 问题 2: 语音识别超时

**原因**:
- 音频文件太大
- CPU 负载高
- 模型加载慢

**解决**:
1. 限制录音时长（建议 30 秒内）
2. 使用 GPU 加速
3. 预热模型（启动时加载）

---

### 问题 3: 识别准确率低

**优化建议**:
1. 使用清晰麦克风
2. 减少环境噪音
3. 说话速度适中
4. 使用标准普通话

---

## 📊 性能优化

### 1. 模型预热

**修改 `stt_service.py`**:
```python
# 启动时加载模型
print("🔧 加载 Whisper 模型...")
model = whisper.load_model("base")
print("✅ 模型加载完成")
```

**效果**: 首次识别不再延迟

---

### 2. 音频压缩

**前端优化**:
```javascript
// 降低采样率
const audioContext = new AudioContext({ sampleRate: 16000 });
```

**效果**: 减少传输数据量，加快识别速度

---

### 3. 流式识别

**未来优化**:
- 支持实时流式传输
- 边说边识别
- 降低延迟

---

## 🎊 服务启动历史

| 时间 | 事件 | 状态 |
|------|------|------|
| 2026-04-09 17:15 | 首次启动 STT 服务 | ✅ |
| 2026-04-09 17:30 | 服务停止 | ❌ |
| 2026-04-09 18:15 | 重启所有服务 | ✅ |
| 2026-04-09 18:38 | 修复 STT 未运行问题 | ✅ |

---

## ✅ 总结

**问题**: STT 语音识别服务未运行  
**解决**: 启动 stt_service.py (5050 端口)  
**状态**: ✅ 已修复  

**服务架构**:
```
STT (5050) ← 语音识别
  ↓
Flask 代理 (7091) ← 统一入口
  ↓
TTS API (7086) ← 文字转语音
```

**一键启动**:
```bash
bash start_everything_v2.sh
```

**立即测试**:
```
https://fast-items-clean.loca.lt/voice_chat.html
```

**现在可以按住说话，进行完整语音对话了！** 🎤✨

---

**修复时间**: 2026-04-09 18:38  
**提交**: 待推送  
**状态**: ✅ 运行正常
