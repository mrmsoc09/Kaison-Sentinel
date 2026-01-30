import json
import re
from pathlib import Path
from typing import Dict, Any, Iterable, List

from .config import OUTPUT_DIR

CVE_PATH = OUTPUT_DIR / "cve_store.jsonl"


def load_cve_store(path: Path | None = None) -> List[Dict[str, Any]]:
    src = path or CVE_PATH
    if not src.exists():
        return []
    items: List[Dict[str, Any]] = []
    with src.open("r", encoding="utf-8") as fh:
        for line in fh:
            try:
                items.append(json.loads(line))
            except Exception:
                continue
    return items


def find_cve_by_id(cve_id: str, store: List[Dict[str, Any]] | None = None) -> Dict[str, Any] | None:
    if not cve_id:
        return None
    store = store or load_cve_store()
    for item in store:
        if item.get("id") == cve_id:
            return item
    return None


def extract_cve_ids(text: str) -> List[str]:
    if not text:
        return []
    return list({m.upper() for m in re.findall(r"CVE-\\d{4}-\\d{4,7}", text, flags=re.IGNORECASE)})


def search_cve(text: str, limit: int = 5, store: List[Dict[str, Any]] | None = None) -> List[Dict[str, Any]]:
    store = store or load_cve_store()
    if not text:
        return []
    query = text.lower()
    results = []
    for item in store:
        desc = (item.get("description") or "").lower()
        if query in desc:
            results.append(item)
        if len(results) >= limit:
            break
    return results
