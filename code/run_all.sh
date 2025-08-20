#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python make_all.py "$@"
