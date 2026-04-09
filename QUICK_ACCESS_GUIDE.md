# 🚀 快速访问指南

---

## ✅ 最新链接

**Localtunnel HTTPS**:
```
https://big-bottles-write.loca.lt
```

**语音对话页面（152 个音色）**:
```
https://big-bottles-write.loca.lt/voice_chat.html
```

**完整语音库（152 个音色试听）**:
```
https://big-bottles-write.loca.lt/voice_library.html
```

---

## ⚠️ 503 错误解决

**如果显示 "503 - Tunnel Unavailable"**:

### 方法 1: 等待几秒
Localtunnel 重启后需要 5-10 秒启动，稍等再刷新页面。

---

### 方法 2: 重启 Localtunnel

**一键重启命令**:
```bash
pkill -f "lt --port" && sleep 2 && lt --port 7091 > /tmp/lt.log 2>&1 &
```

**查看新链接**:
```bash
sleep 3 && cat /tmp/lt.log
```

**新链接格式**:
```
your url is: https://xxx-yyy-zzz.loca.lt
```

---

## 📱 所有可用页面

### 1. 语音对话页面 ⭐
```
/voice_chat.html
```
**功能**:
- ✅ 152 个音色选择
- ✅ 文字输入转语音
- ✅ 语音输入对话（需 HTTPS）
- ✅ 6 种场景切换
- ✅ 实时语音回复

---

### 2. 完整语音库
```
/voice_library.html
```
**功能**:
- ✅ 152 个音频文件
- ✅ 4 个版本对比
- ✅ 搜索和过滤
- ✅ 即时播放

---

### 3. 全版本对比
```
/all_versions.html
```
**功能**:
- ✅ 原版（80 个）
- ✅ 优化版（24 个）
- ✅ 粘人版（24 个）
- ✅ 柔弱版（24 个）

---

### 4. 其他试听页面

```
/listen_here.html          # 原始试听（80 个）
/compare_natural.html      # 优化版对比（24 个）
/cute_voice.html           # 粘人版（24 个）
/weak_voice.html           # 柔弱版（24 个）
```

---

## 🔧 服务检查

### 检查 Localtunnel 进程
```bash
ps aux | grep "lt --port" | grep -v grep
```

**应看到**:
```
admin  123456  0.5  2.9  node /home/admin/.local/bin/lt --port 7091
```

---

### 检查日志
```bash
cat /tmp/lt.log
```

**应看到**:
```
your url is: https://xxx-yyy-zzz.loca.lt
```

---

### 检查 Flask 服务
```bash
ps aux | grep "flask_voice_server.py" | grep -v grep
```

**应看到**:
```
admin  123456  python3 flask_voice_server.py
```

---

### 检查 TTS API
```bash
ps aux | grep "agent_tts_api.py" | grep -v grep
```

**应看到**:
```
admin  123456  python3 agent_tts_api.py
```

---

## 🎯 使用流程

### 步骤 1: 访问页面
```
https://big-bottles-write.loca.lt/voice_chat.html
```

### 步骤 2: 处理证书警告
首次访问会显示：
```
您的连接不是私密连接

→ 点击"高级"
→ 点击"继续访问（不安全）"
```

### 步骤 3: 选择音色
- 默认显示 6 个常用语音
- 点击"展开全部"查看所有 20+ 个语音
- 点击语音名切换

### 步骤 4: 发送消息
- 输入文字
- 按回车或点击"发送"
- 听语音回复！

---

## 📊 服务状态

| 服务 | 端口 | 状态 | 说明 |
|------|------|------|------|
| **Localtunnel** | - | ✅ 运行中 | HTTPS 隧道 |
| **Flask 代理** | 7091 | ✅ 运行中 | Web+API |
| **TTS API** | 7086 | ✅ 运行中 | 文字转语音 |
| **STT API** | 5050 | ✅ 运行中 | 语音识别 |

---

## 🔄 域名历史记录

| 序号 | 域名 | 状态 | 时间 |
|------|------|------|------|
| 1 | young-lizards-open.loca.lt | ❌ 失效 | 第一次 |
| 2 | whole-mice-work.loca.lt | ❌ 失效 | 第二次 |
| 3 | six-turtles-pump.loca.lt | ❌ 失效 | 第三次 |
| 4 | afraid-ads-kick.loca.lt | ❌ 失效 | 第四次 |
| 5 | **big-bottles-write.loca.lt** | ✅ 运行中 | 第五次（当前） |

---

## ⚡ 快速重启脚本

**创建脚本** `quick_restart.sh`:
```bash
#!/bin/bash
echo "🔄 重启 Localtunnel..."
pkill -f "lt --port"
sleep 2
lt --port 7091 > /tmp/lt.log 2>&1 &
echo "⏳ 等待启动..."
sleep 5
echo "✅ 新链接:"
cat /tmp/lt.log
```

**使用**:
```bash
bash quick_restart.sh
```

---

## 🎤 语音功能测试

### 测试 1: 文字转语音
1. 打开 `/voice_chat.html`
2. 输入 "你好"
3. 发送
4. ✅ 应听到语音回复

### 测试 2: 音色切换
1. 点击 "xiaoyi"
2. ✅ 显示 "已切换到 xiaoyi 音色 ✨"
3. 输入文字发送
4. ✅ 应使用 xiaoyi 语音

### 测试 3: 场景切换
1. 点击 "🔥 促销"
2. 输入 "欢迎来到直播间！"
3. 发送
4. ✅ 应使用促销语气

---

## 📖 相关文档

| 文档 | 说明 |
|------|------|
| **VOICE_CHAT_FEATURES.md** | 语音对话功能说明 |
| **VOICE_LIBRARY_GUIDE.md** | 语音库使用指南 |
| **AUDIO_URL_FIX.md** | 音频 URL 修复说明 |
| **QUICK_START_VOICE.md** | 语音输入快速开始 |
| **TEXT_INPUT_GUIDE.md** | 文字输入使用指南 |

---

## 🎊 总结

**当前链接**: `https://big-bottles-write.loca.lt`  
**状态**: ✅ 运行正常  
**功能**: 152 个音色选择、文字/语音输入、实时回复  

**立即访问**:
```
https://big-bottles-write.loca.lt/voice_chat.html
```

**如遇 503 错误**:
1. 等待 5-10 秒再刷新
2. 或运行 `bash quick_restart.sh` 重启

---

**更新时间**: 2026-04-09 17:40  
**当前域名**: big-bottles-write.loca.lt  
**状态**: ✅ 可用
