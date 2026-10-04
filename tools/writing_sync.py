#!/usr/bin/env python3
import hashlib, json, os, pathlib, re, shutil, subprocess, sys, tempfile, time

CACHE = pathlib.Path.home()/".jeremiahai"/"writing-cache"
STATE = CACHE/".sync-state.json"
TOMBSTONES = CACHE/".trash"/"tombstones.json"
REMOTE_TRASH = "/home/jeremiahai/www/writing/.trash"
REMOTE_VERSIONS = "/home/jeremiahai/vKEeQJs/versions"
REMOTE_ALIAS = os.environ.get("JEREMIAHAI_PI_ALIAS", "jeremiahai-pi")
REMOTE_DIR = "/home/jeremiahai/www/writing/documents"
EXT = ".jaiw"

def sh(args, input_text=None, timeout=15):
    try:
        return subprocess.run(args, input=input_text, text=True, capture_output=True, timeout=timeout)
    except subprocess.TimeoutExpired as e:
        def _txt(v):
            if v is None: return ""
            if isinstance(v, bytes): return v.decode("utf-8", "replace")
            return str(v)
        return subprocess.CompletedProcess(
            args=args,
            returncode=124,
            stdout=_txt(e.stdout),
            stderr=(_txt(e.stderr) + ("\n" if e.stderr else "") + f"TIMEOUT after {timeout} seconds")
        )

def sha(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for b in iter(lambda:f.read(65536), b""): h.update(b)
    return h.hexdigest()

def load_state():
    try: return json.loads(STATE.read_text())
    except Exception: return {}

def load_tombstones():
    try:
        data=json.loads(TOMBSTONES.read_text())
        return data if isinstance(data,dict) else {}
    except Exception:
        return {}

def save_tombstones(t):
    TOMBSTONES.parent.mkdir(parents=True,exist_ok=True)
    TOMBSTONES.write_text(json.dumps(t,indent=2))

def save_state(s):
    CACHE.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(s, indent=2))

def remote_ok():
    r=sh(["ssh","-o","BatchMode=yes","-o","ConnectTimeout=4","-o","ConnectionAttempts=1",REMOTE_ALIAS,"printf OK"],timeout=7)
    return r.returncode==0 and r.stdout=="OK"

def remote_used_pct():
    r=sh(["ssh","-o","BatchMode=yes","-o","ConnectTimeout=4","-o","ConnectionAttempts=1",REMOTE_ALIAS,
          "df -P /home/jeremiahai/www | awk 'NR==2{gsub(/%/,\"\",$5);print $5}'"],timeout=8)
    try: return int(r.stdout.strip())
    except Exception: return None

def remote_list():
    cmd=f"mkdir -p {REMOTE_DIR}; find {REMOTE_DIR} -maxdepth 1 -type f -name '*{EXT}' -printf '%f\\n' | sort"
    r=sh(["ssh","-o","BatchMode=yes","-o","ConnectTimeout=4","-o","ConnectionAttempts=1",REMOTE_ALIAS,cmd],timeout=10)
    return [x for x in r.stdout.splitlines() if x.endswith(EXT)] if r.returncode==0 else []

def remote_sha(name):
    r=sh(["ssh","-o","BatchMode=yes","-o","ConnectTimeout=4","-o","ConnectionAttempts=1",REMOTE_ALIAS,
          f"test -f {REMOTE_DIR}/{name} && sha256sum {REMOTE_DIR}/{name} | awk '{{print $1}}' || true"],timeout=8)
    return r.stdout.strip()

def pull(name):
    CACHE.mkdir(parents=True, exist_ok=True)
    r=sh(["scp","-q",f"{REMOTE_ALIAS}:{REMOTE_DIR}/{name}",str(CACHE/name)],timeout=15)
    return r.returncode==0

