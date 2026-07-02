#!/usr/bin/env bash

set -euo pipefail

REPO_URL="${REPO_URL:-https://github.com/wuhanliuwenhui-art/claude-skills.git}"
SKILL_NAME="${SKILL_NAME:-yangge-title}"
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
  rm -rf "${TARGET_DIR}/SKILL.md" "${TARGET_DIR}/agents" "${TARGET_DIR}/references"
else
  echo "==> 安装 skill 到 ${TARGET_DIR}"
  mkdir -p "${TARGET_DIR}"
fi

cp -R "${SOURCE_DIR}/." "${TARGET_DIR}/"

echo "==> 安装完成"
echo "Skill 路径：${TARGET_DIR}"
echo "你现在可以在对话里使用：\$洋哥爆款标题"
