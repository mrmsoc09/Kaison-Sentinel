#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export PYTHONPATH="$ROOT"
export KAI_ALLOW_NETWORK=1
# Requires KAI_ENCRYPTION_KEY or KAI_ALLOW_PLAINTEXT=1
python3 -m kai11.cli --mode execute --scope '{"allowlist":["example.com"]}' --approve --tier standard
