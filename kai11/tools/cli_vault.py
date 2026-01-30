import argparse
import json

from ..core.vault import list_providers, list_keys, add_key


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--list-providers", action="store_true")
    parser.add_argument("--list-keys", action="store_true")
    parser.add_argument("--add-key", help="Source id")
    parser.add_argument("--value", help="Key value")
    args = parser.parse_args()

    if args.list_providers:
        print(json.dumps(list_providers(), ensure_ascii=False, indent=2))
        return

    if args.list_keys:
        print(json.dumps(list_keys(), ensure_ascii=False, indent=2))
        return

    if args.add_key and args.value:
        print(json.dumps(add_key(args.add_key, args.value), ensure_ascii=False, indent=2))
        return

    parser.print_help()


if __name__ == "__main__":
    main()
