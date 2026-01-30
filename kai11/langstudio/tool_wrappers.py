from typing import Dict, Any

from ..core.tool_exec import run_tool


def run_tool_wrapped(tool_id: str, target: str, options: Dict[str, Any]) -> Dict[str, Any]:
    # Thin wrapper to tag runs for LangStudio tracing/metadata
    result = run_tool(tool_id, target, options)
    result.setdefault("langstudio", {})
    result["langstudio"].update({"wrapped": True})
    return result
