#!/usr/bin/env bash
# Surfs up! My computer crashes frequently so could you create a system log  so that if i say my computer crashed, you can check the log to see where i last left off. also print the part between the surfs up in all futuree scripts that are either downloaded or pasted to the terminal.

set -euo pipefail
[[ "$(hostname)" == "we6jbo" ]] || { echo "ABORT: T14 only."; exit 1; }
[[ -f /opt/z/z.txt ]] || { echo "ABORT: /opt/z/z.txt missing."; exit 1; }

command -v t14-finish >/dev/null 2>&1 && t14-finish deadline || true

ROOT="/home/we6jbo/Projects/jeremiahai"
cd "$ROOT"
cmake -S . -B build
cmake --build build -j2
logger -t jeremiahai "Starting JeremiahAI Qt application"
exec "$ROOT/build/jeremiahai"
