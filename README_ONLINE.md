# 🎤 在线口播语音合成系统 - Edge TTS 版

---

## ✅ 优势

相比本地 TTS，Edge TTS 有以下优势：

| 特性 | 本地 TTS (pyttsx3) | Edge TTS (在线) |
|------|-------------------|----------------|
| **音质** | 机械音 | 🟢 接近真人 |
| **语音数量** | 2-5 种 | 🟢 20+ 种中文 |
| **情感表达** | 无 | 🟢 多种情感 |
| **安装依赖** | espeak 等 | 🟢 无需额外依赖 |
| **服务器支持** | ❌ 需要音频设备 | 🟢 完美支持 |
| **网络要求** | 无需网络 | 需要网络 |

---

## 📦 系统组成

```
/home/admin/projects/live-tts/
├── edge_tts_speech.py     # 主程序（在线 TTS）
├── tts_speech.py          # 备用程序（本地 TTS）
├── start.sh               # 启动脚本
├── speech_templates.txt   # 口播文案模板
├── output/                # 输出目录
│   └── test.mp3           # 测试文件（已生成）
└── README_ONLINE.md       # 本文档
```

---

## 🚀 快速开始

### 1. 启动系统

```bash
cd /home/admin/projects/live-tts
bash start.sh
```

### 2. 选择语音

```
🎭 可用语音:
   1. xiaoxiao    - 女声（温暖）⭐推荐
   2. xiaoyi      - 女声（活泼）
   3. yunjian     - 男声（运动）
   4. xiaochen    - 女声（新闻）
   5. xiaohan     - 女声（严肃）
   6. xiaomeng    - 女声（可爱）
   7. xiaomo      - 女声（温柔）
   8. xiaoqiu     - 女声（客服）
   9. xiaorui     - 女声（电话）
  10. xiaoshuang  - 童声（儿童）
  11. xiaoxuan    - 女声（温和）
  12. xiaoyan     - 女声（客服）
  13. xiaoyou     - 童声（儿童）
  14. xiaozhen    - 女声（客服）
  15. yunfeng     - 男声（严肃）
  16. yunhao      - 男声（广告）
  17. yunxia      - 男声（激情）
  18. yunxi       - 男声（故事）
  19. yunye       - 男声（专业）
  20. yunze       - 男声（纪录片）
```

### 3. 生成语音

```
> s
输入文本：欢迎观看直播！
语音 (默认 xiaoxiao): 
语速调整 (-50 到 +50，默认 0): 10
音量调整 (-100 到 +100，默认 0): 0
文件名 (默认 output_时间戳.mp3): welcome.mp3

✅ 生成成功：welcome.mp3
   语音：xiaoxiao (zh-CN-XiaoxiaoNeural)
   语速：+10%
   音量：+0%
```

---

## 🎭 推荐语音配置

### 直播口播

| 场景 | 推荐语音 | 语速 | 音量 |
|------|---------|------|------|
| **通用欢迎** | xiaoxiao (女) | +10% | 0% |
| **促销播报** | yunhao (男) | +20% | +5% |
| **感谢礼物** | xiaoyi (女) | +15% | 0% |
| **儿童内容** | xiaoshuang (童) | 0% | 0% |
| **专业讲解** | yunye (男) | -10% | 0% |

### 语速参考

```
-50% ~ -30%  : 极慢（强调、抒情）
-20% ~ -10%  : 慢速（教学、讲解）
-5% ~ +5%    : 正常（日常对话）
+10% ~ +20%  : 快速（促销、活跃）
+25% ~ +50%  : 极快（紧张、紧急）
```

---

## 📝 批量生成脚本

创建 `batch_generate.py`:

