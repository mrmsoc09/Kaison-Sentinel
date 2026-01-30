from kai11.core.playbooks import resolve_playbook_modules


def test_resolve_playbook_modules():
    res = resolve_playbook_modules(["playbook.osint.basic"])
    assert res["modules"]
    assert "playbook.osint.basic" not in res.get("missing", [])
