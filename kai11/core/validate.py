import json
from pathlib import Path
from typing import Dict, Any, List

from .config import BUILD_ROOT
from .template import extract_placeholders


def _load_schema(name: str) -> Dict[str, Any]:
    p = BUILD_ROOT / "config" / "schemas" / name
    return json.loads(p.read_text()) if p.exists() else {}


def _validate_required(data: Dict[str, Any], required: List[str]) -> List[str]:
    missing = []
    for r in required:
        if r not in data:
            missing.append(r)
    return missing


def validate_prompt_file(path: Path) -> Dict[str, Any]:
    data = json.loads(path.read_text())
    schema = _load_schema("prompt.schema.json")
    missing = _validate_required(data, schema.get("required", []))
    placeholders = list(extract_placeholders(data.get("content", "")))
    return {"id": data.get("id"), "missing": missing, "placeholders": placeholders}


def validate_persona_file(path: Path) -> Dict[str, Any]:
    data = json.loads(path.read_text())
    schema = _load_schema("persona.schema.json")
    missing = _validate_required(data, schema.get("required", []))
    return {"id": data.get("id"), "missing": missing}


def validate_playbook_file(path: Path) -> Dict[str, Any]:
    data = json.loads(path.read_text())
    schema = _load_schema("playbook.schema.json")
    missing = _validate_required(data, schema.get("required", []))
    return {"id": data.get("id"), "missing": missing}


def validate_report_format_file(path: Path) -> Dict[str, Any]:
    data = json.loads(path.read_text())
    schema = _load_schema("report_format.schema.json")
    missing = _validate_required(data, schema.get("required", []))
    return {"id": data.get("id"), "missing": missing}