```python
#!/usr/bin/env python3
"""批量生成口播语音"""

import asyncio
from edge_tts_speech import generate_speech

async def main():
    # 文案列表
    scripts = [
        ("output/welcome_01.mp3", "欢迎观看直播！", "xiaoxiao"),
        ("output/welcome_02.mp3", "欢迎新进来的朋友！", "xiaoyi"),
        ("output/thank_01.mp3", "感谢大家的关注！", "xiaoxiao"),
        ("output/thank_02.mp3", "感谢送出的礼物！", "xiaoyi"),
        ("output/promo_01.mp3", "限时优惠，只剩最后 10 单！", "yunhao"),
        ("output/follow_01.mp3", "喜欢主播的记得点个关注哦！", "xiaomo"),
        ("output/ending_01.mp3", "今天的直播就到这里了！", "xiaoxiao"),
        ("output/ending_02.mp3", "明天晚上 8 点，不见不散！", "xiaoyi"),
    ]
    
    print(f"📝 开始生成 {len(scripts)} 个语音文件...\n")
    
    for filename, text, voice in scripts:
        print(f"生成：{text[:20]}...")
        await generate_speech(text, voice, filename, rate=10, volume=0)
        print()
    
    print("✅ 全部生成完成！")

if __name__ == '__main__':
    asyncio.run(main())
```

运行:
```bash
cd /home/admin/projects/live-tts
python3 batch_generate.py
```

---

## 🎯 直播应用场景

### 场景 1: 自动欢迎

```python
import asyncio
from edge_tts_speech import generate_speech

async def welcome_user(username):
    text = f"欢迎 {username} 加入直播间！"
    await generate_speech(text, "xiaoyi", f"output/welcome_{username}.mp3")
    # 然后播放文件...
```

### 场景 2: 礼物感谢

```python
async def thank_gift(username, gift_name):
    text = f"感谢 {username} 送出的 {gift_name}！"
    await generate_speech(text, "xiaoxiao", "output/thank_gift.mp3")
```

### 场景 3: 定时促销

```python
async def promo_loop():
    while streaming:
        await generate_speech(
            "限时优惠，只剩最后 10 单！错过今天就要等下次了！",
            "yunhao",
            "output/promo.mp3",
            rate=20  # 加快语速，营造紧迫感
        )
        await asyncio.sleep(300)  # 5 分钟一次
```

### 场景 4: 智能回复

```python
async def smart_reply(question):
    # AI 生成回复
    reply = await ai_generate_answer(question)
    
    # TTS 朗读
    await generate_speech(
        reply,
        "xiaoxiao",
        "output/reply.mp3",
        rate=0
    )
```

---

## 🔧 与 OBS 集成

### 方式 1: 预生成音频文件

**步骤**:
1. 批量生成常用语音
2. OBS → 来源 → 添加 → 媒体
3. 选择生成的 MP3 文件
4. 设置快捷键触发

**优点**:
- ✅ 稳定可靠
- ✅ 无延迟
- ✅ 不依赖网络

---

### 方式 2: 实时生成 + 播放

**脚本**: `live_tts_controller.py`

```python
#!/usr/bin/env python3
"""实时 TTS 控制器"""

import asyncio
import pygame
from edge_tts_speech import generate_speech

class LiveTTSController:
    def __init__(self):
        pygame.mixer.init()
    
    async def speak(self, text, voice="xiaoxiao"):
        # 生成语音
        filename = f"/tmp/tts_{int(time.time())}.mp3"
        await generate_speech(text, voice, filename)
        
        # 播放
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        
        # 等待播放完成
        while pygame.mixer.music.get_busy():
            await asyncio.sleep(0.1)

# 使用
async def main():
    controller = LiveTTSController()
    await controller.speak("欢迎观看直播！")

asyncio.run(main())
```

---

### 方式 3: 虚拟音频线

**Windows**:
1. 安装 VB-Cable
2. 设置默认播放设备为 VB-Cable
3. OBS 音频输入选择 VB-Cable
4. 运行 TTS 脚本

**Linux**:
```bash
# 创建虚拟音频设备
pactl load-module module-null-sink sink_name=tts_output

# 设置 TTS 输出
# (需要配置 pulseaudio)

# OBS 捕获 tts_output
```

---

## 📊 音频参数建议

### OBS 混音设置

```
音频源          音量      说明
─────────────────────────────
麦克风          100%     主语音
TTS 音频         60-70%   辅助播报
背景音乐        30-40%   氛围
游戏音效        50-60%   游戏直播
```

### 音频滤镜

