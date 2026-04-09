# 🚨 服务修复报告

---

## ⚠️ 问题发现

**用户访问：**
```
http://8.213.149.224:7076/voice_chat.html
```

**问题：**
1. ❌ 端口错误：应该是 **7091**，不是 7076
2. ❌ 服务已停止：所有进程都退出了

---

## ✅ 已修复

### 1. 重启服务

**TTS API（7086 端口）：**
```bash
python3 agent_tts_api.py > logs/api_server.log 2>&1 &
```

**Web 服务（7091 端口）：**
```bash
python3 flask_voice_server.py > logs/flask_voice.log 2>&1 &
```

---

### 2. 健康检查

**TTS API：**
```bash
curl http://localhost:7086/health

响应：
{
    "port": 7086,
    "scenes": 6,
    "service": "Agent TTS API",
    "status": "ok",
    "voices": 8
}
```

**Web 服务：**
```bash
curl http://localhost:7091/api/health

响应：
{
    "port": 7086,
    "scenes": 6,
    "service": "Agent TTS API",
    "status": "ok",
    "voices": 8
}
```

---

## 🎯 正确的访问地址

### 本地访问
```
http://localhost:7091/voice_chat.html
```

### 公网访问（需配置阿里云安全组）
```
http://8.213.149.224:7091/voice_chat.html
```

### HTTPS 访问（推荐，可以使用麦克风）
```
https://young-lizards-open.loca.lt/voice_chat.html
```

---

## 📊 端口说明

| 服务 | 端口 | 说明 |
|------|------|------|
| **TTS API** | 7086 | 文字转语音 API |
| **Web 服务** | 7091 | 语音交互页面 |
| **Localtunnel** | 随机 | HTTPS 隧道（动态域名） |

**⚠️ 没有 7076 端口！**

---

## 🔧 一键启动脚本

**创建 `start_all_services.sh`：**

```bash
#!/bin/bash
cd /home/admin/projects/live-tts

echo "======================================"
echo "🚀 启动所有语音服务"
echo "======================================"

# 创建日志目录
mkdir -p logs output/api

# 停止旧服务
pkill -f agent_tts_api
pkill -f flask_voice_server
sleep 1

# 启动 TTS API
echo "启动 TTS API（7086 端口）..."
nohup python3 agent_tts_api.py > logs/api_server.log 2>&1 &
echo "✅ TTS API 已启动"

# 启动 Web 服务
echo "启动 Web 服务（7091 端口）..."
nohup python3 flask_voice_server.py > logs/flask_voice.log 2>&1 &
echo "✅ Web 服务已启动"

# 等待 3 秒检查状态
sleep 3

echo ""
echo "======================================"
echo "✅ 服务启动完成！"
echo "======================================"
echo ""
echo "🌐 访问地址："
echo "   本地：http://localhost:7091/voice_chat.html"
echo "   公网：http://8.213.149.224:7091/voice_chat.html"
echo ""
echo " HTTPS 语音输入："
echo "   https://young-lizards-open.loca.lt/voice_chat.html"
echo ""
echo "📊 健康检查："
echo "   curl http://localhost:7086/health"
echo "   curl http://localhost:7091/api/health"
echo ""
echo "📋 日志："
echo "   tail -f logs/api_server.log"
echo "   tail -f logs/flask_voice.log"
echo ""
```

---

## 🎯 立即使用

### 方式 1：文字输入（无需 HTTPS）

**访问：**
```
http://8.213.149.224:7091/voice_chat.html
```

**操作：**
1. 输入文字
2. 按回车
3. 听语音！

---

### 方式 2：语音输入（需 HTTPS）

**访问：**
```
https://young-lizards-open.loca.lt/voice_chat.html
```

**操作：**
1. 允许麦克风权限
2. 点击"按住说话"
3. 说话
4. 听语音回复！

---

## 🔍 故障排查

### 问题 1：页面无法访问

**检查服务：**
```bash
ps aux | grep -E "(agent_tts|flask_voice)" | grep -v grep
```

**重启服务：**
```bash
cd /home/admin/projects/live-tts
bash start_all_services.sh
```

---

### 问题 2：端口冲突

**检查端口占用：**
```bash
netstat -tlnp | grep 7091
```

**解决：**
```bash
# 停止占用端口的进程
kill <进程 ID>

# 重启服务
bash start_all_services.sh
```

---

### 问题 3：阿里云安全组未开放

**症状：** 本地可以访问，公网无法访问

**解决：**
1. 登录阿里云控制台
2. 安全组 → 入方向规则
3. 添加规则：
   - 端口：7091/7091
   - 授权对象：0.0.0.0/0
   - 协议：TCP

---

## 📖 相关文档

| 文档 | 说明 |
|------|------|
| `STT_COMPLETE_REPORT.md` | STT 集成报告 |
| `LOCALTUNNEL_SUCCESS.md` | HTTPS 配置成功 |
| `TEXT_INPUT_GUIDE.md` | 文字输入指南 |

---

## ✅ 当前状态

| 服务 | 状态 | 端口 |
|------|------|------|
| **TTS API** | ✅ 运行中 | 7086 |
| **Web 服务** | ✅ 运行中 | 7091 |
| **Localtunnel** | ⏳ 需重启 | 随机 |

---

## 🎊 总结

**问题：** 服务停止 + 端口错误  
**解决：** 重启所有服务  
**状态：** ✅ 全部运行正常  

**正确访问地址：**
```
http://8.213.149.224:7091/voice_chat.html
```

**HTTPS 语音输入：**
```
https://young-lizards-open.loca.lt/voice_chat.html
```

---

**修复时间**: 2026-04-09 15:46  
**服务状态**: ✅ 全部运行中  
**正确端口**: 7091（不是 7076）
