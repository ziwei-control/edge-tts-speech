#!/bin/bash
cd /home/admin/projects/live-tts
nohup python3 -m http.server 7091 > logs/voice_web.log 2>&1 &
echo "✅ Web 服务已启动：http://localhost:7091/voice_chat.html"
