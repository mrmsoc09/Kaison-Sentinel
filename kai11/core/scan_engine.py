from typing import Dict, Any, List
import os
from datetime import datetime
from .contracts import RunRecord, Approval
from .config import OUTPUT_DIR
from .policy import should_require_hil, enforce_scope
from .module_registry import list_modules, load_module
from .evidence import write_evidence_bundle
from .mitigation import generate_mitigation
from .findings import normalize_findings, dedupe_findings, score_confidence, apply_signal_threshold
from .duplicate_risk import apply_duplicate_risk
from .report import render_report, render_report_with_format, render_report_bundle
from .report_formatter import format_report
from .storage import write_run, write_report
from .audit import append_audit
from .bus import EventBus
from .normalize import normalize_artifacts
from .router import route_artifact
from .policy_engine import allowed as policy_allowed
from ..langstudio import run_flow
from ..langstudio.evals import evaluate_findings
from ..orchestrator.circle import lang_studio_enabled
from .routing import route_for_context
from .prompt_manager import render_prompt
from .correlation import correlate_artifacts, chain_signals
from .evidence_policy import enforce_screen_recording, enforce_evidence_required
from .report_preflight import report_preflight
from .redact import write_redaction_summary
from ..orchestrator.agent_runner import run_orchestration
from .options import get_options
from .reportability import score_reportability
from .retention import apply_retention
from .run_store_pg import store_run_metadata
from .webhooks import post_webhook
from .report_context import build_report_context
from .scan_planner import build_scan_plan
from .autonomy import autonomy_insights
from .validation import validation_checklist
from .graph_builder import write_graph
from .vuln_findings import normalize_vuln_result
from .intelligence_lifecycle import label_findings
from .guardrails import apply_guardrails
from .bigquery_export import export_bigquery_payload
from ..integrations.bigquery_loader import load_to_bigquery
from .training import TRAIN_PATH
from .playbooks import resolve_playbook_modules
from .alerts import maybe_alert, maybe_hil_alert
from .loop_state import build_loop_state, write_loop_state
from .repro_steps import build_repro_steps


def _new_run_id() -> str:
    return datetime.utcnow().strftime("run-%Y%m%d-%H%M%S")


def _effective_kind(module_ids: List[str] | None, requested: str) -> str:
    if not module_ids:
        return requested
    modules = list_modules("all")
    id_to_kind = {m.get("id"): m.get("kind") for m in modules}
    kinds = {id_to_kind.get(mid) for mid in module_ids if id_to_kind.get(mid)}
    if not kinds:
        return requested
    if kinds.issubset({"osint", "recon"}):
        return "osint"
    if kinds == {"vuln"}:
        return "vuln"
    return "all"


def plan_scan(scope: Dict[str, Any], mode: str = "plan", module_kind: str = "all", module_ids: List[str] | None = None) -> RunRecord:
    if not enforce_scope(scope):
        raise ValueError("scope_allowlist_required")
    role = scope.get("role") or "operator"
    if not policy_allowed(role, "plan", module_kind, "low"):
        raise ValueError("policy_denied_plan")
    approvals = Approval(required=should_require_hil(mode, "medium"), approved=False)
    modules = module_ids or [m["id"] for m in list_modules(module_kind)]
    plan = {"modules": modules, "mode": mode, "module_kind": module_kind}
    return RunRecord(run_id=_new_run_id(), mode=mode, scope=scope, plan=plan, approvals=approvals)


