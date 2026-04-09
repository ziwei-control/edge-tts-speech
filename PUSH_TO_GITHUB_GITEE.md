# 📤 推送到 GitHub 和 Gitee 指南

---

## ✅ 本地提交已完成

当前仓库状态：
- ✅ Git 仓库已初始化
- ✅ 所有文件已提交（25 个文件）
- ✅ 提交信息：feat: Edge TTS 口播语音系统 - 152 个音频文件，4 个版本

---

## 🚀 推送到 GitHub

### 1. 创建 GitHub 仓库

访问 https://github.com/new 创建新仓库

**推荐名称**: `edge-tts-speech` 或 `live-tts-system`

**设置**:
- ✅ Public（公开）
- ❌ 不要初始化 README（已有）
- ❌ 不要添加 .gitignore（已有）
- ❌ 不要添加 License（可选）

### 2. 添加远程仓库

```bash
cd /home/admin/projects/live-tts

# 替换 YOUR_USERNAME 为你的 GitHub 用户名
git remote add origin https://github.com/YOUR_USERNAME/edge-tts-speech.git

# 或者使用 SSH（推荐）
git remote add origin git@github.com:YOUR_USERNAME/edge-tts-speech.git
```

### 3. 推送

```bash
git push -u origin main
```

---

## 🚀 推送到 Gitee（码云）

### 1. 创建 Gitee 仓库

访问 https://gitee.com/new 创建新仓库

**推荐名称**: `edge-tts-speech` 或 `live-tts-system`

**设置**:
- ✅ 公开
- ❌ 不要初始化 README
- ❌ 不要添加 .gitignore
- ❌ 不要添加 License

### 2. 添加远程仓库

```bash
cd /home/admin/projects/live-tts

# 替换 YOUR_USERNAME 为你的 Gitee 用户名
git remote add gitee https://gitee.com/YOUR_USERNAME/edge-tts-speech.git

# 或者使用 SSH（推荐）
git remote add gitee git@gitee.com:YOUR_USERNAME/edge-tts-speech.git
```

### 3. 推送

```bash
git push -u gitee main
```

---

## 🔄 同时推送到两个平台

### 1. 配置多个远程

```bash
cd /home/admin/projects/live-tts

# 添加 GitHub
git remote add github https://github.com/YOUR_USERNAME/edge-tts-speech.git

# 添加 Gitee
git remote add gitee https://gitee.com/YOUR_USERNAME/edge-tts-speech.git
```

### 2. 一键推送两个平台

```bash
# 推送到 GitHub
git push github main

# 推送到 Gitee
git push gitee main
```

### 3. 或者配置 pushall

```bash
# 添加远程
git remote add origin https://github.com/YOUR_USERNAME/edge-tts-speech.git

# 添加 Gitee 为 push 目标
git remote set-url --add --push origin https://github.com/YOUR_USERNAME/edge-tts-speech.git
git remote set-url --add --push origin https://gitee.com/YOUR_USERNAME/edge-tts-speech.git

# 一键推送到两个平台
git push origin main
```

---

## 🔑 SSH 密钥配置

### GitHub

```bash
# 生成 SSH 密钥
ssh-keygen -t ed25519 -C "19922307306@189.cn"

# 查看公钥
cat ~/.ssh/id_ed25519.pub

# 复制公钥到 GitHub
# https://github.com/settings/keys
```

### Gitee

```bash
# 使用同一个密钥或生成新的
ssh-keygen -t ed25519 -C "19922307306@189.cn" -f ~/.ssh/id_ed25519_gitee

# 查看公钥
cat ~/.ssh/id_ed25519_gitee.pub

# 复制公钥到 Gitee
# https://gitee.com/profile/sshkeys
```

---

## 📝 后续更新

### 提交新更改

```bash
cd /home/admin/projects/live-tts

# 添加更改
git add -A

# 提交
git commit -m "feat: 添加新功能"

# 推送到两个平台
git push github main
git push gitee main
```

### 查看状态

```bash
git status
git log --oneline
git remote -v
```

---

## 🎯 推荐仓库结构

```
edge-tts-speech/
├── README.md                 # 项目说明
├── edge_tts_speech.py        # TTS 引擎
├── start.sh                  # 启动脚本
├── start_web.sh              # Web 服务启动
├── generate_*.py             # 批量生成脚本
├── *.html                    # 试听页面
├── *.md                      # 文档
├── speech_templates.txt      # 文案模板
├── .gitignore                # Git 忽略文件
└── output/                   # 音频输出（建议不上传）
    ├── demo/
    ├── natural/
    ├── cute/
    └── weak/
```

**注意**: `output/` 目录已在 `.gitignore` 中，不会被上传。
用户可以克隆后自行生成音频文件。

---

## 📦 如果需要上传音频文件

如果希望用户上传音频文件，可以：

### 1. 修改 .gitignore

```bash
# 注释掉 output/
# output/
```

### 2. 添加音频文件

```bash
git add output/
git commit -m "add: 152 个预设音频文件"
git push
```

**注意**: 音频文件较大（2.2 MB），可能影响克隆速度。

---

## 🔗 仓库描述模板

### GitHub/Gitee 描述

```
🎤 Edge TTS 口播语音系统

基于微软 Edge TTS 的直播口播语音合成系统，支持 20+ 中文语音，
4 种版本（原版/优化版/粘人版/柔弱版），152 个预设音频文件。

✨ 特性:
- 20+ 中文语音（14 女声 +6 男声）
- 4 种版本适配不同场景
- Web 试听页面
- 语速音量精细调节
- 批量生成脚本

🚀 快速开始:
pip install edge-tts
bash start.sh

🌐 在线试听:
http://localhost:7085/all_versions.html

#TTS #语音合成 #直播 #EdgeTTS #AI
```

### 话题标签

```
tts text-to-speech edge-tts speech-synthesis live-streaming 
voice-generator chinese-voice ai-voice audio-synthesis
```

---

## ⚠️ 注意事项

1. **音频文件**: `output/` 目录默认不上传（.gitignore）
2. **大文件**: 如需上传音频，考虑使用 Git LFS
3. **API Key**: 不要上传任何 API 密钥
4. **隐私**: 检查不要上传敏感信息

---

## 🎉 完成检查清单

- [ ] 创建 GitHub 仓库
- [ ] 添加 GitHub 远程
- [ ] 推送到 GitHub
- [ ] 创建 Gitee 仓库
- [ ] 添加 Gitee 远程
- [ ] 推送到 Gitee
- [ ] 配置 SSH 密钥（可选）
- [ ] 更新仓库描述
- [ ] 添加话题标签
- [ ] 测试克隆

---

## 📞 快速命令

```bash
# 一键推送两个平台
cd /home/admin/projects/live-tts
git push github main && git push gitee main

# 查看远程仓库
git remote -v

# 查看提交历史
git log --oneline --graph

# 拉取最新代码
git pull github main
git pull gitee main
```

---

**创建时间**: 2026-04-09  
**本地提交**: ✅ 完成  
**待推送**: GitHub + Gitee
