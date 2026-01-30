from typing import Dict, Any, List

from .tool_health import build_health_report
from .program_sync import program_sync_status
from .vault import list_keys
from .key_catalog import load_key_catalog


def _required_keys() -> List[str]:
    catalog = load_key_catalog().get("catalog", [])
    required = []
    for item in catalog:
        if item.get("required"):
            required.append(item.get("vault_source_id"))
    return [k for k in required if k]


def autonomy_insights(options: Dict[str, Any]) -> Dict[str, Any]:
    health = build_health_report(check_version=False)
    missing_tools = health.get("missing", [])
    required_keys = _required_keys()
    existing_keys = list_keys()
    missing_keys = [k for k in required_keys if k not in existing_keys]
    program_state = program_sync_status()

    actions = []
    if missing_tools:
        actions.append("install_tools")
    if missing_keys:
        actions.append("vault_add_keys")
    if program_state.get("status") in {"never", "error", "blocked"}:
        actions.append("sync_program_scopes")

    return {
        "missing_tools": missing_tools,
        "missing_required_keys": missing_keys,
        "program_sync": program_state,
        "recommended_actions": actions,
    }
