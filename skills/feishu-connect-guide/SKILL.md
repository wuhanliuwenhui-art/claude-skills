---
name: feishu-connect-guide
description: Guide the operator step by step through connecting a Feishu app, bot, calendar, docs, and wiki access, including local `.env` setup, app permissions, redirect URL configuration, bot long-connection setup, and user OAuth authorization. Use when the user wants to connect Feishu, bind a Feishu bot, enable Feishu notifications, access Feishu docs/calendar/wiki, or needs a click-by-click setup walkthrough.
---

# 飞书接入引导

按“只做下一步”的方式引导使用者完成飞书接入。每次只给一个明确动作，等使用者确认后再进入下一步。

## 工作方式

1. 先确认目标范围：
   - 只接机器人通知
   - 接机器人 + 日历
   - 接机器人 + 日历 + 文档
   - 接机器人 + 日历 + 文档 + 知识库
2. 默认采用双通道：
   - 应用身份：机器人通知、应用可访问资源
   - 用户身份：访问使用者本人有权限的文档、日历、知识库
3. 不要求使用者把 `App Secret` 直接发到聊天里。
4. 统一要求使用者把凭证写进本地 `.env`。
5. 遇到权限不足时，优先判断是：
   - API 权限没开
   - 资源本身没授权
   - 需要切到用户授权

## 引导节奏

每一步都使用以下格式：

```markdown
第 N 步（使用者操作）
1. 点哪里
2. 填什么
3. 做完后回复我：xxx
```

如果需要你执行本地检查，再补：

```markdown
第 N 步（AI 操作）
- 我会验证：xxx
- 如果失败，我会告诉你下一步补什么
```

不要在同一轮抛给使用者过多动作。优先一步一确认。

## 标准流程

### 第 1 段：飞书后台准备

按顺序引导使用者完成：

1. 打开飞书开放平台并进入目标应用
2. 开启机器人能力
3. 在“开发配置 → 权限管理”开通所需权限
4. 在“安全设置 → 重定向 URL”添加：

```text
http://127.0.0.1:8787/feishu/callback
```

权限清单不要硬背，读取 `references/permission-checklist.md` 后按目标范围给出。

### 第 2 段：本地凭证

引导使用者在项目根目录下准备：

```text
.claudian/feishu/.env
```

内容格式：

```env
FEISHU_APP_ID=你的AppID
FEISHU_APP_SECRET=你的AppSecret
```

必须提醒：
- 不要把密钥直接发到聊天里
- 路径使用相对路径说明，不写任何个人电脑绝对路径

### 第 3 段：应用身份验证

在使用者完成 `.env` 后，执行：

1. 获取 `tenant_access_token`
2. 验证机器人长连接
3. 验证是否能主动发消息
4. 验证应用身份下能访问哪些日历、文档或知识库资源

如果应用身份已经足够，就继续用应用身份。

### 第 4 段：用户授权

出现以下任一情况时，切到用户授权：

- 需要访问使用者本人的知识库空间
- 需要访问“我的文档库”
- 应用身份能读单页但不能读整个 Wiki 空间
- 需要访问使用者本人可见但应用不可见的资源

用户授权时，按顺序引导：

1. 启动本地回调服务
2. 打开授权页
3. 让使用者在浏览器点击“同意授权”
4. 换取 `user_access_token`
5. 保存到：

```text
.claudian/feishu/user_token.json
```

### 第 5 段：资源访问规则

后续默认按以下顺序处理飞书资源请求：

1. 先尝试应用身份
2. 不够再切用户身份
3. 仍然失败再提示补权限或补资源授权

## 常见判断规则

### 机器人发不出消息

优先检查：
- 是否开启机器人能力
- 是否开了消息发送权限
- 是否存在可达的 `open_id` / `chat_id`

### 日历能列出但不能操作

优先检查：
- 目标日历是否对当前身份有 writer / owner 权限
- 是否只是应用主日历，而不是用户主日历

### 知识库单页能读，空间不能展开

直接判断为：
- 应用身份权限不足
- 应切换到用户授权读取 Wiki 空间

### 使用者说“我不会操作”

改为点击式引导，明确写：
- 打开哪里
- 点击哪里
- 填什么
- 做完后回复什么

## 输出要求

1. 用中文简体
2. 用最短可执行话术
3. 一次只推进一步或一小段
4. 每一步明确标注“使用者操作”或“AI 操作”
5. 不主动输出大段原理解释
6. 不暴露使用者个人电脑路径、个人仓库路径、个人知识库名称，除非当前任务必须引用

## 需要时读取的参考文件

- 需要给权限清单时，读取 `references/permission-checklist.md`
- 需要给本地文件结构时，读取 `references/local-files.md`
