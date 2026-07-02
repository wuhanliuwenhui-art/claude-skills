import json
import secrets
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Dict, Optional
from urllib import parse, request

from common import ENV_PATH, get_app_config, load_local_env


REDIRECT_URI = "http://127.0.0.1:8787/feishu/callback"
TOKEN_PATH = Path(__file__).resolve().parent / "user_token.json"

SCOPES = [
    "offline_access",
    "wiki:wiki",
    "wiki:node:retrieve",
    "wiki:space:retrieve",
    "docx:document",
    "docx:document:readonly",
    "drive:drive",
    "calendar:calendar",
    "calendar:calendar:readonly",
    "calendar:calendar.event:create",
]


def build_auth_url(state: str) -> str:
    cfg = get_app_config()
    redirect_uri = load_local_env().get("FEISHU_REDIRECT_URI", REDIRECT_URI)
    query = {
        "client_id": cfg["app_id"],
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "scope": " ".join(SCOPES),
        "prompt": "consent",
        "state": state,
    }
    return "https://accounts.feishu.cn/open-apis/authen/v1/authorize?" + parse.urlencode(query)


def exchange_code_for_token(code: str) -> Dict:
    cfg = get_app_config()
    redirect_uri = load_local_env().get("FEISHU_REDIRECT_URI", REDIRECT_URI)
    payload = json.dumps(
        {
            "grant_type": "authorization_code",
            "client_id": cfg["app_id"],
            "client_secret": cfg["app_secret"],
            "code": code,
            "redirect_uri": redirect_uri,
        }
    ).encode("utf-8")
    req = request.Request(
        "https://accounts.feishu.cn/oauth/v3/token",
        data=payload,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    with request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8"))


def save_token(payload: Dict) -> None:
    TOKEN_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


class CallbackHandler(BaseHTTPRequestHandler):
    state: str = ""
    result: Dict = {}
    done_event: threading.Event

    def log_message(self, format: str, *args) -> None:
        return

    def do_GET(self) -> None:
        parsed = parse.urlparse(self.path)
        if parsed.path != "/feishu/callback":
            self.send_response(404)
            self.end_headers()
            self.wfile.write("not found".encode("utf-8"))
            return

        qs = parse.parse_qs(parsed.query)
        code = qs.get("code", [None])[0]
        state = qs.get("state", [None])[0]
        error = qs.get("error", [None])[0]

        if error:
            CallbackHandler.result = {"ok": False, "error": error}
            self.send_response(200)
            self.end_headers()
            self.wfile.write("飞书授权被取消或失败，你可以关闭这个页面。".encode("utf-8"))
            CallbackHandler.done_event.set()
            return

        if state != CallbackHandler.state or not code:
            CallbackHandler.result = {"ok": False, "error": "state_mismatch_or_missing_code"}
            self.send_response(400)
            self.end_headers()
            self.wfile.write("授权回调无效，你可以关闭这个页面。".encode("utf-8"))
            CallbackHandler.done_event.set()
            return

        try:
            token_resp = exchange_code_for_token(code)
            CallbackHandler.result = {"ok": True, "token_resp": token_resp}
            self.send_response(200)
            self.end_headers()
            self.wfile.write("飞书授权成功，可以回到聊天继续。".encode("utf-8"))
        except Exception as exc:
            CallbackHandler.result = {"ok": False, "error": str(exc)}
            self.send_response(500)
            self.end_headers()
            self.wfile.write("授权成功，但换取 token 失败，请回到聊天查看。".encode("utf-8"))
        finally:
            CallbackHandler.done_event.set()


def main() -> None:
    state = secrets.token_urlsafe(24)
    done_event = threading.Event()
    CallbackHandler.state = state
    CallbackHandler.done_event = done_event

    server = HTTPServer(("127.0.0.1", 8787), CallbackHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    auth_url = build_auth_url(state)
    print("AUTH_URL=" + auth_url)
    print("等待浏览器授权回调...")

    done_event.wait(timeout=600)
    server.shutdown()
    server.server_close()

    result = CallbackHandler.result or {"ok": False, "error": "timeout"}
    if not result.get("ok"):
        print(json.dumps(result, ensure_ascii=False))
        return

    token_resp = result["token_resp"]
    save_token(token_resp)
    print("AUTH_OK")
    print("TOKEN_SAVED=" + str(TOKEN_PATH))
    print("SCOPES=" + token_resp.get("scope", ""))


if __name__ == "__main__":
    main()
