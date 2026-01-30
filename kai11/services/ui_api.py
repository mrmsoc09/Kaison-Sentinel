import json
from urllib.parse import urlparse, parse_qs

from ..core.registry import (
    load_prompts,
    load_personas,
    load_playbooks,
    load_report_formats,
    load_agents,
    load_personas_praison,
    load_personas_langstudio,
)
from ..core.tool_health import build_health_report
from ..core.options import get_options, save_override
from ..core.vault import list_providers, list_keys, add_key
from ..core.config import OUTPUT_DIR, TRACE_DIR, LANGSTUDIO_DIR, LOOPS_DIR, BUILD_ROOT
from ..core.scan_engine import run_plan, run_execute
from ..core.playbooks import save_playbook, export_playbooks, import_playbooks_json, import_playbooks_csv
from ..core.graph_view import load_latest_graph
from ..core.notifications import queue_email
from ..core.validation import validation_checklist
from ..core.evidence_attach import attach_evidence
from ..core.email_drafter import draft_email
from ..core.user_profile import load_profile, save_profile
from ..core.email_config import load_email_config, save_email_config
from ..core.setup_hub import load_setup_hub, update_setup_step
from ..core.key_catalog import load_key_catalog
from ..core.export_bundle import build_bundle
from ..core.task_queue import list_jobs, enqueue_task
from ..core.programs import list_programs
from ..core.program_sync import program_sync_status
from ..core.hardware import hardware_profile
from ..core.llm_registry import load_llm_profiles
from ..core.run_history import list_runs
from ..core.mitre_planner import list_techniques as list_mitre_techniques, build_mitre_plan, export_mitre_bundle


def handle_assets(path: str, query: str = ""):
    if path == "/api/assets/prompts":
        return 200, load_prompts()
    if path == "/api/assets/personas":
        return 200, load_personas()
    if path == "/api/assets/personas_praison":
        return 200, load_personas_praison()
    if path == "/api/assets/personas_langstudio":
        return 200, load_personas_langstudio()
    if path == "/api/assets/playbooks":
        return 200, load_playbooks()
    if path == "/api/assets/report_formats":
        return 200, load_report_formats()
    if path == "/api/assets/agents":
        return 200, load_agents()
    if path == "/api/options":
        qs = parse_qs(query)
        kind = (qs.get("kind") or ["all"])[0]
        return 200, get_options(kind)
    if path == "/api/options/override":
        return 200, json.loads((BUILD_ROOT / "config" / "options_override.json").read_text())
    if path == "/api/vault/providers":
        return 200, list_providers()
    if path == "/api/vault/keys":
        return 200, list_keys()
    if path == "/api/graph/latest":
        return 200, load_latest_graph()
    if path == "/api/playbooks/export":
        return 200, export_playbooks()
    if path == "/api/validation/checklist":
        return 200, validation_checklist()
    if path == "/api/tools/health":
        p = OUTPUT_DIR / "tool_health.json"
        if p.exists():
            return 200, json.loads(p.read_text())
        return 200, build_health_report(check_version=False)
    if path == "/api/tools/registry":
        p = BUILD_ROOT / "config" / "tool_registry.json"
        if p.exists():
            return 200, json.loads(p.read_text())
        return 200, {"tools": []}
    if path == "/api/tools/osint":
        p = BUILD_ROOT / "config" / "tools_osint.json"
        if p.exists():
            return 200, json.loads(p.read_text())
        return 200, {"tools": []}
    if path == "/api/tools/vuln":
        p = BUILD_ROOT / "config" / "tools_vuln.json"
        if p.exists():
            return 200, json.loads(p.read_text())
        return 200, {"tools": []}
    if path == "/api/tools/substitutes":
        p = BUILD_ROOT / "config" / "tool_substitutes.json"
        if p.exists():
            return 200, json.loads(p.read_text())
        return 200, {"tools": []}
    if path == "/api/outputs/traces":
        items = sorted(TRACE_DIR.glob("trace_*.json"), reverse=True)[:25]
        return 200, [str(p) for p in items]
    if path == "/api/outputs/evals":
        items = sorted(LANGSTUDIO_DIR.glob("eval_*.json"), reverse=True)[:25]
        return 200, [str(p) for p in items]
    if path == "/api/outputs/bigquery":
        qs = parse_qs(query)
        run_id = (qs.get("run_id") or [""])[0]
        bq_dir = OUTPUT_DIR / "bigquery"
        if run_id:
            items = sorted(bq_dir.glob(f"{run_id}_*.jsonl"))
            return 200, [str(p) for p in items]
        items = sorted(bq_dir.glob("*.jsonl"), reverse=True)[:25]
        return 200, [str(p) for p in items]
    if path == "/api/outputs/loops":
        qs = parse_qs(query)
        run_id = (qs.get("run_id") or [""])[0]
        if run_id:
            items = sorted(LOOPS_DIR.glob(f"{run_id}_loops.json"))
            return 200, [str(p) for p in items]
        items = sorted(LOOPS_DIR.glob("*_loops.json"), reverse=True)[:25]
        return 200, [str(p) for p in items]
    if path == "/api/loops/state":
        qs = parse_qs(query)
        run_id = (qs.get("run_id") or [""])[0]
        if run_id:
            p = LOOPS_DIR / f"{run_id}_loops.json"
            if p.exists():
                return 200, json.loads(p.read_text())
            return 404, {"error": "loop_state_not_found"}
        items = sorted(LOOPS_DIR.glob("*_loops.json"), key=lambda x: x.stat().st_mtime, reverse=True)
        if not items:
            return 200, {"status": "empty"}
        return 200, json.loads(items[0].read_text())
    if path == "/api/profile":
        return 200, load_profile()
    if path == "/api/email/config":
        return 200, load_email_config()
    if path == "/api/runs/history":
        qs = parse_qs(query)
        limit = int((qs.get("limit") or ["25"])[0])
        return 200, list_runs(limit=limit)
    if path == "/api/programs/list":
        return 200, {"programs": list_programs()}
    if path == "/api/programs/sync/status":
        return 200, program_sync_status()
    if path == "/api/hardware":
        return 200, hardware_profile()
    if path == "/api/llm/providers":
        return 200, load_llm_profiles()
    if path == "/api/jobs":
        return 200, list_jobs()
    if path == "/api/exports/bundle":
        qs = parse_qs(query)
        run_id = (qs.get("run_id") or [""])[0]
        if not run_id:
            return 400, {"error": "run_id_required"}
        return 200, build_bundle(run_id)
    if path == "/api/setup/hub":
        return 200, load_setup_hub()
    if path == "/api/keys/catalog":
        return 200, load_key_catalog()
    if path == "/api/mitre/techniques":
        return 200, list_mitre_techniques()
    return 404, {"error": "not_found"}


