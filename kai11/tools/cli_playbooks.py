import argparse
import json
from pathlib import Path

from ..core.playbooks import export_playbooks, import_playbooks_json, import_playbooks_csv


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--export", action="store_true")
    parser.add_argument("--import-json", help="Path to JSON file")
    parser.add_argument("--import-csv", help="Path to CSV file")
    args = parser.parse_args()

    if args.export:
        print(json.dumps(export_playbooks(), ensure_ascii=False, indent=2))
        return

    if args.import_json:
        data = Path(args.import_json).read_text()
        print(json.dumps(import_playbooks_json(data), ensure_ascii=False, indent=2))
        return

    if args.import_csv:
        data = Path(args.import_csv).read_text()
        print(json.dumps(import_playbooks_csv(data), ensure_ascii=False, indent=2))
        return

    parser.print_help()


if __name__ == "__main__":
    main()
