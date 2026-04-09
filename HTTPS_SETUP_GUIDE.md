# 🔒 HTTPS 配置指南（启用麦克风）

---

## ⚠️ 问题说明

**错误信息：**
```
无法访问麦克风：Cannot read properties of undefined (reading 'getUserMedia')
```

**原因：**
- 浏览器安全策略要求 **麦克风必须在 HTTPS 环境下使用**
- HTTP 公网访问（`http://8.213.149.224:7091`）会被浏览器阻止
- localhost 是例外（可以使用 HTTP）

---

## ✅ 解决方案

### 方案一：使用文字输入（推荐 ⭐⭐⭐）

**无需配置，立即可用！**

**已添加功能：**
- ✅ 文字输入框
- ✅ 按回车发送
- ✅ 自动调用 TTS 生成语音
- ✅ 自动播放生成的音频

**使用方法：**
1. 访问页面：http://8.213.149.224:7091/voice_chat.html
2. 在输入框输入文字
3. 按回车或点击"发送"
4. 系统会自动用 TTS 语音读出文字

---

### 方案二：配置 HTTPS（高级）

#### 方法 A：使用 Nginx + Let's Encrypt（免费）

**步骤 1：安装 Nginx**
```bash
sudo apt update
sudo apt install nginx -y
```

**步骤 2：安装 Certbot**
```bash
sudo apt install certbot python3-certbot-nginx -y
```

**步骤 3：申请证书**
```bash
# 需要域名
sudo certbot --nginx -d your-domain.com
```

**步骤 4：配置 Nginx 反向代理**
```nginx
server {
    listen 443 ssl;
    server_name your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    location / {
        proxy_pass http://localhost:7091;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

**步骤 5：重启 Nginx**
```bash
sudo systemctl restart nginx
```

**访问：** `https://your-domain.com/voice_chat.html`

---

#### 方法 B：使用 Cloudflare Tunnel（免费，无需域名）

**步骤 1：安装 cloudflared**
```bash
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo dpkg -i cloudflared-linux-amd64.deb
```

**步骤 2：创建 Tunnel**
```bash
cloudflared tunnel --url http://localhost:7091
```

**步骤 3：获取 HTTPS 链接**
```
https://xxx-xxx-xxx.trycloudflare.com
```

**优点：**
- ✅ 免费 HTTPS
- ✅ 无需域名
- ✅ 自动证书
- ✅ 穿透内网

---

#### 方法 C：自签名证书（测试用）

**步骤 1：生成证书**
```bash
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
```

**步骤 2：修改 Flask 服务器**

编辑 `flask_voice_server.py`，末尾添加：
```python
if __name__ == '__main__':
    print("=" * 60)
    print("🌐 语音交互 Web 服务器（HTTPS）")
    print("=" * 60)
    app.run(host='0.0.0.0', port=7091, ssl_context=('cert.pem', 'key.pem'))
```

**步骤 3：重启服务**
```bash
pkill -f flask_voice_server
cd /home/admin/projects/live-tts
python3 flask_voice_server.py &
```

**访问：** `https://8.213.149.224:7091/voice_chat.html`

**注意：** 浏览器会显示"证书不安全"，点击"继续访问"即可。

---

### 方案三：本地访问（无需 HTTPS）

**使用 SSH 隧道：**

**本地电脑执行：**
```bash
ssh -L 7091:localhost:7091 root@8.213.149.224
```

**然后访问：**
```
http://localhost:7091/voice_chat.html
```

**优点：**
- ✅ 可以使用麦克风
- ✅ 无需配置 HTTPS
- ✅ 安全加密

**缺点：**
- ❌ 需要保持 SSH 连接

---

## 🎯 推荐方案对比

| 方案 | 难度 | 成本 | 麦克风 | 推荐场景 |
|------|------|------|--------|---------|
| **文字输入** | ⭐ | 免费 | ❌ | 日常使用 ⭐⭐⭐ |
| **Cloudflare** | ⭐⭐ | 免费 | ✅ | 公网访问 ⭐⭐⭐ |
| **Nginx+Let's Encrypt** | ⭐⭐⭐ | 免费 | ✅ | 有域名 ⭐⭐ |
| **自签名证书** | ⭐⭐ | 免费 | ✅ | 测试用 ⭐⭐ |
| **SSH 隧道** | ⭐⭐ | 免费 | ✅ | 本地测试 ⭐⭐⭐ |

---

## 📝 文字输入使用说明

**页面已更新，新增文字输入功能：**

```
┌────────────────────────────────────┐
│  [输入框：输入文字...]  [发送]    │  ← 新增
├────────────────────────────────────┤
│        🎤 按住说话（需 HTTPS）     │
│  ⚠️ 公网访问请使用文字输入...      │  ← 提示
└────────────────────────────────────┘
```

**使用流程：**
1. 访问页面（HTTP 即可）
2. 选择语音场景（通用/温柔/可爱等）
3. 输入框输入文字
4. 按回车或点击"发送"
5. 系统自动用 TTS 读出文字

**示例：**
```
输入："你好，今天天气真好"
→ 系统用选择的语音读出这句话
→ 页面自动播放生成的音频
```

---

## 🔧 验证文字输入功能

**测试命令：**
```bash
# 测试 TTS API
curl -X POST http://localhost:7086/speak \
  -H "Content-Type: application/json" \
  -d '{"text":"测试文字输入功能","scene":"default"}'

# 预期输出
{"success":true,"filename":"speech_xxx.mp3","message":"生成成功"}
```

---

## 🎊 现在刷新页面

**刷新浏览器（Ctrl + F5），你会看到：**

1. ✅ 新增文字输入框
2. ✅ 发送按钮
3. ✅ 提示文字"⚠️ 公网访问请使用文字输入"
4. ✅ 录音按钮标注"（需 HTTPS）"

**使用方法：**
- 输入文字 → 按回车 → 听语音

---

## 📖 相关文档

- `ACCESS_VOICE_HTML.md` - 访问指南
- `SERVICE_FIXED.md` - 服务修复说明
- `AGENT_TTS_COMPLETE.md` - TTS 完整集成文档

---

**更新时间**: 2026-04-09  
**新增功能**: 文字输入 + TTS 语音播放  
**服务状态**: ✅ 运行中
