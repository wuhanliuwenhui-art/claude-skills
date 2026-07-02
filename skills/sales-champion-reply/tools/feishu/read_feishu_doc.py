#!/usr/bin/env python3
import argparse
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from urllib import error, parse

from common import feishu_api, get_tenant_access_token, get_user_access_token


PRESET_CONFIG = {
    "root": {
        "title": "销冠智能体总入口",
        "section": "销冠智能体总入口",
        "env": "SALES_CHAMPION_ROOT_URL",
    },
    "standard": {
        "title": "标准资料库",
        "section": "标准资料库",
        "env": "SALES_CHAMPION_STANDARD_KB_URL",
    },
    "talk-library": {
        "title": "高成交话术库",
        "section": "高成交话术库",
        "env": "SALES_CHAMPION_TALK_LIBRARY_URL",
    },
    "deal-customers": {
        "title": "成交客户",
        "section": "成交客户",
        "env": "SALES_CHAMPION_DEAL_CUSTOMERS_URL",
    },
    "deal-table": {
        "title": "成交微信号总表",
        "section": "成交微信号总表",
        "env": "SALES_CHAMPION_DEAL_TABLE_URL",
    },
}

ALIASES = {
    "标准资料库": "standard",
    "标准": "standard",
    "话术库": "talk-library",
    "高成交话术库": "talk-library",
    "成交客户": "deal-customers",
    "成交微信号总表": "deal-table",
}


class FeishuReadError(RuntimeError):
    pass


def skill_root() -> Path:
    return Path(__file__).resolve().parents[2]


def local_sources_path() -> Path:
    return skill_root() / "references" / "local-sources.md"


def load_local_source_links() -> Dict[str, str]:
    path = local_sources_path()
    if not path.exists():
        return {}

    links: Dict[str, str] = {}
    current_section = ""
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if line.startswith("## "):
            current_section = line[3:].strip()
            continue
        if current_section and line.startswith("- 链接："):
            value = line.split("：", 1)[1].strip()
            if value and value != "待填写":
                links[current_section] = value
    return links


def get_access_token() -> str:
    try:
        return get_user_access_token()
    except Exception:
        return get_tenant_access_token()


def checked_api(
    method: str,
    path: str,
    *,
    query: Optional[Dict[str, Any]] = None,
    access_token: Optional[str] = None,
) -> Dict[str, Any]:
    resp = feishu_api(method, path, query=query, access_token=access_token)
    if resp.get("code") != 0:
        raise FeishuReadError(f"飞书接口返回错误 code={resp.get('code')} msg={resp.get('msg')}")
    return resp.get("data") or {}


def resolve_target(target: str) -> Tuple[str, str]:
    key = ALIASES.get(target, target)
    if key not in PRESET_CONFIG:
        return "自定义飞书链接", target

    config = PRESET_CONFIG[key]
    env_url = os.getenv(config["env"], "").strip()
    if env_url:
        return config["title"], env_url

    links = load_local_source_links()
    local_url = links.get(config["section"], "")
    if local_url:
        return config["title"], local_url

    raise FeishuReadError(
        f"未配置 {config['title']} 链接。请在 {local_sources_path()} 填写对应链接，"
        f"或设置环境变量 {config['env']}。"
    )


def extract_token(url_or_token: str) -> Tuple[str, str]:
    if re.fullmatch(r"[A-Za-z0-9]{16,}", url_or_token):
        return "unknown", url_or_token

    parsed = parse.urlparse(url_or_token)
    parts = [p for p in parsed.path.split("/") if p]
    for kind in ("wiki", "docx", "doc"):
        if kind in parts:
            idx = parts.index(kind)
            if idx + 1 < len(parts):
                return kind, parts[idx + 1]
    raise FeishuReadError("无法从输入中解析飞书 token，请传入 wiki/docx 链接或 token。")


def resolve_wiki_node(token: str, access_token: str) -> Dict[str, Any]:
    data = checked_api(
        "GET",
        "/wiki/v2/spaces/get_node",
        query={"token": token, "obj_type": "wiki"},
        access_token=access_token,
    )
    node = data.get("node")
    if not node:
        raise FeishuReadError("没有读取到 wiki 节点信息。")
    return node