**TTS 音频通道**:
1. **均衡器**: 
   - 低频削减：-3dB @ 100Hz
   - 高频提升：+2dB @ 5kHz

2. **压缩器**:
   - 阈值：-20dB
   - 比率：3:1

3. **限幅器**:
   - 阈值：-1dB
   - 防止爆音

---

## 🌐 API 集成

### 通过 API 调用

创建 `tts_api_server.py`:

```python
from flask import Flask, request, send_file
import asyncio
from edge_tts_speech import generate_speech

app = Flask(__name__)

@app.route('/tts', methods=['POST'])
def tts():
    data = request.json
    text = data.get('text', '')
    voice = data.get('voice', 'xiaoxiao')
    
    filename = f"/tmp/tts_{int(time.time())}.mp3"
    
    asyncio.run(generate_speech(text, voice, filename))
    
    return send_file(filename, mimetype='audio/mpeg')

if __name__ == '__main__':
    app.run(port=7079)
```

使用:
```bash
curl -X POST http://localhost:7079/tts \
  -H "Content-Type: application/json" \
  -d '{"text":"欢迎观看直播！","voice":"xiaoxiao"}' \
  --output welcome.mp3
```

---

## ⚠️ 注意事项

### 1. 网络要求

Edge TTS 需要联网使用。

**检查**:
```bash
ping azure.microsoft.com
```

**失败处理**:
- 准备本地 TTS 备用
- 预生成常用语音
- 使用离线 TTS 引擎

### 2. 速率限制

微软 Edge TTS 有速率限制。

**建议**:
- 避免高频调用（<10 次/分钟）
- 预生成常用语音
- 缓存生成的音频

### 3. 版权问题

生成的音频可用于:
- ✅ 个人直播
- ✅ 视频配音
- ✅ 学习用途

不可用于:
- ❌ 商业销售
- ❌ 冒充真人
- ❌ 虚假宣传

---

## 📁 文件管理

### 推荐结构

```
live-tts/
├── edge_tts_speech.py       # 主程序
├── batch_generate.py        # 批量生成
├── live_tts_controller.py   # 直播控制器
├── tts_api_server.py        # API 服务
├── output/
│   ├── welcome/            # 欢迎语音
│   │   ├── welcome_01.mp3
│   │   └── welcome_02.mp3
│   ├── thank/              # 感谢语音
│   │   ├── thank_gift.mp3
│   │   └── thank_follow.mp3
│   ├── promo/              # 促销语音
│   │   └── limited_offer.mp3
│   └── ending/             # 结束语音
│       └── goodbye.mp3
└── templates/              # 文案模板
    └── scripts.txt
```

### 命名规范

```
{场景}_{内容}_{序号}.mp3

示例:
welcome_general_01.mp3
thank_gift_01.mp3
promo_limited_01.mp3
ending_normal_01.mp3
```

---

## 📞 常见问题

**Q: 生成失败怎么办？**
A: 
- 检查网络连接
- 检查文本是否包含特殊字符
- 尝试更换语音
- 使用本地 TTS 备用

**Q: 音质不好怎么办？**
A:
- 选择更适合的语音
- 调整语速（+10% 更清晰）
- 添加音频滤镜
- 使用付费 Azure TTS

**Q: 如何控制播放时机？**
A:
- 预生成文件 + OBS 快捷键
- 实时生成 + Python 控制
- 接入直播平台 API 触发

**Q: 可以同时播放 BGM 吗？**
A:
- 可以，OBS 中分别控制音量
- TTS: 60-70%
- BGM: 30-40%
- 使用闪避功能（TTS 时自动降低 BGM）

---

## 🚀 下一步

1. **批量生成常用语音**
   ```bash
   python3 batch_generate.py
   ```

2. **导入 OBS**
   - 添加媒体源
   - 设置快捷键

3. **测试直播**
   - 调整音量平衡
   - 测试触发时机

4. **正式使用**
   - 监控观众反馈
   - 优化文案和语音

---

**创建时间**: 2026-04-09  
**版本**: v2.0 (Edge TTS 在线版)  
**依赖**: edge-tts (已安装)  
**测试**: ✅ 成功生成 test.mp3
