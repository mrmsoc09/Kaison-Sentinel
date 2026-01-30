#!/usr/bin/env bash
set -euo pipefail
export PYTHONPATH="/home/user23/KAI/builds/Kai 1.1"
export KAI_ALLOW_NETWORK=1
# Requires KAI_ENCRYPTION_KEY or KAI_ALLOW_PLAINTEXT=1
python3 -m kai11.cli --mode execute --scope '{"allowlist":["example.com"]}' --approve --tier standard
