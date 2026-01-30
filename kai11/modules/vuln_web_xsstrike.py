import os
from typing import Dict, Any
from .base import ModuleBase
from ..agents.agent_vuln_xsstrike import AgentVulnXsstrike
from ..orchestrator.circle import select_circle, lang_studio_enabled



def _allow_network() -> bool:
    return os.getenv("KAI_ALLOW_NETWORK") == "1"


class VulnWebXsstrike(ModuleBase):
    id = "vuln.web.xsstrike"
    kind = "vuln"
    risk = "medium"

    def plan(self, context: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "module": self.id,
            "mode": "plan",
            "actions": [self.id],
            "safe_mode": True,
            "circle": "vuln",
            "lang_studio": lang_studio_enabled("vuln"),
        }

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        if not _allow_network():
            return {"module": self.id, "mode": "execute", "results": [], "findings": [], "note": "network_disabled_set_KAI_ALLOW_NETWORK=1"}
        scope = context.get("scope", {})
        targets = scope.get("allowlist") or []
        circle = select_circle("vuln")
        circle["options"] = context.get("options")
        agent = AgentVulnXsstrike()
        res = agent.run(targets, circle)
        return {"module": self.id, "mode": "execute", "results": res.get("results", []), "findings": [], "circle": circle}
