# 📤 GitHub/Gitee 同步状态

---

## ✅ 本地已完成

### Git 仓库状态

```
📁 仓库位置：/home/admin/projects/live-tts/
📊 提交数：3 个
📄 文件数：27 个
📦 总大小：~2.2 MB（不含 output/）
```

### 提交历史

```
3bc9a75 feat: 添加一键推送脚本
d6ed918 docs: 添加 GitHub 和 Gitee 推送指南
d2a73c0 feat: Edge TTS 口播语音系统 - 152 个音频文件，4 个版本
```

### 包含文件

**核心代码** (4 个):
- `edge_tts_speech.py` - TTS 引擎
- `generate_all_demos.py` - 原版生成
- `generate_natural.py` - 优化版生成
- `generate_cute.py` - 粘人版生成
- `generate_weak.py` - 柔弱版生成

**启动脚本** (2 个):
- `start.sh` - 交互式启动
- `start_web.sh` - Web 服务启动

**Web 页面** (6 个):
- `all_versions.html` - 综合试听页
- `listen_here.html` - 原版试听
- `compare_natural.html` - 优化版对比
- `cute_voice.html` - 粘人版试听
- `weak_voice.html` - 柔弱版试听
- `voice_demo.html` - 语音演示

**文档** (9 个):
- `README.md` - 项目说明
- `README_ONLINE.md` - 在线版指南
- `ACCESS_GUIDE.md` - 访问指南
- `VOICE_LISTEN_GUIDE.md` - 语音试听指南
- `OPTIMIZATION_GUIDE.md` - 优化指南
- `CUTE_VOICE_GUIDE.md` - 粘人版指南
- `WEAK_VOICE_GUIDE.md` - 柔弱版指南
- `ALL_VERSIONS_GUIDE.md` - 全版本指南
- `PUSH_TO_GITHUB_GITEE.md` - 推送指南

**配置** (3 个):
- `.gitignore` - Git 忽略文件
- `speech_templates.txt` - 文案模板
- `push_to_remotes.sh` - 一键推送脚本

**其他** (3 个):
- `tts_api_server.py` - API 服务
- `tts_speech.py` - 语音脚本
- `voice_demo.html` - 演示页面

---

## ⚠️ 待完成：推送到远程

### 当前状态

```
远程仓库：未配置
推送状态：待推送
```

---

## 🚀 推送步骤

### 方法 1: 使用一键推送脚本（推荐）

```bash
cd /home/admin/projects/live-tts
bash push_to_remotes.sh
```

脚本会自动：
1. 检查是否配置远程仓库
2. 引导你配置 GitHub 和 Gitee
3. 提交未提交的更改
4. 推送到两个平台

---

### 方法 2: 手动推送

#### 步骤 1: 创建 GitHub 仓库

1. 访问 https://github.com/new
2. 仓库名：`edge-tts-speech`
3. 公开仓库
4. ❌ 不要初始化（已有代码）
5. 点击"Create repository"

#### 步骤 2: 添加 GitHub 远程

```bash
cd /home/admin/projects/live-tts

# 替换 YOUR_GITHUB_USERNAME 为你的 GitHub 用户名
git remote add github https://github.com/YOUR_GITHUB_USERNAME/edge-tts-speech.git
```

#### 步骤 3: 推送到 GitHub

```bash
git push -u github main
```

#### 步骤 4: 创建 Gitee 仓库

1. 访问 https://gitee.com/new
2. 仓库名：`edge-tts-speech`
3. 公开仓库
4. ❌ 不要初始化
5. 点击"创建"

#### 步骤 5: 添加 Gitee 远程

```bash
# 替换 YOUR_GITEE_USERNAME 为你的 Gitee 用户名
git remote add gitee https://gitee.com/YOUR_GITEE_USERNAME/edge-tts-speech.git
```

#### 步骤 6: 推送到 Gitee

```bash
git push -u gitee main
```

---

## 🔑 SSH 密钥（可选但推荐）

### 生成 SSH 密钥

