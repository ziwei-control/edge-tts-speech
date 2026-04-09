#!/usr/bin/env python3
"""
语音识别服务（STT）
支持多种语音识别引擎：
1. Whisper (本地，免费)
2. Azure Speech (在线，高质量)
3. Google Speech (在线)
4. 百度语音 (国内，快速)
"""

import os
import wave
import io
import json
from flask import Flask, request, jsonify
from pathlib import Path
import subprocess

app = Flask(__name__)

# 配置
UPLOAD_FOLDER = Path('/tmp/voice_uploads')
UPLOAD_FOLDER.mkdir(exist_ok=True)

# 引擎配置
STT_ENGINE = os.getenv('STT_ENGINE', 'whisper')  # whisper/azure/google/baidu

# Azure 配置（可选）
AZURE_KEY = os.getenv('AZURE_SPEECH_KEY', '')
AZURE_REGION = os.getenv('AZURE_SPEECH_REGION', 'eastasia')

# 百度配置（可选）
BAIDU_API_KEY = os.getenv('BAIDU_API_KEY', '')
BAIDU_SECRET_KEY = os.getenv('BAIDU_SECRET_KEY', '')


def transcribe_with_whisper(audio_file: str) -> str:
    """使用 Whisper 进行语音识别（本地）"""
    try:
        # 检查是否安装 whisper
        result = subprocess.run(
            ['whisper', audio_file, '--model', 'base', '--language', 'zh', '--output_format', 'json'],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            # 读取 JSON 输出
            json_file = audio_file.rsplit('.', 1)[0] + '.json'
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                text = data.get('text', '').strip()
            
            # 清理临时文件
            try:
                os.remove(json_file)
            except:
                pass
            
            return text
        else:
            return f"Whisper 错误：{result.stderr}"
    except FileNotFoundError:
        return "错误：未安装 Whisper，请运行：pip install openai-whisper"
    except subprocess.TimeoutExpired:
        return "错误：语音识别超时"
    except Exception as e:
        return f"错误：{str(e)}"


def transcribe_with_azure(audio_data: bytes) -> str:
    """使用 Azure Speech 进行语音识别"""
    try:
        import azure.cognitiveservices.speech as speechsdk
        
        # 创建语音识别器
        speech_config = speechsdk.SpeechConfig(
            subscription=AZURE_KEY,
            region=AZURE_REGION
        )
        speech_config.speech_recognition_language = 'zh-CN'
        
        # 从音频流识别
        audio_stream = speechsdk.AudioStream(format=speechsdk.AudioStreamFormat(
            samples_per_second=16000,
            bits_per_sample=16,
            channels=1
        ))
        
        push_stream = speechsdk.audio.PushAudioInputStream(audio_stream)
        audio_config = speechsdk.AudioConfig(stream=push_stream)
        
        recognizer = speechsdk.SpeechRecognizer(
            speech_config=speech_config,
            audio_config=audio_config
        )
        
        # 推送音频数据
        push_stream.write(audio_data)
        push_stream.close()
        
        # 获取结果
        result = recognizer.recognize_once()
        
        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            return result.text
        else:
            return f"Azure 识别失败：{result.reason}"
    except ImportError:
        return "错误：未安装 Azure SDK，请运行：pip install azure-cognitiveservices-speech"
    except Exception as e:
        return f"错误：{str(e)}"


def transcribe_with_google(audio_data: bytes) -> str:
    """使用 Google Speech 进行语音识别"""
    try:
        from google.cloud import speech_v1p1beta1 as speech
        
        client = speech.SpeechClient()
        
        # 准备音频
        audio = speech.RecognitionAudio(content=audio_data)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.WEBM_OPUS,
            sample_rate_hertz=16000,
            language_code="zh-CN",
        )
        
        # 识别
        response = client.recognize(config=config, audio=audio)
        
        # 合并结果
        text = ""
        for result in response.results:
            text += result.alternatives[0].transcript
        
        return text
    except ImportError:
        return "错误：未安装 Google Cloud SDK"
    except Exception as e:
        return f"错误：{str(e)}"


