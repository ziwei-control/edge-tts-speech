#!/usr/bin/env python3
"""
智能 Agent TTS API 服务
提供 REST API 接口，支持任何智能 Agent 集成
"""

from flask import Flask, request, jsonify, send_file
import asyncio
import edge_tts
import os
from datetime import datetime
from functools import wraps

app = Flask(__name__)

# 输出目录
OUTPUT_DIR = "output/api"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 支持的语音
VOICES = {
    "xiaoxiao": "zh-CN-XiaoxiaoNeural",
    "xiaoyi": "zh-CN-XiaoyiNeural",
    "xiaomeng": "zh-CN-XiaomengNeural",
    "xiaoxuan": "zh-CN-XiaoxuanNeural",
    "xiaoyou": "zh-CN-XiaoyouNeural",
    "yunhao": "zh-CN-YunhaoNeural",
    "yunye": "zh-CN-YunyeNeural",
    "yunxi": "zh-CN-YunxiNeural",
}

# 场景预设
SCENES = {
    "default": {"voice": "xiaoxiao", "rate": -5, "volume": 0},
    "gentle": {"voice": "xiaoxuan", "rate": -10, "volume": -5},
    "cute": {"voice": "xiaomeng", "rate": -10, "volume": 5},
    "professional": {"voice": "yunye", "rate": 0, "volume": 0},
    "promotion": {"voice": "yunhao", "rate": 5, "volume": 5},
    "weak": {"voice": "xiaoxiao", "rate": -20, "volume": -10},
}


def async_route(f):
    """异步路由装饰器"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))
    return wrapper


@app.route('/')
def index():
    """API 首页"""
    return jsonify({
        "name": "Agent TTS API",
        "version": "1.0",
        "description": "智能 Agent TTS 服务 - 支持任意文本转语音",
        "endpoints": {
            "GET /": "API 信息",
            "GET /voices": "可用语音列表",
            "GET /scenes": "场景预设",
            "POST /speak": "生成语音",
            "POST /speak/stream": "流式生成（返回音频数据）",
            "GET /audio/<filename>": "获取音频文件"
        },
        "example": {
            "curl": "curl -X POST http://localhost:7086/speak -d '{\"text\":\"你好\",\"voice\":\"xiaoxiao\"}'"
        }
    })


@app.route('/voices')
def list_voices():
    """获取可用语音列表"""
    return jsonify({
        "voices": [
            {"id": k, "name": k, "voice_id": v, "gender": "female" if "xiao" in k else "male"}
            for k, v in VOICES.items()
        ]
    })


@app.route('/scenes')
def list_scenes():
    """获取场景预设"""
    return jsonify({
        "scenes": {
            k: {"voice": v["voice"], "rate": v["rate"], "volume": v["volume"]}
            for k, v in SCENES.items()
        }
    })


@app.route('/speak', methods=['POST'])
@async_route
async def speak():
    """
    生成语音
    
    JSON Body:
    {
        "text": "要朗读的文本",
        "voice": "xiaoxiao",  // 可选，默认 xiaoxiao
        "scene": "default",   // 可选，场景预设
        "rate": -5,           // 可选，语速调整
        "volume": 0,          // 可选，音量调整
        "save": true          // 可选，是否保存文件
    }
    """
    data = request.get_json()
    
    if not data or 'text' not in data:
        return jsonify({"error": "缺少 text 参数"}), 400
    
    text = data['text']
    
    # 获取场景预设或自定义参数
    scene = data.get('scene', None)
    if scene and scene in SCENES:
        voice = SCENES[scene]['voice']
        rate = SCENES[scene]['rate']
        volume = SCENES[scene]['volume']
    else:
        voice = data.get('voice', 'xiaoxiao')
        rate = data.get('rate', -5)
        volume = data.get('volume', 0)
    
    voice_id = VOICES.get(voice, VOICES['xiaoxiao'])
    
    # 生成文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"speech_{timestamp}.mp3"
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    # 生成语音
    communicate = edge_tts.Communicate(text, voice_id, 
                                       rate=f"{rate:+d}%", 
                                       volume=f"{volume:+d}%")
    await communicate.save(filepath)
    
    return jsonify({
        "success": True,
        "filename": filename,
        "filepath": filepath,
        "url": f"http://localhost:7086/audio/{filename}",
        "text": text,
        "voice": voice,
        "scene": scene,
        "duration_estimate": f"{len(text) * 0.3:.1f}秒"
    })


@app.route('/speak/stream', methods=['POST'])
@async_route
async def speak_stream():
    """
    流式生成语音（直接返回音频数据）
    
    JSON Body:
    {
        "text": "要朗读的文本",
        "voice": "xiaoxiao",
        "scene": "default"
    }
    
    Returns: audio/mpeg
    """
    data = request.get_json()
    
    if not data or 'text' not in data:
        return jsonify({"error": "缺少 text 参数"}), 400
    
    text = data['text']
    scene = data.get('scene', 'default')
    
    if scene in SCENES:
        voice = SCENES[scene]['voice']
        rate = SCENES[scene]['rate']
        volume = SCENES[scene]['volume']
    else:
        voice = data.get('voice', 'xiaoxiao')
        rate = data.get('rate', -5)
        volume = data.get('volume', 0)
    
    voice_id = VOICES.get(voice, VOICES['xiaoxiao'])
    
    # 生成临时文件
    temp_file = os.path.join(OUTPUT_DIR, "temp_stream.mp3")
    communicate = edge_tts.Communicate(text, voice_id, 
                                       rate=f"{rate:+d}%", 
                                       volume=f"{volume:+d}%")
    await communicate.save(temp_file)
    
    # 返回音频文件
    return send_file(temp_file, mimetype='audio/mpeg')


@app.route('/audio/<filename>')
def get_audio(filename):
    """获取音频文件"""
    filepath = os.path.join(OUTPUT_DIR, filename)
    if os.path.exists(filepath):
        return send_file(filepath, mimetype='audio/mpeg')
    return jsonify({"error": "文件不存在"}), 404


@app.route('/health')
def health():
    """健康检查"""
    return jsonify({
        "status": "ok",
        "service": "Agent TTS API",
        "port": 7086,
        "voices": len(VOICES),
        "scenes": len(SCENES)
    })


if __name__ == '__main__':
    print("=" * 50)
    print("🤖 智能 Agent TTS API 服务")
    print("=" * 50)
    print(f"\n📡 服务地址：http://localhost:7086")
    print(f"📂 输出目录：{OUTPUT_DIR}")
    print(f"🎤 可用语音：{len(VOICES)} 个")
    print(f"🎭 场景预设：{len(SCENES)} 个")
    print("\n📖 API 文档：http://localhost:7086/")
    print("\n🚀 启动服务...\n")
    
    app.run(host='0.0.0.0', port=7086, debug=False)
