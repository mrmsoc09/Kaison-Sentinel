#!/usr/bin/env python3
"""
Fetch scope and policy pages for public bug bounty programs.

Outputs per-program folders with scope/policy HTML and text, plus meta.json.
This script is intended to be run by the operator with network access.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import time
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from typing import Dict, Any
from urllib.request import Request, urlopen


class _TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._parts: list[str] = []

    def handle_data(self, data: str) -> None:
        if data.strip():
            self._parts.append(data.strip())

    def text(self) -> str:
        joined = " ".join(self._parts)
        joined = re.sub(r"\s+", " ", joined)
        return joined.strip()


def _fetch(url: str, timeout: int = 20) -> Dict[str, Any]:
    headers = {
        "User-Agent": "KaisonSentinel/1.0 (+https://kaisonai.com) fetch_program_guidelines",
        "Accept": "text/html,application/xhtml+xml",
    }
    req = Request(url, headers=headers)
    try:
        with urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
            status = getattr(resp, "status", 200)
            content_type = resp.headers.get("Content-Type", "")
        return {
            "ok": True,
            "status": status,
            "content_type": content_type,
            "body": raw,
        }
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "error": str(exc), "status": None, "content_type": "", "body": b""}


def _write_text(path: Path, html: bytes) -> None:
    parser = _TextExtractor()
    try:
        parser.feed(html.decode("utf-8", errors="ignore"))
    except Exception:  # noqa: BLE001
        return
    text = parser.text()
    path.write_text(text + "\n", encoding="utf-8")


def _safe_name(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_.-]+", "_", value).strip("_")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--programs", default="config/programs.json", help="Path to programs.json")
    ap.add_argument("--out", default="data/programs/scopes", help="Output folder")
    ap.add_argument("--sleep", type=float, default=1.5, help="Delay between requests (seconds)")
    args = ap.parse_args()

    root = Path(__file__).resolve().parents[1]
    programs_path = (root / args.programs).resolve()
    out_dir = (root / args.out).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    data = json.loads(programs_path.read_text(encoding="utf-8"))
    programs = data.get("programs", [])

    for program in programs:
        pid = _safe_name(program.get("id") or program.get("name") or "unknown")
        scope_url = program.get("scope_url") or ""
        policy_url = program.get("policy_url") or ""
        if not scope_url and not policy_url:
            continue

        dest = out_dir / pid
        dest.mkdir(parents=True, exist_ok=True)
        meta = {
            "id": program.get("id"),
            "name": program.get("name"),
            "platform": program.get("platform"),
            "scope_url": scope_url,
            "policy_url": policy_url,
            "fetched_at": datetime.now(timezone.utc).isoformat(),
            "scope": {},
            "policy": {},
        }

        if scope_url:
            res = _fetch(scope_url)
            meta["scope"] = {k: v for k, v in res.items() if k != "body"}
            if res.get("ok") and res.get("body"):
                (dest / "scope.html").write_bytes(res["body"])
                _write_text(dest / "scope.txt", res["body"])
            time.sleep(args.sleep)

        if policy_url:
            res = _fetch(policy_url)
            meta["policy"] = {k: v for k, v in res.items() if k != "body"}
            if res.get("ok") and res.get("body"):
                (dest / "policy.html").write_bytes(res["body"])
                _write_text(dest / "policy.txt", res["body"])
            time.sleep(args.sleep)

        (dest / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
