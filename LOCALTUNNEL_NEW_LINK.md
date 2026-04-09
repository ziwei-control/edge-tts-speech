# 🔒 Localtunnel 重启 - 新链接

---

## ⚠️ 503 错误原因

**Localtunnel 服务停止了**

免费版 Localtunnel 会：
- 不定期自动停止
- 域名每次重启都变化
- 需要手动重启

---

## ✅ 已修复

**新链接：**
```
https://six-turtles-pump.loca.lt
```

**完整访问地址：**
```
https://six-turtles-pump.loca.lt/voice_library.html
```

---

## 🎯 立即访问

### 完整语音库（152 个音色）
```
https://six-turtles-pump.loca.lt/voice_library.html
```

### 语音交互页面
```
https://six-turtles-pump.loca.lt/voice_chat.html
```

### 4 版本对比页面
```
https://six-turtles-pump.loca.lt/all_versions.html
```

---

## ⚠️ 首次访问提示

**浏览器显示"连接不是私密的"：**
1. 点击"高级"
2. 点击"继续访问"
3. 这是正常的（自签名证书）

---

## 🔄 域名变化记录

| 重启时间 | 域名 |
|---------|------|
| 第一次 | young-lizards-open.loca.lt |
| 第二次 | whole-mice-work.loca.lt |
| 第三次 | six-turtles-pump.loca.lt ✅ |

**每次重启域名都会变化，这是正常的！**

---

## 🚀 一键重启 Localtunnel

**创建 `restart_lt.sh`：**
```bash
#!/bin/bash
pkill -f "lt --port"
lt --port 7091 > /tmp/lt.log 2>&1 &
sleep 5
echo "✅ 新链接："
cat /tmp/lt.log | grep "your url is"
```

**使用方法：**
```bash
bash restart_lt.sh
```

---

## 📊 服务状态检查

**检查 Localtunnel：**
```bash
ps aux | grep "lt --port" | grep -v grep
```

**查看当前链接：**
```bash
cat /tmp/lt.log | grep "your url is"
```

**健康检查：**
```bash
# Web 服务
curl http://localhost:7091/api/health

# TTS API
curl http://localhost:7086/health

# STT API
curl http://localhost:5050/health
```

---

## 💡 使用技巧

### 技巧 1：保存书签

**因为域名会变：**
1. 访问新链接
2. 保存书签
3. 如果 503，重启获取新链接
4. 更新书签

---

### 技巧 2：使用 screen 持久运行

```bash
# 安装 screen
apt install screen -y

# 创建会话
screen -S localtunnel

# 启动 Localtunnel
lt --port 7091

# 按 Ctrl+A, D 分离

# 随时恢复
screen -r localtunnel
```

**优点：**
- 会话持久运行
- SSH 断开也不影响
- 随时恢复控制

---

### 技巧 3：设置自动重启

**创建 `monitor_lt.sh`：**
```bash
#!/bin/bash
while true; do
    if ! pgrep -f "lt --port" > /dev/null; then
        echo "$(date): Localtunnel 停止，重启中..."
        lt --port 7091 > /tmp/lt.log 2>&1 &
    fi
    sleep 60
done
```

**后台运行：**
```bash
nohup bash monitor_lt.sh > logs/lt_monitor.log 2>&1 &
```

**每分钟检查，自动重启**

---

## 🔍 故障排查

### 问题 1：持续 503

**原因：** Localtunnel 服务器问题

**解决：**
```bash
# 重启获取新服务器
pkill -f "lt --port"
sleep 2
lt --port 7091 > /tmp/lt.log 2>&1 &
sleep 5
cat /tmp/lt.log | grep "your url is"
```

---

### 问题 2：页面加载慢

**原因：** Localtunnel 服务器负载高

**解决：**
```bash
# 重启获取更好的服务器
pkill -f "lt --port"
lt --port 7091 > /tmp/lt.log 2>&1 &
```

---

### 问题 3：证书错误

**正常现象！** Localtunnel 使用自签名证书

**解决：**
1. 点击"高级"
2. 点击"继续访问"
3. 添加书签

---

## 📱 移动端访问

**手机/平板也可以访问：**
```
https://six-turtles-pump.loca.lt/voice_library.html
```

**功能：**
- ✅ 响应式设计
- ✅ 触摸优化
- ✅ 即时播放

---

## 🎊 当前状态

### 所有服务运行中

| 服务 | 状态 | 端口 |
|------|------|------|
| **Localtunnel** | ✅ 运行中 | HTTPS |
| **Web 服务** | ✅ 运行中 | 7091 |
| **TTS API** | ✅ 运行中 | 7086 |
| **STT API** | ✅ 运行中 | 5050 |

---

### 最新链接

**HTTPS 访问：**
```
https://six-turtles-pump.loca.lt
```

**完整语音库：**
```
https://six-turtles-pump.loca.lt/voice_library.html
```

**语音交互：**
```
https://six-turtles-pump.loca.lt/voice_chat.html
```

---

## 📖 相关文档

| 文档 | 说明 |
|------|------|
| **LOCALTUNNEL_RESTARTED.md** | Localtunnel 重启报告 |
| **VOICE_LIBRARY_GUIDE.md** | 语音库使用指南 |
| **SERVICE_FIXED_REPORT.md** | 服务修复报告 |

---

## ✅ 总结

**问题：** Localtunnel 停止 → 503 错误  
**解决：** 重启 Localtunnel  
**新链接：** https://six-turtles-pump.loca.lt  
**状态：** ✅ 运行正常  

**立即可用：**
1. 访问新链接
2. 点击"继续访问"
3. 浏览 152 个语音
4. 点击播放！

---

**更新时间**: 2026-04-09 16:35  
**当前链接**: https://six-turtles-pump.loca.lt  
**状态**: ✅ 运行中  
**提示**: 域名会变，重启后查看新链接
