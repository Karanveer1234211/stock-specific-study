"""
find_frozen_copy.py v1 (2026-10-12)

STAGE_C_DECLARATION.json in open_close\ was overwritten (modified 12 Oct 01:13), so the
paper pipeline's freeze check stops at step 3. This looks for the ORIGINAL - the copy
whose SHA-256 starts with the frozen fingerprint e945f62dd321625c - in loose files and
inside every .zip under your Downloads, Desktop, Documents, the PyCharmMiscProject
folder and the freeze folder. If it finds one, it puts it back (the overwritten copy is
kept beside it). If it finds none, it writes nothing.

    python find_frozen_copy.py
"""
import datetime as dt
import hashlib
import os
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
NAME = "STAGE_C_DECLARATION.json"
EXPECT = (sys.argv[sys.argv.index("--expect") + 1] if "--expect" in sys.argv else "e945f62dd321625c").lower()
TARGET = HERE / "open_close" / NAME


def roots():
    home = Path(os.environ.get("USERPROFILE") or Path.home())
    out = [home / "Downloads", home / "Desktop", home / "Documents", HERE.parent]
    if os.environ.get("CACHE_DAILY_ROOT"):
        out.append(Path(os.environ["CACHE_DAILY_ROOT"]) / "panel_oc" / "frozen")
    return [r for r in dict.fromkeys(out) if r.exists()]


def wanted(name: str) -> bool:
    b = name.replace("\\", "/").rsplit("/", 1)[-1].lower()
    return b.startswith("stage_c_declaration") and b.endswith(".json")


def candidates():
    for r in roots():
        for dirpath, dirnames, files in os.walk(r):
            dirnames[:] = [d for d in dirnames if d not in (".git", "__pycache__", "node_modules", ".venv", "venv")]
            for f in files:
                p = Path(dirpath) / f
                try:
                    if wanted(f):
                        yield str(p), p.read_bytes()
                    elif f.lower().endswith(".zip") and p.stat().st_size < 500 * 2**20:
                        with zipfile.ZipFile(p) as z:
                            for m in z.namelist():
                                if wanted(m):
                                    yield f"{p} -> {m}", z.read(m)
                except Exception:
                    continue


def main() -> int:
    if not TARGET.exists():
        print(f"NOT FOUND: {TARGET}")
        return 2
    now = TARGET.read_bytes()
    print(f"current   : {TARGET}  sha256 {hashlib.sha256(now).hexdigest()[:16]}"
          f"  modified {dt.datetime.fromtimestamp(TARGET.stat().st_mtime):%Y-%m-%d %H:%M}")
    if hashlib.sha256(now).hexdigest().startswith(EXPECT):
        print("ALREADY THE FROZEN VERSION - nothing to do.")
        return 0
    print(f"searching : {', '.join(str(r) for r in roots())}")
    seen = 0
    for where, data in candidates():
        seen += 1
        if hashlib.sha256(data).hexdigest().startswith(EXPECT):
            keep = TARGET.with_name(NAME + f".overwritten_{dt.datetime.now():%Y%m%d_%H%M%S}")
            keep.write_bytes(now)
            TARGET.write_bytes(data)
            assert hashlib.sha256(TARGET.read_bytes()).hexdigest().startswith(EXPECT)
            print(f"RESTORED  : the frozen original (sha256 {EXPECT}...) came from")
            print(f"            {where}")
            print(f"            the overwritten copy is kept as {keep.name}")
            return 0
    print(f"NOT FOUND : {seen} other cop{'y' if seen == 1 else 'ies'} of {NAME} checked; none is the frozen original.")
    print("            Nothing was written.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
