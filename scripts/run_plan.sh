#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export PYTHONPATH="$ROOT"
python3 -m kai11.cli --mode plan --scope '{"allowlist":["example.com"]}'
