#!/usr/bin/env python3
"""
CoPaw Agent TTS 集成模块
让 CoPaw Agent 支持语音回复功能
"""

import asyncio
import aiohttp
import os
from typing import Optional, Dict, Any
from datetime import datetime

class CopawAgentTTS:
    """CoPaw Agent TTS 集成类"""
    
    def __init__(self, api_url: str = "http://localhost:7086"):
        self.api_url = api_url
        self.output_dir = "output/copaw"
        os.makedirs(self.output_dir, exist_ok=True)
    
    async def speak(self, text: str, scene: str = "default") -> Dict[str, Any]:
        """
        生成语音回复
        
        Args:
            text: 要朗读的文本
            scene: 场景预设 (default/gentle/cute/professional/promotion/weak)
        
        Returns:
            {
                "success": bool,
                "text": str,
                "audio_url": str,
                "audio_file": str,
                "scene": str,
                "duration": str
            }
        """
        async with aiohttp.ClientSession() as session:
            # 调用 TTS API
            async with session.post(
                f"{self.api_url}/speak",
                json={"text": text, "scene": scene},
                headers={"Content-Type": "application/json"}
            ) as response:
                result = await response.json()
                
                if result.get("success"):
                    # 下载音频文件
                    audio_filename = result["filename"]
                    audio_path = os.path.join(self.output_dir, audio_filename)
                    
                    async with session.get(result["url"]) as audio_response:
                        with open(audio_path, "wb") as f:
                            f.write(await audio_response.read())
                    
                    return {
                        "success": True,
                        "text": text,
                        "audio_url": result["url"],
                        "audio_file": audio_path,
                        "scene": scene,
                        "duration": result.get("duration_estimate", "未知")
                    }
                else:
                    return {
                        "success": False,
                        "error": result.get("error", "未知错误")
                    }
    
    async def respond(self, user_message: str, agent_response: str, 
                     user_scene: str = "default", agent_scene: str = "default") -> Dict[str, Any]:
        """
        生成完整对话（用户 + Agent）
        
        Args:
            user_message: 用户消息
            agent_response: Agent 回复
            user_scene: 用户语音场景
            agent_scene: Agent 语音场景
        
        Returns:
            对话音频信息
        """
        tasks = []
        
        # 生成用户语音
        if user_message:
            tasks.append(self.speak(user_message, user_scene))
        
        # 生成 Agent 语音
        if agent_response:
            tasks.append(self.speak(agent_response, agent_scene))
        
        results = await asyncio.gather(*tasks)
        
        return {
            "success": True,
            "user_audio": results[0] if len(results) > 0 else None,
            "agent_audio": results[1] if len(results) > 1 else None,
            "timestamp": datetime.now().isoformat()
        }
    
    def get_scene_for_intent(self, intent: str) -> str:
        """
        根据意图自动选择场景
        
        Args:
            intent: 意图类型
        
        Returns:
            场景名称
        """
        intent_map = {
            "greeting": "cute",           # 问候
            "farewell": "gentle",         # 告别
            "thank": "gentle",            # 感谢
            "help": "professional",       # 帮助
            "joke": "cute",               # 笑话
            "weather": "professional",    # 天气
            "news": "professional",       # 新闻
            "chat": "default",            # 聊天
            "emotion_positive": "cute",   # 积极情绪
            "emotion_negative": "gentle", # 消极情绪
            "promotion": "promotion",     # 促销
            "comfort": "gentle",          # 安慰
            "encourage": "cute",          # 鼓励
        }
        
        return intent_map.get(intent, "default")
    
    async def auto_respond(self, user_message: str, agent_response: str, 
                          intent: str = "chat") -> Dict[str, Any]:
        """
        自动选择场景并生成回复
        
        Args:
            user_message: 用户消息
            agent_response: Agent 回复
            intent: 意图类型
        
        Returns:
            对话音频信息
        """
        agent_scene = self.get_scene_for_intent(intent)
        
        return await self.respond(
            user_message=user_message,
            agent_response=agent_response,
            user_scene="default",
            agent_scene=agent_scene
        )


# CoPaw Agent 插件示例
class CopawPlugin:
    """CoPaw Agent TTS 插件"""
    
    def __init__(self):
        self.tts = CopawAgentTTS()
    
    async def on_message(self, message: str, context: Dict = None) -> Dict:
        """
        消息处理钩子
        
        Args:
            message: 用户消息
            context: 上下文信息
        
        Returns:
            包含语音的回复
        """
        # 这里简化处理，实际应调用 LLM 生成回复
        agent_response = f"收到：{message}"
        
        # 生成语音回复
        result = await self.tts.auto_respond(
            user_message=message,
            agent_response=agent_response,
            intent="chat"
        )
        
        return {
            "text": agent_response,
            "audio": result["agent_audio"]["audio_file"] if result["agent_audio"] else None,
            "scene": result["agent_audio"]["scene"] if result["agent_audio"] else "default"
        }


# 测试函数
async def test_copaw_tts():
    """测试 CoPaw TTS 集成"""
    print("=" * 60)
    print("🤖 CoPaw Agent TTS 集成测试")
    print("=" * 60)
    
    tts = CopawAgentTTS()
    
    # 测试 1: 简单回复
    print("\n1️⃣ 测试简单回复...")
    result = await tts.speak("你好，我是 CoPaw 智能助手！", "professional")
    print(f"✅ 成功：{result['success']}")
    print(f"📁 文件：{result['audio_file']}")
    print(f"🎭 场景：{result['scene']}")
    
    # 测试 2: 对话回复
    print("\n2️⃣ 测试对话回复...")
    result = await tts.respond(
        user_message="今天天气怎么样？",
        agent_response="今天北京晴，气温 15 到 25 度，适合外出哦！",
        user_scene="default",
        agent_scene="professional"
    )
    print(f"✅ 成功：{result['success']}")
    
    # 测试 3: 自动场景选择
    print("\n3️⃣ 测试自动场景选择...")
    test_cases = [
        ("你好！", "很高兴见到你！", "greeting"),
        ("我很难过", "别难过，一切都会好起来的", "comfort"),
        ("有什么优惠？", "现在下单立减 50 元！", "promotion"),
    ]
    
    for user_msg, agent_msg, intent in test_cases:
        result = await tts.auto_respond(user_msg, agent_msg, intent)
        scene = result["agent_audio"]["scene"] if result["agent_audio"] else "unknown"
        print(f"✅ 意图 {intent} → 场景 {scene}")
    
    print("\n" + "=" * 60)
    print("✅ 测试完成！")
    print("=" * 60)
    print(f"\n📂 音频文件保存在：{tts.output_dir}/")
    print(f"\n💡 提示：可以播放这些文件测试效果")


if __name__ == '__main__':
    asyncio.run(test_copaw_tts())
