# 🚀 一键启用语音输入（3 种方案）

---

## ⚡ 方案一：SSH 隧道（推荐 ⭐⭐⭐）

**最简单，无需安装任何东西！**

### 步骤 1：本地电脑执行

**Mac/Linux：**
```bash
ssh -L 7091:localhost:7091 root@8.213.149.224
```

**Windows（PowerShell）：**
```bash
ssh -L 7091:localhost:7091 root@8.213.149.224
```

**Windows（PuTTY）：**
1. 打开 PuTTY
2. Connection → SSH → Tunnels
3. Source port: `7091`
4. Destination: `localhost:7091`
5. 点击 "Add"
6. 返回 Session，连接服务器

---

### 步骤 2：访问页面

**保持 SSH 连接，打开浏览器访问：**
```
http://localhost:7091/voice_chat.html
```

---

### 步骤 3：使用语音输入

**现在可以使用麦克风了！**
- ✅ 点击"按住说话"
- ✅ 说话
- ✅ 松开结束

---

### 为什么这样可以用？

```
本地电脑 (localhost:7091)
    ↓ SSH 隧道加密
服务器 (localhost:7091)
    ↓ 访问 TTS 服务
```

**localhost 是浏览器安全例外，可以使用麦克风！**

---

## 🎯 方案二：Localtunnel（备选 ⭐⭐）

**如果方案一不行，用这个**

### 步骤 1：一键执行

```bash
bash /home/admin/projects/live-tts/setup_https_lt.sh
```

### 步骤 2：获取 HTTPS 链接

脚本会输出：
```
✅ HTTPS 配置完成！

🌐 访问地址：
   https://xxx-xxx.loca.lt
```

### 步骤 3：访问并使用

打开浏览器访问 HTTPS 链接，可以使用语音输入！

---

## 📝 方案三：文字输入（无需配置 ⭐）

**最简单，无需 HTTPS**

### 访问：
```
http://8.213.149.224:7091/voice_chat.html
```

### 使用：
1. 输入文字
2. 按回车
3. 听语音

---

## 🔍 故障排查

### SSH 隧道常见问题

#### Q1: SSH 连接失败？

**检查：**
```bash
ping 8.213.149.224
```

**解决：**
- 检查网络连接
- 确认服务器 IP 正确
- 检查 SSH 端口（默认 22）

---

#### Q2: 端口转发失败？

**错误：**
```
channel 2: open failed: connect failed: Connection refused
```

**检查服务：**
```bash
# 服务器执行
ps aux | grep flask_voice
curl http://localhost:7091/api/health
```

**重启服务：**
```bash
cd /home/admin/projects/live-tts
bash start_voice_service.sh
```

---

#### Q3: 本地无法访问？

**检查：**
```bash
# 本地电脑执行
curl http://localhost:7091/api/health
```

**如果失败：**
- 确认 SSH 隧道还在运行
- 重新执行 SSH 命令
- 检查端口是否被占用

---

### Localtunnel 常见问题

#### Q1: 安装失败？

**错误：**
```
npm: command not found
```

**解决：**
```bash
# 安装 Node.js
apt update
apt install nodejs npm -y

# 重新执行
bash /home/admin/projects/live-tts/setup_https_lt.sh
```

---

#### Q2: 隧道启动失败？

**检查日志：**
```bash
cat /tmp/lt.log
```

**常见原因：**
- 网络连接问题
- 端口被占用
- Localtunnel 服务异常

**解决：**
```bash
# 停止旧进程
pkill -f "lt --port"

# 重启
lt --port 7091
```

---

## 📊 方案对比

| 方案 | 难度 | 成本 | 麦克风 | 推荐度 |
|------|------|------|--------|--------|
| **SSH 隧道** | ⭐⭐ | 免费 | ✅ | ⭐⭐⭐ 最简单 |
| **Localtunnel** | ⭐⭐ | 免费 | ✅ | ⭐⭐ 备选 |
| **文字输入** | ⭐ | 免费 | ❌ | ⭐⭐ 无需配置 |

---

## 🎊 推荐流程

### 最佳方案：SSH 隧道

**优点：**
- ✅ 无需安装
- ✅ 立即生效
- ✅ 安全加密
- ✅ 稳定可靠

**步骤：**
```bash
# 1. 本地电脑执行
ssh -L 7091:localhost:7091 root@8.213.149.224

# 2. 保持 SSH 连接

# 3. 访问
http://localhost:7091/voice_chat.html

# 4. 使用语音输入
# 点击"按住说话" → 说话 → 听语音！
```

---

### 备选方案：Localtunnel

**优点：**
- ✅ 无需 SSH 连接
- ✅ 公网可访问
- ✅ 自动 HTTPS

**缺点：**
- ❌ 需要安装 Node.js
- ❌ 域名随机变化
- ❌ 可能不稳定

**步骤：**
```bash
# 1. 服务器执行
bash /home/admin/projects/live-tts/setup_https_lt.sh

# 2. 获取 HTTPS 链接
# https://xxx-xxx.loca.lt

# 3. 访问并使用
```

---

## 🎯 立即开始

### 推荐：SSH 隧道

**现在就在本地电脑执行：**
```bash
ssh -L 7091:localhost:7091 root@8.213.149.224
```

**然后访问：**
```
http://localhost:7091/voice_chat.html
```

**点击"按住说话"，开始语音对话！** 🎤

---

## 📖 相关文档

- `ENABLE_HTTPS_GUIDE.md` - HTTPS 配置指南
- `TEXT_INPUT_GUIDE.md` - 文字输入指南
- `ACCESS_VOICE_HTML.md` - 访问指南

---

**更新时间**: 2026-04-09  
**推荐方案**: SSH 隧道（无需安装，立即可用）  
**脚本位置**: `/home/admin/projects/live-tts/setup_https_lt.sh`（备选方案）
