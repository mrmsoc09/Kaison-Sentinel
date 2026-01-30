from kai11.orchestrator.agent_runner import run_orchestration


def test_orchestration_returns_agents():
    out = run_orchestration({"module_kind": "osint", "goal": "test", "scope": {"allowlist": ["example.com"]}})
    assert "agents" in out
    assert len(out["agents"]) >= 2
