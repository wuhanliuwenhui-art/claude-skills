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
  rm -rf "${TARGET_DIR}/SKILL.md" "${TARGET_DIR}/agents" "${TARGET_DIR}/references"
else
  echo "==> 安装 skill 到 ${TARGET_DIR}"
  mkdir -p "${TARGET_DIR}"
fi

cp -R "${SOURCE_DIR}/." "${TARGET_DIR}/"

if [[ -f "${TMP_DIR}/preserve/references/local-sources.md" ]]; then
  mkdir -p "${TARGET_DIR}/references"
  cp "${TMP_DIR}/preserve/references/local-sources.md" "${TARGET_DIR}/references/local-sources.md"
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

## 高成交话术库

- 名称：${SALES_CHAMPION_TALK_LIBRARY_NAME:-待填写}
- 链接：${SALES_CHAMPION_TALK_LIBRARY_URL:-待填写}
EOF
fi

echo "==> 安装完成"
echo "Skill 路径：${TARGET_DIR}"
echo "你现在可以在对话里使用：\$sales-champion-reply"
