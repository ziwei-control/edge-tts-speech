#!/bin/bash
# 一键启动所有语音服务

cd /home/admin/projects/live-tts

echo "======================================"
echo "🚀 启动所有语音服务"
echo "======================================"

# 创建日志目录
mkdir -p logs output/api

# 停止旧服务
echo "停止旧服务..."
pkill -f agent_tts_api 2>/dev/null
pkill -f flask_voice_server 2>/dev/null
sleep 1

# 启动 TTS API
echo "启动 TTS API（7086 端口）..."
nohup python3 agent_tts_api.py > logs/api_server.log 2>&1 &
TTS_PID=$!
echo "✅ TTS API 已启动 (PID: $TTS_PID)"

# 启动 Web 服务
echo "启动 Web 服务（7091 端口）..."
nohup python3 flask_voice_server.py > logs/flask_voice.log 2>&1 &
WEB_PID=$!
echo "✅ Web 服务已启动 (PID: $WEB_PID)"

# 等待 3 秒检查状态
sleep 3

echo ""
echo "======================================"
echo "✅ 服务启动完成！"
echo "======================================"
echo ""
echo "🌐 访问地址："
echo "   本地：http://localhost:7091/voice_chat.html"
echo "   公网：http://8.213.149.224:7091/voice_chat.html"
echo ""
echo "🔒 HTTPS 语音输入："
echo "   重启 Localtunnel：lt --port 7091"
echo "   访问：https://xxx-xxx.loca.lt/voice_chat.html"
echo ""
echo "📊 健康检查："
echo "   curl http://localhost:7086/health"
echo "   curl http://localhost:7091/api/health"
echo ""
echo "📋 日志："
echo "   tail -f logs/api_server.log"
echo "   tail -f logs/flask_voice.log"
echo ""
echo "⏹️  停止服务："
echo "   pkill -f agent_tts_api"
echo "   pkill -f flask_voice_server"
echo ""
