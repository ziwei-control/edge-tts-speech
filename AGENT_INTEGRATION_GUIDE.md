# 🤖 智能 Agent TTS 集成指南

---

## 📊 适配能力总结

| 功能 | 预设音频 (152 个) | TTS 引擎 | API 服务 |
|------|------------------|---------|---------|
| **任意文本** | ❌ | ✅ | ✅ |
| **实时生成** | ❌ | ✅ | ✅ |
| **情感风格** | ⚠️ 固定 4 种 | ✅ 7 种场景 | ✅ 7 种场景 |
| **语速调节** | ❌ | ✅ | ✅ |
| **音量调节** | ❌ | ✅ | ✅ |
| **多语音** | ✅ 20 个 | ✅ 20 个 | ✅ 8 个 |
| **对话场景** | ❌ | ✅ | ✅ |
| **Agent 集成** | ❌ | ⚠️ 代码级 | ✅ API 调用 |

---

## ✅ 可以适配的场景

### 1️⃣ 智能客服对话

```python
from agent_tts import AgentTTS

tts = AgentTTS()

# 用户询问
await tts.speak("你好，我想咨询产品价格", "xiaoxiao", save=True)

# Agent 回复（专业风格）
await tts.speak_with_scene("您好，我们的产品价格为 199 元，现在有限时优惠。", "professional")

# 用户继续询问
await tts.speak("有什么优惠？", "xiaoxiao", save=True)

# Agent 回复（促销风格）
await tts.speak_with_scene("现在下单立减 50 元，还包邮哦！", "promotion")
```

---

### 2️⃣ 直播互动 Agent

```python
# 欢迎观众
await tts.speak_with_scene("欢迎宝宝来到直播间！💕", "cute")

# 回答弹幕问题
await tts.speak_with_scene("这位宝宝问价格，我们直播间特价 99 元！", "promotion")

# 感谢礼物
await tts.speak_with_scene("谢谢宝宝的礼物～爱你哟！😘", "cute")

# 柔弱风格（ASMR 直播）
await tts.speak_with_scene("呼～人家有点累了呢...宝宝陪陪我嘛...", "weak")
```

---

### 3️⃣ 语音助手

```python
# 天气查询
await tts.speak_with_scene("今天北京晴，气温 15 到 25 度，适合外出。", "professional")

# 提醒服务
await tts.speak_with_scene("主人，该喝水了哦～", "cute")

# 新闻播报
await tts.speak_with_scene("现在是北京时间上午 10 点，为您播报最新新闻。", "xiaochen")
```

---

### 4️⃣ 游戏 NPC 对话

```python
# NPC  greeting
await tts.speak_with_scene("欢迎来到冒险者公会，年轻的勇士。", "yunye")

# 任务发布
await tts.speak_with_scene("公会需要你去讨伐城外的哥布林，报酬是 500 金币。", "professional")

# 可爱 NPC
await tts.speak_with_scene("哥哥～人家等你好久了呢！一起去冒险吧！", "cute")
```

---

### 5️⃣ 教育内容

```python
# 儿童故事
await tts.speak_with_scene("从前有一只小兔子，它住在一个美丽的森林里。", "xiaoyou")

# 课程讲解
await tts.speak_with_scene("今天我们学习三角函数，首先来看正弦函数的定义。", "yunye")

# 英语发音
await tts.speak("Hello, welcome to English class!", "xiaoyan")
```

---

## 🔌 API 集成方式

### 启动 API 服务

```bash
cd /home/admin/projects/live-tts
python agent_tts_api.py
```

服务地址：`http://localhost:7086`

---

### API 调用示例

#### 1. 简单调用

```bash
curl -X POST http://localhost:7086/speak \
  -H "Content-Type: application/json" \
  -d '{"text":"你好，我是智能助手","voice":"xiaoxiao"}'
```

响应：
```json
{
  "success": true,
  "filename": "speech_20260409_120000.mp3",
  "url": "http://localhost:7086/audio/speech_20260409_120000.mp3",
  "text": "你好，我是智能助手",
  "voice": "xiaoxiao",
  "duration_estimate": "3.6 秒"
}
```

#### 2. 使用场景预设

