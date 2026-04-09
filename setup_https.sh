#!/bin/bash
# 一键配置 HTTPS（Cloudflare Tunnel）

echo "======================================"
echo "🔒 一键配置 HTTPS（启用语音输入）"
echo "======================================"

# 检查 cloudflared
if ! command -v cloudflared &> /dev/null; then
    echo "📦 安装 cloudflared..."
    wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
    sudo dpkg -i cloudflared-linux-amd64.deb 2>/dev/null
    rm -f cloudflared-linux-amd64.deb
    echo "✅ cloudflared 安装完成"
else
    echo "✅ cloudflared 已安装"
fi

echo ""
echo "🚀 启动 Cloudflare Tunnel..."
echo "======================================"
echo ""

# 启动 tunnel（后台运行）
cloudflared tunnel --url http://localhost:7091 2>&1 | tee /tmp/cloudflared.log &
TUNNEL_PID=$!

# 等待 10 秒获取 URL
echo "等待隧道建立..."
sleep 10

# 提取 HTTPS URL
HTTPS_URL=$(grep -oP 'https://[^\s]+' /tmp/cloudflared.log | head -1)

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
    echo "   进程 ID: $TUNNEL_PID"
    echo "   日志：/tmp/cloudflared.log"
    echo ""
    echo "⏹️  停止服务："
    echo "   kill $TUNNEL_PID"
    echo ""
else
    echo "❌ 隧道启动失败，请检查网络连接"
    echo "   日志：/tmp/cloudflared.log"
fi
