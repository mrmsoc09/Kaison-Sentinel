import json
import subprocess
from pathlib import Path
from typing import Dict, Any, List

from .config import BUILD_ROOT
from .keys import get_active_key

VAULT_DIR = BUILD_ROOT / "config" / "vault"
KEY_DIR = VAULT_DIR / "keys"
PROVIDERS = VAULT_DIR / "providers.json"


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
    if not KEY_DIR.exists():
        return []
    return [p.stem.replace("_key", "") for p in KEY_DIR.glob("*_key.enc")]


def add_key(source_id: str, key_value: str) -> Dict[str, Any]:
    KEY_DIR.mkdir(parents=True, exist_ok=True)
    key = get_active_key()
    if not key:
        return {"status": "error", "reason": "encryption_key_required"}
    path = KEY_DIR / f"{source_id.replace('.', '_')}_key.enc"
    payload = json.dumps({"source_id": source_id, "key": key_value})
    _encrypt(payload, key, path)
    return {"status": "ok", "path": str(path)}


def get_key(source_id: str) -> Dict[str, Any]:
    key = get_active_key()
    if not key:
        return {"status": "error", "reason": "encryption_key_required"}
    path = KEY_DIR / f"{source_id.replace('.', '_')}_key.enc"
    if not path.exists():
        return {"status": "missing"}
    data = json.loads(_decrypt(path, key))
    return {"status": "ok", "source_id": source_id, "key": data.get("key")}
