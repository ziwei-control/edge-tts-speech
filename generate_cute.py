#!/usr/bin/env python3
"""
生成粘人版语音 - 撒娇、可爱、亲和力
"""

import asyncio
import os
from edge_tts_speech import generate_speech

# 粘人版文案（添加撒娇语气词、叠词、拖长音）
CUTE_TEXTS = {
    "欢迎": "欢迎宝宝～来看直播呀！好想你哦～快坐下嘛～💕",
    "感谢": "谢谢宝宝～的关注！爱你哟～啾咪～❤️",
    "求关注": "点点关注嘛～人家会想你的～好不好呀～✨",
    "撒娇": "不要走嘛～再陪人家一会儿～求求你啦～🥺",
    "促销": "宝宝～这个超划算的！买一个嘛～人家帮你省钱呀～💰",
    "互动": "宝宝最好了～给个小心心嘛～爱你～😘",
}

# 粘人语音配置（更慢语速、更高音调）
CUTE_VOICES = {
    "xiaomeng": {"rate": "-15%", "volume": "+5%", "desc": "可爱萌妹 ⭐⭐⭐"},
    "xiaoyou": {"rate": "-10%", "volume": "+0%", "desc": "童声萝莉 ⭐⭐⭐"},
    "xiaoxiao": {"rate": "-10%", "volume": "+0%", "desc": "温柔姐姐 ⭐⭐"},
    "xiaoyi": {"rate": "-5%", "volume": "+5%", "desc": "活泼妹妹 ⭐⭐"},
}

async def generate_cute_demos():
    output_dir = "/home/admin/projects/live-tts/output/cute"
    os.makedirs(output_dir, exist_ok=True)
    
    print("=" * 70)
    print("🎀 生成粘人版语音（撒娇可爱风）")
    print("=" * 70)
    
    total = len(CUTE_VOICES) * len(CUTE_TEXTS)
    current = 0
    success = 0
    
    for voice_name, params in CUTE_VOICES.items():
        print(f"\n🎀 {voice_name} - {params['desc']}")
        
        for text_name, text in CUTE_TEXTS.items():
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
    print(f"✅ 完成！成功生成 {success}/{total} 个粘人版音频")
    print(f"📁 输出目录：{output_dir}")
    print("=" * 70)

if __name__ == '__main__':
    asyncio.run(generate_cute_demos())
