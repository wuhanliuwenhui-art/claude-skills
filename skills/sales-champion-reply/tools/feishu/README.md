# 飞书资料读取工具

这个目录随 `sales-champion-reply` Skill 一起安装，用于读取飞书 wiki/docx 文档。

## 配置

复制 `.env.example` 为 `.env`，填写飞书应用凭证：

```text
FEISHU_APP_ID=
FEISHU_APP_SECRET=
FEISHU_REDIRECT_URI=http://127.0.0.1:8787/feishu/callback
```

资料库链接填写在 Skill 的 `references/local-sources.md` 中。

## 授权

```bash
cd ~/.codex/skills/sales-champion-reply/tools/feishu
python3 oauth_user_auth.py
```

脚本会输出 `AUTH_URL=`，打开链接授权后会保存 `user_token.json`。

## 读取资料

```bash
cd ~/.codex/skills/sales-champion-reply
python3 tools/feishu/read_feishu_doc.py standard
python3 tools/feishu/read_feishu_doc.py talk-library
python3 tools/feishu/read_feishu_doc.py deal-table
```

也可以直接传飞书 wiki/docx 链接。
