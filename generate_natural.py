#!/usr/bin/env python3
"""
生成更自然的语音试听
优化语速、音调、情感表达
"""

import asyncio
import os
from edge_tts_speech import generate_speech, CHINESE_VOICES

# 更自然的试听文本（添加停顿、语气词）
TEST_TEXTS = {
    "欢迎": "欢迎～观看直播！感谢～大家的关注！❤️",
    "互动": "点点关注～不迷路，主播带你～上高速！✨",
    "促销": "限时优惠～只剩最后 10 单！错过～今天就要等下次了！🔥",
    "温柔": "喜欢主播的～记得点个关注哦～💕",
}

# 推荐的自然语音
RECOMMENDED_VOICES = {
    "xiaoxiao": {"rate": "-5%", "volume": "+0%", "desc": "温暖自然 ⭐⭐⭐"},
    "xiaomo": {"rate": "-10%", "volume": "-5%", "desc": "温柔情感 ⭐⭐⭐"},
    "xiaoyi": {"rate": "0%", "volume": "+0%", "desc": "活泼亲切 ⭐⭐"},
    "xiaoxuan": {"rate": "-5%", "volume": "+0%", "desc": "温和亲切 ⭐⭐"},
    "yunye": {"rate": "-10%", "volume": "+0%", "desc": "专业讲解 ⭐⭐"},
    "yunhao": {"rate": "0%", "volume": "+5%", "desc": "广告促销 ⭐⭐"},
}

async def generate_natural_demos():
    output_dir = "/home/admin/projects/live-tts/output/natural"
    os.makedirs(output_dir, exist_ok=True)
    
    print("=" * 70)
    print("🎤 生成更自然的语音试听（优化版）")
    print("=" * 70)
    
    total = len(RECOMMENDED_VOICES) * len(TEST_TEXTS)
    current = 0
    
    for voice_name, params in RECOMMENDED_VOICES.items():
        print(f"\n🎤 {voice_name} - {params['desc']}")
        
        for text_name, text in TEST_TEXTS.items():
            current += 1
            filename = f"{voice_name}_{text_name}.mp3"
            filepath = os.path.join(output_dir, filename)
            
            print(f"  [{current}/{total}] {text_name}...")
            
            try:
                # 解析参数
                rate = int(params['rate'].replace('%', ''))
                volume = int(params['volume'].replace('%', ''))
                
                await generate_speech(text, voice_name, filepath, rate, volume)
            except Exception as e:
                print(f"  ❌ 失败：{e}")
    
    print("\n" + "=" * 70)
    print(f"✅ 完成！共生成 {total} 个优化版音频文件")
    print(f"📁 输出目录：{output_dir}")
    print("=" * 70)

if __name__ == '__main__':
    asyncio.run(generate_natural_demos())
