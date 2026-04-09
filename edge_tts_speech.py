#!/usr/bin/env python3
"""
在线口播语音合成系统（使用 Edge TTS）
无需本地语音引擎，使用微软 Azure 在线服务
音质更好，支持更多语音
"""

import asyncio
import edge_tts
import os
from datetime import datetime

# 支持的中文语音
CHINESE_VOICES = {
    "xiaoxiao": "zh-CN-XiaoxiaoNeural",      # 女声（温暖）
    "xiaoyi": "zh-CN-XiaoyiNeural",          # 女声（活泼）
    "yunjian": "zh-CN-YunjianNeural",        # 男声（运动）
    "xiaochen": "zh-CN-XiaochenNeural",      # 女声（新闻）
    "xiaohan": "zh-CN-XiaohanNeural",        # 女声（严肃）
    "xiaomeng": "zh-CN-XiaomengNeural",      # 女声（可爱）
    "xiaomo": "zh-CN-XiaomoNeural",          # 女声（温柔）
    "xiaoqiu": "zh-CN-XiaoqiuNeural",        # 女声（客服）
    "xiaorui": "zh-CN-XiaoruiNeural",        # 女声（电话）
    "xiaoshuang": "zh-CN-XiaoshuangNeural",  # 童声（儿童）
    "xiaoxuan": "zh-CN-XiaoxuanNeural",      # 女声（温和）
    "xiaoyan": "zh-CN-XiaoyanNeural",        # 女声（客服）
    "xiaoyou": "zh-CN-XiaoyouNeural",        # 童声（儿童）
    "xiaozhen": "zh-CN-XiaozhenNeural",      # 女声（客服）
    "yunfeng": "zh-CN-YunfengNeural",        # 男声（严肃）
    "yunhao": "zh-CN-YunhaoNeural",          # 男声（广告）
    "yunxia": "zh-CN-YunxiaNeural",          # 男声（激情）
    "yunxi": "zh-CN-YunxiNeural",            # 男声（故事）
    "yunye": "zh-CN-YunyeNeural",            # 男声（专业）
    "yunze": "zh-CN-YunzeNeural",            # 男声（纪录片）
}

async def generate_speech(text, voice="xiaoxiao", output_file="output.mp3", rate=0, volume=0):
    """
    生成语音
    
    Args:
        text: 要朗读的文本
        voice: 语音名称（见 CHINESE_VOICES）
        output_file: 输出文件名
        rate: 语速调整 (-50 到 +50，默认 0)
        volume: 音量调整 (-100 到 +100，默认 0)
    """
    voice_id = CHINESE_VOICES.get(voice, CHINESE_VOICES["xiaoxiao"])
    
    # 创建输出目录
    os.makedirs(os.path.dirname(output_file) if os.path.dirname(output_file) else '.', exist_ok=True)
    
    # 创建 communicate 对象
    communicate = edge_tts.Communicate(text, voice_id, rate=f"{rate:+d}%", volume=f"{volume:+d}%")
    
    # 保存到文件
    await communicate.save(output_file)
    
    print(f"✅ 生成成功：{output_file}")
    print(f"   语音：{voice} ({voice_id})")
    print(f"   语速：{rate:+d}%")
    print(f"   音量：{volume:+d}%")
    
    return output_file


async def main():
    import sys
    
    print("=" * 50)
    print("🎤 在线口播语音合成系统（Edge TTS）")
    print("=" * 50)
    
    # 显示可用语音
    print("\n🎭 可用语音:")
    for i, (name, voice_id) in enumerate(CHINESE_VOICES.items(), 1):
        gender = "女" if any(x in name for x in ["xiao", "xia"]) else "男"
        print(f"  {i:2d}. {name:12s} - {gender}声")
    
    print("\n" + "=" * 50)
    print("命令:")
    print("  [s] 生成语音（保存文件）")
    print("  [b] 批量生成")
    print("  [l] 列出语音")
    print("  [q] 退出")
    print("=" * 50)
    
    while True:
        cmd = input("\n> ").strip().lower()
        
        if cmd == 'q':
            print("👋 再见！")
            break
        
        elif cmd == 'l':
            print("\n🎭 可用语音列表:")
            for name, voice_id in CHINESE_VOICES.items():
                gender = "女" if any(x in name for x in ["xiao", "xia"]) else "男"
                print(f"  {name:12s} - {gender}声 - {voice_id}")
        
        elif cmd == 's':
            text = input("输入文本：").strip()
            if not text:
                continue
            
            voice = input("语音 (默认 xiaoxiao): ").strip() or "xiaoxiao"
            if voice not in CHINESE_VOICES:
                print(f"⚠️  未知语音，使用默认 xiaoxiao")
                voice = "xiaoxiao"
            
            try:
                rate = int(input("语速调整 (-50 到 +50，默认 0): ").strip() or "0")
                volume = int(input("音量调整 (-100 到 +100，默认 0): ").strip() or "0")
            except:
                rate, volume = 0, 0
            
            filename = input("文件名 (默认 output_时间戳.mp3): ").strip()
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"output_{timestamp}.mp3"
            if not filename.endswith('.mp3'):
                filename += '.mp3'
            
            await generate_speech(text, voice, filename, rate, volume)
        
        elif cmd == 'b':
            print("输入多行文本（空行结束）:")
            texts = []
            while True:
                line = input()
                if not line.strip():
                    break
                texts.append(line)
            
            if texts:
                voice = input("语音 (默认 xiaoxiao): ").strip() or "xiaoxiao"
                
                for i, text in enumerate(texts, 1):
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"speech_{i}_{timestamp}.mp3"
                    print(f"\n[{i}/{len(texts)}] {text[:30]}...")
                    await generate_speech(text, voice, filename)
        
        elif cmd == '':
            print("当前：Edge TTS 在线服务（微软 Azure）")
        
        else:
            print("未知命令")


if __name__ == '__main__':
    asyncio.run(main())