def get_document(document_id: str, access_token: str) -> Dict[str, Any]:
    data = checked_api("GET", f"/docx/v1/documents/{document_id}", access_token=access_token)
    return data.get("document") or {}


def get_document_content(document_id: str, access_token: str) -> str:
    data = checked_api(
        "GET",
        f"/docx/v1/documents/{document_id}/raw_content",
        query={"lang": 0},
        access_token=access_token,
    )
    return (data.get("content") or "").strip()


def list_child_nodes(space_id: str, node_token: str, access_token: str) -> List[Dict[str, Any]]:
    children: List[Dict[str, Any]] = []
    page_token = ""
    while True:
        query: Dict[str, Any] = {
            "page_size": 50,
            "parent_node_token": node_token,
        }
        if page_token:
            query["page_token"] = page_token
        data = checked_api(
            "GET",
            f"/wiki/v2/spaces/{space_id}/nodes",
            query=query,
            access_token=access_token,
        )
        children.extend(data.get("items") or [])
        if not data.get("has_more"):
            break
        page_token = data.get("page_token") or ""
        if not page_token:
            break
    return children


def read_target(title_hint: str, source_url: str) -> Dict[str, Any]:
    link_kind, token = extract_token(source_url)
    access_token = get_access_token()

    if link_kind == "docx":
        document = get_document(token, access_token)
        content = get_document_content(token, access_token)
        return {
            "title": document.get("title") or title_hint,
            "url": source_url,
            "type": "docx",
            "content": content,
            "children": [],
        }

    if link_kind == "doc":
        raise FeishuReadError("当前轻量脚本只支持 wiki 节点和新版 docx 文档，暂不支持旧版 doc。")

    node = resolve_wiki_node(token, access_token)
    obj_type = node.get("obj_type") or ""
    node_title = node.get("title") or title_hint
    node_url = node.get("url") or source_url

    if obj_type == "docx" and node.get("obj_token"):
        document = get_document(node["obj_token"], access_token)
        content = get_document_content(node["obj_token"], access_token)
        children: List[Dict[str, Any]] = []
        if node.get("has_child") and node.get("space_id") and node.get("node_token"):
            children = list_child_nodes(str(node["space_id"]), node["node_token"], access_token)
        return {
            "title": document.get("title") or node_title,
            "url": node_url,
            "type": "wiki/docx",
            "content": content,
            "children": children,
        }

    if node.get("has_child") and node.get("space_id") and node.get("node_token"):
        children = list_child_nodes(str(node["space_id"]), node["node_token"], access_token)
        return {
            "title": node_title,
            "url": node_url,
            "type": f"wiki/{obj_type or 'folder'}",
            "content": "",
            "children": children,
        }

    raise FeishuReadError(f"当前节点类型暂不支持读取正文：obj_type={obj_type or '空'}。")


def format_result(result: Dict[str, Any]) -> str:
    lines = [
        f"标题：{result['title']}",
        f"链接：{result['url']}",
        f"类型：{result['type']}",
        "",
        "正文：",
        result.get("content") or "未读取到正文。",
    ]

    children = result.get("children") or []
    if children:
        lines.append("")
        lines.append("子文档：" if result.get("content") else "这是一个目录，请从下面子文档中选择具体文档继续读取：")
        for idx, child in enumerate(children, start=1):
            title = child.get("title") or "未命名"
            obj_type = child.get("obj_type") or child.get("node_type") or "unknown"
            url = child.get("url") or ""
            lines.append(f"{idx}. {title} | 类型：{obj_type} | 链接：{url}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="读取飞书 wiki/docx 文档，输出标题、链接和纯文本正文。"
    )
    parser.add_argument(
        "target",
        help="飞书 wiki/docx 链接、token，或预设名：standard、talk-library、deal-customers、deal-table",
    )
    args = parser.parse_args()

    try:
        title_hint, source_url = resolve_target(args.target)
        print(format_result(read_target(title_hint, source_url)))
        return 0
    except error.URLError as exc:
        print(f"读取失败：无法访问飞书 API，可能是网络受限或服务不可达。详情：{exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"读取失败：{exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
