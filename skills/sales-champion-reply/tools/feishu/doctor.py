#!/usr/bin/env python3
from pathlib import Path


REQUIRED_SECTIONS = [
    "标准资料库",
    "高成交话术库",
    "成交微信号总表",
]


def skill_root() -> Path:
    return Path(__file__).resolve().parents[2]


def feishu_dir() -> Path:
    return Path(__file__).resolve().parent


def local_sources_path() -> Path:
    return skill_root() / "references" / "local-sources.md"


def read_env_keys(path: Path) -> set:
    keys = set()
    if not path.exists():
        return keys
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        if value.strip():
            keys.add(key.strip())
    return keys


def read_source_links(path: Path) -> dict:
    links = {}
    if not path.exists():
        return links
    current_section = ""
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if line.startswith("## "):
            current_section = line[3:].strip()
            continue
        if current_section and line.startswith("- 链接："):
            value = line.split("：", 1)[1].strip()
            links[current_section] = value
    return links


def status_line(ok: bool, text: str) -> str:
    return ("[OK] " if ok else "[待处理] ") + text


def main() -> int:
    env_path = feishu_dir() / ".env"
    token_path = feishu_dir() / "user_token.json"
    sources_path = local_sources_path()

    env_keys = read_env_keys(env_path)
    source_links = read_source_links(sources_path)

    print("销冠话术助手飞书读取能力检查")
    print("")
    print(status_line(env_path.exists(), f"飞书应用凭证文件：{env_path}"))
    print(status_line("FEISHU_APP_ID" in env_keys, "已填写 FEISHU_APP_ID"))
    print(status_line("FEISHU_APP_SECRET" in env_keys, "已填写 FEISHU_APP_SECRET"))
    print(status_line(token_path.exists(), f"飞书用户授权 token：{token_path}"))
    print(status_line(sources_path.exists(), f"本地资料源配置：{sources_path}"))

    for section in REQUIRED_SECTIONS:
        value = source_links.get(section, "")
        ok = bool(value and value != "待填写")
        print(status_line(ok, f"{section}链接"))

    print("")
    print("下一步：")
    if not env_path.exists():
        print("1. 把 tools/feishu/.env.example 复制为 tools/feishu/.env，并填写飞书 App ID / App Secret。")
    elif "FEISHU_APP_ID" not in env_keys or "FEISHU_APP_SECRET" not in env_keys:
        print("1. 打开 tools/feishu/.env，补全 FEISHU_APP_ID 和 FEISHU_APP_SECRET。")
    elif not token_path.exists():
        print("1. 运行：cd tools/feishu && python3 oauth_user_auth.py")
        print("2. 打开脚本输出的 AUTH_URL，完成飞书授权。")
    elif any(not (source_links.get(section, "") and source_links.get(section, "") != "待填写") for section in REQUIRED_SECTIONS):
        print("1. 打开 references/local-sources.md，把标准资料库、高成交话术库、成交微信号总表链接填好。")
    else:
        print("1. 已具备基础查询条件，可运行：python3 tools/feishu/read_feishu_doc.py standard")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
