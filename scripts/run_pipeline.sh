#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export PYTHONPATH="$ROOT"
python3 -m kai11.pipelines.pipeline --source "$ROOT" --out "$ROOT/outputs"
