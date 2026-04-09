#!/bin/bash
# 一键配置 HTTPS（使用 Ngrok）

echo "======================================"
echo "🔒 一键配置 HTTPS（使用 Ngrok）"
echo "======================================"
echo ""

# 检查 ngrok
if ! command -v ngrok &> /dev/null; then
    echo "📦 Ngrok 未安装，正在下载..."
    
    # 下载 ngrok
    cd /tmp
    wget -q https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz
    
    if [ $? -eq 0 ]; then
        tar -xzf ngrok-v3-stable-linux-amd64.tgz
        sudo mv ngrok /usr/local/bin/
        echo "✅ Ngrok 安装完成"
    else
        echo "❌ 下载失败，请检查网络连接"
        exit 1
    fi
else
    echo "✅ Ngrok 已安装"
fi

echo ""
echo "🚀 启动 Ngrok 隧道..."
echo "======================================"
echo ""

# 启动 ngrok（后台运行）
ngrok http 7091 --log=stdout > /tmp/ngrok.log 2>&1 &
NGROK_PID=$!

# 等待 5 秒获取 URL
echo "等待隧道建立（约 5 秒）..."
sleep 5

# 提取 HTTPS URL
HTTPS_URL=$(curl -s http://127.0.0.1:4040/api/tunnels | grep -oP '"public_url":"\K[^"]+' | head -1)

if [ -n "$HTTPS_URL" ]; then
    echo ""
    echo "======================================"
    echo "✅ HTTPS 配置完成！"
    echo "======================================"
    echo ""
    echo "🌐 访问地址："
    echo "   $HTTPS_URL/voice_chat.html"
    echo ""
    echo "🎤 现在可以使用语音输入了！"
    echo ""
    echo "📋 服务信息："
    echo "   进程 ID: $NGROK_PID"
    echo "   管理界面：http://127.0.0.1:4040"
    echo "   日志：/tmp/ngrok.log"
    echo ""
    echo "⏹️  停止服务："
    echo "   kill $NGROK_PID"
    echo ""
    echo "💡 提示：Ngrok 免费版会随机分配域名，每次启动域名不同"
    echo ""
else
    echo "❌ 隧道启动失败"
    echo "   日志：/tmp/ngrok.log"
    echo "   请检查网络连接或尝试其他方案"
fi
