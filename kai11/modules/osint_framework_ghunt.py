import os
from typing import Dict, Any
from .base import ModuleBase
from ..agents.agent_osint_ghunt import AgentOsintGhunt
from ..orchestrator.circle import select_circle, lang_studio_enabled


def _allow_network() -> bool:
    return os.getenv("KAI_ALLOW_NETWORK") == "1"


class OsintFrameworkGhunt(ModuleBase):
    id = "osint.framework.ghunt"
    kind = "recon"
    risk = "low"

    def plan(self, context: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "module": self.id,
            "mode": "plan",
            "actions": [self.id],
            "safe_mode": True,
            "circle": "osint",
            "lang_studio": lang_studio_enabled("osint"),
        }

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        if not _allow_network():
            return {"module": self.id, "mode": "execute", "results": [], "findings": [], "note": "network_disabled_set_KAI_ALLOW_NETWORK=1"}
        scope = context.get("scope", {})
        targets = scope.get("allowlist") or []
        circle = select_circle("osint")
        circle["options"] = context.get("options")
        agent = AgentOsintGhunt()
        res = agent.run(targets, circle)
        return {"module": self.id, "mode": "execute", "results": res.get("results", []), "findings": [], "circle": circle}
