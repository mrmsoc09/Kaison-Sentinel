import json
from pathlib import Path
from typing import Dict, Any

from .config import BUILD_ROOT

PRAISON_DIR = BUILD_ROOT / "config" / "personas_praison"
LANG_DIR = BUILD_ROOT / "config" / "personas_langstudio"


def save_persona(persona_id: str, praison: Dict[str, Any], langstudio: Dict[str, Any]) -> Dict[str, str]:
    PRAISON_DIR.mkdir(parents=True, exist_ok=True)
    LANG_DIR.mkdir(parents=True, exist_ok=True)
    pr_path = PRAISON_DIR / f"{persona_id.replace('.', '_')}.json"
    ls_path = LANG_DIR / f"{persona_id.replace('.', '_')}.json"
    pr_path.write_text(json.dumps(praison, ensure_ascii=False, indent=2))
    ls_path.write_text(json.dumps(langstudio, ensure_ascii=False, indent=2))
    return {"praison": str(pr_path), "langstudio": str(ls_path)}
