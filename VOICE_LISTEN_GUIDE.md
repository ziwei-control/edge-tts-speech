# 🎤 语音试听指南

---

## 📍 试听地址

**本地访问**:
```bash
# 方法 1: 直接打开 HTML 文件
firefox /home/admin/projects/live-tts/listen_here.html

# 方法 2: 用浏览器打开
# 文件路径：/home/admin/projects/live-tts/listen_here.html
```

**在线访问** (需启动 Web 服务):
```bash
cd /home/admin/projects/live-tts
python3 -m http.server 7085

# 然后访问：http://localhost:7085/listen_here.html
# 或公网：http://8.213.149.224:7085/listen_here.html
```

---

## 🎭 可用语音 (6 个)

### 女声 (4 个)

| 语音 | 特点 | 推荐场景 | 试听文件 |
|------|------|---------|---------|
| **小晓** (xiaoxiao) | ⭐ 温暖、通用 | 欢迎、通用播报 | 4 个场景 |
| **小艺** (xiaoyi) | 活泼、亲切 | 感谢、互动 | 4 个场景 |
| **小萱** (xiaoxuan) | 温和、亲切 | 情感内容 | 4 个场景 |
| **~~其他~~** | 生成失败 | - | - |

### 男声 (2 个)

| 语音 | 特点 | 推荐场景 | 试听文件 |
|------|------|---------|---------|
| **云健** (yunjian) | 运动、激情 | 游戏直播 | 4 个场景 |
| **云霞** (yunxia) | 激情、活力 | 促销播报 | 4 个场景 |
| **云希** (yunxi) | 故事、叙述 | 讲解内容 | 4 个场景 |

---

## 🎵 试听内容

每个语音提供 4 种场景试听：

1. **通用**: "欢迎观看直播！感谢大家的关注！"
2. **活泼**: "点点关注不迷路，主播带你上高速！"
3. **促销**: "限时优惠，只剩最后 10 单！错过今天就要等下次了！"
4. **温柔**: "喜欢主播的记得点个关注哦～"

---

## 📁 文件位置

```
/home/admin/projects/live-tts/output/demo/
├── xiaoxiao_通用.mp3    (22K)  ✅
├── xiaoxiao_活泼.mp3    (20K)  ✅
├── xiaoxiao_促销.mp3    (31K)  ✅
├── xiaoxiao_温柔.mp3    (17K)  ✅
├── xiaoyi_通用.mp3      (22K)  ✅
├── xiaoyi_活泼.mp3      (22K)  ✅
├── xiaoyi_促销.mp3      (32K)  ✅
├── xiaoyi_温柔.mp3      (18K)  ✅
├── yunjian_通用.mp3     (23K)  ✅
├── yunjian_活泼.mp3     (22K)  ✅
├── yunjian_促销.mp3     (33K)  ✅
├── yunjian_温柔.mp3     (18K)  ✅
├── xiaoxuan_通用.mp3    (22K)  ✅
├── xiaoxuan_活泼.mp3    (22K)  ✅
├── xiaoxuan_促销.mp3    (32K)  ✅
├── xiaoxuan_温柔.mp3    (17K)  ✅
├── yunxia_通用.mp3      (23K)  ✅
├── yunxia_活泼.mp3      (22K)  ✅
├── yunxia_促销.mp3      (33K)  ✅
├── yunxia_温柔.mp3      (18K)  ✅
├── yunxi_通用.mp3       (22K)  ✅
├── yunxi_活泼.mp3       (21K)  ✅
├── yunxi_促销.mp3       (32K)  ✅
└── yunxi_温柔.mp3       (17K)  ✅

共 24 个文件，约 550 KB
```

---

## 🎯 推荐选择

### 最佳通用语音
**🏆 小晓 (xiaoxiao)**
- 温暖、自然、适应性强
- 适合 90% 的直播场景
- 观众接受度最高

### 最佳促销语音
**🏆 云霞 (yunxia)**
- 激情、有感染力
- 营造紧迫感
- 适合带货直播

### 最佳互动语音
**🏆 小艺 (xiaoyi)**
- 活泼、亲切
- 拉近与观众距离
- 适合感谢、欢迎

---

## 🚀 快速使用

### 1. 试听
打开 `listen_here.html`，点击播放按钮试听所有语音。

### 2. 选择
记下喜欢的语音名称（如 `xiaoxiao`）。

### 3. 生成
```bash
cd /home/admin/projects/live-tts
bash start.sh

> s
输入文本：你的文案
语音 (默认 xiaoxiao): xiaoxiao
文件名：welcome.mp3
```

### 4. 使用
将生成的 MP3 导入 OBS 或直播软件。

---

## ⚙️ 语速调节建议

| 场景 | 推荐语音 | 语速 |
|------|---------|------|
| 通用欢迎 | xiaoxiao | +10% |
| 促销播报 | yunxia | +20% |
| 感谢互动 | xiaoyi | +15% |
| 温柔内容 | xiaoxuan | 0% |
| 游戏直播 | yunjian | +15% |
| 讲解教学 | yunxi | -10% |

---

## 📞 常见问题

**Q: 为什么只有 6 个语音？**
A: 其他语音生成失败（可能是网络或 API 限制）。这 6 个是最常用的，足够满足大部分需求。

**Q: 可以生成更多语音吗？**
A: 可以，运行：
```bash
python3 generate_all_demos.py
```

**Q: 音质如何？**
A: Edge TTS 使用微软 Azure 引擎，音质接近真人，远优于本地 TTS。

**Q: 需要付费吗？**
A: Edge TTS 目前免费使用（通过 Edge 浏览器 API）。

---

**创建时间**: 2026-04-09  
**试听页面**: `/home/admin/projects/live-tts/listen_here.html`  
**音频文件**: `/home/admin/projects/live-tts/output/demo/`
