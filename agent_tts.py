#!/usr/bin/env python3
"""
智能 Agent TTS 集成服务
支持实时文字转语音，适配任何语音对话场景
"""

import asyncio
import edge_tts
import os
from datetime import datetime
from typing import Optional

# 支持的中文语音
CHINESE_VOICES = {
    "xiaoxiao": "zh-CN-XiaoxiaoNeural",      # 女声（温暖通用）⭐⭐⭐
    "xiaoyi": "zh-CN-XiaoyiNeural",          # 女声（活泼亲切）⭐⭐
    "yunjian": "zh-CN-YunjianNeural",        # 男声（运动激情）
    "xiaochen": "zh-CN-XiaochenNeural",      # 女声（新闻播报）
    "xiaohan": "zh-CN-XiaohanNeural",        # 女声（严肃正式）
    "xiaomeng": "zh-CN-XiaomengNeural",      # 女声（可爱萌妹）⭐⭐⭐
    "xiaomo": "zh-CN-XiaomoNeural",          # 女声（温柔）⭐⭐
    "xiaoqiu": "zh-CN-XiaoqiuNeural",        # 女声（客服）⭐⭐
    "xiaorui": "zh-CN-XiaoruiNeural",        # 女声（电话客服）
    "xiaoshuang": "zh-CN-XiaoshuangNeural",  # 童声（儿童）
    "xiaoxuan": "zh-CN-XiaoxuanNeural",      # 女声（温和亲切）⭐⭐
    "xiaoyan": "zh-CN-XiaoyanNeural",        # 女声（客服）
    "xiaoyou": "zh-CN-XiaoyouNeural",        # 童声（萝莉）⭐⭐⭐
    "xiaozhen": "zh-CN-XiaozhenNeural",      # 女声（客服）
    "yunfeng": "zh-CN-YunfengNeural",        # 男声（严肃正式）
    "yunhao": "zh-CN-YunhaoNeural",          # 男声（广告促销）⭐⭐⭐
    "yunxia": "zh-CN-YunxiaNeural",          # 男声（激情活力）
    "yunxi": "zh-CN-YunxiNeural",            # 男声（讲故事）⭐⭐
    "yunye": "zh-CN-YunyeNeural",            # 男声（专业讲解）⭐⭐⭐
    "yunze": "zh-CN-YunzeNeural",            # 男声（纪录片）
}

# 场景预设配置
SCENE_PRESETS = {
    "default": {"rate": -5, "volume": 0, "voice": "xiaoxiao"},      # 通用
    "gentle": {"rate": -10, "volume": -5, "voice": "xiaoxuan"},     # 温柔
    "cute": {"rate": -10, "volume": 5, "voice": "xiaomeng"},        # 可爱
    "professional": {"rate": 0, "volume": 0, "voice": "yunye"},     # 专业
    "promotion": {"rate": 5, "volume": 5, "voice": "yunhao"},       # 促销
    "weak": {"rate": -20, "volume": -10, "voice": "xiaoxiao"},      # 柔弱
    "child": {"rate": 0, "volume": 0, "voice": "xiaoyou"},          # 童声
}


class AgentTTS:
    """智能 Agent TTS 服务类"""
    
    def __init__(self, output_dir: str = "output/agent"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    async def speak(self, text: str, voice: str = "xiaoxiao", 
                   rate: int = 0, volume: int = 0,
                   save: bool = False, filename: Optional[str] = None) -> str:
        """
        生成语音（核心方法）
        
        Args:
            text: 要朗读的文本
            voice: 语音名称
            rate: 语速调整 (-50 到 +50)
            volume: 音量调整 (-100 到 +100)
            save: 是否保存文件
            filename: 保存文件名（可选）
        
        Returns:
            输出文件路径
        """
        voice_id = CHINESE_VOICES.get(voice, CHINESE_VOICES["xiaoxiao"])
        
        if save:
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"speech_{timestamp}.mp3"
            output_file = os.path.join(self.output_dir, filename)
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
        else:
            output_file = os.path.join(self.output_dir, "temp.mp3")
        
        # 创建 communicate 对象
        communicate = edge_tts.Communicate(text, voice_id, 
                                           rate=f"{rate:+d}%", 
                                           volume=f"{volume:+d}%")
        
        # 保存到文件
        await communicate.save(output_file)
        
        return output_file
    
    async def speak_with_scene(self, text: str, scene: str = "default",
                               filename: Optional[str] = None) -> str:
        """
        使用场景预设生成语音
        
        Args:
            text: 要朗读的文本
            scene: 场景名称 (default/gentle/cute/professional/promotion/weak/child)
            filename: 保存文件名
        
        Returns:
            输出文件路径
        """
        preset = SCENE_PRESETS.get(scene, SCENE_PRESETS["default"])
        return await self.speak(
            text=text,
            voice=preset["voice"],
            rate=preset["rate"],
            volume=preset["volume"],
            save=True,
            filename=filename
        )
    
    async def respond(self, user_message: str, agent_response: str,
                     user_voice: str = "xiaoxiao", agent_voice: str = "xiaoxiao") -> tuple:
        """
        生成对话响应（用户 + Agent）
        
        Args:
            user_message: 用户消息（可选，用于生成用户语音）
            agent_response: Agent 回复
            user_voice: 用户语音
            agent_voice: Agent 语音
        
        Returns:
            (用户语音文件，Agent 语音文件)
        """
        user_file = None
        agent_file = None
        
        if user_message:
            user_file = await self.speak(user_message, user_voice, save=True,
                                        filename=f"user_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3")
        
        if agent_response:
            agent_file = await self.speak(agent_response, agent_voice, save=True,
                                         filename=f"agent_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3")
        
        return user_file, agent_file


# 快速测试
async def test_agent_tts():
    """测试 Agent TTS 功能"""
    tts = AgentTTS()
    
    print("=" * 50)
    print("🤖 智能 Agent TTS 测试")
    print("=" * 50)
    
    # 测试 1: 通用对话
    print("\n1️⃣ 通用对话测试...")
    await tts.speak_with_scene("你好，我是你的智能助手！", "default", "test1.mp3")
    
    # 测试 2: 温柔风格
    print("2️⃣ 温柔风格测试...")
    await tts.speak_with_scene("有什么可以帮你的吗？～", "gentle", "test2.mp3")
    
    # 测试 3: 可爱风格
    print("3️⃣ 可爱风格测试...")
    await tts.speak_with_scene("主人～人家在这里哦！💕", "cute", "test3.mp3")
    
    # 测试 4: 专业讲解
    print("4️⃣ 专业讲解测试...")
    await tts.speak_with_scene("根据数据分析，当前市场趋势如下。", "professional", "test4.mp3")
    
    # 测试 5: 促销话术
    print("5️⃣ 促销话术测试...")
    await tts.speak_with_scene("限时优惠！现在下单立减 50 元！", "promotion", "test5.mp3")
    
    # 测试 6: 柔弱风格
    print("6️⃣ 柔弱风格测试...")
    await tts.speak_with_scene("呼～人家有点累了呢...", "weak", "test6.mp3")
    
    print("\n✅ 测试完成！音频文件保存在 output/agent/ 目录")


if __name__ == '__main__':
    asyncio.run(test_agent_tts())
