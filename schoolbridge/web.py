import asyncio
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import os
from schoolbridge import assistant, server, store

HOST = "127.0.0.1"
PORT = int(os.getenv("SCHOOLBRIDGE_WEB_PORT", "8765"))
PAGE = Path(__file__).resolve().parent / "static" / "index.html"
ALLOWED_HOSTS = {f"127.0.0.1:{PORT}", f"localhost:{PORT}"}
MAX_BODY = 20_000


def state() -> dict:
    return {
        "language": store.get_setting("language", "en"),
        "children": store.list_children(),
        "actions": store.list_actions(only_open=False),
    }


class Handler(BaseHTTPRequestHandler):
    def _send(self, code: int, body: bytes, ctype: str = "application/json; charset=utf-8") -> None:
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def _json(self, code: int, data: dict) -> None:
        self._send(code, json.dumps(data, ensure_ascii=False).encode("utf-8"))

    def _host_ok(self) -> bool:
        return self.headers.get("Host", "") in ALLOWED_HOSTS  # защита от DNS rebinding

    def do_GET(self) -> None:
        if not self._host_ok():
            return self._json(403, {"error": "forbidden"})
        if self.path in ("/", "/index.html"):
            return self._send(200, PAGE.read_bytes(), "text/html; charset=utf-8")
        if self.path == "/api/state":
            return self._json(200, state())
        self._json(404, {"error": "not found"})

    def do_POST(self) -> None:
        if not self._host_ok():
            return self._json(403, {"error": "forbidden"})
        if self.headers.get("Content-Type", "").split(";")[0].strip() != "application/json":
            return self._json(415, {"error": "JSON only"})
        length = int(self.headers.get("Content-Length") or 0)
        if length <= 0 or length > MAX_BODY:
            return self._json(413, {"error": "bad size"})
        try:
            data = json.loads(self.rfile.read(length))
            if not isinstance(data, dict):
                raise ValueError
        except ValueError:
            return self._json(400, {"error": "bad json"})

        if self.path == "/api/say":
            out = asyncio.run(assistant.handle(str(data.get("text", ""))))
        elif self.path == "/api/notice":
            out = asyncio.run(assistant.handle_notice(str(data.get("text", "")), str(data.get("child", ""))))
        elif self.path == "/api/language":
            out = asyncio.run(server.set_language(language=str(data.get("language", ""))))
        elif self.path == "/api/done":
            try:
                action_id = int(data.get("id"))
            except (TypeError, ValueError):
                return self._json(400, {"error": "bad id"})
            out = asyncio.run(server.complete_action(action_id=action_id))
        else:
            return self._json(404, {"error": "not found"})
        self._json(200, out)

    def log_message(self, *args) -> None:
        pass


if __name__ == "__main__":
    print(f"School Bridge demo: http://{HOST}:{PORT}  (Ctrl+C to stop)")
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()