def run_plan(scope: Dict[str, Any]) -> Dict[str, Any]:
    module_kind = scope.get("module_kind", "all")
    options = get_options(module_kind)
    routing = route_for_context(scope)
    scan_prompt = render_prompt(routing["scan_prompt"], {
        "goal": scope.get("goal", ""),
        "scope": str(scope.get("allowlist", [])),
        "mode": "plan",
        "modules": ",".join([m["id"] for m in list_modules(module_kind)]),
        "constraints": scope.get("constraints", "plan-first"),
    })
    module_ids = None
    playbook_ids = scope.get("playbook_ids") or []
    resolved = resolve_playbook_modules(playbook_ids)
    if resolved.get("modules"):
        module_ids = resolved["modules"]
    module_kind_effective = _effective_kind(module_ids, module_kind)
    options = get_options(module_kind_effective)
    record = plan_scan(scope, mode="plan", module_kind=module_kind_effective, module_ids=module_ids)
    module_plans: List[Dict[str, Any]] = []
    modules = list_modules("all") if module_ids else list_modules(module_kind)
    if module_ids:
        modules = [m for m in modules if m.get("id") in set(module_ids)]
    for m in modules:
        inst = load_module(m["entry"])
        module_plans.append(inst.plan({"scope": scope}))
    record.plan["module_plans"] = module_plans
    record.plan["options"] = options
    if playbook_ids:
        record.plan["playbook_ids"] = playbook_ids
        if resolved.get("missing"):
            record.plan["playbook_missing"] = resolved.get("missing")
    scan_plan = build_scan_plan(scope, options, record.run_id)
    record.plan.update(scan_plan)
    record.plan["autonomy"] = autonomy_insights(options)
    evidence_path = write_evidence_bundle(record.run_id, module_plans)
    append_audit({"event": "plan", "run_id": record.run_id, "modules": record.plan["modules"]})
    orchestration = run_orchestration({
        "module_kind": module_kind,
        "goal": scope.get("goal", ""),
        "constraints": scope.get("constraints", ""),
        "scope": scope,
        "modules": record.plan["modules"],
        "mode": "plan",
    })
    return {
        "run_id": record.run_id,
        "mode": record.mode,
        "plan": record.plan,
        "routing": routing,
        "scan_prompt": scan_prompt,
        "orchestration": orchestration,
        "options": options,
        "scan_profile": scan_plan.get("scan_profile"),
        "scan_pool": scan_plan.get("scan_pool"),
        "autonomy": record.plan.get("autonomy"),
        "evidence_bundle": evidence_path,
    }


