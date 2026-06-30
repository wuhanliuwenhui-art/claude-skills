# 本地文件约定

所有说明都使用相对路径，不写个人绝对路径。

## 必需文件

### 应用凭证

```text
.claudian/feishu/.env
```

内容：

```env
FEISHU_APP_ID=你的AppID
FEISHU_APP_SECRET=你的AppSecret
```

### 用户授权结果

```text
.claudian/feishu/user_token.json
```

## 常见脚本

```text
.claudian/feishu/common.py
.claudian/feishu/check_connection.py
.claudian/feishu/bot_longconn.py
.claudian/feishu/oauth_user_auth.py
```

## 引导原则

1. 只告诉使用者需要创建什么文件
2. 只告诉使用者相对路径
3. 不引用任何个人电脑目录
4. 不要求使用者把密钥直接粘贴到聊天里
