from kai11.core.registry import load_prompts, load_personas


def test_registry_loads_defaults():
    assert len(load_prompts()) >= 1
    assert len(load_personas()) >= 1
