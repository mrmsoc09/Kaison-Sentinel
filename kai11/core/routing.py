from typing import Dict, Any

from .prompt_manager import select_prompt, select_prompt_by_tag, select_persona
from .agent_routing import select_persona as select_persona_by_rules


def route_for_context(context: Dict[str, Any]) -> Dict[str, Any]:
    module_kind = context.get("module_kind", "osint")
    vertical = context.get("vertical", "general")

    system_prompt = select_prompt("system")
    scan_prompt = select_prompt_by_tag("scan", module_kind if module_kind in {"osint", "vuln"} else "osint")
    report_prompt = select_prompt_by_tag("report", module_kind if module_kind in {"osint", "vuln"} else "osint")

    persona_id = context.get("persona_id") or select_persona_by_rules({"module_kind": module_kind, "vertical": vertical})
    persona = select_persona(persona_id)

    return {
        "system_prompt": system_prompt,
        "scan_prompt": scan_prompt,
        "report_prompt": report_prompt,
        "persona": persona,
        "routing": {
            "module_kind": module_kind,
            "vertical": vertical,
        },
    }