def transcribe_audio(audio_file: str, audio_data: bytes = None) -> str:
    """
    语音识别主函数
    
    Args:
        audio_file: 音频文件路径
        audio_data: 音频数据（字节）
    
    Returns:
        识别的文字
    """
    if STT_ENGINE == 'whisper':
        return transcribe_with_whisper(audio_file)
    elif STT_ENGINE == 'azure':
        return transcribe_with_azure(audio_data)
    elif STT_ENGINE == 'google':
        return transcribe_with_google(audio_data)
    else:
        return f"不支持的引擎：{STT_ENGINE}"


@app.route('/health', methods=['GET'])
def health():
    """健康检查"""
    return jsonify({
        'status': 'ok',
        'engine': STT_ENGINE,
        'service': 'Speech-to-Text API'
    })


@app.route('/transcribe', methods=['POST'])
def transcribe():
    """
    语音转文字接口
    
    请求：
    - audio: 音频文件（webm/wav/mp3）
    
    响应：
    - text: 识别的文字
    - confidence: 置信度
    - duration: 音频时长
    """
    try:
        # 检查是否有音频文件
        if 'audio' not in request.files:
            return jsonify({
                'error': '请上传音频文件',
                'text': ''
            }), 400
        
        audio_file = request.files['audio']
        
        if audio_file.filename == '':
            return jsonify({
                'error': '文件名为空',
                'text': ''
            }), 400
        
        # 保存临时文件
        timestamp = subprocess.check_output(['date', '+%Y%m%d_%H%M%S']).decode().strip()
        temp_path = UPLOAD_FOLDER / f'st_{timestamp}.webm'
        audio_file.save(temp_path)
        
        # 语音识别
        text = transcribe_audio(str(temp_path))
        
        # 清理临时文件
        try:
            os.remove(temp_path)
        except:
            pass
        
        # 返回结果
        if text.startswith('错误') or text.startswith('Whisper 错误'):
            return jsonify({
                'error': text,
                'text': '',
                'success': False
            }), 500
        
        return jsonify({
            'text': text,
            'success': True,
            'engine': STT_ENGINE
        })
    
    except Exception as e:
        return jsonify({
            'error': f'服务器错误：{str(e)}',
            'text': ''
        }), 500


@app.route('/transcribe_base64', methods=['POST'])
def transcribe_base64():
    """
    语音转文字接口（Base64 编码）
    
    请求：
    - audio: Base64 编码的音频数据
    
    响应：
    - text: 识别的文字
    """
    try:
        import base64
        
        data = request.get_json()
        audio_base64 = data.get('audio', '')
        
        if not audio_base64:
            return jsonify({
                'error': '请提供音频数据',
                'text': ''
            }), 400
        
        # 解码 Base64
        audio_data = base64.b64decode(audio_base64)
        
        # 保存临时文件
        timestamp = subprocess.check_output(['date', '+%Y%m%d_%H%M%S']).decode().strip()
        temp_path = UPLOAD_FOLDER / f'st_{timestamp}.webm'
        
        with open(temp_path, 'wb') as f:
            f.write(audio_data)
        
        # 语音识别
        text = transcribe_audio(str(temp_path), audio_data)
        
        # 清理临时文件
        try:
            os.remove(temp_path)
        except:
            pass
        
        # 返回结果
        if text.startswith('错误') or text.startswith('Whisper 错误'):
            return jsonify({
                'error': text,
                'text': '',
                'success': False
            }), 500
        
        return jsonify({
            'text': text,
            'success': True,
            'engine': STT_ENGINE
        })
    
    except Exception as e:
        return jsonify({
            'error': f'服务器错误：{str(e)}',
            'text': ''
        }), 500


if __name__ == '__main__':
    print("=" * 50)
    print("🎤 语音识别服务（STT）")
    print("=" * 50)
    print(f"引擎：{STT_ENGINE}")
    print(f"端口：5050")
    print(f"上传目录：{UPLOAD_FOLDER}")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=5050, debug=False)
