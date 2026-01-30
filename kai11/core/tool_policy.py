from typing import Dict, Any


def tool_allowed(tool_category: str, options: Dict[str, Any]) -> bool:
    allow = options.get("tool_categories_allowlist")
    if not allow:
        return True
    return tool_category in set(allow)
