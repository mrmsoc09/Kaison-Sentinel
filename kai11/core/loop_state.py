from typing import Dict, Any, List
import os

from .contracts import Finding
from .hil_cadence import compute_hil_cadence
from .config import LOOPS_DIR, OUTPUT_DIR


def _intel_counts(findings: List[Finding]) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for f in findings:
        key = f.intel_state or "raw"
        counts[key] = counts.get(key, 0) + 1
    return counts


def _avg_reportability(findings: List[Finding]) -> float:
    if not findings:
        return 0.0
    return round(sum([f.reportability for f in findings]) / max(1, len(findings)), 2)


def build_loop_state(
    run_id: str,
    module_kind: str,
    findings: List[Finding],
    options: Dict[str, Any],
    scope: Dict[str, Any],
    approvals: Dict[str, Any],
    policy_denials: List[Dict[str, Any]],
    evidence_missing: List[str],
    attachments_present: bool,
    report_blocked_reason: str,
) -> Dict[str, Any]:
    intel_counts = _intel_counts(findings)
    strategy_status = "ok" if findings else "blocked"
    tactical_status = "ok"
    controlled_status = "warn" if policy_denials else "ok"
    evidence_status = "ok"
    if module_kind == "vuln" and not scope.get("validation_confirmed"):
        evidence_status = "blocked"
    if evidence_missing:
        evidence_status = "blocked"
    reportability_status = "blocked" if report_blocked_reason else "ok"
    screen_recording_attached = attachments_present
    loops = {
        "strategy_gate": {
            "hypothesis_count": len(findings),
            "intel_state_counts": intel_counts,
            "notes": "hypotheses derived from normalized findings",
            "status": strategy_status,
            "action": "collect_more_intel" if strategy_status != "ok" else "proceed",
        },
        "tactical_selection": {
            "modules_planned": scope.get("module_kind", module_kind),
            "tool_pairing": "primary+corroborator (policy planned)",
            "constraints": scope.get("constraints", ""),
            "status": tactical_status,
            "action": "review_constraints" if tactical_status != "ok" else "proceed",
        },
        "controlled_execution": {
            "approved": bool(approvals.get("approved")),
            "hil_required": bool(approvals.get("required")),
            "policy_denials": len(policy_denials),
            "network_allowed": os.getenv("KAI_ALLOW_NETWORK") == "1",
            "active_allowed": os.getenv("KAI_ALLOW_ACTIVE") == "1",
            "status": controlled_status,
            "action": "review_policy_denials" if controlled_status != "ok" else "proceed",
        },
        "evidence_validation": {
            "validation_confirmed": bool(scope.get("validation_confirmed")),
            "evidence_missing": len(evidence_missing),
            "attachments_present": attachments_present,
            "screen_recording_attached": bool(screen_recording_attached),
            "status": evidence_status,
            "action": "attach_evidence" if evidence_status != "ok" else "proceed",
        },
        "reportability": {
            "avg_reportability": _avg_reportability(findings),
            "blocked_reason": report_blocked_reason or "",
            "status": reportability_status,
            "action": "resolve_blockers" if reportability_status != "ok" else "proceed",
        },
        "learning_feedback": {
            "training_path": str(OUTPUT_DIR / "training_data.jsonl"),
            "vector_store": str(OUTPUT_DIR / "vector_store.jsonl"),
            "bigquery_enabled": bool(options.get("bigquery", {}).get("enabled", False)) if options else False,
            "status": "ok",
            "action": "review_feedback",
        },
        "hil_cadence": {
            **compute_hil_cadence(run_id, scope),
            "action": "request_hil_confirmation",
        },
    }

    return {
        "run_id": run_id,
        "module_kind": module_kind,
        "loops": loops,
    }


def write_loop_state(run_id: str, state: Dict[str, Any]) -> str:
    LOOPS_DIR.mkdir(parents=True, exist_ok=True)
    path = LOOPS_DIR / f"{run_id}_loops.json"
    path.write_text(__import__("json").dumps(state, ensure_ascii=False, indent=2))
    return str(path)
