# 🔧 GitHub/Gitee 推送配置指南

---

## ⚠️ 当前状态

### GitHub
- ✅ 本地仓库已创建（28 个文件，4 次提交）
- ✅ 远程仓库已配置（SSH: git@github.com:Spanda/edge-tts-speech.git）
- ❌ SSH 密钥未添加到 GitHub
- ❌ Token 认证失败

### Gitee
- ✅ 本地仓库已创建
- ✅ 远程仓库已配置（HTTPS: pandac0@gitee.com/pandac0/edge-tts-speech.git）
- ❌ Token 认证失败

---

## 🚀 解决方案

### 方案 1: GitHub SSH 推送（推荐）

#### 步骤 1: 复制 SSH 公钥

```bash
cat ~/.ssh/id_ed25519.pub
```

输出：
```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIAURHiZestvzS9Md5rlLG9g8VUFsBmzGhzFWywxE179a pandaco-20260401
```

#### 步骤 2: 添加到 GitHub

1. 访问：https://github.com/settings/keys
2. 点击 "New SSH key"
3. 标题：`pandaco-20260401`
4. 粘贴公钥内容
5. 点击 "Add SSH key"

#### 步骤 3: 创建 GitHub 仓库

1. 访问：https://github.com/new
2. 仓库名：`edge-tts-speech`
3. 公开仓库
4. ❌ 不要初始化
5. 点击 "Create repository"

#### 步骤 4: 推送

```bash
cd /home/admin/projects/live-tts
git push -u github main
```

---

### 方案 2: Gitee HTTPS 推送

#### 步骤 1: 获取 Gitee 密码

Token 认证失败，请使用 Gitee 账号密码。

#### 步骤 2: 配置密码

```bash
cd /home/admin/projects/live-tts
git remote remove gitee
git remote add gitee https://pandac0@gitee.com/pandac0/edge-tts-speech.git
```

#### 步骤 3: 创建 Gitee 仓库

1. 访问：https://gitee.com/new
2. 仓库名：`edge-tts-speech`
3. 公开仓库
4. ❌ 不要初始化
5. 点击 "创建"

#### 步骤 4: 推送

```bash
git push -u gitee main
```

会提示输入密码，输入你的 Gitee 密码。

---

### 方案 3: 使用一键配置脚本

```bash
cd /home/admin/projects/live-tts
bash setup_remotes_with_token.sh
```

脚本会提示输入用户名并自动配置。

---

## 📝 快速命令

### 检查远程配置

```bash
git remote -v
```

### 测试 SSH 连接

```bash
ssh -T git@github.com
```

成功会显示：
```
Hi Spanda! You've successfully authenticated, but GitHub does not provide shell access.
```

### 推送代码

```bash
# 推送到 GitHub
git push github main

# 推送到 Gitee
git push gitee main

# 推送所有远程
git push --all
```

---

## 🔑 SSH 密钥信息

**公钥**:
```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIAURHiZestvzS9Md5rlLG9g8VUFsBmzGhzFWywxE179a pandaco-20260401
```

**私钥位置**: `~/.ssh/id_ed25519`

**需要添加到的平台**:
- GitHub: https://github.com/settings/keys
- Gitee: https://gitee.com/profile/sshkeys

---

## ✅ 完成检查清单

### GitHub
- [ ] 复制 SSH 公钥
- [ ] 添加到 GitHub Settings
- [ ] 创建 edge-tts-speech 仓库
- [ ] 测试 SSH 连接：`ssh -T git@github.com`
- [ ] 推送代码：`git push github main`

### Gitee
- [ ] 确认 Gitee 密码
- [ ] 创建 edge-tts-speech 仓库
- [ ] 推送代码：`git push gitee main`

---

## 🎯 推荐流程

1. **先配置 GitHub**（SSH 方式）
   - 添加 SSH 公钥到 GitHub
   - 创建仓库
   - 推送

2. **再配置 Gitee**（HTTPS 方式）
   - 创建仓库
   - 使用密码推送

3. **验证**
   - 访问 GitHub 仓库确认文件已上传
   - 访问 Gitee 仓库确认文件已上传

---

## 📞 遇到问题？

### Token 认证失败
- Token 可能已过期
- Token 权限不足
- 使用 SSH 方式替代

### SSH 认证失败
- SSH 密钥未添加到平台
- 用户名错误
- 仓库不存在

### 仓库不存在
- 需要先在平台创建仓库
- 不要初始化（已有代码）

---

**创建时间**: 2026-04-09  
**本地状态**: ✅ 完成  
**远程状态**: ⚠️ 待配置 SSH/密码  
**下一步**: 添加 SSH 公钥到 GitHub，创建仓库后推送
