#!/bin/bash
# 启动 TTS 试听页面 HTTP 服务

cd /home/admin/projects/live-tts

# 检查是否已运行
if ps aux | grep "http.server 7085" | grep -v grep > /dev/null; then
    echo "✅ HTTP 服务已在运行"
    ps aux | grep "http.server 7085" | grep -v grep
else
    echo "🚀 启动 HTTP 服务..."
    nohup python3 -m http.server 7085 > /tmp/tts_web.log 2>&1 &
    sleep 2
    
    if ps aux | grep "http.server 7085" | grep -v grep > /dev/null; then
        echo "✅ 服务启动成功！"
        echo ""
        echo "📱 访问地址:"
        echo "   本地：http://localhost:7085/listen_here.html"
        echo "   公网：http://8.213.149.224:7085/listen_here.html"
        echo ""
        echo "🎵 音频文件:"
        echo "   /home/admin/projects/live-tts/output/demo/"
        echo ""
        echo "📊 服务信息:"
        ps aux | grep "http.server 7085" | grep -v grep
    else
        echo "❌ 服务启动失败"
        cat /tmp/tts_web.log
    fi
fi