def push(name):
    used=remote_used_pct()
    if used is not None and used >= 50:
        print(f"REFUSED upload {name}: Pi disk usage is {used}% (limit is below 50%).")
        return False
    r=sh(["ssh","-o","BatchMode=yes","-o","ConnectTimeout=4","-o","ConnectionAttempts=1",REMOTE_ALIAS,f"mkdir -p {REMOTE_DIR}"],timeout=8)
    if r.returncode!=0: return False
    remote_preserve_before_overwrite(name)
    r=sh(["scp","-q",str(CACHE/name),f"{REMOTE_ALIAS}:{REMOTE_DIR}/{name}"],timeout=15)
    return r.returncode==0

def conflict_copy(path, label):
    stamp=time.strftime("%Y%m%d-%H%M%S")
    dest=path.with_name(path.stem+f".conflict-{label}-{stamp}"+EXT)
    shutil.copy2(path,dest)
    return dest

def remote_soft_delete(name):
    stamp=time.strftime("%Y%m%d-%H%M%S")
    cmd=(
        f"mkdir -p {REMOTE_TRASH}; "
        f"if test -f {REMOTE_DIR}/{name}; then "
        f"mv {REMOTE_DIR}/{name} {REMOTE_TRASH}/{stamp}-{name}; fi"
    )
    r=sh(["ssh","-o","BatchMode=yes","-o","ConnectTimeout=4","-o","ConnectionAttempts=1",REMOTE_ALIAS,cmd],timeout=10)
    return r.returncode==0

def remote_preserve_before_overwrite(name):
    digest=remote_sha(name)
    if not digest:
        return True
    stamp=time.strftime("%Y%m%d-%H%M%S")
    safe=re.sub(r"[^A-Za-z0-9_.-]+","_",name)
    target=f"{REMOTE_VERSIONS}/{safe}"
    cmd=(
        f"mkdir -p {target}; "
        f"cp -p {REMOTE_DIR}/{name} {target}/{stamp}-{digest}.jaiw"
    )
    r=sh(["ssh","-o","BatchMode=yes","-o","ConnectTimeout=4","-o","ConnectionAttempts=1",REMOTE_ALIAS,cmd],timeout=10)
    return r.returncode==0

def sync_all():
    CACHE.mkdir(parents=True, exist_ok=True)
    state=load_state()
    if not remote_ok():
        print("PI UNAVAILABLE: cache retained; no data lost.")
        return 2

    tombstones=load_tombstones()
    for name in sorted(tombstones):
        if remote_sha(name):
            if remote_soft_delete(name):
                print("REMOTE SOFT-DELETED",name)
            else:
                print("WARNING: could not soft-delete remote",name)

    local={p.name for p in CACHE.glob(f"*{EXT}") if ".conflict-" not in p.name and p.name not in tombstones}
    remote=set(remote_list())
    names=sorted(local|remote)

    for name in names:
        lp=CACHE/name
        lh=sha(lp) if lp.exists() else ""
        rh=remote_sha(name)
        last=state.get(name,"")

        if lh and rh and lh==rh:
            state[name]=lh
            print("OK",name)
        elif not lh and rh:
            if pull(name):
                state[name]=sha(lp)
                print("PULLED",name)
        elif lh and not rh:
            if push(name):
                state[name]=lh
                print("PUSHED",name)
        elif lh and rh:
            if last==lh and last!=rh:
                if pull(name):
                    state[name]=sha(lp)
                    print("REMOTE NEWER -> PULLED",name)
            elif last==rh and last!=lh:
                if push(name):
                    state[name]=lh
                    print("LOCAL NEWER -> PUSHED",name)
            else:
                local_conf=conflict_copy(lp,"t14")
                with tempfile.TemporaryDirectory() as td:
                    temp=pathlib.Path(td)/name
                    rr=sh(["scp","-q",f"{REMOTE_ALIAS}:{REMOTE_DIR}/{name}",str(temp)],timeout=15)
                    if rr.returncode==0:
                        remote_conf=CACHE/(lp.stem+f".conflict-pi-{time.strftime('%Y%m%d-%H%M%S')}"+EXT)
                        shutil.copy2(temp,remote_conf)
                print("CONFLICT",name)
                print("  preserved local:",local_conf.name)
                print("  preserved Pi copy in cache; merge manually/Vibe.")
    save_state(state)
    return 0

if __name__=="__main__":
    sys.exit(sync_all())
