from typing import Dict, Any
from ..core.tool_exec import run_tool


class ToolSslyze:
    id = "tool.sslyze"

    def run(self, target: str, **kwargs) -> Dict[str, Any]:
        return run_tool(self.id, target, options=kwargs.get("options"))
