# 🌐 语音交互 HTML 页面访问指南

---

## ✅ 服务状态

| 服务 | 端口 | 状态 | 说明 |
|------|------|------|------|
| **TTS API** | 7086 | ✅ 运行中 | 文字转语音服务 |
| **Web 服务** | 7091 | ✅ 运行中 | 语音交互页面 |
| **HTML 文件** | - | ✅ 已创建 | voice_chat.html (9.8KB) |

---

## 🚀 访问方式

### 方法一：服务器本机访问（最简单）

**直接在服务器浏览器打开：**

```
http://localhost:7091/voice_chat.html
```

或

```
http://127.0.0.1:7091/voice_chat.html
```

---

### 方法二：本地电脑访问（需配置阿里云）

#### 1️⃣ 开放阿里云安全组端口

**步骤：**
1. 登录阿里云控制台
2. 进入 ECS → 安全组
3. 添加入方向规则：
   - 协议：TCP
   - 端口：7091
   - 授权对象：0.0.0.0/0

#### 2️⃣ 访问公网地址

```
http://8.213.149.224:7091/voice_chat.html
```

---

### 方法三：SSH 隧道（无需开放端口）

**在本地电脑执行：**

```bash
# Mac/Linux
ssh -L 7091:localhost:7091 root@8.213.149.224

# Windows (PowerShell)
ssh -L 7091:localhost:7091 root@8.213.149.224
```

**然后访问：**

```
http://localhost:7091/voice_chat.html
```

---

## 📱 页面功能

### 界面预览

```
┌────────────────────────────────────┐
│     🎤 OpenClaw 语音交互           │
│     说话即可与 AI 对话              │
├────────────────────────────────────┤
│  🟢 服务正常  🎭 场景：通用        │
├────────────────────────────────────┤
│  🤖 你好！我是 OpenClaw 智能助手   │
│     点击按钮开始语音对话吧！        │
│                                    │
│  👤 🗣️ 语音消息已发送             │
│  🤖 演示模式：语音识别未配置...    │
├────────────────────────────────────┤
│  🎵通用 🌸温柔 🎀可爱 💼专业 🔥促销 🌙柔弱 │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│        🎤 按住说话                 │
└────────────────────────────────────┘
```

### 核心功能

| 功能 | 状态 | 说明 |
|------|------|------|
| **语音输入** | ⚠️ 演示模式 | 需要配置语音识别 API |
| **场景选择** | ✅ 可用 | 6 种语音风格 |
| **TTS 输出** | ✅ 可用 | 调用 7086 端口 API |
| **对话历史** | ✅ 可用 | 本地存储 |
| **服务监控** | ✅ 可用 | 实时状态显示 |

---

## 🔧 完整功能配置（可选）

### 启用语音识别

当前页面是**演示模式**，要启用完整语音功能：

#### 1️⃣ 安装语音识别库

```bash
cd /home/admin/projects/live-tts
uv pip install speechrecognition flask flask-cors
```

#### 2️⃣ 创建 OpenClaw 服务

```bash
# 创建 openclaw_voice.py 文件
# （参考 OPENCLAW_VOICE_INTEGRATION.md 中的完整代码）
```

#### 3️⃣ 启动服务

```bash
python3 openclaw_voice.py &
```

#### 4️⃣ 更新页面 API 地址

编辑 `voice_chat.html`，修改：

```javascript
const OPENCLAW_BASE = 'http://localhost:7090';  // 添加这行
```

并更新 `processAudio` 函数调用 OpenClaw API。

---

## 🎭 语音场景说明

| 场景 | 图标 | 语音 | 适用场景 |
|------|------|------|---------|
| **通用** | 🎵 | xiaoxiao | 日常对话 ⭐⭐⭐ |
| **温柔** | 🌸 | xiaoxuan | 安慰鼓励 ⭐⭐ |
| **可爱** | 🎀 | xiaomeng | 娱乐互动 ⭐⭐⭐ |
| **专业** | 💼 | yunye | 知识讲解 ⭐⭐⭐ |
| **促销** | 🔥 | yunhao | 广告带货 ⭐⭐⭐ |
| **柔弱** | 🌙 | xiaoxiao | ASMR ⭐⭐ |

