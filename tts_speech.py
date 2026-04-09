#!/usr/bin/env python3
"""
口播语音合成系统
支持多种语音、语速、音量调节
适用于直播口播、视频配音、通知播报
"""

import pyttsx3
import os
from datetime import datetime

class TTSEngine:
    def __init__(self):
        self.engine = pyttsx3.init()
        
        # 获取可用语音
        self.voices = self.engine.getProperty('voices')
        
        # 默认设置
        self.rate = 150  # 语速（字/分钟）
        self.volume = 1.0  # 音量 (0.0-1.0)
        self.voice_id = 0  # 默认第一个语音
        
        # 应用默认设置
        self.apply_settings()
    
    def list_voices(self):
        """列出所有可用语音"""
        print("\n" + "=" * 50)
        print("🎭 可用语音列表")
        print("=" * 50)
        
        for i, voice in enumerate(self.voices):
            print(f"\n{i}. {voice.name}")
            print(f"   ID: {voice.id}")
            print(f"   语言：{voice.languages}")
            print(f"   性别：{'女' if 'female' in voice.name.lower() or 'Female' in voice.name else '男'}")
        
        print("\n" + "=" * 50)
        print(f"当前选择：{self.voice_id} - {self.voices[self.voice_id].name if self.voices else '无'}")
        print("=" * 50 + "\n")
    
    def set_voice(self, voice_id):
        """设置语音"""
        if 0 <= voice_id < len(self.voices):
            self.voice_id = voice_id
            self.engine.setProperty('voice', self.voices[voice_id].id)
            print(f"✅ 语音已切换：{self.voices[voice_id].name}")
        else:
            print(f"❌ 无效的语音 ID (0-{len(self.voices)-1})")
    
    def set_rate(self, rate):
        """设置语速"""
        self.rate = max(50, min(300, rate))
        self.engine.setProperty('rate', self.rate)
        print(f"✅ 语速：{self.rate} 字/分钟")
    
    def set_volume(self, volume):
        """设置音量"""
        self.volume = max(0.0, min(1.0, volume))
        self.engine.setProperty('volume', self.volume)
        print(f"✅ 音量：{int(self.volume * 100)}%")
    
    def apply_settings(self):
        """应用当前设置"""
        self.engine.setProperty('rate', self.rate)
        self.engine.setProperty('volume', self.volume)
        if self.voices:
            self.engine.setProperty('voice', self.voices[self.voice_id].id)
    
    def speak(self, text):
        """朗读文本"""
        print(f"🔊 播放：{text[:50]}...")
        self.engine.say(text)
        self.engine.runAndWait()
    
    def save_to_file(self, text, filename):
        """保存为音频文件"""
        print(f"💾 保存到：{filename}")
        
        # 创建输出目录
        os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else '.', exist_ok=True)
        
        self.engine.save_to_file(text, filename)
        self.engine.runAndWait()
        print(f"✅ 保存成功：{filename}")
    
    def speak_batch(self, texts, delay=0.5):
        """批量朗读"""
        import time
        
        for i, text in enumerate(texts, 1):
            print(f"[{i}/{len(texts)}] {text[:50]}...")
            self.engine.say(text)
            self.engine.runAndWait()
            time.sleep(delay)


def main():
    import sys
    
    tts = TTSEngine()
    
    print("=" * 50)
    print("🎤 口播语音合成系统")
    print("=" * 50)
    
    # 显示可用语音
    tts.list_voices()
    
    # 默认设置
    tts.set_rate(180)  # 稍快，适合口播
    tts.set_volume(0.8)
    
    # 示例文本
    demo_texts = [
        "欢迎观看直播！",
        "感谢大家的点赞和关注！",
        "更多精彩内容，敬请期待！",
    ]
    
    print("\n🎯 示例朗读:")
    for text in demo_texts:
        tts.speak(text)
    
    # 交互模式
    print("\n" + "=" * 50)
    print("命令:")
    print("  [s] 朗读文本")
    print("  [f] 保存到文件")
    print("  [v] 切换语音")
    print("  [r] 设置语速")
    print("  [l] 设置音量")
    print("  [b] 批量朗读")
    print("  [q] 退出")
    print("=" * 50)
    
    while True:
        cmd = input("\n> ").strip().lower()
        
        if cmd == 'q':
            print("👋 再见！")
            break
        
        elif cmd == 's':
            text = input("输入文本：").strip()
            if text:
                tts.speak(text)
        
        elif cmd == 'f':
            text = input("输入文本：").strip()
            if text:
                filename = input("文件名 (默认 output.mp3): ").strip() or "output.mp3"
                if not filename.endswith('.mp3'):
                    filename += '.mp3'
                tts.save_to_file(text, filename)
        
        elif cmd == 'v':
            tts.list_voices()
            try:
                voice_id = int(input("选择语音 ID: ").strip())
                tts.set_voice(voice_id)
            except:
                print("❌ 无效输入")
        
        elif cmd == 'r':
            try:
                rate = int(input("语速 (50-300): ").strip())
                tts.set_rate(rate)
            except:
                print("❌ 无效输入")
        
        elif cmd == 'l':
            try:
                volume = float(input("音量 (0-1): ").strip())
                tts.set_volume(volume)
            except:
                print("❌ 无效输入")
        
        elif cmd == 'b':
            print("输入多行文本（空行结束）:")
            texts = []
            while True:
                line = input()
                if not line.strip():
                    break
                texts.append(line)
            
            if texts:
                tts.speak_batch(texts)
        
        elif cmd == '':
            print(f"当前设置：语音={tts.voices[tts.voice_id].name if tts.voices else '无'}, "
                  f"语速={tts.rate}, 音量={int(tts.volume*100)}%")
        
        else:
            print("未知命令")


if __name__ == '__main__':
    main()
