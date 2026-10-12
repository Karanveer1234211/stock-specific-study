"""
restore_frozen_file.py v1 (2026-10-12)

The paper pipeline refused to run: "frozen files changed since the freeze:
['code/STAGE_C_DECLARATION.json']". This tool checks whether the change is only
line endings / a final line break / a byte-order mark - what an editor such as
PyCharm does when it re-saves a file - and, ONLY if one of those variants
reproduces the frozen fingerprint exactly, writes that variant back. The
changed copy is kept beside it. If no variant matches, the content itself
changed and nothing is written.

    python restore_frozen_file.py            (STAGE_C_DECLARATION.json)
    python restore_frozen_file.py OTHER.json
"""
import datetime as dt
import hashlib
import itertools
import json
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
NAME = sys.argv[1] if len(sys.argv) > 1 else "STAGE_C_DECLARATION.json"
KNOWN = {"STAGE_C_DECLARATION.json": "e945f62dd321625c"}   # fingerprint in the bundle manifest
HEX = re.compile(r"[0-9a-fA-F]{16,64}")


def registry_hashes():
    root = os.environ.get("CACHE_DAILY_ROOT")
    if not root:
        return None, []
    p = Path(root) / "panel_oc" / "frozen" / "FROZEN_ENGINES.json"
    if not p.exists():
        return p, []
    found = set()

    def walk(o, hit=False):
        if isinstance(o, dict):
            here = hit or any(NAME in str(k) or NAME in str(v) for k, v in o.items() if not isinstance(v, (dict, list)))
            for k, v in o.items():
                if isinstance(v, str) and HEX.fullmatch(v) and (here or NAME in str(k)):
                    found.add(v.lower())
                walk(v, NAME in str(k))
        elif isinstance(o, list):
            for v in o:
                walk(v, hit)

    walk(json.loads(p.read_text(encoding="utf-8")))
    return p, sorted(found)


def variants(raw: bytes):
    yield "unchanged", raw
    body = raw[3:] if raw.startswith(b"\xef\xbb\xbf") else raw
    lf = body.replace(b"\r\n", b"\n")
    for bom, style, eof in itertools.product((False, True), ("LF", "CRLF"), ("none", "one")):
        t = lf.rstrip(b"\r\n")
        if eof == "one":
            t += b"\n"
        if style == "CRLF":
            t = t.replace(b"\n", b"\r\n")
        if bom:
            t = b"\xef\xbb\xbf" + t
        yield f"{style} line endings, {'a final line break' if eof == 'one' else 'no final line break'}{', BOM' if bom else ''}", t


def main() -> int:
    path = next((p for p in (HERE / "open_close" / NAME, HERE / NAME) if p.exists()), None)
    if path is None:
        print(f"NOT FOUND: {NAME} in {HERE / 'open_close'} or {HERE}")
        return 2
    reg_path, reg = registry_hashes()
    targets = reg + ([KNOWN[NAME]] if NAME in KNOWN else [])
    raw = path.read_bytes()
    now = hashlib.sha256(raw).hexdigest()
    print(f"file      : {path}")
    print(f"modified  : {dt.datetime.fromtimestamp(path.stat().st_mtime):%Y-%m-%d %H:%M:%S}")
    print(f"sha256    : {now}")
    print(f"frozen    : {', '.join(targets) or 'none found'}  (registry: {reg_path or 'CACHE_DAILY_ROOT not set'})")
    if not targets:
        print("NOT CHECKED: no frozen fingerprint to compare against.")
        return 2
    for label, b in variants(raw):
        h = hashlib.sha256(b).hexdigest()
        if any(h.startswith(t) for t in targets):
            if b == raw:
                print("ALREADY MATCHES the frozen fingerprint - nothing to restore.")
                return 0
            keep = path.with_name(path.name + f".changed_{dt.datetime.now():%Y%m%d_%H%M%S}")
            keep.write_bytes(raw)
            path.write_bytes(b)
            assert any(hashlib.sha256(path.read_bytes()).hexdigest().startswith(t) for t in targets)
            print(f"RESTORED  : only the formatting had changed; written back with {label}.")
            print(f"            it now matches the frozen fingerprint. The changed copy is kept as {keep.name}")
            return 0
    print("NOT RESTORED: the content itself changed (not just line endings). Nothing was written.")
    print("              Restore this one file from the bundle zip you installed it from.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
