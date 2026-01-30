import os
from typing import Dict, Any, List
from .base import ModuleBase
from ..agents.osint_dns_agent import OsintDNSAgent
from ..orchestrator.circle import select_circle, lang_studio_enabled


def _allow_network() -> bool:
    return os.getenv("KAI_ALLOW_NETWORK") == "1"


class OsintDNSModule(ModuleBase):
    id = "osint.dns_lookup"
    kind = "recon"
    risk = "low"

    def plan(self, context: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "module": self.id,
            "mode": "plan",
            "actions": ["dns_lookup"],
            "safe_mode": True,
            "circle": "osint",
            "lang_studio": lang_studio_enabled("osint"),
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
        circle = select_circle("osint")
        circle["options"] = context.get("options")
        agent = OsintDNSAgent()
        res = agent.run(targets, circle)
        return {
            "module": self.id,
            "mode": "execute",
            "results": res.get("results", []),
            "assets": res.get("assets", []),
            "findings": [],
            "circle": circle,
        }
