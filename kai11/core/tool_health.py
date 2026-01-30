import json
import shutil
import subprocess
import time
from pathlib import Path
from typing import Dict, Any, List

from .config import BUILD_ROOT, OUTPUT_DIR

CONF_OSINT = BUILD_ROOT / "config" / "tools_osint.json"
CONF_VULN = BUILD_ROOT / "config" / "tools_vuln.json"
SUBS = BUILD_ROOT / "config" / "tool_substitutes.json"


def _load_tools() -> List[Dict[str, Any]]:
    tools: List[Dict[str, Any]] = []
    for conf in [CONF_OSINT, CONF_VULN]:
        if not conf.exists():
            continue
        try:
            data = json.loads(conf.read_text())
            tools.extend(data.get("tools", []))
        except Exception:
            continue
    return tools


def _load_substitutes() -> Dict[str, Any]:
    if not SUBS.exists():
        return {}
    try:
        return json.loads(SUBS.read_text())
    except Exception:
        return {}


def _tool_version(binary: str) -> str:
    try:
        result = subprocess.run([binary, "--version"], capture_output=True, text=True, timeout=5)
        out = (result.stdout or result.stderr).strip()
        return out.splitlines()[0] if out else "unknown"
    except Exception:
        return "unknown"


def build_health_report(check_version: bool = False) -> Dict[str, Any]:
    tools = _load_tools()
    subs = _load_substitutes()
    report = {"generated_at": time.time(), "total": len(tools), "missing": 0, "tools": []}
    for t in tools:
        tool_id = t.get("tool_id")
        binary = t.get("binary")
        status = "missing_binary"
        version = ""
        if binary and shutil.which(binary):
            status = "ok"
            if check_version:
                version = _tool_version(binary)
        else:
            report["missing"] += 1
        meta = subs.get(tool_id, {}) if tool_id else {}
        report["tools"].append({
            "tool_id": tool_id,
            "module_id": t.get("module_id"),
            "binary": binary,
            "status": status,
            "version": version,
            "active": bool(t.get("active", False)),
            "substitutes": meta.get("substitutes", []),
            "install_hint": meta.get("install_hint", ""),
        })
    return report


def write_health_report(check_version: bool = False) -> str:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    report = build_health_report(check_version=check_version)
    path = OUTPUT_DIR / "tool_health.json"
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2))
    return str(path)
