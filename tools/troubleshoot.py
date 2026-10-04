#!/usr/bin/env python3
# zrIyFl4vKEeQJsoH78vaA9seiGUlYAUY4pOnp3lbaQ67XPiDP5gh5wFwglmJjUD
import json, pathlib, subprocess, time

MARKER="zrIyFl4vKEeQJsoH78vaA9seiGUlYAUY4pOnp3lbaQ67XPiDP5gh5wFwglmJjUD"
ROOT=pathlib.Path("/home/we6jbo/jeremiahai-troubeshooting")
STATE=ROOT/"reports"
TMP=pathlib.Path("/tmp/jeremiahai-troubleshooting")
FIX=TMP/"fix.sh"

ROOT.mkdir(parents=True,exist_ok=True)
STATE.mkdir(parents=True,exist_ok=True)
TMP.mkdir(parents=True,exist_ok=True)

def run(cmd):
    p=subprocess.run(cmd,text=True,capture_output=True)
    return p.returncode,(p.stdout+p.stderr)

checks=[]
for name,cmd in [
    ("hostname",["hostname"]),
    ("project-files",["bash","-lc","find /home/we6jbo/Projects/jeremiahai -maxdepth 2 -type f | sort | head -200"]),
    ("journal",["bash","-lc","journalctl -t jeremiahai -n 200 --no-pager 2>&1"]),
    ("disk",["df","-h","/home/we6jbo"]),
    ("cache",["bash","-lc","find /home/we6jbo/.jeremiahai/writing-cache -maxdepth 1 -type f -name '*.jaiw' -printf '%f %s bytes\\n' 2>/dev/null | sort"]),
]:
    rc,out=run(cmd)
    checks.append({"name":name,"rc":rc,"output":out[-20000:]})

stamp=time.strftime("%Y%m%d-%H%M%S")
report=STATE/f"report-{stamp}.json"
report.write_text(json.dumps({"marker":MARKER,"generated_at":stamp,"checks":checks},indent=2))

fix = """#!/usr/bin/env bash
# zrIyFl4vKEeQJsoH78vaA9seiGUlYAUY4pOnp3lbaQ67XPiDP5gh5wFwglmJjUD
set -euo pipefail
[[ "$(hostname)" == "we6jbo" ]] || { echo "ABORT: T14 only."; exit 1; }
[[ -f /opt/z/z.txt ]] || { echo "ABORT: /opt/z/z.txt missing."; exit 1; }

echo "JeremiahAI troubleshooting helper"
echo "No automatic repair has been selected."
echo "Review the Troubleshooting tab/report first."
echo "This script intentionally makes no changes."
"""
FIX.write_text(fix)
FIX.chmod(0o755)

print("REPORT",report)
print("FIX_SCRIPT",FIX)
print("MARKER",MARKER)
