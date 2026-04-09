#!/usr/bin/env python3
"""
批量生成所有语音的试听文件
"""

import asyncio
import os
from edge_tts_speech import generate_speech, CHINESE_VOICES

# 试听文本
TEST_TEXTS = {
    "通用": "欢迎观看直播！感谢大家的关注！",
    "活泼": "点点关注不迷路，主播带你上高速！",
    "促销": "限时优惠，只剩最后 10 单！错过今天就要等下次了！",
    "温柔": "喜欢主播的记得点个关注哦～",
}

async def generate_all():
    output_dir = "/home/admin/projects/live-tts/output/demo"
    os.makedirs(output_dir, exist_ok=True)
    
    print("=" * 60)
    print("🎤 批量生成所有语音试听文件")
    print("=" * 60)
    
    total = len(CHINESE_VOICES) * len(TEST_TEXTS)
    current = 0
    
    for voice_name, voice_id in CHINESE_VOICES.items():
        gender = "女" if any(x in voice_name for x in ["xiao", "xia"]) else "男"
        print(f"\n🎤 {voice_name} ({gender}声) - {voice_id}")
        
        for text_name, text in TEST_TEXTS.items():
            current += 1
            filename = f"{voice_name}_{text_name}.mp3"
            filepath = os.path.join(output_dir, filename)
            
            print(f"  [{current}/{total}] 生成：{text_name}...")
            
            try:
                await generate_speech(text, voice_name, filepath, rate=10, volume=0)
            except Exception as e:
                print(f"  ❌ 失败：{e}")
    
    print("\n" + "=" * 60)
    print(f"✅ 全部完成！共生成 {total} 个文件")
    print(f"📁 输出目录：{output_dir}")
    print("=" * 60)

if __name__ == '__main__':
    asyncio.run(generate_all())
