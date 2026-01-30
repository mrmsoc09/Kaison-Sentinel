import json
import re
from typing import Dict

PLACEHOLDER_RE = re.compile(r"\{([a-zA-Z0-9_]+)\}")


def extract_placeholders(text: str) -> set[str]:
    return set(PLACEHOLDER_RE.findall(text or ""))


def render_template(text: str, values: Dict[str, str]) -> str:
    def _replace(match: re.Match) -> str:
        key = match.group(1)
        return str(values.get(key, ""))

    return PLACEHOLDER_RE.sub(_replace, text)


def validate_template(text: str, values: Dict[str, str]) -> Dict[str, str]:
    placeholders = extract_placeholders(text)
    missing = [p for p in placeholders if p not in values]
    return {"missing": ",".join(missing)} if missing else {}


def render_json_template(text: str, values: Dict[str, str]) -> Dict:
    rendered = render_template(text, values)
    try:
        return json.loads(rendered)
    except Exception:
        return {"raw": rendered}
