# 销冠话术助手安装后设置

这份说明给第一次使用的人看。先不用理解技术细节，只按步骤检查。

## 你需要准备什么

1. 飞书账号，并且这个账号能打开团队的销售资料库。
2. 团队负责人提供的飞书应用 `App ID` 和 `App Secret`。
3. 三个飞书资料链接：
   - 标准资料库
   - 高成交话术库
   - 成交微信号总表

没有这些信息时，不要自己猜，找团队负责人要。

## 第一步：检查缺什么

打开终端，运行：

```bash
cd ~/.codex/skills/sales-champion-reply
python3 tools/feishu/doctor.py
```

它会告诉你哪些已经准备好，哪些还缺。

## 第二步：填写飞书应用凭证

打开这个文件：

```text
~/.codex/skills/sales-champion-reply/tools/feishu/.env
```

如果没有这个文件，就把同目录下的 `.env.example` 复制一份，改名为 `.env`。

填入团队负责人给你的：

```text
FEISHU_APP_ID=这里填 App ID
FEISHU_APP_SECRET=这里填 App Secret
FEISHU_REDIRECT_URI=http://127.0.0.1:8787/feishu/callback
```

## 第三步：完成飞书授权

运行：

```bash
cd ~/.codex/skills/sales-champion-reply/tools/feishu
python3 oauth_user_auth.py
```

看到 `AUTH_URL=` 后，把后面的链接复制到浏览器打开，按页面提示授权。

授权成功后，会生成：

```text
user_token.json
```

## 第四步：填写资料库链接

打开：

```text
~/.codex/skills/sales-champion-reply/references/local-sources.md
```

把里面的“待填写”换成团队负责人给你的飞书链接。

至少要填：

- 标准资料库
- 高成交话术库
- 成交微信号总表

## 第五步：测试能不能读取

运行：

```bash
cd ~/.codex/skills/sales-champion-reply
python3 tools/feishu/read_feishu_doc.py standard
```

如果能看到标题、链接、正文或子文档列表，就说明配置成功。

## 常见问题

### 提示缺少 FEISHU_APP_ID / FEISHU_APP_SECRET

说明 `.env` 没填好。找团队负责人要 App ID 和 App Secret。

### 提示缺少 user_token.json

说明还没完成飞书授权。重新运行：

```bash
cd ~/.codex/skills/sales-champion-reply/tools/feishu
python3 oauth_user_auth.py
```

### 提示未配置资料库链接

说明 `references/local-sources.md` 里还有“待填写”。把团队飞书链接填进去。

### 提示没有权限

说明你的飞书账号打不开对应文档。让团队负责人给你开文档权限。
