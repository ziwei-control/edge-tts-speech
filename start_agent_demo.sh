#!/bin/bash
# 启动智能 Agent TTS 演示服务

echo "======================================"
echo "🤖 智能 Agent TTS 演示服务"
echo "======================================"
echo ""

# 检查 API 服务是否运行
if ! pgrep -f "agent_tts_api.py" > /dev/null; then
    echo "📡 启动 API 服务..."
    cd /home/admin/projects/live-tts
    nohup python3 agent_tts_api.py > logs/api_server.log 2>&1 &
    sleep 3
    echo "✅ API 服务已启动 (端口 7086)"
else
    echo "✅ API 服务已在运行 (端口 7086)"
fi

# 启动 Web 服务
echo ""
echo "🌐 启动 Web 服务..."
cd /home/admin/projects/live-tts
nohup python3 -m http.server 7087 > logs/web_server.log 2>&1 &

sleep 2

echo ""
echo "======================================"
echo "✅ 服务启动完成！"
echo "======================================"
echo ""
echo "📡 API 服务：http://localhost:7086"
echo "🌐 Web 试听：http://localhost:7087/agent_tts_demo.html"
echo ""
echo "📖 API 文档：http://localhost:7086/"
echo "📂 输出目录：/home/admin/projects/live-tts/output/"
echo ""
echo "💡 提示："
echo "  - 访问 Web 页面进行试听"
echo "  - 使用 API 集成到你的 Agent"
echo "  - 查看 logs/ 目录查看日志"
echo ""
