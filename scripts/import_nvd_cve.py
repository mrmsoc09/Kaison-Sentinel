#!/usr/bin/env python3
"""
Import NVD JSON 2.0 feed into a compact JSONL store for CVE enrichment.

Usage:
  python3 scripts/import_nvd_cve.py --input /path/to/nvdcve-1.1-2024.json.gz
  python3 scripts/import_nvd_cve.py --input /path/to/nvdcve-2.0.json --limit 50000
"""

from __future__ import annotations

import argparse
import gzip
import json
from pathlib import Path
from typing import Any, Dict, Iterable

OUTPUT = Path(__file__).resolve().parents[1] / "outputs" / "cve_store.jsonl"


def _open(path: Path):
    if path.suffix == ".gz":
        return gzip.open(path, "rt", encoding="utf-8", errors="ignore")
    return path.open("r", encoding="utf-8", errors="ignore")


def _parse_records(data: Dict[str, Any]) -> Iterable[Dict[str, Any]]:
    vulns = data.get("vulnerabilities") or data.get("CVE_Items") or []
    for item in vulns:
        cve = item.get("cve") or {}
        cve_id = cve.get("id") or cve.get("CVE_data_meta", {}).get("ID")
        if not cve_id:
            continue
        descs = cve.get("descriptions") or cve.get("description", {}).get("description_data", [])
        desc = ""
        if isinstance(descs, list) and descs:
            desc = descs[0].get("value") or descs[0].get("lang") or ""
        metrics = item.get("metrics") or {}
        cvss = None
        for key in ("cvssMetricV31", "cvssMetricV30", "cvssMetricV2"):
            if metrics.get(key):
                cvss = metrics[key][0].get("cvssData", {}).get("baseScore")
                break
        weaknesses = cve.get("weaknesses") or cve.get("problemtype", {}).get("problemtype_data", [])
        cwes = []
        if isinstance(weaknesses, list):
            for w in weaknesses:
                for d in w.get("description", []) if isinstance(w, dict) else []:
                    val = d.get("value")
                    if val and val not in cwes:
                        cwes.append(val)
        yield {
            "id": cve_id,
            "description": desc,
            "cvss": cvss,
            "cwe": cwes,
        }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="Path to NVD JSON feed (json or json.gz)")
    ap.add_argument("--limit", type=int, default=0, help="Limit records processed")
    args = ap.parse_args()

    src = Path(args.input).expanduser()
    if not src.exists():
        raise SystemExit(f"Input not found: {src}")
    with _open(src) as fh:
        data = json.load(fh)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with OUTPUT.open("w", encoding="utf-8") as out:
        for record in _parse_records(data):
            out.write(json.dumps(record, ensure_ascii=False) + "\n")
            count += 1
            if args.limit and count >= args.limit:
                break
    print({"status": "ok", "count": count, "path": str(OUTPUT)})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
