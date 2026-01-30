import csv
import io
import json
from pathlib import Path
from typing import Dict, Any, List

from .config import BUILD_ROOT

PLAYBOOK_DIR = BUILD_ROOT / "config" / "playbooks"


def save_playbook(playbook: Dict[str, Any]) -> Dict[str, Any]:
    PLAYBOOK_DIR.mkdir(parents=True, exist_ok=True)
    pid = playbook.get("id")
    if not pid:
        return {"status": "error", "reason": "id_required"}
    path = PLAYBOOK_DIR / f"{pid.replace('.', '_')}.json"
    path.write_text(json.dumps(playbook, ensure_ascii=False, indent=2))
    return {"status": "ok", "path": str(path)}


def list_playbooks() -> List[Dict[str, Any]]:
    if not PLAYBOOK_DIR.exists():
        return []
    items = []
    for p in sorted(PLAYBOOK_DIR.glob("*.json")):
        try:
            items.append(json.loads(p.read_text()))
        except Exception:
            continue
    return items


def _normalize_ids(ids: List[str] | None) -> List[str]:
    if not ids:
        return []
    if isinstance(ids, str):
        ids = [i.strip() for i in ids.split(",") if i.strip()]
    return [i for i in ids if i]


def resolve_playbook_modules(ids: List[str] | None) -> Dict[str, Any]:
    requested = _normalize_ids(ids)
    if not requested:
        return {"modules": [], "missing": []}
    playbooks = {p.get("id"): p for p in list_playbooks()}
    modules: List[str] = []
    missing: List[str] = []
    for pid in requested:
        pb = playbooks.get(pid)
        if not pb:
            missing.append(pid)
            continue
        modules.extend(pb.get("modules") or [])
    return {"modules": sorted(set(modules)), "missing": missing}


def export_playbooks() -> Dict[str, Any]:
    return {"version": 1, "playbooks": list_playbooks()}


def import_playbooks_json(data: str) -> Dict[str, Any]:
    try:
        payload = json.loads(data)
    except Exception:
        return {"status": "error", "reason": "invalid_json"}
    items = payload.get("playbooks", []) if isinstance(payload, dict) else payload
    count = 0
    for pb in items:
        if isinstance(pb, dict):
            save_playbook(pb)
            count += 1
    return {"status": "ok", "imported": count}


def import_playbooks_csv(data: str) -> Dict[str, Any]:
    reader = csv.DictReader(io.StringIO(data))
    count = 0
    for row in reader:
        pid = row.get("id")
        name = row.get("name") or pid
        modules = [m.strip() for m in (row.get("modules") or "").split(",") if m.strip()]
        pb = {"id": pid, "name": name, "version": "1.0", "modules": modules, "tags": []}
        if pid:
            save_playbook(pb)
            count += 1
    return {"status": "ok", "imported": count}
