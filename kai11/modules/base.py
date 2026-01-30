from typing import Dict, Any


class ModuleBase:
    id = "module.base"
    kind = "generic"
    risk = "low"

    def plan(self, context: Dict[str, Any]) -> Dict[str, Any]:
        return {"module": self.id, "mode": "plan", "actions": []}

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        return {"module": self.id, "mode": "execute", "results": []}

    def parse(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        return {"module": self.id, "parsed": raw}

    def normalize(self, parsed: Dict[str, Any]) -> Dict[str, Any]:
        return {"module": self.id, "normalized": parsed}
