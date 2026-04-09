# ✅ Localtunnel HTTPS 配置成功！

---

## 🎉 配置完成

**HTTPS 链接已生成：**
```
https://young-lizards-open.loca.lt
```

**完整访问地址：**
```
https://young-lizards-open.loca.lt/voice_chat.html
```

---

## 🎤 立即可用语音输入！

### 步骤 1：访问链接

**用浏览器打开：**
```
https://young-lizards-open.loca.lt/voice_chat.html
```

---

### 步骤 2：允许麦克风

**浏览器会弹出：**
```
 请求使用麦克风

[允许] [拒绝]
```

**点击"允许"**

---

### 步骤 3：使用语音输入

1. ✅ 选择语音场景（🎵通用/温柔等）
2. ✅ 点击"🎤 按住说话"
3. ✅ 说话
4. ✅ 松开结束
5. ✅ 听语音回复

---

## 📊 服务状态

| 服务 | 状态 | 说明 |
|------|------|------|
| **Localtunnel** | ✅ 运行中 | HTTPS 隧道 |
| **TTS API** | ✅ 运行中 | 文字转语音 |
| **Web 服务** | ✅ 运行中 | 语音交互页面 |

---

## 🔧 服务管理

### 查看状态

```bash
# 检查 Localtunnel
ps aux | grep "lt --port" | grep -v grep

# 检查日志
cat /tmp/lt.log

# 检查 TTS API
curl http://localhost:7086/health

# 检查 Web 服务
curl http://localhost:7091/api/health
```

---

### 重启服务

```bash
# 停止旧服务
pkill -f "lt --port"
pkill -f flask_voice
pkill -f agent_tts

# 启动新服务
cd /home/admin/projects/live-tts

# 启动 TTS API
python3 agent_tts_api.py > logs/api_server.log 2>&1 &

# 启动 Web 服务
python3 flask_voice_server.py > logs/flask_voice.log 2>&1 &

# 启动 Localtunnel
lt --port 7091 > /tmp/lt.log 2>&1 &

# 等待 5 秒
sleep 5

# 获取 HTTPS 链接
cat /tmp/lt.log | grep "your url is"
```

---

### 停止服务

```bash
# 停止 Localtunnel
pkill -f "lt --port"

# 或者使用进程 ID
kill <进程 ID>
```

---

## ⚠️ 注意事项

### 1. Localtunnel 域名会变化

**每次启动域名不同：**
```
第 1 次：https://young-lizards-open.loca.lt
第 2 次：https://abc-def-ghi.loca.lt
第 3 次：https://xyz-123-456.loca.lt
```

**解决：**
- 每次启动后查看最新域名
- 使用书签保存当前域名

---

### 2. Localtunnel 可能不稳定

**如果连接断开：**
```bash
# 查看日志
cat /tmp/lt.log

# 重启
pkill -f "lt --port"
lt --port 7091 > /tmp/lt.log 2>&1 &
```

---

### 3. 首次访问需要确认

**浏览器会显示：**
```
⚠️ 此连接不是私密连接

[高级] [返回安全]
```

**点击"高级" → "继续访问"**

**原因：** Localtunnel 使用自签名证书

---

## 🎯 使用技巧

### 技巧 1：保存书签

**访问后保存书签：**
```
https://young-lizards-open.loca.lt/voice_chat.html
```

**下次直接打开（如果域名未变）**

---

### 技巧 2：后台运行

**使用 screen 或 tmux：**
```bash
# 安装 screen
apt install screen -y

# 创建会话
screen -S voice

# 启动服务
lt --port 7091

# 按 Ctrl+A, D 分离会话

# 随时恢复
screen -r voice
```

---

### 技巧 3：自动启动脚本

**创建 `start_voice_https.sh`：**
```bash
#!/bin/bash
cd /home/admin/projects/live-tts

# 启动服务
bash start_voice_service.sh

# 启动 Localtunnel
lt --port 7091 > /tmp/lt.log 2>&1 &

# 等待并显示链接
sleep 5
echo ""
echo "✅ HTTPS 链接："
cat /tmp/lt.log | grep "your url is"
```

---

## 📱 移动端访问

**手机/平板也可以访问：**

1. 打开 HTTPS 链接
2. 允许麦克风权限
3. 按住说话
4. 听语音

**注意：** 移动端浏览器可能需要额外权限

---

## 🔍 故障排查

### 问题 1：页面无法访问

**检查：**
```bash
# Localtunnel 是否运行
ps aux | grep "lt --port"

# 日志
cat /tmp/lt.log
```

**解决：**
```bash
# 重启
pkill -f "lt --port"
lt --port 7091 > /tmp/lt.log 2>&1 &
```

---

### 问题 2：麦克风无法使用

**检查浏览器权限：**

1. 点击地址栏左侧的 🔒
2. 点击"网站设置"
3. 找到"麦克风"
4. 改为"允许"
5. 刷新页面

---

### 问题 3：语音不播放

**检查：**
```bash
# TTS API 状态
curl http://localhost:7086/health

# 测试生成
curl -X POST http://localhost:7086/speak \
  -H "Content-Type: application/json" \
  -d '{"text":"测试","scene":"default"}'
```

**解决：**
```bash
# 重启 TTS API
pkill -f agent_tts_api
cd /home/admin/projects/live-tts
python3 agent_tts_api.py &
```

---

## 🎊 当前链接

**HTTPS 访问地址：**
```
https://young-lizards-open.loca.lt/voice_chat.html
```

**服务状态：**
- ✅ Localtunnel：运行中
- ✅ TTS API：运行中
- ✅ Web 服务：运行中

**立即可用：**
1. 打开链接
2. 允许麦克风
3. 按住说话
4. 听语音！

---

## 📖 相关文档

- `QUICK_START_VOICE.md` - 快速开始指南
- `ENABLE_HTTPS_GUIDE.md` - HTTPS 配置指南
- `TEXT_INPUT_GUIDE.md` - 文字输入指南

---

**配置时间**: 2026-04-09 15:15  
**HTTPS 链接**: https://young-lizards-open.loca.lt  
**服务状态**: ✅ 全部运行中  
**推荐**: 立即访问并使用语音输入！
