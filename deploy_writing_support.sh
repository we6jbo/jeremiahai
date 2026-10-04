#!/usr/bin/env bash
# Surfs up! My computer crashes frequently so could you create a system log  so that if i say my computer crashed, you can check the log to see where i last left off. also print the part between the surfs up in all futuree scripts that are either downloaded or pasted to the terminal.

set -euo pipefail

[[ "$(hostname)" == "we6jbo" ]] || { echo "ABORT: T14 only."; exit 1; }
[[ -f /opt/z/z.txt ]] || { echo "ABORT: /opt/z/z.txt missing."; exit 1; }

ROOT="/home/we6jbo/Projects/jeremiahai"
REMOTE="jeremiahai-pi"

echo "===== VERIFY PI ====="
ssh -o BatchMode=yes "$REMOTE" '
set -e
[[ "$(hostname)" == "we6jbo1" ]]
[[ -f /etc/ladybug/this-is-the-pi ]]
grep -qx "we6jbo1 ladybug recovery pi" /etc/ladybug/this-is-the-pi
'

echo "===== CHECK PI DISK ====="
USED="$(ssh -o BatchMode=yes "$REMOTE" "df -P /home/jeremiahai | awk 'NR==2{gsub(/%/,\"\",\$5);print \$5}'")"
echo "Pi disk used: ${USED}%"
if [[ "$USED" -ge 50 ]]; then
    echo "ABORT: Ladybug storage policy requires Pi disk use below 50%."
    exit 1
fi

echo "===== CREATE WRITING SUPPORT DIRECTORIES ====="
ssh "$REMOTE" '
set -e
mkdir -p /home/jeremiahai/writing-tools
mkdir -p /home/jeremiahai/writing-draft
chmod 700 /home/jeremiahai/writing-draft
'

echo "===== COPY LIGHTWEIGHT WRITING TOOLS ====="
scp "$ROOT/pi-writing-tools/privacy_check.py" "$REMOTE:/home/jeremiahai/writing-tools/privacy_check.py"
scp "$ROOT/pi-writing-tools/README.md" "$REMOTE:/home/jeremiahai/writing-tools/README.md"
scp "$ROOT/pi-writing-tools/EXPANSION_GUIDE.md" "$REMOTE:/home/jeremiahai/writing-tools/EXPANSION_GUIDE.md"

ssh "$REMOTE" '
chmod 700 /home/jeremiahai/writing-tools/privacy_check.py
python3 - <<'"'"'PY'"'"'
from pathlib import Path
src=Path("/home/jeremiahai/writing-tools/privacy_check.py").read_text()
compile(src,"privacy_check.py","exec")
print("privacy_check.py syntax OK")
PY
'

logger -t jeremiahai "Deployed Ladybug-safe Vibe writing support tools"

echo
echo "Writing support directories are ready:"
echo "  /home/jeremiahai/writing-tools"
echo "  /home/jeremiahai/writing-draft"
echo
echo "No packages were installed."
echo "No services were changed."
