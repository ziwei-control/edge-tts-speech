#!/usr/bin/env python3
"""
生成柔弱版语音 - 喘气、虚弱、轻轻柔柔
"""

import asyncio
import os
from edge_tts_speech import generate_speech

# 柔弱版文案（添加呼吸声、停顿、虚弱语气）
WEAK_TEXTS = {
    "欢迎": "呼～欢迎...宝宝...来看我...呼...好累哦...坐下...陪陪我...💕",
    "感谢": "呼～谢谢...宝宝...的关注...呼...好开心...爱你...啾咪...❤️",
    "求关注": "呼...点点...关注嘛...呼...人家...会想你...的...好不好...✨",
    "撒娇": "呼～不要...走嘛...呼...再陪...人家...一会...求求你...🥺",
    "虚弱": "呼...呼...今天...好累...呼...宝宝...别走...陪我...💕",
    "互动": "呼...宝宝...最好了...呼...给个...小心心...嘛...爱你...😘",
}

# 柔弱语音配置（更慢语速、更轻音量、添加停顿）
WEAK_VOICES = {
    "xiaoxiao": {"rate": "-20%", "volume": "-10%", "desc": "温柔柔弱 ⭐⭐⭐"},
    "xiaomo": {"rate": "-25%", "volume": "-15%", "desc": "虚弱病娇 ⭐⭐⭐"},
    "xiaoxuan": {"rate": "-20%", "volume": "-10%", "desc": "轻柔无力 ⭐⭐"},
    "xiaoyi": {"rate": "-15%", "volume": "-5%", "desc": "虚弱活泼 ⭐⭐"},
}

async def generate_weak_demos():
    output_dir = "/home/admin/projects/live-tts/output/weak"
    os.makedirs(output_dir, exist_ok=True)
    
    print("=" * 70)
    print("🌸 生成柔弱版语音（喘气虚弱风）")
    print("=" * 70)
    
    total = len(WEAK_VOICES) * len(WEAK_TEXTS)
    current = 0
    success = 0
    
    for voice_name, params in WEAK_VOICES.items():
        print(f"\n🌸 {voice_name} - {params['desc']}")
        
        for text_name, text in WEAK_TEXTS.items():
            current += 1
            filename = f"{voice_name}_{text_name}.mp3"
            filepath = os.path.join(output_dir, filename)
            
            print(f"  [{current}/{total}] {text_name}...")
            
            try:
                rate = int(params['rate'].replace('%', ''))
                volume = int(params['volume'].replace('%', ''))
                
                await generate_speech(text, voice_name, filepath, rate, volume)
                success += 1
                print(f"    ✅ 成功")
            except Exception as e:
                print(f"    ❌ 失败：{e}")
    
    print("\n" + "=" * 70)
    print(f"✅ 完成！成功生成 {success}/{total} 个柔弱版音频")
    print(f"📁 输出目录：{output_dir}")
    print("=" * 70)

if __name__ == '__main__':
    asyncio.run(generate_weak_demos())
