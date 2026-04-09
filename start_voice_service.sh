#!/bin/bash
# 启动语音交互服务（带 API 代理）

echo "======================================"
echo "🎤 启动语音交互服务"
echo "======================================"

cd /home/admin/projects/live-tts

# 停止旧服务
echo "📋 停止旧服务..."
pkill -9 -f "http.server" 2>/dev/null
pkill -9 -f "simple_proxy" 2>/dev/null
pkill -9 -f "web_server_with" 2>/dev/null
sleep 1

# 检查 TTS API
echo "📡 检查 TTS API..."
if curl -s http://localhost:7086/health > /dev/null 2>&1; then
    echo "✅ TTS API 运行正常"
else
    echo "⚠️  TTS API 未运行，启动中..."
    nohup python3 agent_tts_api.py > logs/api_server.log 2>&1 &
    sleep 3
fi

# 启动 Web 服务（带 API 代理）
echo "🌐 启动 Web 服务（端口 7091）..."
nohup python3 simple_proxy.py > logs/voice_web.log 2>&1 &
sleep 2

# 验证服务
echo ""
echo "======================================"
echo "✅ 服务启动完成！"
echo "======================================"
echo ""
echo "📡 TTS API:   http://localhost:7086"
echo "🌐 Web 页面： http://localhost:7091/voice_chat.html"
echo ""
echo "🔗 公网访问：http://8.213.149.224:7091/voice_chat.html"
echo "   (需配置阿里云安全组开放 7091 端口)"
echo ""
echo "📋 测试命令:"
echo "  curl http://localhost:7091/api/health"
echo ""