```bash
curl -X POST http://localhost:7086/speak \
  -H "Content-Type: application/json" \
  -d '{"text":"欢迎宝宝来到直播间","scene":"cute"}'
```

#### 3. 流式返回（直接播放）

```bash
curl -X POST http://localhost:7086/speak/stream \
  -H "Content-Type: application/json" \
  -d '{"text":"你好","scene":"default"}' \
  --output response.mp3
```

---

### Python 集成

```python
import requests

# 调用 API
response = requests.post('http://localhost:7086/speak', json={
    "text": "你好，我是你的智能助手",
    "scene": "professional"
})

data = response.json()
audio_url = data['url']
print(f"音频 URL: {audio_url}")

# 下载音频
audio_response = requests.get(audio_url)
with open('output.mp3', 'wb') as f:
    f.write(audio_response.content)
```

---

### JavaScript/Node.js 集成

```javascript
// 调用 API
const response = await fetch('http://localhost:7086/speak', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        text: '你好，我是智能助手',
        scene: 'professional'
    })
});

const data = await response.json();
console.log('音频 URL:', data.url);

// 播放音频
const audio = new Audio(data.url);
audio.play();
```

---

### 前端集成

```html
<!DOCTYPE html>
<html>
<head>
    <title>TTS Agent 集成</title>
</head>
<body>
    <input type="text" id="text" placeholder="输入文本" value="你好">
    <select id="scene">
        <option value="default">通用</option>
        <option value="cute">可爱</option>
        <option value="gentle">温柔</option>
        <option value="professional">专业</option>
        <option value="promotion">促销</option>
    </select>
    <button onclick="speak()">朗读</button>
    
    <script>
    async function speak() {
        const text = document.getElementById('text').value;
        const scene = document.getElementById('scene').value;
        
        const response = await fetch('http://localhost:7086/speak', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text, scene })
        });
        
        const data = await response.json();
        
        // 播放音频
        const audio = new Audio(data.url);
        audio.play();
    }
    </script>
</body>
</html>
```

---

## 🎭 场景预设

| 场景 | 语音 | 语速 | 音量 | 适用场景 |
|------|------|------|------|---------|
| `default` | xiaoxiao | -5% | 0% | 通用对话 ⭐⭐⭐ |
| `gentle` | xiaoxuan | -10% | -5% | 温柔安慰 ⭐⭐ |
| `cute` | xiaomeng | -10% | +5% | 可爱互动 ⭐⭐⭐ |
| `professional` | yunye | 0% | 0% | 专业讲解 ⭐⭐⭐ |
| `promotion` | yunhao | +5% | +5% | 促销广告 ⭐⭐⭐ |
| `weak` | xiaoxiao | -20% | -10% | 柔弱 ASMR ⭐⭐ |

---

## 🎤 可用语音

### 女声 (14 个)

| 语音 | 风格 | 适用场景 |
|------|------|---------|
| xiaoxiao | 温暖亲切 | 通用 ⭐⭐⭐ |
| xiaoyi | 活泼开朗 | 娱乐 ⭐⭐ |
| xiaomeng | 可爱萌妹 | 撒娇 ⭐⭐⭐ |
| xiaoxuan | 温和亲切 | 温柔 ⭐⭐ |
| xiaoyou | 童声萝莉 | 儿童 ⭐⭐⭐ |
| yunhao | 广告促销 | 带货 ⭐⭐⭐ |
| yunye | 专业讲解 | 知识 ⭐⭐⭐ |

### 男声 (6 个)

| 语音 | 风格 | 适用场景 |
|------|------|---------|
| yunfeng | 严肃正式 | 新闻 |
| yunhao | 激情广告 | 促销 ⭐⭐⭐ |
| yunxi | 讲故事 | 儿童 ⭐⭐ |
| yunye | 专业讲解 | 知识 ⭐⭐⭐ |

---

## 📦 完整集成示例

### CoPaw Agent 集成

