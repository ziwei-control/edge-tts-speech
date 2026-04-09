#!/usr/bin/env python3
"""
TTS 试听 API 服务
提供 HTTP 接口生成语音
"""

from flask import Flask, request, send_file, jsonify
import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from edge_tts_speech import generate_speech

app = Flask(__name__)

# 临时文件目录
TEMP_DIR = '/tmp/tts_demo'
os.makedirs(TEMP_DIR, exist_ok=True)

@app.route('/')
def index():
    """返回试听页面"""
    return send_file('voice_demo.html')

@app.route('/api/tts', methods=['POST'])
def tts():
    """生成语音 API"""
    try:
        data = request.json
        text = data.get('text', '欢迎观看直播！')
        voice = data.get('voice', 'xiaoxiao')
        rate = data.get('rate', 0)
        volume = data.get('volume', 0)
        
        # 生成文件名
        import time
        filename = f"tts_{voice}_{int(time.time())}.mp3"
        filepath = os.path.join(TEMP_DIR, filename)
        
        # 生成语音
        asyncio.run(generate_speech(text, voice, filepath, rate, volume))
        
        # 返回音频文件
        return send_file(filepath, mimetype='audio/mpeg', as_attachment=True, download_name=filename)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/voices', methods=['GET'])
def list_voices():
    """列出所有可用语音"""
    from edge_tts_speech import CHINESE_VOICES
    
    voices = []
    for name, voice_id in CHINESE_VOICES.items():
        gender = 'female' if any(x in name for x in ['xiao', 'xia']) else 'male'
        voices.append({
            'id': name,
            'voiceId': voice_id,
            'gender': gender
        })
    
    return jsonify({'voices': voices})

if __name__ == '__main__':
    print("=" * 50)
    print("🎤 TTS 试听服务启动")
    print("=" * 50)
    print(f"📱 访问地址：http://localhost:7080")
    print(f"🌐 公网访问：http://8.213.149.224:7080")
    print("=" * 50)
    app.run(host='0.0.0.0', port=7080, debug=False)
