# 🎤 Edge TTS 口播语音系统

基于微软 Edge TTS 的直播口播语音合成系统，支持 20+ 中文语音，音质接近真人。

---

## ✨ 特性

- 🎯 **20+ 中文语音**：14 女声 + 6 男声，多种风格可选
- 🎨 **4 种版本**：原版、优化版、粘人版、柔弱版
- 🎵 **152 个预设音频**：欢迎、感谢、求关注、撒娇、促销、互动等场景
- 🎛️ **语速音量调节**：-50% 到 +50% 精细调整
- 📝 **文案模板**：6 类话术模板，开箱即用
- 🌐 **Web 试听页面**：在线试听，快速选择
- 🎧 **批量生成**：一键生成所有语音组合

---

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install edge-tts
# 或使用 uv
uv pip install edge-tts
```

### 2. 生成语音

```bash
bash start.sh
```

### 3. 试听

访问试听页面：
```
http://localhost:7085/all_versions.html
```

---

## 🎤 语音版本

| 版本 | 特色 | 语速 | 音量 | 适合场景 |
|------|------|------|------|---------|
| 🎵 **原版** | 基础未优化 | 0% | 0% | 测试对比 |
| 🎯 **优化版** | 自然度提升 | -5% | 0% | 通用直播 ⭐⭐⭐ |
| 🎀 **粘人版** | 撒娇可爱 | -10% | 0% | 娱乐带货 ⭐⭐⭐ |
| 🌸 **柔弱版** | 喘气虚弱 | -20% | -10% | ASMR/病娇 ⭐⭐⭐ |

---

## 🎯 推荐语音

### 通用直播
- **xiaoxiao (小晓)**：温暖通用 ⭐⭐⭐
- **xiaoyi (小艺)**：活泼亲切 ⭐⭐

### 娱乐带货
- **xiaoxiao (小晓)**：撒娇粘人 ⭐⭐⭐
- **yunhao (云浩)**：广告促销 ⭐⭐⭐

### ASMR/病娇
- **xiaoxiao (小晓)**：柔弱虚弱 ⭐⭐⭐
- **xiaoxuan (小萱)**：轻柔无力 ⭐⭐

---

## 📁 文件结构

```
live-tts/
├── edge_tts_speech.py      # TTS 引擎
├── generate_all_demos.py   # 原版生成脚本
├── generate_natural.py     # 优化版生成脚本
├── generate_cute.py        # 粘人版生成脚本
├── generate_weak.py        # 柔弱版生成脚本
├── start.sh                # 启动脚本
├── start_web.sh            # Web 服务启动
├── speech_templates.txt    # 文案模板
├── all_versions.html       # 综合试听页面
├── README.md               # 本文件
└── output/                 # 音频输出目录
    ├── demo/               # 原版 (80 个)
    ├── natural/            # 优化版 (24 个)
    ├── cute/               # 粘人版 (24 个)
    └── weak/               # 柔弱版 (24 个)
```

---

## 💡 使用示例

### 交互式生成

```bash
bash start.sh

# 选择模式
> s  # 单条生成
> b  # 批量生成
> l  # 列出所有语音

# 输入文案
输入文本：欢迎宝宝～来看直播呀！
语音：xiaoxiao
语速：-10
文件名：welcome.mp3
```

### 代码调用

```python
from edge_tts_speech import generate_speech
import asyncio

async def main():
    await generate_speech(
        text="欢迎宝宝～来看直播呀！💕",
        voice="xiaoxiao",
        output_file="welcome.mp3",
        rate=-10,
        volume=0
    )

asyncio.run(main())
```

---

## 🎛️ 语音列表

### 女声 (14 个)

| 语音 | 描述 | 推荐场景 |
|------|------|---------|
| xiaoxiao | 温暖亲切 | 通用 ⭐⭐⭐ |
| xiaoyi | 活泼开朗 | 娱乐 ⭐⭐ |
| xiaoxuan | 温柔亲切 | 睡前故事 ⭐⭐ |
| xiaomo | 可爱萌妹 | 二次元 ⭐⭐ |
| xiaoyou | 童声萝莉 | 萝莉角色 ⭐ |
| yunjian | 新闻播报 | 正式 ⭐ |
| yunxi | 青年男声 | 通用 ⭐ |
| ... | ... | ... |

### 男声 (6 个)

| 语音 | 描述 | 推荐场景 |
|------|------|---------|
| yunhao | 广告促销 | 带货 ⭐⭐⭐ |
| yunye | 专业讲解 | 知识分享 ⭐⭐⭐ |
| yunfeng | 成熟稳重 | 正式 ⭐⭐ |
| ... | ... | ... |

---

## 📊 音频统计

- **总文件数**: 152 个
- **总大小**: ~2.2 MB
- **语音时长**: 平均 3-5 秒/个
- **支持格式**: MP3

---

## 🔗 在线试听

### 综合页面
- http://localhost:7085/all_versions.html

### 独立页面
- 🎵 原版：http://localhost:7085/listen_here.html
- 🎯 优化版：http://localhost:7085/compare_natural.html
- 🎀 粘人版：http://localhost:7085/cute_voice.html
- 🌸 柔弱版：http://localhost:7085/weak_voice.html

---

## 📖 文档

- `README.md` - 基础使用指南
- `README_ONLINE.md` - 在线版指南
- `ACCESS_GUIDE.md` - 访问指南
- `VOICE_LISTEN_GUIDE.md` - 语音试听指南
- `OPTIMIZATION_GUIDE.md` - 优化指南
- `CUTE_VOICE_GUIDE.md` - 粘人版指南
- `WEAK_VOICE_GUIDE.md` - 柔弱版指南
- `ALL_VERSIONS_GUIDE.md` - 全版本整合指南

---

## ⚠️ 注意事项

1. **需要网络连接**：Edge TTS 是在线服务
2. **服务器无音频设备**：需在本地电脑播放
3. **部分语音可能失败**：网络问题导致
4. **建议预先生成**：常用语提前生成

---

## 🎉 应用场景

- ✅ **直播口播**：欢迎、感谢、促销
- ✅ **短视频配音**：自动旁白
- ✅ **有声书**：批量生成
- ✅ **客服语音**：自动回复
- ✅ **教育内容**：课程配音
- ✅ **游戏直播**：互动语音
- ✅ **ASMR**：柔弱版专用

---

## 📄 许可证

MIT License

---

## 🙏 致谢

- 微软 Edge TTS：https://github.com/rany2/edge-tts
- Azure Cognitive Services

---

**创建时间**: 2026-04-09  
**版本**: 1.0.0  
**作者**: CoPaw AI Agent  
**音频数**: 152 个  
**总大小**: 2.2 MB
