from kai11.orchestrator.deepagents import run_deepagents


def test_deepagents_stub_returns_status():
    res = run_deepagents({"module_kind": "osint"})
    assert res["status"] in {"disabled", "blocked", "ready", "ok"}