```python
# copaw_agent_tts.py
from agent_tts import AgentTTS

class CopawAgentWithTTS:
    def __init__(self):
        self.tts = AgentTTS()
    
    async def respond(self, message: str, style: str = "default"):
        """Agent 回复并生成语音"""
        # 生成文本回复（这里简化，实际调用 LLM）
        response_text = f"收到：{message}"
        
        # 生成语音
        audio_file = await self.tts.speak_with_scene(
            text=response_text,
            scene=style
        )
        
        return {
            "text": response_text,
            "audio": audio_file,
            "style": style
        }

# 使用
agent = CopawAgentWithTTS()
result = await agent.respond("今天天气怎么样？", "professional")
print(f"回复：{result['text']}")
print(f"语音：{result['audio']}")
```

---

### 直播弹幕机器人集成

```python
# live_tts_bot.py
from agent_tts import AgentTTS
import asyncio

class LiveTTSBot:
    def __init__(self):
        self.tts = AgentTTS()
    
    async def handle_danmu(self, user: str, message: str):
        """处理弹幕"""
        if "欢迎" in message:
            await self.tts.speak_with_scene(
                f"欢迎{user}宝宝来到直播间！",
                "cute"
            )
        elif "价格" in message:
            await self.tts.speak_with_scene(
                "宝宝问价格啦，我们直播间特价 99 元包邮！",
                "promotion"
            )
        elif "谢谢" in message:
            await self.tts.speak_with_scene(
                "不客气哦～有问题随时问我！",
                "gentle"
            )

# 使用
bot = LiveTTSBot()
await bot.handle_danmu("小明", "欢迎主播！")
```

---

## ⚠️ 限制说明

### 预设音频 (152 个文件)

**不能适配**：
- ❌ 任意对话内容
- ❌ 实时生成回复
- ❌ 个性化语音

**只能用于**：
- ✅ 固定场景（欢迎、感谢、求关注）
- ✅ 背景音乐
- ✅ 氛围音效

---

### TTS 引擎

**可以适配**：
- ✅ 任意文本
- ✅ 实时生成
- ✅ 多种风格
- ✅ Agent 对话

**限制**：
- ⚠️ 需要网络连接（Edge TTS 在线服务）
- ⚠️ 生成需要时间（约 1-3 秒/句）
- ⚠️ 有 API 速率限制

---

## 🚀 推荐方案

### 方案 1: 混合使用（推荐）

```
固定场景 → 预设音频（快速播放）
动态对话 → TTS 引擎（实时生成）
```

**优点**：
- ✅ 常用语音快速响应
- ✅ 动态内容灵活生成
- ✅ 节省 API 调用

---

### 方案 2: 纯 TTS

```
所有内容 → TTS 引擎实时生成
```

**优点**：
- ✅ 完全灵活
- ✅ 无需管理音频文件

**缺点**：
- ⚠️ 每次都需要生成时间
- ⚠️ 依赖网络

---

### 方案 3: 缓存 TTS

```
首次生成 → TTS → 缓存文件
后续使用 → 直接播放缓存
```

**优点**：
- ✅ 平衡灵活性和速度
- ✅ 减少重复生成

---

## 📖 快速开始

### 1. 测试 TTS 引擎

```bash
cd /home/admin/projects/live-tts
python agent_tts.py
```

### 2. 启动 API 服务

```bash
python agent_tts_api.py
```

### 3. 调用 API

```bash
curl -X POST http://localhost:7086/speak \
  -H "Content-Type: application/json" \
  -d '{"text":"你好","scene":"cute"}'
```

### 4. 集成到你的 Agent

参考上面的 Python/JavaScript 示例。

---

## ✅ 总结

| 问题 | 答案 |
|------|------|
| **预设音频能适配任意对话吗？** | ❌ 不能，只能播放固定内容 |
| **TTS 引擎能适配任意对话吗？** | ✅ 可以，支持任意文本转语音 |
| **如何集成到智能 Agent？** | 使用 `agent_tts.py` 或 API 服务 |
| **支持多少种语音？** | 20 个中文语音 |
| **支持多少种风格？** | 7 种场景预设 |
| **需要网络吗？** | ✅ 需要（Edge TTS 在线服务） |
| **生成速度快吗？** | ⚠️ 约 1-3 秒/句 |

---

**创建时间**: 2026-04-09  
**版本**: 1.0  
**API 端口**: 7086  
**语音数**: 20 个  
**场景数**: 7 个
