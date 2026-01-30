import json
from pathlib import Path
from typing import Dict, Any, List

MITRE_LIBRARY: Dict[str, Dict[str, Any]] = {
    "T1562.001": {
        "tactic_id": "TA0005",
        "tactic": "Defense Evasion",
        "technique": "Impair Defenses: Disable or Modify Tools",
        "safe_objective": "Assess potential impairment of defenses without altering target state.",
        "risk": "high",
        "playbooks": {
            "osint": ["playbook.osint.basic"],
            "vuln": ["playbook.vuln.basic"],
            "validation": ["playbook.vuln.validation"]
        },
        "report_templates": ["mitre_plan_md", "mitre_plan_html", "mitre_plan_json"]
    }
}

CONF = Path(__file__).resolve().parents[1] / "config" / "mitre_attack.json"
if CONF.exists():
    try:
        data = json.loads(CONF.read_text())
        for entry in data.get("techniques", []):
            tid = entry.get("technique_id")
            if not tid:
                continue
            MITRE_LIBRARY[tid] = {
                "tactic_id": entry.get("tactic_id"),
                "tactic": entry.get("tactic"),
                "technique": entry.get("technique"),
                "safe_objective": entry.get("safe_objective"),
                "risk": entry.get("risk", "medium"),
                "playbooks": entry.get("playbooks", {}),
                "report_templates": entry.get("report_templates", []),
            }
    except Exception:
        pass


def list_techniques() -> List[Dict[str, Any]]:
    return [
        {"technique_id": tid, **data} for tid, data in sorted(MITRE_LIBRARY.items())
    ]


def build_plan(technique_id: str, scope: Dict[str, Any] | None = None, hil_approved: bool = False) -> Dict[str, Any]:
    scope = scope or {}
    record = MITRE_LIBRARY.get(technique_id)
    if not record:
        return {"status": "unknown_technique", "technique_id": technique_id}

    gating = {
        "hil_required": True,
        "hil_approved": bool(hil_approved),
        "scope_required": True,
        "scope_allowlist": scope.get("allowlist") or [],
    }

    if not gating["scope_allowlist"]:
        return {
            "status": "blocked",
            "reason": "scope_required",
            "technique_id": technique_id,
            "gating": gating,
        }

    if gating["hil_required"] and not gating["hil_approved"]:
        return {
            "status": "blocked",
            "reason": "hil_required",
            "technique_id": technique_id,
            "gating": gating,
        }

    steps = [
        {
            "id": "scope_verify",
            "type": "gate",
            "description": "Confirm authorization and scope alignment for defensive assessment.",
        },
        {
            "id": "inventory_controls",
            "type": "read_only",
            "description": "Inventory security tooling and control ownership (EDR/AV/agent registry) without modification.",
        },
        {
            "id": "telemetry_review",
            "type": "read_only",
            "description": "Review logs/telemetry for evidence of disabled or modified controls.",
        },
        {
            "id": "control_integrity",
            "type": "read_only",
            "description": "Check control integrity signals (service state, config drift, policy tamper indicators).",
        },
        {
            "id": "evidence_bundle",
            "type": "evidence",
            "description": "Capture non-destructive evidence for HiL validation and reporting.",
        },
        {
            "id": "notification",
            "type": "notify",
            "description": "Send sanitized findings to internal webhook/notification channel (no target data exfiltration).",
        },
    ]

    muted_plan = {
        "note": "Muted plan uses read-only validation and internal notifications only. No destructive actions.",
        "channels": ["internal_webhook", "audit_log"],
    }

    playbooks = record.get("playbooks", {}) if isinstance(record.get("playbooks", {}), dict) else {}
    plan = {
        "status": "ok",
        "technique_id": technique_id,
        "tactic_id": record["tactic_id"],
        "tactic": record["tactic"],
        "technique": record["technique"],
        "objective": record["safe_objective"],
        "risk": record["risk"],
        "gating": gating,
        "steps": steps,
        "muted_plan": muted_plan,
        "playbooks_by_module": playbooks,
        "recommended_playbooks": (playbooks.get("osint", []) + playbooks.get("vuln", []) + playbooks.get("validation", [])),
        "report_templates": record.get("report_templates", []),
    }
    return plan


def pathfinder(technique_id: str, scope: Dict[str, Any] | None = None, hil_approved: bool = False) -> Dict[str, Any]:
    """Pathfinder module: safe MITRE-aligned planner with HiL gating."""
    return build_plan(technique_id, scope=scope, hil_approved=hil_approved)


if __name__ == "__main__":
    print(json.dumps({"techniques": list_techniques()}, indent=2))
