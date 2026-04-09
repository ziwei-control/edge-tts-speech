#!/bin/bash
# 启动语音识别服务（STT）

cd /home/admin/projects/live-tts

echo "======================================"
echo "🎤 启动语音识别服务（STT）"
echo "======================================"

# 检查 Whisper 是否安装
if ! python3 -c "import whisper" 2>/dev/null; then
    echo "⚠️  Whisper 未安装"
    echo ""
    echo "请选择安装方式："
    echo ""
    echo "1️⃣  使用 Whisper（本地，免费，推荐）"
    echo "   pip install openai-whisper"
    echo ""
    echo "2️⃣  使用系统 STT 服务（需要配置 API Key）"
    echo "   编辑 stt_service.py 设置 Azure/Google/百度 Key"
    echo ""
    echo "3️⃣  跳过 STT，仅使用文字输入"
    echo ""
    read -p "是否安装 Whisper？(y/n): " choice
    if [[ $choice == "y" ]]; then
        echo "正在安装 Whisper..."
        pip install openai-whisper
    fi
fi

# 启动 STT 服务
echo ""
echo "🚀 启动 STT 服务（端口 5050）..."
nohup python3 stt_service.py > logs/stt_service.log 2>&1 &
STT_PID=$!

echo "✅ STT 服务已启动"
echo "   进程 ID: $STT_PID"
echo "   日志：logs/stt_service.log"
echo ""

# 等待 3 秒检查状态
sleep 3
if ps -p $STT_PID > /dev/null; then
    echo "✅ 服务运行正常"
    curl -s http://localhost:5050/health | python3 -m json.tool
else
    echo "❌ 服务启动失败"
    echo "查看日志：tail -f logs/stt_service.log"
fi
