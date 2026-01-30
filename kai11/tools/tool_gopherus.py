from typing import Dict, Any
from ..core.tool_exec import run_tool


class ToolGopherus:
    id = "tool.gopherus"

    def run(self, target: str, **kwargs) -> Dict[str, Any]:
        return run_tool(self.id, target, options=kwargs.get("options"))
