#!/usr/bin/env python3
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from kai11.core.options import get_options
from kai11.core.tool_health import build_health_report
from kai11.core.playbooks import export_playbooks
from kai11.core.registry import load_report_formats
from kai11.core.scan_engine import run_plan


def main() -> None:
    report = {"checks": []}

    # options
    report["checks"].append({"name": "options_osint", "ok": bool(get_options("osint"))})
    report["checks"].append({"name": "options_vuln", "ok": bool(get_options("vuln"))})

    # tool health
    health = build_health_report(check_version=False)
    report["checks"].append({"name": "tool_health", "ok": isinstance(health, dict), "missing": health.get("missing")})

    # playbooks
    report["checks"].append({"name": "playbooks", "ok": len(export_playbooks().get("playbooks", [])) >= 1})

    # report formats
    report["checks"].append({"name": "report_formats", "ok": len(load_report_formats()) >= 1})

    # plan
    plan = run_plan({"allowlist": ["example.com"], "module_kind": "osint"})
    report["checks"].append({"name": "plan", "ok": "plan" in plan})

    # vuln plan
    vuln_plan = run_plan({"allowlist": ["example.com"], "module_kind": "vuln"})
    report["checks"].append({"name": "plan_vuln", "ok": "plan" in vuln_plan})

    path = ROOT / "outputs" / "mvp_check.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2))
    print(json.dumps({"status": "ok", "path": str(path)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
