import json
from pathlib import Path
from typing import Dict, Any

from .config import BUILD_ROOT

CONF = BUILD_ROOT / "config" / "email.json"


def load_email_config() -> Dict[str, Any]:
    if not CONF.exists():
        return {
            "enabled": False,
            "provider": "gmail_smtp",
            "from_email": "",
            "smtp_host": "smtp.gmail.com",
            "smtp_port": 587,
            "username": "",
            "password_source_id": "source.gmail_smtp",
            "use_starttls": True,
            "use_ssl": False,
            "allow_insecure": False,
        }
    try:
        return json.loads(CONF.read_text())
    except Exception:
        return {"enabled": False}


def save_email_config(data: Dict[str, Any]) -> Dict[str, Any]:
    cfg = load_email_config()
    cfg.update({k: v for k, v in data.items() if v is not None})
    CONF.write_text(json.dumps(cfg, ensure_ascii=False, indent=2))
    return cfg
