#!/usr/bin/env python3
"""Flask Web 服务器，支持 TTS 和 STT"""

from flask import Flask, send_from_directory, jsonify, request
import requests
import os

app = Flask(__name__)

# TTS API 地址
TTS_API_URL = "http://localhost:7086"
# STT API 地址
STT_API_URL = "http://localhost:5050"

@app.route('/')
def index():
    return send_from_directory('.', 'voice_chat.html')

@app.route('/<path:filename>')
def static_file(filename):
    return send_from_directory('.', filename)

@app.route('/api/health')
def health():
    """代理健康检查"""
    try:
        resp = requests.get(f"{TTS_API_URL}/health", timeout=5)
        return jsonify(resp.json())
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/speak', methods=['POST'])
def speak():
    """代理 TTS 生成"""
    try:
        data = request.get_json()
        resp = requests.post(f"{TTS_API_URL}/speak", json=data, timeout=30)
        return jsonify(resp.json())
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/transcribe', methods=['POST'])
def transcribe():
    """代理语音识别（STT）"""
    try:
        # 转发音频文件到 STT 服务
        files = request.files
        resp = requests.post(f"{STT_API_URL}/transcribe", files=files, timeout=60)
        return jsonify(resp.json())
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/audio/<filename>')
def audio(filename):
    """代理音频文件"""
    try:
        filepath = f"output/api/{filename}"
        return send_from_directory("output/api", filename)
    except Exception as e:
        return jsonify({"error": str(e)}), 404

if __name__ == '__main__':
    print("=" * 60)
    print("🌐 语音交互 Web 服务器（Flask + CORS）")
    print("=" * 60)
    print("📡 地址：http://localhost:7091")
    print("📄 页面：http://localhost:7091/voice_chat.html")
    print("🔌 TTS API:  http://localhost:7091/api/speak")
    print("🎤 STT API:  http://localhost:7091/api/transcribe")
    print("=" * 60)
    app.run(host='0.0.0.0', port=7091, debug=False)
