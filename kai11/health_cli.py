import argparse
import json

from .core.tool_health import build_health_report, write_health_report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-version", action="store_true")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    if args.write:
        path = write_health_report(check_version=args.check_version)
        print(json.dumps({"status": "written", "path": path}, ensure_ascii=False, indent=2))
        return

    report = build_health_report(check_version=args.check_version)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
