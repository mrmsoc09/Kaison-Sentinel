#!/usr/bin/env bash
set -euo pipefail
export PYTHONPATH="/home/user23/KAI/builds/Kai 1.1"
python3 -m kai11.cli --mode plan --scope '{"allowlist":["example.com"]}'
