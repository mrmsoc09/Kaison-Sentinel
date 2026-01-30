import json
import re
from pathlib import Path
from typing import Dict, Any, List

from .config import BUILD_ROOT, OUTPUT_DIR

CACHE_DIR = BUILD_ROOT / "data" / "programs" / "scopes"
OUT_PATH = OUTPUT_DIR / "program_scopes_parsed.json"


DOMAIN_RE = re.compile(r"(?:(?:\\*\\.)?[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\\.)+[a-z]{2,}", re.IGNORECASE)


def _extract_domains(text: str) -> List[str]:
    if not text:
        return []
    items = set(m.lower() for m in DOMAIN_RE.findall(text))
    return sorted(items)


def parse_cached_scopes() -> Dict[str, Any]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    results = {}
    if not CACHE_DIR.exists():
        payload = {"status": "missing_cache", "programs": {}}
        OUT_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2))
        return payload
    for program_dir in CACHE_DIR.iterdir():
        if not program_dir.is_dir():
            continue
        scope_txt = program_dir / "scope.txt"
        policy_txt = program_dir / "policy.txt"
        scope_text = scope_txt.read_text(encoding="utf-8", errors="ignore") if scope_txt.exists() else ""
        policy_text = policy_txt.read_text(encoding="utf-8", errors="ignore") if policy_txt.exists() else ""
        domains = _extract_domains(scope_text)
        results[program_dir.name] = {
            "domains": domains,
            "domain_count": len(domains),
            "has_scope_text": bool(scope_text),
            "has_policy_text": bool(policy_text),
        }
    payload = {"status": "ok", "programs": results}
    OUT_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2))
    return payload


def load_parsed_scopes() -> Dict[str, Any]:
    if not OUT_PATH.exists():
        return {"status": "missing", "programs": {}}
    try:
        return json.loads(OUT_PATH.read_text())
    except Exception:
        return {"status": "error", "programs": {}}


def allowlist_for_program(program_id: str) -> List[str]:
    data = load_parsed_scopes()
    programs = data.get("programs", {})
    entry = programs.get(program_id, {})
    return entry.get("domains", [])
