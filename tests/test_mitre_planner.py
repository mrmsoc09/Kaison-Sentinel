import os

from kai11.core.mitre_planner import list_techniques, build_mitre_plan, export_mitre_bundle


def test_mitre_list_contains_default():
    data = list_techniques()
    techniques = [t["technique_id"] for t in data.get("techniques", [])]
    assert "T1562.001" in techniques


def test_mitre_plan_requires_scope():
    plan = build_mitre_plan("T1562.001", scope={}, hil_approved=True)
    assert plan["status"] == "blocked"
    assert plan["reason"] == "scope_required"


def test_mitre_plan_requires_hil():
    plan = build_mitre_plan("T1562.001", scope={"allowlist": ["example.com"]}, hil_approved=False)
    assert plan["status"] == "blocked"
    assert plan["reason"] == "hil_required"


def test_mitre_plan_ok():
    plan = build_mitre_plan("T1562.001", scope={"allowlist": ["example.com"]}, hil_approved=True)
    assert plan["status"] == "ok"
    assert plan["steps"]


def test_mitre_export_bundle():
    os.environ["KAI_ALLOW_PLAINTEXT"] = "1"
    plan = export_mitre_bundle("T1562.001", scope={"allowlist": ["example.com"]}, hil_approved=True)
    assert plan["status"] == "ok"
    assert plan.get("report_bundle")
