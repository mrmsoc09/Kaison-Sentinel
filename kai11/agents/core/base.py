import json
from pathlib import Path
from typing import Dict, Any

from ...core.config import BUILD_ROOT
from ...core.audit import append_audit
from ...core.prompt_manager import render_prompt, select_prompt
from ...core.registry import load_personas


class AgentBase:
    id = "agent.base"

    def __init__(self):
        self.config = self._load_config()
        self.persona = self._load_persona()
        self.prompt = self._load_prompt()

    def _load_config(self) -> Dict[str, Any]:
        path = BUILD_ROOT / "config" / "agents" / f"{self.id.replace('.', '_')}.json"
        if path.exists():
            return json.loads(path.read_text())
        return {"id": self.id}

    def _load_prompt(self) -> Dict[str, Any]:
        pid = self.config.get("prompt_id")
        if pid:
            return select_prompt("system", prompt_id=pid)
        return select_prompt("system")

    def _load_persona(self) -> Dict[str, Any]:
        pid = self.config.get("persona_id")
        for p in load_personas():
            if p.get("id") == pid:
                return p
        return {"id": "none"}

    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        append_audit({"event": "agent_run", "agent": self.id, "context": context})
        prompt = render_prompt(self.prompt, {
            "goal": context.get("goal", ""),
            "scope": str(context.get("scope", {})),
            "mode": context.get("mode", "plan"),
            "modules": ",".join(context.get("modules", [])),
            "constraints": context.get("constraints", ""),
        })
        return {
            "agent": self.id,
            "persona": self.persona,
            "prompt": prompt,
            "context": context,
        }
