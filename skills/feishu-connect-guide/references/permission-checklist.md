# 飞书接入权限清单

按目标范围给使用者最小权限清单。

## 只接机器人通知

- `im:message:send_as_bot`
- `im:message.p2p_msg:readonly`
- `im:message.group_at_msg:readonly`

## 机器人 + 日历

在机器人权限基础上增加：

- `calendar:calendar`
- `calendar:calendar:readonly`
- `calendar:calendar.event:create`

## 机器人 + 日历 + 文档

在上面基础上增加：

- `docx:document`
- `docx:document:readonly`
- `drive:drive`

## 机器人 + 日历 + 文档 + 知识库

在上面基础上增加：

- `wiki:wiki`
- `wiki:space:retrieve`
- `wiki:node:retrieve`

## 需要用户长期授权

额外增加：

- `offline_access`

## 重定向 URL

要求使用者在飞书开放平台的：

- **安全设置 → 重定向 URL**

添加：

```text
http://127.0.0.1:8787/feishu/callback
```
