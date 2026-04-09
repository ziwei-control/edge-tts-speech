#!/bin/bash
# 一键配置 HTTPS（使用 Localtunnel）

echo "======================================"
echo "🔒 一键配置 HTTPS（使用 Localtunnel）"
echo "======================================"
echo ""

# 检查 Node.js
if ! command -v node &> /dev/null; then
    echo "❌ 未安装 Node.js"
    echo "   请先安装：apt install nodejs npm"
    exit 1
fi

# 检查 localtunnel
if ! command -v lt &> /dev/null; then
    echo "📦 安装 Localtunnel..."
    npm install -g localtunnel 2>&1 | tail -2
    echo "✅ Localtunnel 安装完成"
else
    echo "✅ Localtunnel 已安装"
fi

echo ""
echo "🚀 启动 Localtunnel..."
echo "======================================"
echo ""

# 启动 localtunnel（后台运行）
lt --port 7091 > /tmp/lt.log 2>&1 &
LT_PID=$!

# 等待 5 秒获取 URL
echo "等待隧道建立（约 5 秒）..."
sleep 5

# 提取 HTTPS URL
HTTPS_URL=$(cat /tmp/lt.log | grep -oP 'your url is: \K.*' | head -1)

if [ -n "$HTTPS_URL" ]; then
    echo ""
    echo "======================================"
    echo "✅ HTTPS 配置完成！"
    echo "======================================"
    echo ""
    echo "🌐 访问地址："
    echo "   $HTTPS_URL"
    echo "   $HTTPS_URL/voice_chat.html"
    echo ""
    echo "🎤 现在可以使用语音输入了！"
    echo ""
    echo "📋 服务信息："
    echo "   进程 ID: $LT_PID"
    echo "   日志：/tmp/lt.log"
    echo ""
    echo "⏹️  停止服务："
    echo "   kill $LT_PID"
    echo ""
    echo "💡 提示：Localtunnel 免费版会随机分配域名"
    echo ""
else
    echo "❌ 隧道启动失败"
    echo "   日志：/tmp/lt.log"
    cat /tmp/lt.log
    echo ""
    echo "💡 建议尝试其他方案："
    echo "   1. SSH 隧道（无需配置）"
    echo "   2. 文字输入（无需 HTTPS）"
fi
