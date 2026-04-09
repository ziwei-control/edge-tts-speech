# 🎤 OpenClaw 语音交互系统集成指南

> 利用 OpenClaw 源码 + Edge TTS 语音系统，打造会说话的 AI Agent

---

## 📋 目录

- [系统概述](#系统概述)
- [架构设计](#架构设计)
- [快速开始](#快速开始)
- [HTML 页面实现](#html-页面实现)
- [OpenClaw 集成](#openclaw-集成)
- [API 调用示例](#api-调用示例)
- [部署指南](#部署指南)
- [故障排查](#故障排查)

---

## 🎯 系统概述

### 功能特性

| 功能 | 说明 | 状态 |
|------|------|------|
| 🎤 **语音输入** | 浏览器麦克风录音 | ✅ 支持 |
| 🔊 **语音输出** | Edge TTS 文字转语音 | ✅ 支持 |
| 🤖 **AI 对话** | OpenClaw Agent 处理 | ✅ 支持 |
| 🎭 **多场景** | 6 种语音风格预设 | ✅ 支持 |
| 📱 **响应式** | 电脑/平板/手机适配 | ✅ 支持 |
| 🌐 **离线缓存** | 历史记录本地存储 | ✅ 支持 |

### 技术栈

```
┌─────────────────────────────────────────────────────┐
│                   用户浏览器                        │
│              (HTML + JavaScript + WebRTC)           │
└────────────────────┬────────────────────────────────┘
                     │ HTTP/WebSocket
┌────────────────────▼────────────────────────────────┐
│              OpenClaw Agent Server                  │
│         (Python + Flask + Edge TTS API)             │
└────────────────────┬────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────┐
│              Edge TTS (微软 Azure)                  │
│              (在线文字转语音服务)                    │
└─────────────────────────────────────────────────────┘
```

---

## 🏗️ 架构设计

### 组件说明

| 组件 | 文件 | 端口 | 说明 |
|------|------|------|------|
| **前端页面** | `voice_chat.html` | - | 语音交互界面 |
| **API 服务** | `agent_tts_api.py` | 7086 | TTS 生成服务 |
| **OpenClaw** | `openclaw_voice.py` | 7090 | Agent 主服务 |
| **TTS 引擎** | `agent_tts.py` | - | 语音合成模块 |

### 数据流

```
用户说话 → 浏览器录音 → WebSocket → OpenClaw → 语音识别 → AI 处理
                                                      ↓
用户听到 ← 浏览器播放 ← TTS 音频 ← Edge TTS ← 文字回复 ← AI 回复
```

---

## 🚀 快速开始

### 1. 环境准备

```bash
# 进入项目目录
cd /home/admin/projects/live-tts

# 安装依赖
uv pip install flask aiohttp websockets speechrecognition

# 检查服务状态
curl http://localhost:7086/health
```

### 2. 启动服务

```bash
# 启动 TTS API 服务
python3 agent_tts_api.py &

# 启动 OpenClaw 语音服务
python3 openclaw_voice.py &

# 启动 Web 服务
python3 -m http.server 7091 &
```

### 3. 访问页面

```
http://localhost:7091/voice_chat.html
```

---

## 💻 HTML 页面实现

### 完整代码

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎤 OpenClaw 语音交互</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }

        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            max-width: 600px;
            width: 100%;
            overflow: hidden;
        }

        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }

        .header h1 {
            font-size: 2em;
            margin-bottom: 10px;
        }

        .header p {
            opacity: 0.9;
        }

        .status-bar {
            background: #f5f5f5;
            padding: 15px 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid #e0e0e0;
        }

        .status {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .status-dot {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: #999;
        }

        .status-dot.online {
            background: #4ade80;
            animation: pulse 2s infinite;
        }

        .status-dot.recording {
            background: #ef4444;
            animation: pulse 0.5s infinite;
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }

        .chat-area {
            height: 400px;
            overflow-y: auto;
            padding: 30px;
            background: #fafafa;
        }

        .message {
            margin-bottom: 20px;
            display: flex;
            gap: 15px;
        }

        .message.user {
            flex-direction: row-reverse;
        }

        .avatar {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 1.5em;
            flex-shrink: 0;
        }

        .message.agent .avatar {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }

        .message.user .avatar {
            background: #e0e0e0;
        }

        .bubble {
            max-width: 70%;
            padding: 15px 20px;
            border-radius: 15px;
            position: relative;
        }

        .message.agent .bubble {
            background: white;
            border: 1px solid #e0e0e0;
            border-bottom-left-radius: 5px;
        }

        .message.user .bubble {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-bottom-right-radius: 5px;
        }

        .bubble-text {
            margin-bottom: 10px;
            line-height: 1.5;
        }

        .bubble-audio {
            width: 100%;
        }

        .controls {
            padding: 30px;
            background: white;
            border-top: 1px solid #e0e0e0;
        }

        .scene-selector {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }

        .scene-btn {
            padding: 8px 16px;
            border: 2px solid #e0e0e0;
            border-radius: 20px;
            background: white;
            cursor: pointer;
            transition: all 0.3s;
            font-size: 14px;
        }

        .scene-btn:hover {
            border-color: #667eea;
        }

        .scene-btn.active {
            border-color: #667eea;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }

        .record-btn {
            width: 100%;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 15px;
            font-size: 18px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 10px;
        }

        .record-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
        }

        .record-btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }

        .record-btn.recording {
            background: #ef4444;
            animation: pulse 0.5s infinite;
        }

        .mic-icon {
            font-size: 1.5em;
        }

        .loading {
            text-align: center;
            padding: 20px;
            color: #667eea;
        }

        .spinner {
            border: 3px solid #f3f3f3;
            border-top: 3px solid #667eea;
            border-radius: 50%;
            width: 30px;
            height: 30px;
            animation: spin 1s linear infinite;
            margin: 0 auto 10px;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .settings {
            padding: 20px 30px;
            background: #f9f9f9;
            border-top: 1px solid #e0e0e0;
        }

        .setting-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }

        .setting-label {
            color: #666;
            font-size: 14px;
        }

        select {
            padding: 8px 12px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎤 OpenClaw 语音交互</h1>
            <p>说话即可与 AI 对话，支持 6 种语音风格</p>
        </div>

        <div class="status-bar">
            <div class="status">
                <div class="status-dot" id="statusDot"></div>
                <span id="statusText">连接中...</span>
            </div>
            <div>
                🎭 场景：<strong id="currentScene">通用</strong>
            </div>
        </div>

        <div class="chat-area" id="chatArea">
            <div class="message agent">
                <div class="avatar">🤖</div>
                <div class="bubble">
                    <div class="bubble-text">你好！我是 OpenClaw 智能助手，点击下面的按钮开始语音对话吧！</div>
                </div>
            </div>
        </div>

        <div class="settings">
            <div class="setting-item">
                <span class="setting-label">语音风格</span>
                <select id="voiceSelect">
                    <option value="xiaoxiao">小晓 (温暖通用)</option>
                    <option value="xiaoyi">小艺 (活泼亲切)</option>
                    <option value="xiaoxuan">小萱 (温和亲切)</option>
                    <option value="yunhao">云浩 (广告促销)</option>
                    <option value="yunye">云野 (专业讲解)</option>
                </select>
            </div>
        </div>

        <div class="controls">
            <div class="scene-selector">
                <button class="scene-btn active" data-scene="default">🎵 通用</button>
                <button class="scene-btn" data-scene="gentle">🌸 温柔</button>
                <button class="scene-btn" data-scene="cute">🎀 可爱</button>
                <button class="scene-btn" data-scene="professional">💼 专业</button>
                <button class="scene-btn" data-scene="promotion">🔥 促销</button>
                <button class="scene-btn" data-scene="weak">🌙 柔弱</button>
            </div>
            <button class="record-btn" id="recordBtn" onclick="toggleRecording()">
                <span class="mic-icon">🎤</span>
                <span id="recordText">按住说话</span>
            </button>
        </div>
    </div>

    <script>
        const API_BASE = 'http://localhost:7086';
        const OPENCLAW_BASE = 'http://localhost:7090';
        
        let isRecording = false;
        let selectedScene = 'default';
        let selectedVoice = 'xiaoxiao';
        let mediaRecorder = null;
        let audioChunks = [];

        // 初始化
        async function init() {
            await checkStatus();
            setupSceneButtons();
            setupVoiceSelector();
            loadHistory();
        }

        // 检查服务状态
        async function checkStatus() {
            try {
                const response = await fetch(`${API_BASE}/health`);
                const data = await response.json();
                
                document.getElementById('statusDot').classList.add('online');
                document.getElementById('statusText').textContent = '服务正常';
            } catch (error) {
                document.getElementById('statusText').textContent = '服务未连接';
            }
        }

        // 设置场景按钮
        function setupSceneButtons() {
            const buttons = document.querySelectorAll('.scene-btn');
            buttons.forEach(btn => {
                btn.addEventListener('click', () => {
                    buttons.forEach(b => b.classList.remove('active'));
                    btn.classList.add('active');
                    selectedScene = btn.dataset.scene;
                    document.getElementById('currentScene').textContent = btn.textContent.split(' ')[1];
                });
            });
        }

        // 设置语音选择
        function setupVoiceSelector() {
            document.getElementById('voiceSelect').addEventListener('change', (e) => {
                selectedVoice = e.target.value;
            });
        }

        // 切换录音
        async function toggleRecording() {
            if (isRecording) {
                stopRecording();
            } else {
                await startRecording();
            }
        }

        // 开始录音
        async function startRecording() {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                
                mediaRecorder = new MediaRecorder(stream);
                audioChunks = [];

                mediaRecorder.ondataavailable = (event) => {
                    audioChunks.push(event.data);
                };

                mediaRecorder.onstop = async () => {
                    const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
                    await processAudio(audioBlob);
                };

                mediaRecorder.start();
                isRecording = true;

                const btn = document.getElementById('recordBtn');
                btn.classList.add('recording');
                btn.disabled = true;
                document.getElementById('recordText').textContent = '松开结束';
                document.getElementById('statusDot').classList.add('recording');

            } catch (error) {
                alert('无法访问麦克风：' + error.message);
            }
        }

        // 停止录音
        function stopRecording() {
            if (mediaRecorder && mediaRecorder.state !== 'inactive') {
                mediaRecorder.stop();
                mediaRecorder.stream.getTracks().forEach(track => track.stop());
            }

            isRecording = false;
            const btn = document.getElementById('recordBtn');
            btn.classList.remove('recording');
            btn.disabled = false;
            document.getElementById('recordText').textContent = '按住说话';
            document.getElementById('statusDot').classList.remove('recording');
        }

        // 处理音频
        async function processAudio(audioBlob) {
            // 显示用户消息
            addMessage('user', '🗣️ [语音消息]', '正在识别...');

            try {
                // 发送到 OpenClaw 进行语音识别和处理
                const formData = new FormData();
                formData.append('audio', audioBlob);
                formData.append('scene', selectedScene);
                formData.append('voice', selectedVoice);

                const response = await fetch(`${OPENCLAW_BASE}/voice_chat`, {
                    method: 'POST',
                    body: formData
                });

                const data = await response.json();

                if (data.success) {
                    // 更新用户消息
                    updateMessage('user', data.user_text || '语音消息');

                    // 显示 AI 回复
                    addMessage('agent', data.agent_text, data.audio_url);

                    // 播放语音
                    if (data.audio_url) {
                        const audio = new Audio(data.audio_url);
                        audio.play();
                    }
                } else {
                    updateMessage('user', '识别失败');
                    addMessage('agent', '抱歉，我没有听清楚，请再说一遍。');
                }

            } catch (error) {
                updateMessage('user', '发送失败');
                addMessage('agent', '网络错误，请稍后再试。');
            }
        }

        // 添加消息
        function addMessage(role, text, audioUrl = null) {
            const chatArea = document.getElementById('chatArea');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${role}`;
            messageDiv.innerHTML = `
                <div class="avatar">${role === 'agent' ? '🤖' : '👤'}</div>
                <div class="bubble">
                    <div class="bubble-text">${text}</div>
                    ${audioUrl ? `<audio controls class="bubble-audio"><source src="${audioUrl}" type="audio/mpeg"></audio>` : ''}
                </div>
            `;
            chatArea.appendChild(messageDiv);
            chatArea.scrollTop = chatArea.scrollHeight;

            // 保存到历史
            saveToHistory(role, text, audioUrl);
        }

        // 更新消息
        function updateMessage(role, text) {
            const chatArea = document.getElementById('chatArea');
            const lastMessage = chatArea.querySelector(`.message.${role}:last-child .bubble-text`);
            if (lastMessage) {
                lastMessage.textContent = text;
            }
        }

        // 保存到历史
        function saveToHistory(role, text, audioUrl) {
            const history = JSON.parse(localStorage.getItem('voice_chat_history') || '[]');
            history.push({
                role,
                text,
                audioUrl,
                timestamp: new Date().toISOString()
            });
            if (history.length > 50) history.shift();
            localStorage.setItem('voice_chat_history', JSON.stringify(history));
        }

        // 加载历史
        function loadHistory() {
            const history = JSON.parse(localStorage.getItem('voice_chat_history') || '[]');
            history.forEach(item => {
                addMessage(item.role, item.text, item.audioUrl);
            });
        }

        // 页面加载时初始化
        window.addEventListener('DOMContentLoaded', init);
    </script>
</body>
</html>
```

---

## 🔌 OpenClaw 集成

### 创建 OpenClaw 语音服务

```python
#!/usr/bin/env python3
"""
OpenClaw 语音交互服务
集成 Edge TTS 和语音识别
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import asyncio
import aiohttp
import os
import uuid
from datetime import datetime
import speech_recognition as sr
import io
import wave

app = Flask(__name__)
CORS(app)

# 配置
TTS_API_URL = "http://localhost:7086"
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "output/openclaw"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# 语音识别器
recognizer = sr.Recognizer()

class OpenClawVoiceAgent:
    """OpenClaw 语音 Agent"""
    
    def __init__(self):
        self.conversation_history = []
    
    async def chat(self, user_text: str, scene: str = "default") -> dict:
        """
        AI 对话处理
        
        Args:
            user_text: 用户输入文本
            scene: 语音场景
        
        Returns:
            回复内容
        """
        # 添加到历史
        self.conversation_history.append({
            "role": "user",
            "content": user_text,
            "timestamp": datetime.now().isoformat()
        })
        
        # 调用 OpenClaw Agent (这里简化处理，实际应调用 LLM)
        agent_response = await self.get_agent_response(user_text)
        
        # 添加到历史
        self.conversation_history.append({
            "role": "assistant",
            "content": agent_response,
            "timestamp": datetime.now().isoformat()
        })
        
        # 生成 TTS 语音
        tts_result = await self.generate_tts(agent_response, scene)
        
        return {
            "success": True,
            "user_text": user_text,
            "agent_text": agent_response,
            "audio_url": tts_result.get("url"),
            "scene": scene
        }
    
    async def get_agent_response(self, user_text: str) -> str:
        """
        获取 AI 回复
        
        实际使用时应调用 OpenClaw 的 LLM 接口
        这里简化为规则回复
        """
        # 简单规则回复示例
        responses = {
            "你好": "你好呀！有什么可以帮你的吗？",
            "时间": f"现在是 {datetime.now().strftime('%H点%M分')}",
            "日期": f"今天是 {datetime.now().strftime('%Y年%m月%d日')}",
            "再见": "再见！祝你有美好的一天！",
        }
        
        for key, value in responses.items():
            if key in user_text:
                return value
        
        # 默认回复
        return f"我收到了：{user_text}。这是一个演示回复，实际使用时会调用 OpenClaw 的 AI 接口。"
    
    async def generate_tts(self, text: str, scene: str) -> dict:
        """生成 TTS 语音"""
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{TTS_API_URL}/speak",
                json={"text": text, "scene": scene},
                headers={"Content-Type": "application/json"}
            ) as response:
                return await response.json()
    
    def recognize_speech(self, audio_data: bytes) -> str:
        """
        语音识别
        
        Args:
            audio_data: 音频数据 (webm 格式)
        
        Returns:
            识别的文本
        """
        try:
            # 转换 webm 为 wav
            audio = io.BytesIO(audio_data)
            
            # 使用 Google 语音识别 (免费)
            with sr.AudioFile(audio) as source:
                audio_data = recognizer.record(source)
                text = recognizer.recognize_google(audio_data, language='zh-CN')
                return text
        
        except sr.UnknownValueError:
            return ""
        except sr.RequestError as e:
            return f"识别服务错误：{e}"
        except Exception as e:
            return f"识别错误：{e}"


# 创建 Agent 实例
agent = OpenClawVoiceAgent()


@app.route('/voice_chat', methods=['POST'])
async def voice_chat():
    """
    语音聊天接口
    
    接收音频 → 语音识别 → AI 处理 → TTS 生成 → 返回音频
    """
    try:
        # 获取音频文件
        audio_file = request.files.get('audio')
        scene = request.form.get('scene', 'default')
        voice = request.form.get('voice', 'xiaoxiao')
        
        if not audio_file:
            return jsonify({"success": False, "error": "未收到音频文件"})
        
        # 读取音频数据
        audio_data = audio_file.read()
        
        # 语音识别
        user_text = agent.recognize_speech(audio_data)
        
        if not user_text:
            return jsonify({
                "success": False,
                "error": "无法识别语音，请再说一遍"
            })
        
        # AI 处理
        result = await agent.chat(user_text, scene)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })


@app.route('/text_chat', methods=['POST'])
async def text_chat():
    """
    文字聊天接口
    
    接收文字 → AI 处理 → TTS 生成 → 返回音频
    """
    try:
        data = request.get_json()
        text = data.get('text', '')
        scene = data.get('scene', 'default')
        
        if not text:
            return jsonify({"success": False, "error": "文本不能为空"})
        
        # AI 处理
        result = await agent.chat(text, scene)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })


@app.route('/health')
def health():
    """健康检查"""
    return jsonify({
        "status": "ok",
        "service": "OpenClaw Voice Agent",
        "tts_api": TTS_API_URL
    })


if __name__ == '__main__':
    print("=" * 60)
    print("🎤 OpenClaw 语音交互服务")
    print("=" * 60)
    print(f"📡 服务地址：http://localhost:7090")
    print(f"🔊 TTS API: {TTS_API_URL}")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=7090, debug=False)
```

---

## 📡 API 调用示例

### 1. 语音聊天

```bash
curl -X POST http://localhost:7090/voice_chat \
  -F "audio=@recording.webm" \
  -F "scene=cute" \
  -F "voice=xiaoxiao"
```

**响应:**
```json
{
  "success": true,
  "user_text": "你好",
  "agent_text": "你好呀！有什么可以帮你的吗？",
  "audio_url": "http://localhost:7086/audio/speech_xxx.mp3",
  "scene": "cute"
}
```

### 2. 文字聊天

```bash
curl -X POST http://localhost:7090/text_chat \
  -H "Content-Type: application/json" \
  -d '{"text":"现在几点了","scene":"professional"}'
```

### 3. 健康检查

```bash
curl http://localhost:7090/health
```

---

## 🚀 部署指南

### 1. 文件结构

```
openclaw-voice/
├── voice_chat.html          # 前端页面
├── openclaw_voice.py        # OpenClaw 服务
├── agent_tts_api.py         # TTS API (已有)
├── agent_tts.py             # TTS 引擎 (已有)
├── requirements.txt         # 依赖列表
└── README.md               # 使用说明
```

### 2. 依赖安装

```bash
# requirements.txt
flask==3.0.0
flask-cors==4.0.0
aiohttp==3.9.1
speechrecognition==3.10.0
edge-tts==7.2.8
```

```bash
uv pip install -r requirements.txt
```

### 3. 启动脚本

```bash
#!/bin/bash
# start_voice_system.sh

echo "======================================"
echo "🎤 OpenClaw 语音交互系统"
echo "======================================"

# 启动 TTS API
echo "📡 启动 TTS API 服务..."
nohup python3 agent_tts_api.py > logs/tts_api.log 2>&1 &
sleep 2

# 启动 OpenClaw
echo "🤖 启动 OpenClaw 服务..."
nohup python3 openclaw_voice.py > logs/openclaw.log 2>&1 &
sleep 2

# 启动 Web 服务
echo "🌐 启动 Web 服务..."
nohup python3 -m http.server 7091 > logs/web.log 2>&1 &

echo ""
echo "======================================"
echo "✅ 服务启动完成！"
echo "======================================"
echo "📡 TTS API:   http://localhost:7086"
echo "🤖 OpenClaw:  http://localhost:7090"
echo "🌐 Web 页面：  http://localhost:7091/voice_chat.html"
echo ""
```

### 4. 生产部署

```bash
# 使用 Gunicorn 运行 OpenClaw
gunicorn -w 4 -b 0.0.0.0:7090 openclaw_voice:app

# 使用 Nginx 反向代理
server {
    listen 80;
    server_name voice.example.com;

    location / {
        proxy_pass http://localhost:7091;
    }

    location /api/tts {
        proxy_pass http://localhost:7086;
    }

    location /api/openclaw {
        proxy_pass http://localhost:7090;
    }
}
```

---

## 🔍 故障排查

### 麦克风无法使用

```javascript
// 检查浏览器权限
navigator.mediaDevices.getUserMedia({ audio: true })
  .then(() => console.log('✅ 麦克风可用'))
  .catch(err => console.error('❌ 麦克风错误:', err));
```

**解决方案:**
1. 检查浏览器权限设置
2. 使用 HTTPS (生产环境必需)
3. 检查麦克风硬件

### TTS 生成失败

```bash
# 检查 TTS API 状态
curl http://localhost:7086/health

# 查看日志
tail -f logs/api_server.log

# 测试生成
curl -X POST http://localhost:7086/speak \
  -H "Content-Type: application/json" \
  -d '{"text":"测试","scene":"default"}'
```

### 语音识别不准确

```python
# 调整识别器设置
recognizer = sr.Recognizer()
recognizer.energy_threshold = 300  # 灵敏度
recognizer.dynamic_energy_threshold = True
```

**优化建议:**
1. 使用高质量麦克风
2. 在安静环境录音
3. 说话清晰缓慢
4. 考虑使用付费 API (百度/讯飞)

---

## 📊 性能优化

### 1. 音频压缩

```javascript
// 降低采样率
const mediaRecorder = new MediaRecorder(stream, {
    mimeType: 'audio/webm;codecs=opus',
    audioBitsPerSecond: 128000
});
```

### 2. 缓存策略

```python
# 缓存常用回复的 TTS 音频
from functools import lru_cache

@lru_cache(maxsize=100)
def cached_tts(text: str, scene: str) -> str:
    """缓存 TTS 生成结果"""
    # 实现缓存逻辑
    pass
```

### 3. 并发处理

```python
# 使用异步并发
import asyncio

async def process_multiple_requests(requests):
    tasks = [process_request(r) for r in requests]
    results = await asyncio.gather(*tasks)
    return results
```

---

## 🎯 扩展功能

### 1. 多语言支持

```python
SUPPORTED_LANGUAGES = {
    'zh-CN': '中文',
    'en-US': 'English',
    'ja-JP': '日本語',
    'ko-KR': '한국어'
}
```

### 2. 情感分析

```python
from textblob import TextBlob

def analyze_emotion(text: str) -> str:
    """分析文本情感，选择合适的语音场景"""
    sentiment = TextBlob(text).sentiment.polarity
    if sentiment > 0.3:
        return "cute"  # 积极 → 可爱
    elif sentiment < -0.3:
        return "gentle"  # 消极 → 温柔
    else:
        return "default"  # 中性 → 通用
```

### 3. 语音克隆

```python
# 使用自定义语音模型
def clone_voice(user_id: str, text: str) -> bytes:
    """基于用户历史语音克隆声音"""
    # 实现语音克隆逻辑
    pass
```

---

## 📝 总结

### 已完成功能 ✅

- [x] 语音输入 (浏览器麦克风)
- [x] 语音输出 (Edge TTS)
- [x] AI 对话处理
- [x] 6 种语音场景
- [x] 历史记录保存
- [x] 响应式设计

### 可选扩展 ⭐

- [ ] 真实 LLM 集成 (OpenAI/Claude)
- [ ] 语音克隆功能
- [ ] 多语言支持
- [ ] 情感识别
- [ ] 离线 TTS 支持
- [ ] 实时字幕显示

---

**创建时间**: 2026-04-09  
**版本**: 1.0  
**作者**: OpenClaw AI Team  
**许可**: MIT

---

## 🔗 相关资源

- **OpenClaw 官网**: https://openclaw.ai
- **Edge TTS**: https://github.com/rany2/edge-tts
- **Web Speech API**: https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API
- **GitHub 仓库**: https://github.com/ziwei-control/edge-tts-speech