def handle_plan(payload: dict):
    scope = payload.get("scope") or {}
    if "allowlist" not in scope:
        scope["allowlist"] = payload.get("allowlist") or []
    return 200, run_plan(scope)


def handle_execute(payload: dict):
    scope = payload.get("scope") or {}
    if "allowlist" not in scope:
        scope["allowlist"] = payload.get("allowlist") or []
    approved = bool(payload.get("approve"))
    tier = payload.get("mitigation_tier") or "standard"
    return 200, run_execute(scope, approved=approved, mitigation_tier=tier)


def handle_add_key(payload: dict):
    source_id = payload.get("source_id")
    key_value = payload.get("key")
    if not source_id or not key_value:
        return 400, {"error": "source_id_and_key_required"}
    return 200, add_key(source_id, key_value)


def handle_save_playbook(payload: dict):
    return 200, save_playbook(payload)


def handle_import_playbooks(payload: dict):
    data = payload.get("data", "")
    fmt = payload.get("format", "json")
    if fmt == "csv":
        return 200, import_playbooks_csv(data)
    return 200, import_playbooks_json(data)


def handle_queue_email(payload: dict):
    return 200, queue_email(payload)


def handle_email_draft(payload: dict):
    return 200, draft_email(payload)


def handle_profile_update(payload: dict):
    return 200, save_profile(payload)


def handle_email_config_update(payload: dict):
    return 200, save_email_config(payload)


def handle_setup_update(payload: dict):
    step_id = payload.get("step_id")
    status = payload.get("status") or "todo"
    if not step_id:
        return 400, {"error": "step_id_required"}
    return 200, update_setup_step(step_id, status)


def handle_attach_evidence(payload: dict):
    run_id = payload.get("run_id")
    finding_id = payload.get("finding_id")
    kind = payload.get("kind") or "screenshot"
    path = payload.get("path")
    if not run_id or not finding_id or not path:
        return 400, {"error": "run_id_finding_id_path_required"}
    return 200, attach_evidence(run_id, finding_id, kind, path)


def handle_options_override(payload: dict):
    return 200, save_override(payload or {})


def handle_execute_async(payload: dict):
    scope = payload.get("scope") or {}
    if "allowlist" not in scope:
        scope["allowlist"] = payload.get("allowlist") or []
    task = {
        "mode": "execute",
        "scope": scope,
        "approve": bool(payload.get("approve")),
        "tier": payload.get("mitigation_tier") or "standard",
    }
    return 202, enqueue_task(task)


def handle_program_sync(payload: dict):
    task = {
        "mode": "program_sync",
        "force": bool(payload.get("force")),
    }
    return 202, enqueue_task(task)


def handle_mitre_plan(payload: dict):
    technique_id = payload.get("technique_id")
    if not technique_id:
        return 400, {"error": "technique_id_required"}
    scope = payload.get("scope") or {}
    hil = bool(payload.get("hil_approved"))
    return 200, build_mitre_plan(technique_id, scope=scope, hil_approved=hil)


def handle_mitre_export(payload: dict):
    technique_id = payload.get("technique_id")
    if not technique_id:
        return 400, {"error": "technique_id_required"}
    scope = payload.get("scope") or {}
    hil = bool(payload.get("hil_approved"))
    return 200, export_mitre_bundle(technique_id, scope=scope, hil_approved=hil)
