import os
import socket
from typing import Dict, Any, List
from .base import ModuleBase


def _allow_network() -> bool:
    return os.getenv("KAI_ALLOW_NETWORK") == "1"


def _resolve_target(t: str) -> Dict[str, Any]:
    try:
        host, aliases, ips = socket.gethostbyname_ex(t)
        return {"target": t, "host": host, "aliases": aliases, "ips": ips}
    except Exception as e:
        return {"target": t, "error": str(e), "ips": []}


class OsintReconModule(ModuleBase):
    id = "osint.recon"
    kind = "recon"
    risk = "low"

    def plan(self, context: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "module": self.id,
            "mode": "plan",
            "actions": ["dns_lookup", "asset_inventory"],
            "safe_mode": True,
        }

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        if not _allow_network():
            return {
                "module": self.id,
                "mode": "execute",
                "results": [],
                "assets": [],
                "findings": [],
                "note": "network_disabled_set_KAI_ALLOW_NETWORK=1",
            }

        scope = context.get("scope", {})
        targets = scope.get("allowlist") or []
        results: List[Dict[str, Any]] = []
        assets: List[str] = []

        for t in targets:
            res = _resolve_target(t)
            results.append(res)
            for ip in res.get("ips", []):
                assets.append(ip)

        return {
            "module": self.id,
            "mode": "execute",
            "results": results,
            "assets": sorted(set(assets)),
            "findings": [],
            "note": "dns_resolution_complete",
        }
