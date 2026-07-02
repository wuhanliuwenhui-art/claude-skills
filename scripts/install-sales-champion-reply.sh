#!/usr/bin/env bash

set -euo pipefail

REPO_URL="${REPO_URL:-https://github.com/wuhanliuwenhui-art/claude-skills.git}"
SKILL_NAME="${SKILL_NAME:-sales-champion-reply}"
TARGET_DIR="${TARGET_DIR:-${HOME}/.codex/skills/${SKILL_NAME}}"
TMP_DIR="$(mktemp -d)"

cleanup() {
  rm -rf "${TMP_DIR}"
}
trap cleanup EXIT

echo "==> 克隆仓库到临时目录"
git clone --depth 1 "${REPO_URL}" "${TMP_DIR}/repo" >/dev/null 2>&1

SOURCE_DIR="${TMP_DIR}/repo/skills/${SKILL_NAME}"

if [[ ! -d "${SOURCE_DIR}" ]]; then
  echo "安装失败：未找到 ${SOURCE_DIR}"
  exit 1
fi

mkdir -p "$(dirname "${TARGET_DIR}")"

if [[ -e "${TARGET_DIR}" ]]; then
  echo "==> 发现已存在 skill，原地更新 ${TARGET_DIR}"
  if [[ -f "${TARGET_DIR}/references/local-sources.md" ]]; then
    mkdir -p "${TMP_DIR}/preserve/references"
    cp "${TARGET_DIR}/references/local-sources.md" "${TMP_DIR}/preserve/references/local-sources.md"
  fi
  if [[ -f "${TARGET_DIR}/tools/feishu/.env" ]]; then
    mkdir -p "${TMP_DIR}/preserve/tools/feishu"
    cp "${TARGET_DIR}/tools/feishu/.env" "${TMP_DIR}/preserve/tools/feishu/.env"
  fi
  if [[ -f "${TARGET_DIR}/tools/feishu/user_token.json" ]]; then
    mkdir -p "${TMP_DIR}/preserve/tools/feishu"
    cp "${TARGET_DIR}/tools/feishu/user_token.json" "${TMP_DIR}/preserve/tools/feishu/user_token.json"
  fi
  rm -rf "${TARGET_DIR}/SKILL.md" "${TARGET_DIR}/agents" "${TARGET_DIR}/references" "${TARGET_DIR}/tools"
else
  echo "==> 安装 skill 到 ${TARGET_DIR}"
  mkdir -p "${TARGET_DIR}"
fi

cp -R "${SOURCE_DIR}/." "${TARGET_DIR}/"

if [[ -f "${TMP_DIR}/preserve/references/local-sources.md" ]]; then
  mkdir -p "${TARGET_DIR}/references"
  cp "${TMP_DIR}/preserve/references/local-sources.md" "${TARGET_DIR}/references/local-sources.md"
fi

if [[ -f "${TMP_DIR}/preserve/tools/feishu/.env" ]]; then
  mkdir -p "${TARGET_DIR}/tools/feishu"
  cp "${TMP_DIR}/preserve/tools/feishu/.env" "${TARGET_DIR}/tools/feishu/.env"
fi

if [[ -f "${TMP_DIR}/preserve/tools/feishu/user_token.json" ]]; then
  mkdir -p "${TARGET_DIR}/tools/feishu"
  cp "${TMP_DIR}/preserve/tools/feishu/user_token.json" "${TARGET_DIR}/tools/feishu/user_token.json"
fi

LOCAL_SOURCES="${TARGET_DIR}/references/local-sources.md"

if [[ ! -f "${LOCAL_SOURCES}" ]]; then
  cat > "${LOCAL_SOURCES}" <<EOF
# 本地资料源配置

这个文件由安装脚本生成，只保存在你的本地电脑里。不要把包含内部链接的文件提交到公开仓库。

## 销冠智能体总入口

- 名称：${SALES_CHAMPION_ROOT_NAME:-待填写}
- 链接：${SALES_CHAMPION_ROOT_URL:-待填写}

## 标准资料库

- 名称：${SALES_CHAMPION_STANDARD_KB_NAME:-待填写}
- 链接：${SALES_CHAMPION_STANDARD_KB_URL:-待填写}
- 用途：产品事实唯一来源。

## 销售聊天记录

- 名称：${SALES_CHAMPION_CHAT_LOGS_NAME:-待填写}
- 链接：${SALES_CHAMPION_CHAT_LOGS_URL:-待填写}

## 成交客户

- 名称：${SALES_CHAMPION_DEAL_CUSTOMERS_NAME:-待填写}
- 链接：${SALES_CHAMPION_DEAL_CUSTOMERS_URL:-待填写}

## 成交微信号总表

- 名称：${SALES_CHAMPION_DEAL_TABLE_NAME:-待填写}
- 链接：${SALES_CHAMPION_DEAL_TABLE_URL:-待填写}

## 高成交话术库

- 名称：${SALES_CHAMPION_TALK_LIBRARY_NAME:-待填写}
- 链接：${SALES_CHAMPION_TALK_LIBRARY_URL:-待填写}
EOF
fi

FEISHU_ENV="${TARGET_DIR}/tools/feishu/.env"

if [[ ! -f "${FEISHU_ENV}" && -n "${FEISHU_APP_ID:-}" && -n "${FEISHU_APP_SECRET:-}" ]]; then
  mkdir -p "$(dirname "${FEISHU_ENV}")"
  cat > "${FEISHU_ENV}" <<EOF
FEISHU_APP_ID=${FEISHU_APP_ID}
FEISHU_APP_SECRET=${FEISHU_APP_SECRET}
FEISHU_REDIRECT_URI=${FEISHU_REDIRECT_URI:-http://127.0.0.1:8787/feishu/callback}
EOF
fi

echo "==> 安装完成"
echo "Skill 路径：${TARGET_DIR}"
echo "你现在可以在对话里使用：\$sales-champion-reply"
echo "飞书读取工具：${TARGET_DIR}/tools/feishu/read_feishu_doc.py"
