import json
from pathlib import Path
from typing import Dict, Tuple, List

from .contracts import Finding
from .config import RUNS_DIR


def _key(title: str, target: str, severity: str) -> Tuple[str, str, str]:
    return (title.strip().lower(), target.strip().lower(), severity.strip().lower())


def _load_history_counts(run_id: str) -> Tuple[Dict[Tuple[str, str, str], int], Dict[Tuple[str, str, str], int]]:
    counts: Dict[Tuple[str, str, str], int] = {}
    validated: Dict[Tuple[str, str, str], int] = {}
    for p in sorted(RUNS_DIR.glob("*.json")):
        if p.name.startswith(run_id):
            continue
        try:
            data = json.loads(p.read_text())
        except Exception:
            continue
        for f in data.get("findings", []) or []:
            key = _key(f.get("title", ""), f.get("target", ""), f.get("severity", ""))
            counts[key] = counts.get(key, 0) + 1
            if f.get("status") in {"validated", "likely"}:
                validated[key] = validated.get(key, 0) + 1
    return counts, validated


def apply_duplicate_risk(findings: List[Finding], run_id: str) -> List[Finding]:
    counts, validated = _load_history_counts(run_id)
    for f in findings:
        key = _key(f.title, f.target, f.severity)
        match_count = counts.get(key, 0)
        validated_count = validated.get(key, 0)
        if validated_count >= 1:
            risk = "high"
        elif match_count >= 3:
            risk = "high"
        elif match_count >= 1:
            risk = "medium"
        else:
            risk = "low"
        f.duplicate_matches = match_count
        f.duplicate_validated = validated_count
        f.duplicate_risk = risk
    return findings
