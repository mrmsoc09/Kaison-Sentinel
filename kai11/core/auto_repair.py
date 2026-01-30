import os
import subprocess
from typing import Dict, Any, List

from .config import BUILD_ROOT
from .tool_health import build_health_report
from .program_sync import sync_program_scopes, program_sync_status
from .scope_parser import parse_cached_scopes, load_parsed_scopes
from .options import get_options


def _allow_install(options: Dict[str, Any]) -> bool:
    return bool(options.get("allow_install") or os.getenv("KAI_ALLOW_INSTALL") == "1")


def _install_scripts_for_missing(missing_tools: List[Dict[str, Any]], options: Dict[str, Any]) -> List[Dict[str, Any]]:
    if not missing_tools or not _allow_install(options):
        return []
    has_osint = any((t.get("module_id") or "").startswith("osint") for t in missing_tools)
    has_vuln = any((t.get("module_id") or "").startswith("vuln") for t in missing_tools)
    results = []
    if has_osint:
        script = BUILD_ROOT / "scripts" / "install_osint_core.sh"
        if script.exists():
            try:
                subprocess.run(["bash", str(script)], check=True)
                results.append({"script": str(script), "status": "ok"})
            except Exception as exc:  # noqa: BLE001
                results.append({"script": str(script), "status": "error", "reason": str(exc)})
    if has_vuln:
        script = BUILD_ROOT / "scripts" / "install_vuln_core.sh"
        if script.exists():
            try:
                subprocess.run(["bash", str(script)], check=True)
                results.append({"script": str(script), "status": "ok"})
            except Exception as exc:  # noqa: BLE001
                results.append({"script": str(script), "status": "error", "reason": str(exc)})
    return results


def run_auto_repair() -> Dict[str, Any]:
    options = get_options("all")
    health = build_health_report(check_version=False)
    missing_tools = [t for t in health.get("tools", []) if t.get("status") != "ok"]

    install_results = _install_scripts_for_missing(missing_tools, options)

    program_state = program_sync_status()
    sync_result = None
    if options.get("program_sync", {}).get("enabled"):
        if os.getenv("KAI_ALLOW_NETWORK") == "1":
            if program_state.get("status") in {"never", "error", "blocked"}:
                sync_result = sync_program_scopes(force=True)

    parsed = load_parsed_scopes()
    parse_result = None
    if parsed.get("status") in {"missing", "error"}:
        parse_result = parse_cached_scopes()

    return {
        "missing_tools": len(missing_tools),
        "install_results": install_results,
        "program_sync": sync_result or program_state,
        "scope_parse": parse_result or parsed,
    }
