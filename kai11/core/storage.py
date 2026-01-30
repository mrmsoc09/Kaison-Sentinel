import os
import json
import subprocess
from pathlib import Path
from typing import Any, Dict

from .config import RUNS_DIR, REPORTS_DIR
from .keys import get_active_key

RUNS_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)


def _encrypt_file(src: Path, dst: Path, key: str) -> None:
    # AES-256-CBC with PBKDF2 via openssl (local)
    cmd = [
        "openssl", "enc", "-aes-256-cbc", "-pbkdf2",
        "-in", str(src), "-out", str(dst), "-pass", f"pass:{key}",
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def write_json(path: Path, data: Dict[str, Any]) -> str:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2))

    key = get_active_key()
    allow_plain = os.getenv("KAI_ALLOW_PLAINTEXT") == "1"

    if key:
        enc_path = path.with_suffix(path.suffix + ".enc")
        _encrypt_file(tmp, enc_path, key)
        tmp.unlink(missing_ok=True)
        return str(enc_path)

    if not allow_plain:
        tmp.unlink(missing_ok=True)
        raise RuntimeError("encryption_key_required")

    tmp.rename(path)
    return str(path)


def write_run(run_id: str, data: Dict[str, Any]) -> str:
    path = RUNS_DIR / f"{run_id}.json"
    return write_json(path, data)


def write_report(run_id: str, text: str | bytes, ext: str = "md") -> str:
    safe_ext = ext.lstrip(".")
    path = REPORTS_DIR / f"{run_id}.{safe_ext}"
    tmp = path.with_suffix(path.suffix + ".tmp")
    if isinstance(text, bytes):
        tmp.write_bytes(text)
    else:
        tmp.write_text(text, encoding="utf-8")

    key = get_active_key()
    allow_plain = os.getenv("KAI_ALLOW_PLAINTEXT") == "1"

    if key:
        enc_path = path.with_suffix(path.suffix + ".enc")
        _encrypt_file(tmp, enc_path, key)
        tmp.unlink(missing_ok=True)
        return str(enc_path)

    if not allow_plain:
        tmp.unlink(missing_ok=True)
        raise RuntimeError("encryption_key_required")

    tmp.rename(path)
    return str(path)
