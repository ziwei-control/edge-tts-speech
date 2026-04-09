#!/bin/bash
# 一键推送到 GitHub 和 Gitee

echo "======================================"
echo "📤 Edge TTS 一键推送到 GitHub 和 Gitee"
echo "======================================"
echo ""

# 检查是否已配置远程
if ! git remote | grep -q "github"; then
    echo "❌ 未配置 GitHub 远程仓库"
    echo ""
    echo "请先运行以下命令（替换 YOUR_USERNAME）："
    echo "git remote add github https://github.com/YOUR_USERNAME/edge-tts-speech.git"
    echo ""
    read -p "是否现在配置？(y/n) " config_github
    if [ "$config_github" = "y" ]; then
        read -p "输入 GitHub 用户名：" github_user
        git remote add github https://github.com/$github_user/edge-tts-speech.git
        echo "✅ GitHub 远程仓库已配置"
    fi
fi

if ! git remote | grep -q "gitee"; then
    echo "❌ 未配置 Gitee 远程仓库"
    echo ""
    echo "请先运行以下命令（替换 YOUR_USERNAME）："
    echo "git remote add gitee https://gitee.com/YOUR_USERNAME/edge-tts-speech.git"
    echo ""
    read -p "是否现在配置？(y/n) " config_gitee
    if [ "$config_gitee" = "y" ]; then
        read -p "输入 Gitee 用户名：" gitee_user
        git remote add gitee https://gitee.com/$gitee_user/edge-tts-speech.git
        echo "✅ Gitee 远程仓库已配置"
    fi
fi

echo ""
echo "当前远程仓库："
git remote -v
echo ""

# 提交未提交的更改
if [ -n "$(git status --porcelain)" ]; then
    echo "📝 检测到未提交的更改..."
    git add -A
    git commit -m "chore: 自动提交更新"
    echo "✅ 更改已提交"
    echo ""
fi

# 推送到 GitHub
if git remote | grep -q "github"; then
    echo "🚀 推送到 GitHub..."
    git push github main
    if [ $? -eq 0 ]; then
        echo "✅ GitHub 推送成功"
    else
        echo "❌ GitHub 推送失败"
    fi
    echo ""
fi

# 推送到 Gitee
if git remote | grep -q "gitee"; then
    echo "🚀 推送到 Gitee..."
    git push gitee main
    if [ $? -eq 0 ]; then
        echo "✅ Gitee 推送成功"
    else
        echo "❌ Gitee 推送失败"
    fi
    echo ""
fi

echo "======================================"
echo "📊 推送完成统计"
echo "======================================"
echo "提交数：$(git rev-list --count HEAD)"
echo "文件大小：$(du -sh . | cut -f1)"
echo "文件数：$(git ls-files | wc -l)"
echo ""
echo "🎉 完成！"
