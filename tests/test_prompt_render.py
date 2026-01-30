from kai11.core.prompt_manager import select_prompt, render_prompt


def test_render_scan_prompt_defaults():
    prompt = select_prompt("scan")
    out = render_prompt(prompt, {"goal": "Test", "scope": "[]", "mode": "plan", "modules": "m1", "constraints": "none"})
    assert out["missing"] == {}
    assert "Test" in out["content"]
