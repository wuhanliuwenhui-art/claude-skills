import json
import os
from pathlib import Path
from typing import Any, Dict, Optional
from urllib import parse, request


BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"
USER_TOKEN_PATH = BASE_DIR / "user_token.json"
OPEN_API_BASE = "https://open.feishu.cn/open-apis"


def load_local_env() -> Dict[str, str]:
    data: Dict[str, str] = {}
    if ENV_PATH.exists():
        for line in ENV_PATH.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            data[k.strip()] = v.strip()
    return data


def get_app_config() -> Dict[str, str]:
    env = load_local_env()
    app_id = env.get("FEISHU_APP_ID") or os.getenv("FEISHU_APP_ID")
    app_secret = env.get("FEISHU_APP_SECRET") or os.getenv("FEISHU_APP_SECRET")
    if not app_id or not app_secret:
        raise RuntimeError("缺少 FEISHU_APP_ID / FEISHU_APP_SECRET，请检查 .claudian/feishu/.env")
    return {
        "app_id": app_id,
        "app_secret": app_secret,
    }


def _http_json(
    method: str,
    url: str,
    *,
    headers: Optional[Dict[str, str]] = None,
    query: Optional[Dict[str, Any]] = None,
    body: Optional[Dict[str, Any]] = None,
    timeout: int = 20,
) -> Dict[str, Any]:
    if query:
        url = f"{url}?{parse.urlencode(query)}"
    payload = None
    final_headers = dict(headers or {})
    if body is not None:
        payload = json.dumps(body, ensure_ascii=False).encode("utf-8")
        final_headers.setdefault("Content-Type", "application/json; charset=utf-8")
    req = request.Request(url, data=payload, headers=final_headers, method=method)
    with request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def get_tenant_access_token() -> str:
    cfg = get_app_config()
    resp = _http_json(
        "POST",
        f"{OPEN_API_BASE}/auth/v3/tenant_access_token/internal",
        body={"app_id": cfg["app_id"], "app_secret": cfg["app_secret"]},
    )
    if resp.get("code") != 0 or not resp.get("tenant_access_token"):
        raise RuntimeError(f"获取 tenant_access_token 失败: {resp}")
    return resp["tenant_access_token"]


def get_user_access_token() -> str:
    if not USER_TOKEN_PATH.exists():
        raise RuntimeError("缺少 user_token.json，请先完成飞书用户授权")
    data = json.loads(USER_TOKEN_PATH.read_text(encoding="utf-8"))
    token = data.get("access_token")
    if not token:
        raise RuntimeError("user_token.json 中没有 access_token")
    return token


def feishu_api(
    method: str,
    path: str,
    *,
    query: Optional[Dict[str, Any]] = None,
    body: Optional[Dict[str, Any]] = None,
    access_token: Optional[str] = None,
    timeout: int = 20,
) -> Dict[str, Any]:
    token = access_token or get_tenant_access_token()
    return _http_json(
        method,
        f"{OPEN_API_BASE}{path}",
        headers={"Authorization": f"Bearer {token}"},
        query=query,
        body=body,
        timeout=timeout,
    )
