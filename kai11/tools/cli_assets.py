import argparse
import json
from pathlib import Path

from ..core.validate import (
    validate_prompt_file,
    validate_persona_file,
    validate_playbook_file,
    validate_report_format_file,
)
from ..core.registry import (
    load_prompts,
    load_personas,
    load_playbooks,
    load_report_formats,
    load_agents,
    load_personas_praison,
    load_personas_langstudio,
)


def _list(kind: str) -> None:
    if kind == "prompts":
        items = load_prompts()
    elif kind == "personas":
        items = load_personas()
    elif kind == "personas_praison":
        items = load_personas_praison()
    elif kind == "personas_langstudio":
        items = load_personas_langstudio()
    elif kind == "playbooks":
        items = load_playbooks()
    elif kind == "agents":
        items = load_agents()
    else:
        items = load_report_formats()
    print(json.dumps(items, ensure_ascii=False, indent=2))


def _validate(kind: str, path: str) -> None:
    p = Path(path)
    if kind == "prompts":
        out = validate_prompt_file(p)
    elif kind == "personas":
        out = validate_persona_file(p)
    elif kind == "playbooks":
        out = validate_playbook_file(p)
    else:
        out = validate_report_format_file(p)
    print(json.dumps(out, ensure_ascii=False, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--list", choices=["prompts", "personas", "personas_praison", "personas_langstudio", "playbooks", "report_formats", "agents"])
    parser.add_argument("--validate", choices=["prompts", "personas", "playbooks", "report_formats"])
    parser.add_argument("--path", help="Path to JSON file to validate")
    args = parser.parse_args()

    if args.list:
        _list(args.list)
        return

    if args.validate and args.path:
        _validate(args.validate, args.path)
        return

    parser.print_help()


if __name__ == "__main__":
    main()
