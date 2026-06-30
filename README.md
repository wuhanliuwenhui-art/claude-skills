# Claude Skills

这个仓库用于存放可复用的 Claude / Codex skill。

## 当前可用 skill

### 1. 飞书接入引导

目录：

```text
skills/feishu-connect-guide/
```

作用：

- 分步骤引导使用者接入飞书应用
- 引导配置机器人、日历、文档、知识库访问
- 引导完成用户授权
- 引导把飞书知识库挂成资料库
- 引导设置“相关问题先查知识库再回答”的默认规则

---

## 安装方式

### 方式 1：一键安装

复制执行：

```bash
curl -fsSL https://raw.githubusercontent.com/wuhanliuwenhui-art/claude-skills/main/scripts/install-feishu-connect-guide.sh | bash
```

默认安装到：

```text
~/.codex/skills/feishu-connect-guide
```

---

### 方式 2：手动安装

```bash
git clone https://github.com/wuhanliuwenhui-art/claude-skills.git
mkdir -p ~/.codex/skills
cp -R claude-skills/skills/feishu-connect-guide ~/.codex/skills/
```

---

## 使用前准备

安装 skill 后，仍需要使用者自己准备：

1. 飞书开放平台应用
2. App ID / App Secret
3. 本地 `.env` 文件
4. 浏览器授权一次

这个过程会由 `feishu-connect-guide` skill 一步步引导完成。

---

## 目录结构

```text
skills/
  feishu-connect-guide/
scripts/
  install-feishu-connect-guide.sh
```
