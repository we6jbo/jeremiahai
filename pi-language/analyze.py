#!/usr/bin/env python3
import argparse, datetime, json, pathlib, re, shutil, sqlite3, subprocess, sys, tempfile

ROOT = pathlib.Path("/home/jeremiahai/language")
RULES = ROOT/"learned_rules.json"
DICT = ROOT/"personal_dictionary.txt"
DB = ROOT/"mistakes.db"

def run(args, input_text=None, timeout=75):
    try:
        return subprocess.run(args, input=input_text, text=True, capture_output=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return subprocess.CompletedProcess(args, 124, "", f"TIMEOUT after {timeout}s")

def init_db():
    con = sqlite3.connect(DB)
    con.execute("""CREATE TABLE IF NOT EXISTS mistakes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        rule_id TEXT,
        category TEXT,
        observed TEXT,
        suggestion TEXT,
        seen_at TEXT
    )""")
    con.commit()
    return con

def load_rules():
    try:
        return json.loads(RULES.read_text()).get("rules", [])
    except Exception:
        return []

def ignored_words():
    if not DICT.exists():
        return set()
    return {x.strip().lower() for x in DICT.read_text().splitlines() if x.strip() and not x.startswith("#")}

def learned_findings(text, con):
    out=[]
    for rule in load_rules():
        if not rule.get("enabled", True):
            continue
        rid=rule.get("id","")
        cat=rule.get("category","writing")
        expl=rule.get("explanation","")
        suggestion=rule.get("suggestion","")
        if rule.get("wrong"):
            pat=r"(?<![\w'])"+re.escape(rule["wrong"])+r"(?![\w'])"
        elif rule.get("pattern"):
            pat=rule["pattern"]
        else:
            continue
        try:
            matches=list(re.finditer(pat,text,re.I))
        except re.error:
            continue
        for m in matches:
            observed=m.group(0)
            out.append({
                "source":"Jeremiah learned rules",
                "category":cat,
                "observed":observed,
                "suggestion":suggestion,
                "explanation":expl,
                "offset":m.start()
            })
            con.execute(
                "INSERT INTO mistakes(rule_id,category,observed,suggestion,seen_at) VALUES(?,?,?,?,?)",
                (rid,cat,observed,suggestion,datetime.datetime.now(datetime.timezone.utc).isoformat())
            )
    con.commit()
    return out

def hunspell_findings(text):
    exe=shutil.which("hunspell")
    if not exe:
        return [], "Hunspell unavailable"
    miss=run([exe,"-l","-d","en_US"],text,45)
    if miss.returncode not in (0,1):
        return [], "Hunspell error"
    words=sorted({w.strip() for w in miss.stdout.splitlines() if w.strip()})
    ignores=ignored_words()
    findings=[]
    for word in words:
        if word.lower() in ignores:
            continue
        sug=run([exe,"-a","-d","en_US"],word+"\n",20)
        suggestions=[]
        for line in sug.stdout.splitlines():
            if line.startswith("&") and ":" in line:
                suggestions=[x.strip() for x in line.split(":",1)[1].split(",") if x.strip()][:5]
                break
        findings.append({
            "source":"Hunspell",
            "category":"spelling",
            "observed":word,
            "suggestion":suggestions[0] if suggestions else "",
            "alternatives":suggestions,
            "explanation":"Type the correction yourself, then analyze again."
        })
    return findings, "Hunspell completed"

def languagetool_findings(text):
    exe=shutil.which("languagetool-commandline") or shutil.which("languagetool")
    if not exe:
        return [], "LanguageTool unavailable"
    with tempfile.NamedTemporaryFile("w",suffix=".txt",delete=False) as f:
        f.write(text); path=f.name
    try:
        r=run([exe,path],timeout=90)
        raw=(r.stdout or "") + ("\n"+r.stderr if r.stderr else "")
        # Preserve LT's own readable output rather than pretending to fully parse every version.
        return ([{"source":"LanguageTool","category":"grammar","raw":raw.strip()}]
                if raw.strip() else []), "LanguageTool completed"
    finally:
        pathlib.Path(path).unlink(missing_ok=True)

def vale_findings(text):
    exe=shutil.which("vale")
    if not exe:
        return [], "Vale unavailable"
    with tempfile.NamedTemporaryFile("w",suffix=".md",delete=False) as f:
        f.write(text); path=f.name
    try:
        r=run([exe,path],timeout=60)
        raw=(r.stdout or "") + ("\n"+r.stderr if r.stderr else "")
        return ([{"source":"Vale","category":"style","raw":raw.strip()}]
                if raw.strip() else []), "Vale completed"
    finally:
        pathlib.Path(path).unlink(missing_ok=True)

def markdown_report(findings, statuses):
    lines=["# JeremiahAI Pi Language Coach",""]
    for s in statuses:
        lines.append(f"- {s}")
    lines.append("")
    if not findings:
        lines += ["No issues were found by the available Pi checks.",""]
        return "\n".join(lines)
    for i,f in enumerate(findings,1):
        lines += [f"## {i}. {f.get('source','Coach')} — {f.get('category','writing')}"]
        if f.get("observed"):
            lines.append(f"**Found:** `{f['observed']}`")
        if f.get("suggestion"):
            lines.append(f"**Correct/suggested text:** `{f['suggestion']}`")
        if f.get("alternatives"):
            lines.append("**Other possibilities:** "+", ".join(f["alternatives"][1:]))
        if f.get("explanation"):
            lines.append(f"**Why:** {f['explanation']}")
        if f.get("raw"):
            lines += ["","```text",f["raw"],"```"]
        lines.append("")
    lines += ["JeremiahAI does not auto-apply these fixes. Make the edit yourself and analyze again.",""]
    return "\n".join(lines)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--json", action="store_true")
    args=ap.parse_args()
    p=pathlib.Path(args.file)
    if not p.exists():
        print("Input file not found.", file=sys.stderr); return 2
    raw=p.read_text()
    try:
        obj=json.loads(raw)
        text=obj.get("body", raw) if isinstance(obj,dict) else raw
    except Exception:
        text=raw

    con=init_db()
    findings=learned_findings(text,con)
    statuses=["Jeremiah learned rules completed"]

    f,s=hunspell_findings(text); findings+=f; statuses.append(s)
    f,s=languagetool_findings(text); findings+=f; statuses.append(s)
    f,s=vale_findings(text); findings+=f; statuses.append(s)

    if args.json:
        print(json.dumps({"statuses":statuses,"findings":findings},indent=2,ensure_ascii=False))
    else:
        print(markdown_report(findings,statuses))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
