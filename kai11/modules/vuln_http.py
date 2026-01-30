import os
import urllib.request
import urllib.error
from typing import Dict, Any, List
from .base import ModuleBase

SEC_HEADERS = {
    "strict-transport-security": "Missing HSTS (Strict-Transport-Security)",
    "content-security-policy": "Missing Content-Security-Policy",
    "x-frame-options": "Missing X-Frame-Options",
    "x-content-type-options": "Missing X-Content-Type-Options",
    "referrer-policy": "Missing Referrer-Policy",
    "permissions-policy": "Missing Permissions-Policy",
}


def _allow_network() -> bool:
    return os.getenv("KAI_ALLOW_NETWORK") == "1"


def _as_url(target: str) -> List[str]:
    if target.startswith("http://") or target.startswith("https://"):
        return [target]
    return [f"https://{target}", f"http://{target}"]


def _probe(url: str) -> Dict[str, Any]:
    try:
        req = urllib.request.Request(url, method="HEAD")
        with urllib.request.urlopen(req, timeout=10) as resp:
            headers = {k.lower(): v for k, v in resp.headers.items()}
            return {
                "url": url,
                "status": resp.status,
                "headers": headers,
            }
    except urllib.error.HTTPError as e:
        return {"url": url, "status": e.code, "headers": {k.lower(): v for k, v in e.headers.items()}}
    except Exception as e:
        return {"url": url, "error": str(e)}


class VulnScanModule(ModuleBase):
    id = "vuln.scan"
    kind = "vuln"
    risk = "medium"

    def plan(self, context: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "module": self.id,
            "mode": "plan",
            "actions": ["http_head_probe", "header_misconfig_checks"],
            "safe_mode": True,
        }

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        if not _allow_network():
            return {
                "module": self.id,
                "mode": "execute",
                "results": [],
                "findings": [],
                "note": "network_disabled_set_KAI_ALLOW_NETWORK=1",
            }

        scope = context.get("scope", {})
        targets = scope.get("allowlist") or []
        assets = context.get("assets") or []
        targets = list(dict.fromkeys(targets + assets))

        results: List[Dict[str, Any]] = []
        findings: List[Dict[str, Any]] = []

        for t in targets:
            for url in _as_url(t):
                res = _probe(url)
                results.append(res)
                headers = res.get("headers", {})
                if not headers:
                    continue
                for key, title in SEC_HEADERS.items():
                    if key not in headers:
                        findings.append({
                            "title": title,
                            "severity": "low",
                            "confidence": 0.6,
                            "target": url,
                            "evidence": [{"kind": "headers", "path": "inline"}],
                            "status": "signal",
                        })

        return {
            "module": self.id,
            "mode": "execute",
            "results": results,
            "findings": findings,
            "note": "http_header_checks_complete",
        }
