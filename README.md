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

### 2. 销冠话术助手

目录：

```text
skills/sales-champion-reply/
```

作用：

- 销售粘贴客户问题或企微聊天上下文后，生成可直接发客户的合规销售回复
- 严格遵守飞书标准资料库、高成交话术库、安全红线和输出规则
- 运营可基于新增企微聊天记录和成交微信号，复盘真实成交话术
- 以企微聊天记录中的真实发送内容作为后续迭代事实，不要求销售额外登记最终话术
- GitHub 仓库不保存内部飞书链接；安装后在本地配置资料源

---

## 安装方式

### 方式 1：一键安装

安装飞书接入引导：

复制执行：

```bash
curl -fsSL https://raw.githubusercontent.com/wuhanliuwenhui-art/claude-skills/main/scripts/install-feishu-connect-guide.sh | bash
```

安装销冠话术助手：

```bash
curl -fsSL https://raw.githubusercontent.com/wuhanliuwenhui-art/claude-skills/main/scripts/install-sales-champion-reply.sh | bash
```

如果要一键写入团队飞书资料源，可在私下发给团队成员类似命令：

```bash
curl -fsSL https://raw.githubusercontent.com/wuhanliuwenhui-art/claude-skills/main/scripts/install-sales-champion-reply.sh | \
SALES_CHAMPION_ROOT_URL="你的销冠智能体总入口" \
SALES_CHAMPION_STANDARD_KB_URL="你的标准资料库链接" \
SALES_CHAMPION_CHAT_LOGS_URL="你的销售聊天记录链接" \
SALES_CHAMPION_DEAL_CUSTOMERS_URL="你的成交客户链接" \
SALES_CHAMPION_TALK_LIBRARY_URL="你的高成交话术库链接" \
bash
```

默认安装到：

```text
~/.codex/skills/<skill-name>
```

---

### 方式 2：手动安装

```bash
git clone https://github.com/wuhanliuwenhui-art/claude-skills.git
mkdir -p ~/.codex/skills
cp -R claude-skills/skills/feishu-connect-guide ~/.codex/skills/
cp -R claude-skills/skills/sales-champion-reply ~/.codex/skills/
```

---

## 使用前准备

安装 skill 后，仍需要使用者自己准备：

1. 飞书开放平台应用
2. App ID / App Secret
3. 本地 `.env` 文件
4. 浏览器授权一次

这个过程会由 `feishu-connect-guide` skill 一步步引导完成。

使用 `sales-champion-reply` 前，需要使用者具备对应飞书资料库访问权限，并在本地配置资料源：

```text
~/.codex/skills/sales-champion-reply/references/local-sources.md
```

配置项包括：销冠智能体资料体系、标准资料库、高成交话术库、销售聊天记录、成交微信号总表。

---

## 目录结构

```text
skills/
  feishu-connect-guide/
  sales-champion-reply/
scripts/
  install-feishu-connect-guide.sh
  install-sales-champion-reply.sh
```