```bash
# 生成密钥（如果已有可跳过）
ssh-keygen -t ed25519 -C "19922307306@189.cn"
```

### 添加到 GitHub

1. 查看公钥：
```bash
cat ~/.ssh/id_ed25519.pub
```

2. 复制到：https://github.com/settings/keys

### 添加到 Gitee

1. 查看公钥：
```bash
cat ~/.ssh/id_ed25519.pub
```

2. 复制到：https://gitee.com/profile/sshkeys

### 使用 SSH 远程

```bash
# GitHub
git remote set-url github git@github.com:YOUR_USERNAME/edge-tts-speech.git

# Gitee
git remote set-url gitee git@gitee.com:YOUR_USERNAME/edge-tts-speech.git
```

---

## 📊 推送后验证

### 检查远程仓库

```bash
git remote -v
```

应该看到：
```
github  https://github.com/YOUR_USERNAME/edge-tts-speech.git (fetch)
github  https://github.com/YOUR_USERNAME/edge-tts-speech.git (push)
gitee   https://gitee.com/YOUR_USERNAME/edge-tts-speech.git (fetch)
gitee   https://gitee.com/YOUR_USERNAME/edge-tts-speech.git (push)
```

### 查看 GitHub/Gitee 仓库

访问：
- https://github.com/YOUR_USERNAME/edge-tts-speech
- https://gitee.com/YOUR_USERNAME/edge-tts-speech

确认文件已上传。

---

## 📝 仓库描述建议

### 简短描述

```
🎤 Edge TTS 口播语音系统 - 20+ 中文语音，4 种版本，152 个预设音频
```

### 详细描述

```
基于微软 Edge TTS 的直播口播语音合成系统

✨ 特性:
- 20+ 中文语音（14 女声 +6 男声）
- 4 种版本：原版/优化版/粘人版/柔弱版
- 152 个预设音频文件
- Web 试听页面
- 语速音量精细调节（-50% 到 +50%）
- 批量生成脚本

🚀 快速开始:
pip install edge-tts
bash start.sh

🌐 在线试听:
http://localhost:7085/all_versions.html

适用场景：直播口播、娱乐带货、ASMR、短视频配音、有声书制作

#TTS #语音合成 #直播 #EdgeTTS #AI
```

### 话题标签

```
tts, text-to-speech, edge-tts, speech-synthesis, live-streaming, 
voice-generator, chinese-voice, ai-voice, audio-synthesis, 语音合成, 
直播工具
```

---

## ⚠️ 注意事项

### 音频文件

`output/` 目录已在 `.gitignore` 中，**不会被上传**。

原因：
- 152 个音频文件，2.2 MB
- 用户可以自行生成
- 避免仓库过大

如需上传音频：
```bash
# 编辑 .gitignore，注释掉 output/
# 然后
git add output/
git commit -m "add: 152 个预设音频文件"
git push
```

### 大文件

如果上传音频，建议使用 Git LFS：
```bash
git lfs install
git lfs track "output/*.mp3"
```

### 隐私

- ✅ 已配置 `.gitignore`
- ✅ 无 API 密钥
- ✅ 无敏感信息

---

## 🎯 快速命令总结

```bash
# 1. 进入目录
cd /home/admin/projects/live-tts

# 2. 运行一键推送脚本
bash push_to_remotes.sh

# 或手动推送
git remote add github https://github.com/YOUR_USERNAME/edge-tts-speech.git
git remote add gitee https://gitee.com/YOUR_USERNAME/edge-tts-speech.git
git push github main
git push gitee main

# 3. 验证
git remote -v
git log --oneline
```

---

## 📞 后续更新

### 提交新更改

```bash
git add -A
git commit -m "feat: 添加新功能"
git push github main
git push gitee main
```

### 拉取更新

```bash
git pull github main
git pull gitee main
```

---

**创建时间**: 2026-04-09  
**本地状态**: ✅ 完成（27 个文件，3 次提交）  
**远程状态**: ⚠️ 待推送  
**下一步**: 配置远程仓库并推送
