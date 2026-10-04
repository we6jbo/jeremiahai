#!/usr/bin/env python3
# zrIyFl4vKEeQJsoH78vaA9seiGUlYAUY4pOnp3lbaQ67XPiDP5gh5wFwglmJjUD
import argparse, hashlib, json, os, pathlib, shutil, sqlite3, time

MARKER = 'zrIyFl4vKEeQJsoH78vaA9seiGUlYAUY4pOnp3lbaQ67XPiDP5gh5wFwglmJjUD'
PI_ROOT = pathlib.Path("/home/jeremiahai")
VC_DIR = PI_ROOT / ".zrIyFl4vK"
DB = VC_DIR / "version-control.db"
MD = VC_DIR / "version-control.md"
BACKUP = PI_ROOT / "vKEeQJs"

TRACK_ROOTS = [
    PI_ROOT / "www" / "writing",
    PI_ROOT / "writing-tools",
    PI_ROOT / "writing-draft",
]

def md5(path):
    h=hashlib.md5()
    with open(path,"rb") as f:
        for b in iter(lambda:f.read(1024*1024), b""):
            h.update(b)
    return h.hexdigest()

def eligible(path):
    try:
        return path.is_file() and not str(path).startswith(str(VC_DIR)) and not str(path).startswith(str(BACKUP))
    except OSError:
        return False

def iter_files():
    seen=set()
    for root in TRACK_ROOTS:
        if root.exists():
            for p in root.rglob("*"):
                if eligible(p):
                    rp=str(p.resolve())
                    if rp not in seen:
                        seen.add(rp); yield p

def ensure_db():
    VC_DIR.mkdir(parents=True,exist_ok=True)
    BACKUP.mkdir(parents=True,exist_ok=True)
    con=sqlite3.connect(DB)
    con.execute("""CREATE TABLE IF NOT EXISTS files(
      path TEXT PRIMARY KEY,
      md5 TEXT NOT NULL,
      size INTEGER NOT NULL,
      mtime REAL NOT NULL,
      backup_path TEXT,
      marker TEXT NOT NULL,
      last_seen TEXT NOT NULL
    )""")
    con.execute("""CREATE TABLE IF NOT EXISTS history(
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      path TEXT NOT NULL,
      md5 TEXT NOT NULL,
      observed_at TEXT NOT NULL,
      action TEXT NOT NULL
    )""")
    con.commit()
    return con

def backup_path_for(path):
    rel=str(path).lstrip("/").replace("/", "__")
    return BACKUP / rel

def register(path, con):
    digest=md5(path)
    st=path.stat()
    bp=backup_path_for(path)
    changed=True
    row=con.execute("SELECT md5,backup_path FROM files WHERE path=?",(str(path),)).fetchone()
    if row and row[0]==digest:
        changed=False
    if changed or not bp.exists():
        shutil.copy2(path,bp)
    now=time.strftime("%Y-%m-%dT%H:%M:%S%z")
    con.execute("""INSERT INTO files(path,md5,size,mtime,backup_path,marker,last_seen)
                   VALUES(?,?,?,?,?,?,?)
                   ON CONFLICT(path) DO UPDATE SET
                     md5=excluded.md5,size=excluded.size,mtime=excluded.mtime,
                     backup_path=excluded.backup_path,marker=excluded.marker,last_seen=excluded.last_seen""",
                (str(path),digest,st.st_size,st.st_mtime,str(bp),MARKER,now))
    con.execute("INSERT INTO history(path,md5,observed_at,action) VALUES(?,?,?,?)",
                (str(path),digest,now,"register" if not row else ("update" if changed else "verify")))
    return digest,changed

def write_md(con):
    rows=con.execute("SELECT path,md5,size,backup_path,last_seen FROM files ORDER BY path").fetchall()
    lines=[
      f"# JeremiahAI Version Control {MARKER}",
      "",
      "This file is generated from version-control.db.",
      "",
      "| Path | MD5 | Size | Backup | Last seen |",
      "|---|---|---:|---|---|",
    ]
    for p,d,s,b,t in rows:
        lines.append(f"| `{p}` | `{d}` | {s} | `{b or ''}` | {t} |")
    MD.write_text("\n".join(lines)+"\n")

def audit(con):
    issues=[]
    for p,d,b in con.execute("SELECT path,md5,backup_path FROM files ORDER BY path"):
        path=pathlib.Path(p)
        if not path.exists():
            issues.append((p,"missing",d,b))
        else:
            cur=md5(path)
            if cur!=d:
                issues.append((p,"modified",d,b))
    return issues

def restore(con,path_text):
    row=con.execute("SELECT md5,backup_path FROM files WHERE path=?",(path_text,)).fetchone()
    if not row: raise SystemExit("Not tracked")
    expected,bp=row
    bp=pathlib.Path(bp)
    target=pathlib.Path(path_text)
    if not bp.exists(): raise SystemExit("Backup missing")
    target.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(bp,target)
    if md5(target)!=expected: raise SystemExit("Restore hash mismatch")
    print("RESTORED",target)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("action",choices=["register-all","audit","restore"])
    ap.add_argument("path",nargs="?")
    a=ap.parse_args()
    con=ensure_db()
    if a.action=="register-all":
        count=0
        for p in iter_files():
            digest,changed=register(p,con); count+=1
            print(("BACKED-UP" if changed else "OK"),digest,p)
        con.commit(); write_md(con)
        print("TRACKED",count)
        print("DB",DB)
        print("SUMMARY",MD)
    elif a.action=="audit":
        issues=audit(con)
        if not issues:
            print("PASS: all tracked files match recorded MD5 values")
        else:
            for p,status,d,b in issues:
                print("ISSUE",status,p,"expected",d,"backup",b or "")
        print("ISSUES",len(issues))
    elif a.action=="restore":
        if not a.path: raise SystemExit("restore requires an exact tracked path")
        restore(con,a.path)
        con.commit(); write_md(con)

if __name__=="__main__":
    main()
