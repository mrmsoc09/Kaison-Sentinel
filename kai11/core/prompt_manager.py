from typing import Dict, Any, List

from .registry import load_prompts, load_personas, load_report_formats
from .template import render_template, validate_template


def select_prompt(prompt_type: str, prompt_id: str | None = None) -> Dict[str, Any]:
    prompts = [p for p in load_prompts() if p.get("type") == prompt_type]
    if prompt_id:
        for p in prompts:
            if p.get("id") == prompt_id:
                return p
    return prompts[0] if prompts else {"id": "none", "type": prompt_type, "content": ""}


def select_prompt_by_tag(prompt_type: str, tag: str) -> Dict[str, Any]:
    prompts = [p for p in load_prompts() if p.get("type") == prompt_type]
    for p in prompts:
        if tag in (p.get("tags") or []):
            return p
    return select_prompt(prompt_type)


def select_persona(persona_id: str | None = None) -> Dict[str, Any]:
    personas = load_personas()
    if persona_id:
        for p in personas:
            if p.get("id") == persona_id:
                return p
    return personas[0] if personas else {"id": "none", "name": "None", "principles": []}


def render_prompt(prompt: Dict[str, Any], values: Dict[str, str]) -> Dict[str, Any]:
    content = prompt.get("content", "")
    missing = validate_template(content, values)
    rendered = render_template(content, values)
    return {"id": prompt.get("id"), "type": prompt.get("type"), "content": rendered, "missing": missing}


def list_report_formats() -> List[Dict[str, Any]]:
    return load_report_formats()
