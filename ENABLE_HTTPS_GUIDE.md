# 🔒 一键配置 HTTPS（启用语音输入）

---

## ⚡ 快速方案（5 分钟搞定）

### 方案一：Cloudflare Tunnel（推荐 ⭐⭐⭐）

**免费 HTTPS，无需域名！**

#### 步骤 1：一键执行

```bash
bash /home/admin/projects/live-tts/setup_https.sh
```

#### 步骤 2：获取 HTTPS 链接

脚本会输出：
```
✅ HTTPS 配置完成！

🌐 访问地址：
   https://xxx-xxx-xxx.trycloudflare.com/voice_chat.html

🎤 现在可以使用语音输入了！
```

#### 步骤 3：访问并使用语音

打开浏览器访问 HTTPS 链接，点击"按住说话"即可！

---

### 方案二：SSH 隧道（无需配置）

**适合临时使用**

#### 步骤 1：本地电脑执行

```bash
ssh -L 7091:localhost:7091 root@8.213.149.224
```

#### 步骤 2：访问

```
http://localhost:7091/voice_chat.html
```

**localhost 可以使用麦克风！**

---

### 方案三：文字输入（无需 HTTPS）

**最简单，无需配置**

1. 访问：http://8.213.149.224:7091/voice_chat.html
2. 输入文字
3. 按回车
4. 听语音

---

## 📋 详细配置步骤

### Cloudflare Tunnel 详解

#### 1️⃣ 安装 cloudflared

**手动安装：**
```bash
# 下载
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb

# 安装
sudo dpkg -i cloudflared-linux-amd64.deb

# 验证
cloudflared --version
```

**一键安装（推荐）：**
```bash
bash /home/admin/projects/live-tts/setup_https.sh
```

---

#### 2️⃣ 启动 Tunnel

**方式 A：前台运行（查看日志）**
```bash
cloudflared tunnel --url http://localhost:7091
```

**方式 B：后台运行**
```bash
nohup cloudflared tunnel --url http://localhost:7091 > /tmp/cloudflared.log 2>&1 &
```

**查看日志：**
```bash
tail -f /tmp/cloudflared.log
```

---

#### 3️⃣ 获取 HTTPS URL

启动后会自动生成：
```
Your quick Tunnel has been created! Visit it at (it may take some time to be reachable):
https://xxx-xxx-xxx-xxx.trycloudflare.com
```

**提取 URL：**
```bash
grep -oP 'https://[^\s]+' /tmp/cloudflared.log | head -1
```

---

#### 4️⃣ 访问页面

```
https://xxx-xxx-xxx-xxx.trycloudflare.com/voice_chat.html
```

**现在可以：**
- ✅ 使用麦克风语音输入
- ✅ 按住说话
- ✅ 实时语音对话

---

## 🔧 故障排查

### 问题 1：cloudflared 安装失败

**错误：**
```
dpkg: error: 无法访问归档文件
```

**解决：**
```bash
# 手动下载
cd /tmp
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64
chmod +x cloudflared-linux-amd64
sudo mv cloudflared-linux-amd64 /usr/local/bin/cloudflared

# 验证
cloudflared --version
```

---

### 问题 2：Tunnel 启动失败

**错误：**
```
Failed to create tunnel
```

**原因：** 网络连接问题

**解决：**
```bash
# 检查网络
ping cloudflare.com

# 使用备用镜像
cloudflared tunnel --url http://localhost:7091 --protocol quic
```

---

### 问题 3：页面无法访问

**检查：**
```bash
# 查看 Tunnel 状态
ps aux | grep cloudflared

# 查看日志
tail -f /tmp/cloudflared.log
```

**重启：**
```bash
# 停止
pkill -f cloudflared

# 启动
cloudflared tunnel --url http://localhost:7091 &
```

---

### 问题 4：仍然无法使用麦克风

**检查浏览器权限：**

1. 点击地址栏左侧的 🔒 锁图标
2. 点击"网站设置"
3. 找到"麦克风"
4. 改为"允许"
5. 刷新页面

**检查浏览器：**
- Chrome/Edge：✅ 支持
- Firefox：✅ 支持
- Safari：⚠️ 需要额外配置

---

## 🎯 使用指南

### 语音输入步骤

1. **访问 HTTPS 链接**
   ```
   https://xxx-xxx-xxx.trycloudflare.com/voice_chat.html
   ```

2. **允许麦克风权限**
   - 浏览器会弹出权限请求
   - 点击"允许"

3. **选择语音场景**
   - 🎵 通用
   - 🌸 温柔
   - 🎀 可爱
   - 💼 专业
   - 🔥 促销
   - 🌙 柔弱

4. **按住说话**
   - 按住"🎤 按住说话"按钮
   - 说话
   - 松开结束

5. **等待处理**
   - 系统自动识别语音
   - 转换为文字
   - 显示在对话框

---

## 📊 方案对比

| 方案 | 难度 | 成本 | 麦克风 | 推荐度 |
|------|------|------|--------|--------|
| **Cloudflare** | ⭐⭐ | 免费 | ✅ | ⭐⭐⭐ |
| **SSH 隧道** | ⭐⭐ | 免费 | ✅ | ⭐⭐⭐ |
| **文字输入** | ⭐ | 免费 | ❌ | ⭐⭐ |
| **自签名证书** | ⭐⭐⭐ | 免费 | ✅ | ⭐⭐ |
| **Nginx+Let's Encrypt** | ⭐⭐⭐⭐ | 免费 | ✅ | ⭐⭐ |

---

## 🔗 相关文档

- `TEXT_INPUT_GUIDE.md` - 文字输入使用指南
- `ACCESS_VOICE_HTML.md` - 访问指南
- `SERVICE_FIXED.md` - 服务修复说明

---

##  快速开始

**推荐方案（Cloudflare Tunnel）：**

```bash
# 1. 执行一键脚本
bash /home/admin/projects/live-tts/setup_https.sh

# 2. 等待获取 HTTPS 链接
# 输出：https://xxx-xxx-xxx.trycloudflare.com

# 3. 访问链接
# 打开浏览器，访问 HTTPS 链接

# 4. 使用语音输入
# 点击"按住说话"，开始语音对话！
```

---

## 📞 获取帮助

**查看日志：**
```bash
tail -f /tmp/cloudflared.log
```

**检查服务：**
```bash
ps aux | grep -E "(cloudflared|flask_voice|agent_tts)" | grep -v grep
```

**重启服务：**
```bash
pkill -f cloudflared
pkill -f flask_voice
pkill -f agent_tts

cd /home/admin/projects/live-tts
bash start_voice_service.sh
```

---

**更新时间**: 2026-04-09  
**推荐方案**: Cloudflare Tunnel（5 分钟，免费）  
**脚本位置**: `/home/admin/projects/live-tts/setup_https.sh`
