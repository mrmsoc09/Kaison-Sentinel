import json
from pathlib import Path
from typing import Dict, Any

from .config import OUTPUT_DIR, BUILD_ROOT
from .mitre_reports import render_mitre_bundle


def _load_mapper():
    import importlib.util

    mapper_path = BUILD_ROOT / "planner" / "mitre_mapper.py"
    spec = importlib.util.spec_from_file_location("planner.mitre_mapper", mapper_path)
    if not spec or not spec.loader:
        raise RuntimeError("mitre_mapper_not_found")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[attr-defined]
    return module


def list_techniques() -> Dict[str, Any]:
    mapper = _load_mapper()
    return {"techniques": mapper.list_techniques()}


def build_mitre_plan(technique_id: str, scope: Dict[str, Any] | None = None, hil_approved: bool = False) -> Dict[str, Any]:
    mapper = _load_mapper()
    plan = mapper.build_plan(technique_id, scope=scope or {}, hil_approved=hil_approved)
    out_dir = OUTPUT_DIR / "mitre"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{technique_id.replace('.', '_')}_plan.json"
    out_path.write_text(json.dumps(plan, ensure_ascii=False, indent=2))
    plan["output_path"] = str(out_path)
    return plan


def export_mitre_bundle(technique_id: str, scope: Dict[str, Any] | None = None, hil_approved: bool = False) -> Dict[str, Any]:
    plan = build_mitre_plan(technique_id, scope=scope, hil_approved=hil_approved)
    if plan.get("status") != "ok":
        return plan
    bundle = render_mitre_bundle(plan)
    plan["report_bundle"] = bundle.get("report_bundle", {})
    plan["report_templates"] = bundle.get("report_templates", [])
    return plan
