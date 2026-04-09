#!/bin/bash
# 一键启动所有语音服务（STT + TTS + Web + HTTPS）

cd /home/admin/projects/live-tts

echo "======================================"
echo "🚀 启动所有语音服务"
echo "======================================"

# 创建日志目录
mkdir -p logs output/api

# 停止旧服务
echo "⏹️  停止旧服务..."
pkill -f stt_service 2>/dev/null
pkill -f agent_tts_api 2>/dev/null
pkill -f flask_voice_server 2>/dev/null
pkill -f "lt --port" 2>/dev/null
sleep 2

# 启动 STT 服务（5050 端口）
echo "🎤 启动 STT 服务（5050 端口）..."
nohup python3 stt_service.py > logs/stt_service.log 2>&1 &
STT_PID=$!
echo "✅ STT API 已启动 (PID: $STT_PID)"

# 启动 TTS API（7086 端口）
echo "🔊 启动 TTS API（7086 端口）..."
nohup python3 agent_tts_api.py > logs/api_server.log 2>&1 &
TTS_PID=$!
echo "✅ TTS API 已启动 (PID: $TTS_PID)"

# 启动 Web 服务（7091 端口）
echo "🌐 启动 Web 服务（7091 端口）..."
nohup python3 flask_voice_server.py > logs/flask_voice.log 2>&1 &
WEB_PID=$!
echo "✅ Web 服务已启动 (PID: $WEB_PID)"

# 启动 Localtunnel（HTTPS 隧道）
echo "🔒 启动 Localtunnel..."
lt --port 7091 > /tmp/lt.log 2>&1 &
LT_PID=$!
echo "✅ Localtunnel 已启动 (PID: $LT_PID)"

# 等待 5 秒检查状态
echo ""
echo "等待服务启动..."
sleep 5

echo ""
echo "======================================"
echo "✅ 所有服务启动完成！"
echo "======================================"
echo ""

# 健康检查
echo "📊 健康检查："
echo ""

# STT 健康检查
STT_HEALTH=$(curl -s http://localhost:5050/health 2>/dev/null)
if [ -n "$STT_HEALTH" ]; then
    echo "✅ STT API (5050): 运行正常"
    echo "   $STT_HEALTH"
else
    echo "❌ STT API (5050): 未响应"
fi
echo ""

# TTS 健康检查
TTS_HEALTH=$(curl -s http://localhost:7086/health 2>/dev/null)
if [ -n "$TTS_HEALTH" ]; then
    echo "✅ TTS API (7086): 运行正常"
    echo "   $TTS_HEALTH"
else
    echo "❌ TTS API (7086): 未响应"
fi
echo ""

# Web 健康检查
WEB_HEALTH=$(curl -s http://localhost:7091/api/health 2>/dev/null)
if [ -n "$WEB_HEALTH" ]; then
    echo "✅ Web 服务 (7091): 运行正常"
    echo "   $WEB_HEALTH"
else
    echo "❌ Web 服务 (7091): 未响应"
fi
echo ""

# Localtunnel 链接
echo "🌐 访问地址："
echo ""
echo "   本地访问："
echo "   http://localhost:7091/voice_chat.html"
echo ""
echo "   公网访问（文字输入）："
echo "   http://8.213.149.224:7091/voice_chat.html"
echo ""

LT_URL=$(cat /tmp/lt.log 2>/dev/null | grep "your url is" | grep -oP 'https://[^\s]+')
if [ -n "$LT_URL" ]; then
    echo "   HTTPS 访问（语音输入）："
    echo "   $LT_URL/voice_chat.html"
    echo ""
    echo "   ⚠️ 首次访问点击'高级' → '继续访问'"
else
    echo "    Localtunnel 正在启动，稍后查看链接："
    echo "   cat /tmp/lt.log | grep 'your url is'"
fi
echo ""

echo "======================================"
echo "📋 服务信息："
echo "======================================"
echo ""
echo "进程 ID:"
echo "   STT:  $STT_PID"
echo "   TTS:  $TTS_PID"
echo "   Web:  $WEB_PID"
echo "   LT:   $LT_PID"
echo ""
echo "日志文件:"
echo "   STT:  tail -f logs/stt_service.log"
echo "   TTS:  tail -f logs/api_server.log"
echo "   Web:  tail -f logs/flask_voice.log"
echo "   LT:   cat /tmp/lt.log"
echo ""
echo "停止服务:"
echo "   pkill -f stt_service"
echo "   pkill -f agent_tts_api"
echo "   pkill -f flask_voice_server"
echo "   pkill -f 'lt --port'"
echo ""
echo "或者一键停止："
echo "   bash $0 stop"
echo ""
