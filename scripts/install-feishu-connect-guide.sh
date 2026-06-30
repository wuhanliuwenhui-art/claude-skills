#!/usr/bin/env bash

set -euo pipefail

REPO_URL="${REPO_URL:-https://github.com/wuhanliuwenhui-art/claude-skills.git}"
SKILL_NAME="${SKILL_NAME:-feishu-connect-guide}"
TARGET_DIR="${TARGET_DIR:-${HOME}/.codex/skills/${SKILL_NAME}}"
TMP_DIR="$(mktemp -d)"
BACKUP_SUFFIX="$(date +%Y%m%d-%H%M%S)"

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
  BACKUP_DIR="${TARGET_DIR}.bak.${BACKUP_SUFFIX}"
  echo "==> 发现已存在 skill，先备份到 ${BACKUP_DIR}"
  mv "${TARGET_DIR}" "${BACKUP_DIR}"
fi

echo "==> 安装 skill 到 ${TARGET_DIR}"
cp -R "${SOURCE_DIR}" "${TARGET_DIR}"

echo "==> 安装完成"
echo "Skill 路径：${TARGET_DIR}"
echo "你现在可以在对话里使用：\$feishu-connect-guide"