---

## 📊 服务检查命令

```bash
# 检查 TTS API
curl http://localhost:7086/health

# 检查 Web 服务
curl http://localhost:7091/voice_chat.html | head -5

# 检查进程
ps aux | grep -E "(7086|7091)" | grep -v grep

# 查看日志
tail -f /home/admin/projects/live-tts/logs/api_server.log
tail -f /home/admin/projects/live-tts/logs/voice_web.log
```

---

## 🔍 故障排查

### 问题 1: 页面无法访问

**检查：**
```bash
# 服务是否运行
ps aux | grep "http.server 7091"

# 端口是否监听
netstat -tlnp | grep 7091
```

**解决：**
```bash
cd /home/admin/projects/live-tts
python3 -m http.server 7091 &
```

### 问题 2: TTS API 未连接

**检查：**
```bash
curl http://localhost:7086/health
```

**解决：**
```bash
cd /home/admin/projects/live-tts
python3 agent_tts_api.py &
```

### 问题 3: 麦克风无法使用

**原因：**
- 浏览器权限未授予
- HTTP 环境（生产需 HTTPS）
- 麦克风硬件问题

**解决：**
1. 浏览器地址栏左侧点击锁图标 → 允许麦克风
2. 使用 HTTPS 或本地访问（localhost）
3. 检查系统麦克风设置

---

## 📝 快速启动脚本

```bash
#!/bin/bash
# start_voice_chat.sh

echo "======================================"
echo "🎤 语音交互系统启动"
echo "======================================"

cd /home/admin/projects/live-tts

# 启动 TTS API
if ! pgrep -f "agent_tts_api.py" > /dev/null; then
    echo "📡 启动 TTS API..."
    nohup python3 agent_tts_api.py > logs/api_server.log 2>&1 &
    sleep 2
else
    echo "✅ TTS API 已在运行"
fi

# 启动 Web 服务
if ! pgrep -f "http.server 7091" > /dev/null; then
    echo "🌐 启动 Web 服务..."
    nohup python3 -m http.server 7091 > logs/voice_web.log 2>&1 &
    sleep 2
else
    echo "✅ Web 服务已在运行"
fi

echo ""
echo "======================================"
echo "✅ 服务启动完成！"
echo "======================================"
echo ""
echo "📡 TTS API:   http://localhost:7086"
echo "🌐 Web 页面： http://localhost:7091/voice_chat.html"
echo ""
echo "🔗 公网访问：http://8.213.149.224:7091/voice_chat.html"
echo "   (需配置阿里云安全组开放 7091 端口)"
echo ""
```

**使用方法：**
```bash
chmod +x start_voice_chat.sh
./start_voice_chat.sh
```

---

## 🎯 访问总结

| 场景 | 推荐方式 | 地址 |
|------|---------|------|
| **服务器测试** | 本机访问 | http://localhost:7091/voice_chat.html |
| **本地电脑（快速）** | SSH 隧道 | http://localhost:7091/voice_chat.html |
| **本地电脑（长期）** | 阿里云公网 | http://8.213.149.224:7091/voice_chat.html |
| **移动端测试** | 公网 IP | http://8.213.149.224:7091/voice_chat.html |

---

## 📖 相关文档

- **完整集成指南**: `OPENCLAW_VOICE_INTEGRATION.md` (28KB)
- **TTS 完成报告**: `AGENT_TTS_COMPLETE.md` (8.7KB)
- **GitHub 仓库**: https://github.com/ziwei-control/edge-tts-speech

---

**创建时间**: 2026-04-09  
**页面版本**: 1.0 (演示模式)  
**服务状态**: ✅ 运行中