def run_execute(scope: Dict[str, Any], approved: bool = False, mitigation_tier: str = "standard") -> Dict[str, Any]:
    module_kind = scope.get("module_kind", "all")
    options = get_options(module_kind)
    role = scope.get("role") or "operator"
    if scope.get("validation_confirmed") and not scope.get("validation_confirmed_at"):
        scope["validation_confirmed_at"] = __import__("datetime").datetime.utcnow().isoformat()
    if scope.get("report_hil_confirmed") and not scope.get("report_hil_confirmed_at"):
        scope["report_hil_confirmed_at"] = __import__("datetime").datetime.utcnow().isoformat()
    module_ids = None
    playbook_ids = scope.get("playbook_ids") or []
    resolved = resolve_playbook_modules(playbook_ids)
    if resolved.get("modules"):
        module_ids = resolved["modules"]
    module_kind_effective = _effective_kind(module_ids, module_kind)
    options = get_options(module_kind_effective)
    record = plan_scan(scope, mode="execute", module_kind=module_kind_effective, module_ids=module_ids)
    record.approvals.approved = approved
    if record.approvals.required and not approved:
        append_audit({"event": "blocked", "run_id": record.run_id, "reason": "hil_required"})
        return {"status": "blocked", "reason": "hil_required", "run_id": record.run_id}

    target = (scope.get("allowlist") or [""])[0]
    raw_findings: List[Dict[str, Any]] = []
    module_exec: List[Dict[str, Any]] = []
    policy_denials: List[Dict[str, Any]] = []
    assets: List[str] = []
    all_artifacts: List[Dict[str, Any]] = []
    bus = EventBus()
    bus.subscribe("artifact", route_artifact)

    modules = list_modules("all") if module_ids else list_modules(module_kind)
    if module_ids:
        modules = [m for m in modules if m.get("id") in set(module_ids)]
    for m in modules:
        kind = m.get("kind", "unknown")
        if kind == "recon":
            kind = "osint"
        if not policy_allowed(role, "execute", kind, m.get("risk", "low")):
            append_audit({"event": "blocked", "run_id": record.run_id, "module": m.get("id"), "reason": "policy_denied"})
            policy_denials.append({"module": m.get("id"), "reason": "policy_denied"})
            module_exec.append({"module": m.get("id"), "mode": "execute", "results": [], "findings": [], "note": "policy_denied"})
            continue
        inst = load_module(m["entry"])
        out = inst.execute({"scope": scope, "assets": assets, "options": options})
        module_exec.append(out)
        raw_findings.extend(out.get("findings", []))
        assets.extend(out.get("assets", []))

        # Normalize and route artifacts from tool outputs if present
        module_artifacts = []
        for r in out.get("results", []) or []:
            tool_id = r.get("tool")
            parsed = r.get("parsed")
            output_kind = r.get("output_kind") or "items"
            for art in normalize_artifacts(out.get("module", m["id"]), tool_id, output_kind, parsed, target, record.run_id):
                bus.publish("artifact", art)
                module_artifacts.append(art)
                all_artifacts.append(art)
            if module_kind == "vuln":
                v = normalize_vuln_result(r)
                if v:
                    raw_findings.extend(v)

        if lang_studio_enabled(kind if kind != "recon" else "osint") and module_artifacts:
            out["flow"] = run_flow(kind if kind != "recon" else "osint", out.get("module", m["id"]), module_artifacts)

    raw_findings.extend(correlate_artifacts(all_artifacts))
    raw_findings.extend(chain_signals(all_artifacts))
    findings = normalize_findings(raw_findings, target)
    findings = dedupe_findings(findings)
    findings = score_confidence(findings)
    findings = apply_signal_threshold(findings)
    findings = enforce_screen_recording(findings, scope)
    findings = enforce_evidence_required(findings)
    findings = score_reportability(findings, module_kind)
    findings = label_findings(findings, scope)
    findings = apply_guardrails(findings, scope)
    findings = apply_duplicate_risk(findings, record.run_id)
    alert_info = maybe_alert(findings, options, record.run_id, module_kind, scope)
    evidence_missing = [f.id for f in findings if not f.evidence]
    attachments_path = (OUTPUT_DIR / "evidence" / f"{record.run_id}_attachments.jsonl")
    attachments_present = attachments_path.exists()
    for f in findings:
        f.mitigation = generate_mitigation(mitigation_tier, title=f.title)
        f.repro_steps = build_repro_steps(f, scope)

    format_id = scope.get("report_format_id")
    report_context = build_report_context(scope, assets, findings, module_kind)
    summary = f"Findings summary. Policy denials: {len(policy_denials)}" if policy_denials else "Findings summary"
    report_blocked_reason = ""
    report_bundle = []
    ready, reason = report_preflight(
        findings,
        scope,
        attachments_path,
        module_kind,
    )
    if not ready:
        report_blocked_reason = reason
        report_bundle = [{
            "format": "md",
            "content": f"Report blocked: {reason}. Resolve blockers and re-run.",
            "id": "blocked.md",
        }]
    else:
        if format_id:
            report_bundle = [format_report(record.run_id, summary, [f.__dict__ for f in findings], "See mitigation guidance for tiered steps.", format_id=format_id, context=report_context)]
        else:
            report_bundle = render_report_bundle(record.run_id, findings, summary_override=summary, context=report_context)
    loop_state = build_loop_state(
        record.run_id,
        module_kind,
        findings,
        options,
        scope,
        record.approvals.__dict__,
        policy_denials,
        evidence_missing,
        attachments_present,
        report_blocked_reason,
    )
    hil_alert = maybe_hil_alert(loop_state.get("loops", {}).get("hil_cadence", {}), options, record.run_id, scope)
    loop_state_path = write_loop_state(record.run_id, loop_state)

    report_paths = {}
    for r in report_bundle:
        fmt = (r.get("format") or "md").lower()
        ext = "md" if fmt == "md" else fmt
        report_paths[fmt] = write_report(record.run_id, r.get("content", ""), ext=ext)

    run_record = {
        "run_id": record.run_id,
        "mode": record.mode,
        "scope": scope,
        "tenant_id": scope.get("tenant_id", ""),
        "approvals": record.approvals.__dict__,
        "playbook_ids": playbook_ids,
        "playbook_missing": resolved.get("missing", []),
        "modules_executed": module_exec,
        "policy_denials": policy_denials,
        "findings": [f.__dict__ for f in findings],
        "options": options,
        "intelligence_policy": "config/intelligence_lifecycle.json",
        "validation_checklist": validation_checklist() if module_kind == "vuln" else [],
        "evidence_missing": evidence_missing,
        "report_blocked_reason": report_blocked_reason,
        "alerts": alert_info,
        "hil_alert": hil_alert,
        "loop_state": loop_state,
        "loop_state_path": loop_state_path,
        "report_bundle": report_paths,
        "validation_recommendation": report_context.get("validation_recommendation"),
    }
    eval_path = evaluate_findings([f.__dict__ for f in findings], record.run_id)
    run_record["eval_path"] = eval_path
    evidence_path = write_evidence_bundle(record.run_id, module_exec)
    run_path = write_run(record.run_id, run_record)
    report_path = report_paths.get("md") or next(iter(report_paths.values()), "")
    redaction_path = write_redaction_summary(record.run_id)
    graph_path = write_graph(record.run_id, all_artifacts)
    orchestration = run_orchestration({
        "module_kind": module_kind,
        "goal": scope.get("goal", ""),
        "constraints": scope.get("constraints", ""),
        "scope": scope,
        "modules": record.plan["modules"],
        "mode": "execute",
        "artifacts": all_artifacts,
        "findings": [f.__dict__ for f in findings],
    })

    append_audit({"event": "execute", "run_id": record.run_id, "modules": record.plan["modules"]})

    bq_export = export_bigquery_payload(
        record.run_id,
        scope,
        all_artifacts,
        [f.__dict__ for f in findings],
        report_path,
        eval_path,
        module_exec,
        training_path=str(TRAIN_PATH),
    )
    bq_load = load_to_bigquery(bq_export.get("payload", {}))
    retention = None
    if options.get("retention", {}).get("enabled", False):
        retention = apply_retention()

    db_store = None
    if os.getenv("KAI_RUN_DB") == "pg":
        db_store = store_run_metadata({
            "run_id": record.run_id,
            "tenant_id": scope.get("tenant_id", ""),
            "mode": record.mode,
            "created_at": run_record.get("created_at"),
            "findings_count": len(findings),
            "report_bundle": report_paths,
        })

    webhook = post_webhook("run.completed", {
        "run_id": record.run_id,
        "tenant_id": scope.get("tenant_id", ""),
        "findings_count": len(findings),
        "report_bundle": report_paths,
    })

    return {
        "status": "completed",
        "run_id": record.run_id,
        "run_record": run_path,
        "evidence_bundle": evidence_path,
        "report": report_path,
        "report_bundle": report_paths,
        "redaction_summary": redaction_path,
        "findings_count": len(findings),
        "validation_recommendation": report_context.get("validation_recommendation"),
        "orchestration": orchestration,
        "options": options,
        "graph": graph_path,
        "evals": eval_path,
        "alerts": alert_info,
        "loop_state": loop_state_path,
        "bigquery_export": bq_export.get("paths", {}),
        "bigquery_validation": bq_export.get("validation", {}),
        "bigquery_load": bq_load,
        "retention": retention,
        "db_store": db_store,
        "webhook": webhook,
    }
