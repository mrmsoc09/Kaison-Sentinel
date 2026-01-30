import argparse
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
from pathlib import Path

from ..vector.store_factory import get_store
from ..vector.vector_store import VectorStore
from ..core.api_auth import auth_enabled, validate_api_key, header_name
from ..core.api_limits import check_rate_limit
from ..core.rbac import has_permission
from ..core.config import BUILD_ROOT
from .ui_api import handle_assets, handle_plan, handle_execute, handle_add_key, handle_save_playbook, handle_import_playbooks, handle_queue_email, handle_attach_evidence, handle_email_draft, handle_profile_update, handle_email_config_update, handle_setup_update, handle_options_override, handle_execute_async, handle_mitre_plan, handle_mitre_export, handle_program_sync

UI_DIR = BUILD_ROOT / "ui"


class SearchHandler(BaseHTTPRequestHandler):
    store = VectorStore()
    _cache = {}
    _cache_order = []
    _cache_limit = 64

    def _auth_context(self):
        if not auth_enabled():
            return {"status": "disabled"}
        key = self.headers.get(header_name())
        return validate_api_key(key)

    def _ensure_auth(self, perm: str | None = None):
        auth = self._auth_context()
        if auth.get("status") in {"invalid", "missing"}:
            self._send_json(401, {"error": "unauthorized"})
            return None
        if perm and auth.get("status") == "ok":
            role = auth.get("role", "viewer")
            if not has_permission(role, perm):
                self._send_json(403, {"error": "forbidden"})
                return None
        return auth

    def _apply_rate_limit(self, route: str) -> bool:
        client_ip = self.client_address[0] if self.client_address else "unknown"
        res = check_rate_limit(client_ip, route)
        if res.get("status") != "ok":
            self._send_json(429, {"error": "rate_limited"})
            return False
        return True

    def _send_json(self, status: int, payload: dict) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self._send_security_headers()
        self.end_headers()
        self.wfile.write(body)

    def _send_file(self, path: Path, content_type: str) -> None:
        if not path.exists():
            self._send_json(404, {"error": "not_found"})
            return
        body = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self._send_security_headers()
        self.end_headers()
        self.wfile.write(body)

    def _send_security_headers(self) -> None:
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("Permissions-Policy", "geolocation=(), microphone=(), camera=()")
        self.send_header("Content-Security-Policy", "default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; script-src 'self'; object-src 'none'")

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path.startswith("/api/"):
            if not self._apply_rate_limit(parsed.path):
                return
            auth = self._ensure_auth("view")
            if auth is None:
                return
            status, payload = handle_assets(parsed.path, parsed.query)
            return self._send_json(status, payload)
        if parsed.path in ("/", "/index.html"):
            return self._send_file(UI_DIR / "index.html", "text/html; charset=utf-8")
        if parsed.path == "/styles.css":
            return self._send_file(UI_DIR / "styles.css", "text/css; charset=utf-8")
        if parsed.path == "/app.js":
            return self._send_file(UI_DIR / "app.js", "text/javascript; charset=utf-8")
        if parsed.path == "/api.js":
            return self._send_file(UI_DIR / "api.js", "text/javascript; charset=utf-8")
        if parsed.path == "/assets.js":
            return self._send_file(UI_DIR / "assets.js", "text/javascript; charset=utf-8")
        if parsed.path == "/loops.js":
            return self._send_file(UI_DIR / "loops.js", "text/javascript; charset=utf-8")
        if parsed.path == "/playbooks.js":
            return self._send_file(UI_DIR / "playbooks.js", "text/javascript; charset=utf-8")
        if parsed.path == "/wizard.json":
            return self._send_file(UI_DIR / "wizard.json", "application/json; charset=utf-8")
        if parsed.path == "/wizard.js":
            return self._send_file(UI_DIR / "wizard.js", "text/javascript; charset=utf-8")
        if parsed.path == "/graph.js":
            return self._send_file(UI_DIR / "graph.js", "text/javascript; charset=utf-8")
        if parsed.path == "/execute.js":
            return self._send_file(UI_DIR / "execute.js", "text/javascript; charset=utf-8")
        if parsed.path == "/validation.js":
            return self._send_file(UI_DIR / "validation.js", "text/javascript; charset=utf-8")
        if parsed.path == "/email.js":
            return self._send_file(UI_DIR / "email.js", "text/javascript; charset=utf-8")
        if parsed.path == "/email_config.js":
            return self._send_file(UI_DIR / "email_config.js", "text/javascript; charset=utf-8")
        if parsed.path == "/setup.js":
            return self._send_file(UI_DIR / "setup.js", "text/javascript; charset=utf-8")
        if parsed.path == "/options_override.js":
            return self._send_file(UI_DIR / "options_override.js", "text/javascript; charset=utf-8")
        if parsed.path == "/exports.js":
            return self._send_file(UI_DIR / "exports.js", "text/javascript; charset=utf-8")
        if parsed.path == "/run_history.js":
            return self._send_file(UI_DIR / "run_history.js", "text/javascript; charset=utf-8")
        if parsed.path == "/jobs.js":
            return self._send_file(UI_DIR / "jobs.js", "text/javascript; charset=utf-8")
        if parsed.path == "/evidence.js":
            return self._send_file(UI_DIR / "evidence.js", "text/javascript; charset=utf-8")
        if parsed.path == "/mitre.js":
            return self._send_file(UI_DIR / "mitre.js", "text/javascript; charset=utf-8")
        if parsed.path == "/search":
            qs = parse_qs(parsed.query)
            query = (qs.get("q") or [""])[0]
            top_k = int((qs.get("k") or ["5"])[0])
            cache_key = f"{query}:{top_k}"
            if cache_key in self._cache:
                results = self._cache[cache_key]
            else:
                results = self.store.search(query, top_k=top_k)
                self._cache[cache_key] = results
                self._cache_order.append(cache_key)
                if len(self._cache_order) > self._cache_limit:
                    old = self._cache_order.pop(0)
                    self._cache.pop(old, None)
            self._send_json(200, {"query": query, "results": results})
            return
        if parsed.path == "/stats":
            self._send_json(200, {"rows": len(self.store.rows)})
            return
        self._send_json(404, {"error": "not_found"})

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path.startswith("/api/") and not self._apply_rate_limit(parsed.path):
            return
        if parsed.path == "/api/plan":
            auth = self._ensure_auth("plan")
            if auth is None:
                return
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length).decode("utf-8") if length else "{}"
            try:
                payload = json.loads(raw)
            except Exception:
                payload = {}
            if auth.get("status") == "ok":
                scope = payload.get("scope") or {}
                scope["role"] = auth.get("role")
                scope["tenant_id"] = auth.get("tenant_id")
                payload["scope"] = scope
            status, data = handle_plan(payload)
            return self._send_json(status, data)
        if parsed.path == "/api/vault/add":
            auth = self._ensure_auth("approve")
            if auth is None:
                return
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length).decode("utf-8") if length else "{}"
            try:
                payload = json.loads(raw)
            except Exception:
                payload = {}
            status, data = handle_add_key(payload)
            return self._send_json(status, data)
        if parsed.path == "/api/playbooks/add":
            auth = self._ensure_auth("plan")
            if auth is None:
                return
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length).decode("utf-8") if length else "{}"
            try:
                payload = json.loads(raw)
            except Exception:
                payload = {}
            status, data = handle_save_playbook(payload)
            return self._send_json(status, data)
        if parsed.path == "/api/playbooks/import":
            auth = self._ensure_auth("plan")
            if auth is None:
                return
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length).decode("utf-8") if length else "{}"
            try:
                payload = json.loads(raw)
            except Exception:
                payload = {}
            status, data = handle_import_playbooks(payload)
            return self._send_json(status, data)
        if parsed.path == "/api/execute":
            auth = self._ensure_auth("execute")
            if auth is None:
                return
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length).decode("utf-8") if length else "{}"
            try:
                payload = json.loads(raw)
            except Exception:
                payload = {}
            if auth.get("status") == "ok":
                scope = payload.get("scope") or {}
                scope["role"] = auth.get("role")
                scope["tenant_id"] = auth.get("tenant_id")
                payload["scope"] = scope
            status, data = handle_execute(payload)
            return self._send_json(status, data)
        if parsed.path == "/api/execute/async":
            auth = self._ensure_auth("execute")
            if auth is None:
                return
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length).decode("utf-8") if length else "{}"
            try:
                payload = json.loads(raw)
            except Exception:
                payload = {}
            if auth.get("status") == "ok":
                scope = payload.get("scope") or {}
                scope["role"] = auth.get("role")
                scope["tenant_id"] = auth.get("tenant_id")
                payload["scope"] = scope
            status, data = handle_execute_async(payload)
            return self._send_json(status, data)
        if parsed.path == "/api/mitre/plan":
            auth = self._ensure_auth("plan")
            if auth is None:
                return
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length).decode("utf-8") if length else "{}"
            try:
                payload = json.loads(raw)
            except Exception:
                payload = {}
            if auth.get("status") == "ok":
                scope = payload.get("scope") or {}
                scope["role"] = auth.get("role")
                scope["tenant_id"] = auth.get("tenant_id")
                payload["scope"] = scope
            status, data = handle_mitre_plan(payload)
            return self._send_json(status, data)
        if parsed.path == "/api/mitre/export":
            auth = self._ensure_auth("plan")
            if auth is None:
                return
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length).decode("utf-8") if length else "{}"
            try:
                payload = json.loads(raw)
            except Exception:
                payload = {}
            if auth.get("status") == "ok":
                scope = payload.get("scope") or {}
                scope["role"] = auth.get("role")
                scope["tenant_id"] = auth.get("tenant_id")
                payload["scope"] = scope
            status, data = handle_mitre_export(payload)
            return self._send_json(status, data)
        if parsed.path == "/api/notify/email":
            auth = self._ensure_auth("approve")
            if auth is None:
                return
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length).decode("utf-8") if length else "{}"
            try:
                payload = json.loads(raw)
            except Exception:
                payload = {}
            status, data = handle_queue_email(payload)
            return self._send_json(status, data)
        if parsed.path == "/api/email/draft":
            auth = self._ensure_auth("view")
            if auth is None:
                return
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length).decode("utf-8") if length else "{}"
            try:
                payload = json.loads(raw)
            except Exception:
                payload = {}
            status, data = handle_email_draft(payload)
            return self._send_json(status, data)
        if parsed.path == "/api/profile/update":
            auth = self._ensure_auth("view")
            if auth is None:
                return
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length).decode("utf-8") if length else "{}"
            try:
                payload = json.loads(raw)
            except Exception:
                payload = {}
            status, data = handle_profile_update(payload)
            return self._send_json(status, data)
        if parsed.path == "/api/email/config":
            auth = self._ensure_auth("approve")
            if auth is None:
                return
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length).decode("utf-8") if length else "{}"
            try:
                payload = json.loads(raw)
            except Exception:
                payload = {}
            status, data = handle_email_config_update(payload)
            return self._send_json(status, data)
        if parsed.path == "/api/setup/hub":
            auth = self._ensure_auth("plan")
            if auth is None:
                return
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length).decode("utf-8") if length else "{}"
            try:
                payload = json.loads(raw)
            except Exception:
                payload = {}
            status, data = handle_setup_update(payload)
            return self._send_json(status, data)
        if parsed.path == "/api/evidence/attach":
            auth = self._ensure_auth("execute")
            if auth is None:
                return
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length).decode("utf-8") if length else "{}"
            try:
                payload = json.loads(raw)
            except Exception:
                payload = {}
            status, data = handle_attach_evidence(payload)
            return self._send_json(status, data)
        if parsed.path == "/api/options/override":
            auth = self._ensure_auth("plan")
            if auth is None:
                return
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length).decode("utf-8") if length else "{}"
            try:
                payload = json.loads(raw)
            except Exception:
                payload = {}
            status, data = handle_options_override(payload)
            return self._send_json(status, data)
        if parsed.path == "/api/programs/sync":
            auth = self._ensure_auth("plan")
            if auth is None:
                return
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length).decode("utf-8") if length else "{}"
            try:
                payload = json.loads(raw)
            except Exception:
                payload = {}
            status, data = handle_program_sync(payload)
            return self._send_json(status, data)
        self._send_json(404, {"error": "not_found"})


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--index", required=True, help="Path to vector_store.jsonl")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", default=7878, type=int)
    args = parser.parse_args()

    store = get_store(Path(args.index))
    SearchHandler.store = store

    server = HTTPServer((args.host, args.port), SearchHandler)
    print(f"Kaison Sentinel server listening on http://{args.host}:{args.port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
