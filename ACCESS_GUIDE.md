# 🎤 TTS 语音试听服务 - 访问指南

---

## ✅ 服务已启动

**HTTP 服务**: 运行中 (端口 7085)  
**进程 ID**: 1515846  
**启动时间**: 2026-04-09 09:19

---

## 🌐 访问地址

### 本地访问
```
http://localhost:7085/listen_here.html
```

### 公网访问
```
http://8.213.149.224:7085/listen_here.html
```

> ⚠️ **注意**: 如果公网无法访问，需要在阿里云安全组开放 7085 端口

---

## 🎭 可用语音 (20 个)

### 女声 (14 个)

| 语音 | 名称 | 特点 | 推荐 |
|------|------|------|------|
| xiaoxiao | 小晓 | 温暖、通用 | ⭐⭐⭐ |
| xiaoyi | 小艺 | 活泼、亲切 | ⭐⭐ |
| xiaomo | 小墨 | 温柔、情感 | ⭐⭐ |
| xiaoxuan | 小萱 | 温和、亲切 | ⭐⭐ |
| xiaochen | 小晨 | 新闻、正式 | ⭐ |
| xiaohan | 小涵 | 严肃、专业 | ⭐ |
| xiaomeng | 小萌 | 可爱、活泼 | ⭐ |
| xiaoqiu | 小秋 | 客服、友好 | ⭐ |
| xiaorui | 小睿 | 电话、客服 | ⭐ |
| xiaoshuang | 小爽 | 童声 | ⭐ |
| xiaoyan | 小颜 | 客服、友好 | ⭐ |
| xiaoyou | 小优 | 童声 | ⭐ |
| xiaozhen | 小珍 | 客服、专业 | ⭐ |

### 男声 (6 个)

| 语音 | 名称 | 特点 | 推荐 |
|------|------|------|------|
| yunhao | 云浩 | 广告、促销 | ⭐⭐⭐ |
| yunye | 云野 | 专业、讲解 | ⭐⭐⭐ |
| yunxia | 云霞 | 激情、活力 | ⭐⭐ |
| yunxi | 云希 | 故事、叙述 | ⭐⭐ |
| yunjian | 云健 | 运动、激情 | ⭐ |
| yunfeng | 云峰 | 严肃、正式 | ⭐ |
| yunze | 云泽 | 纪录片、正式 | ⭐ |

---

## 🎵 试听内容

每个语音提供 4 种场景：

1. **通用**: "欢迎观看直播！感谢大家的关注！"
2. **活泼**: "点点关注不迷路，主播带你上高速！"
3. **促销**: "限时优惠，只剩最后 10 单！错过今天就要等下次了！"
4. **温柔**: "喜欢主播的记得点个关注哦～"

**总计**: 20 语音 × 4 场景 = **80 个音频文件**

---

## 📱 使用步骤

### 1. 打开试听页面

**方式 A**: 本地浏览器
```
http://localhost:7085/listen_here.html
```

**方式 B**: 公网浏览器
```
http://8.213.149.224:7085/listen_here.html
```

**方式 C**: 直接打开文件
```bash
firefox /home/admin/projects/live-tts/listen_here.html
```

### 2. 试听语音

- 页面显示所有 20 个语音
- 每个语音有 4 个播放按钮（4 种场景）
- 点击播放按钮即可试听

### 3. 选择喜欢的语音

- 记下语音 ID（如 `xiaoxiao`）
- 比较不同语音的效果
- 选择最适合直播场景的语音

### 4. 开始使用

```bash
cd /home/admin/projects/live-tts
bash start.sh
```

---

## 🎯 推荐配置

### 通用直播
```
语音：xiaoxiao (小晓)
语速：+10%
音量：0%
场景：通用、活泼
```

### 带货直播
```
语音：yunhao (云浩)
语速：+20%
音量：+5%
场景：促销
```

### 游戏直播
```
语音：yunxia (云霞)
语速：+15%
音量：0%
场景：活泼、促销
```

### 教学直播
```
语音：yunye (云野)
语速：-10%
音量：0%
场景：通用、温柔
```

---

## 🔧 服务管理

### 启动服务
```bash
cd /home/admin/projects/live-tts
bash start_web.sh
```

### 停止服务
```bash
# 找到进程 ID
ps aux | grep "http.server 7085"

# 杀死进程
kill <PID>
```

### 重启服务
```bash
# 先停止
pkill -f "http.server 7085"

# 再启动
bash start_web.sh
```

### 查看日志
```bash
cat /tmp/tts_web.log
```

---

## 📁 文件结构

```
/home/admin/projects/live-tts/
├── listen_here.html           # 🎧 试听页面
├── start_web.sh               # 🚀 启动脚本
├── edge_tts_speech.py         # 🎤 TTS 引擎
├── generate_all_demos.py      # 📦 批量生成脚本
├── output/demo/               # 🎵 音频文件
│   ├── xiaoxiao_通用.mp3
│   ├── xiaoxiao_活泼.mp3
│   ├── xiaoxiao_促销.mp3
│   ├── xiaoxiao_温柔.mp3
│   └── ... (共 80 个文件)
├── VOICE_LISTEN_GUIDE.md      # 📖 详细指南
└── ACCESS_GUIDE.md            # 📱 访问指南（本文档）
```

---

## ⚠️ 阿里云安全组配置

如果公网无法访问，需要开放 7085 端口：

### 步骤

1. 登录阿里云控制台
2. 进入 ECS 实例管理
3. 安全组 → 配置规则
4. 入方向 → 添加规则
5. 配置：
   - 协议：TCP
   - 端口：7085/7085
   - 授权对象：0.0.0.0/0
   - 描述：TTS 试听服务

### 验证

```bash
# 检查端口是否监听
netstat -tlnp | grep 7085

# 测试本地访问
curl http://localhost:7085/listen_here.html

# 测试公网访问（从其他设备）
# http://8.213.149.224:7085/listen_here.html
```

---

## 📊 服务信息

| 项目 | 值 |
|------|-----|
| **服务类型** | Python HTTP Server |
| **端口** | 7085 |
| **进程 ID** | 1515846 |
| **音频文件数** | 80 |
| **总大小** | ~1.5 MB |
| **语音数量** | 20 (14 女 + 6 男) |
| **场景数量** | 4 (通用/活泼/促销/温柔) |

---

## 🎉 快速开始

```bash
# 1. 打开浏览器
http://localhost:7085/listen_here.html

# 2. 试听所有语音
# 点击播放按钮

# 3. 选择喜欢的语音
# 记下语音 ID（如 xiaoxiao）

# 4. 开始生成
cd /home/admin/projects/live-tts
bash start.sh
```

---

**服务状态**: ✅ 运行中  
**创建时间**: 2026-04-09  
**最后更新**: 2026-04-09 09:19
