#!/usr/bin/env python3
import json, pathlib, re
ROOT=pathlib.Path("/home/jeremiahai/language")
STYLE=ROOT/"vale"/"styles"/"Jeremiah"
STYLE.mkdir(parents=True,exist_ok=True)
data=json.loads((ROOT/"learned_rules.json").read_text())
count=0
for rule in data.get("rules",[]):
    if not rule.get("enabled",True): continue
    wrong=rule.get("wrong")
    suggestion=rule.get("suggestion")
    if not wrong or not suggestion: continue
    name=re.sub(r"[^A-Za-z0-9]+","_",rule.get("id","rule")).strip("_") or "rule"
    (STYLE/f"{name}.yml").write_text(
f"""extends: substitution
message: 'JeremiahAI learned rule: consider "%s" instead of "%s".'
level: suggestion
ignorecase: true
swap:
  '{wrong}': '{suggestion}'
""" % (suggestion, wrong))
    count+=1
print(f"Generated {count} Jeremiah Vale rule(s) in {STYLE}")
