import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import Dict, Any, List

from .config import BUILD_ROOT
from .keys import get_active_key
from .options import get_options

VAULT_DIR = BUILD_ROOT / "config" / "vault"
KEY_DIR = VAULT_DIR / "keys"
PROVIDERS = VAULT_DIR / "providers.json"
HASHICORP_PREFIX = "secret/kaison"


def _backend() -> str:
    env = os.getenv("KAI_VAULT_BACKEND")
    if env:
        return env
    opts = get_options("all")
    return opts.get("vault_backend", "local")


def _vault_cli_available() -> bool:
    return shutil.which("vault") is not None


def _vault_cli(args: List[str]) -> Dict[str, Any]:
    if not _vault_cli_available():
        return {"status": "error", "reason": "vault_cli_missing"}
    try:
        result = subprocess.run(["vault", *args], capture_output=True, text=True, check=True)
        return {"status": "ok", "stdout": result.stdout.strip(), "stderr": result.stderr.strip()}
    except Exception as exc:  # noqa: BLE001
        return {"status": "error", "reason": str(exc)}


def _encrypt(text: str, key: str, out_path: Path) -> None:
    tmp = out_path.with_suffix(".tmp")
    tmp.write_text(text)
    cmd = [
        "openssl", "enc", "-aes-256-cbc", "-pbkdf2",
        "-in", str(tmp), "-out", str(out_path), "-pass", f"pass:{key}",
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    tmp.unlink(missing_ok=True)


def _decrypt(path: Path, key: str) -> str:
    out = path.with_suffix(".dec")
    cmd = [
        "openssl", "enc", "-d", "-aes-256-cbc", "-pbkdf2",
        "-in", str(path), "-out", str(out), "-pass", f"pass:{key}",
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    text = out.read_text()
    out.unlink(missing_ok=True)
    return text


def list_providers() -> List[Dict[str, Any]]:
    if not PROVIDERS.exists():
        return []
    return json.loads(PROVIDERS.read_text()).get("sources", [])


def list_keys() -> List[str]:
    if _backend() == "hashicorp":
        res = _vault_cli(["kv", "list", "-format=json", HASHICORP_PREFIX])
        if res.get("status") != "ok":
            return []
        try:
            return json.loads(res.get("stdout") or "[]")
        except Exception:
            return []
    if not KEY_DIR.exists():
        return []
    return [p.stem.replace("_key", "") for p in KEY_DIR.glob("*_key.enc")]


def add_key(source_id: str, key_value: str) -> Dict[str, Any]:
    if _backend() == "hashicorp":
        if not os.getenv("VAULT_ADDR") or not os.getenv("VAULT_TOKEN"):
            return {"status": "error", "reason": "vault_env_required"}
        res = _vault_cli(["kv", "put", f"{HASHICORP_PREFIX}/{source_id}", f"key={key_value}"])
        if res.get("status") != "ok":
            return res
        return {"status": "ok", "backend": "hashicorp", "path": f"{HASHICORP_PREFIX}/{source_id}"}
    KEY_DIR.mkdir(parents=True, exist_ok=True)
    key = get_active_key()
    if not key:
        return {"status": "error", "reason": "encryption_key_required"}
    path = KEY_DIR / f"{source_id.replace('.', '_')}_key.enc"
    payload = json.dumps({"source_id": source_id, "key": key_value})
    _encrypt(payload, key, path)
    return {"status": "ok", "backend": "local", "path": str(path)}


def get_key(source_id: str) -> Dict[str, Any]:
    if _backend() == "hashicorp":
        if not os.getenv("VAULT_ADDR") or not os.getenv("VAULT_TOKEN"):
            return {"status": "error", "reason": "vault_env_required"}
        res = _vault_cli(["kv", "get", "-format=json", f"{HASHICORP_PREFIX}/{source_id}"])
        if res.get("status") != "ok":
            return res
        try:
            payload = json.loads(res.get("stdout") or "{}")
            return {"status": "ok", "source_id": source_id, "key": payload.get("data", {}).get("data", {}).get("key")}
        except Exception:
            return {"status": "error", "reason": "vault_parse_failed"}
    key = get_active_key()
    if not key:
        return {"status": "error", "reason": "encryption_key_required"}
    path = KEY_DIR / f"{source_id.replace('.', '_')}_key.enc"
    if not path.exists():
        return {"status": "missing"}
    data = json.loads(_decrypt(path, key))
    return {"status": "ok", "source_id": source_id, "key": data.get("key")}
