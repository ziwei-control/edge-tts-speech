#!/bin/bash
echo "=========================================="
echo "🚀 一键启动所有语音服务"
echo "=========================================="
echo

# 1. 停止旧进程
echo "🛑 停止旧进程..."
pkill -f "lt --port" 2>/dev/null
pkill -f "flask_voice_server.py" 2>/dev/null
pkill -f "agent_tts_api.py" 2>/dev/null
pkill -f "stt_service.py" 2>/dev/null
sleep 2

# 2. 启动 STT 服务
echo "🎤 启动 STT 语音识别服务 (5050)..."
cd /home/admin/projects/live-tts
nohup python3 stt_service.py > /tmp/stt.log 2>&1 &
sleep 3

# 检查 STT
if curl -s http://localhost:5050/health > /dev/null 2>&1; then
    echo "✅ STT 服务启动成功"
else
    echo "❌ STT 服务启动失败，检查日志：/tmp/stt.log"
fi

# 3. 启动 TTS API
echo "🎵 启动 TTS API 服务 (7086)..."
nohup python3 agent_tts_api.py > /tmp/tts_api.log 2>&1 &
sleep 3

# 检查 TTS API
if curl -s http://localhost:7086/health > /dev/null 2>&1; then
    echo "✅ TTS API 启动成功"
else
    echo "❌ TTS API 启动失败，检查日志：/tmp/tts_api.log"
fi

# 4. 启动 Flask 代理服务器
echo "🌐 启动 Flask 代理服务器 (7091)..."
nohup python3 flask_voice_server.py > /tmp/flask_voice.log 2>&1 &
sleep 3

# 检查 Flask
if curl -s http://localhost:7091/api/health > /dev/null 2>&1; then
    echo "✅ Flask 代理启动成功"
else
    echo "❌ Flask 代理启动失败，检查日志：/tmp/flask_voice.log"
fi

# 5. 启动 Localtunnel
echo "🔒 启动 Localtunnel HTTPS 隧道..."
nohup lt --port 7091 > /tmp/lt.log 2>&1 &
sleep 5

# 获取新链接
if [ -f /tmp/lt.log ]; then
    LT_URL=$(grep -o 'https://[^ ]*' /tmp/lt.log | head -1)
    if [ ! -z "$LT_URL" ]; then
        echo "✅ Localtunnel 启动成功"
        echo
        echo "=========================================="
        echo "🎉 所有服务已启动！"
        echo "=========================================="
        echo
        echo "🔗 HTTPS 链接:"
        echo "   $LT_URL"
        echo
        echo "📱 可用页面:"
        echo "   语音对话：$LT_URL/voice_chat.html"
        echo "   语音库：  $LT_URL/voice_library.html"
        echo "   全版本：  $LT_URL/all_versions.html"
        echo
        echo "⚠️ 首次访问需点击"高级 → 继续访问""
        echo
        echo "🎤 语音识别已启用，可以按住说话！"
        echo
    else
        echo "❌ Localtunnel 启动失败，检查日志：/tmp/lt.log"
    fi
else
    echo "❌ Localtunnel 日志文件不存在"
fi

echo "=========================================="
echo "💡 提示：服务停止时运行此脚本重启"
echo "=========================================="
