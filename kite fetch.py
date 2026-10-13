"""
intraday_lab / kite_fetch.py
Download 1-minute candles from Kite Connect into <ROOT>/minute/<SYMBOL>.parquet.
Resumable: re-running only fetches days after the last stored bar.

Auth (same key/token you use for Daily_cache_v27):
  set KITE_API_KEY=xxxx
  set KITE_ACCESS_TOKEN=yyyy        (or KITE_TOKEN_FILE=path to a file holding the token)

Limits respected: minute candles are requested in 60-day chunks, ~3 requests/second.
Kite does NOT serve expired futures, so we fetch the NIFTY index itself and use it as the
price proxy for NIFTY futures (costs are still charged as futures).
"""
import os
import time
import datetime as dt
from pathlib import Path
import pandas as pd
import config
import data

CHUNK_DAYS = 60
PAUSE = 0.35


DEFAULT_TOKEN_FILE = Path(__file__).resolve().parent.parent / "kite_token.json"   # written by Kiteconnect.py


def _read_token_file(path):
    """Plain-text token, or JSON with access_token (and optionally api_key)."""
    txt = Path(path).read_text(encoding="utf-8").strip()
    if not txt.startswith("{"):
        return txt, None
    import json
    d = json.loads(txt)
    tok = d.get("access_token") or d.get("token") or d.get("accessToken")
    key = d.get("api_key") or d.get("apiKey")
    if not tok:
        raise SystemExit(f"{path} has no access_token field. Keys found: {list(d)}")
    return tok, key


def _kite():
    from kiteconnect import KiteConnect
    key = os.environ.get("KITE_API_KEY")
    tok = os.environ.get("KITE_ACCESS_TOKEN")
    src = "KITE_ACCESS_TOKEN"
    if not tok:
        f = os.environ.get("KITE_TOKEN_FILE") or (DEFAULT_TOKEN_FILE if DEFAULT_TOKEN_FILE.exists() else None)
        if f:
            tok, file_key = _read_token_file(f)
            key = key or file_key
            src = str(f)
    if not key or not tok:
        raise SystemExit("Need the API key and an access token: set KITE_API_KEY, and either run "
                         "Kiteconnect.py (writes kite_token.json) or set KITE_ACCESS_TOKEN.")
    print(f"Using access token from {src}")
    k = KiteConnect(api_key=key)
    k.set_access_token(tok)
    return k


def _tokens(kite, symbols):
    inst = pd.DataFrame(kite.instruments("NSE"))
    inst = inst[inst["segment"].isin(["NSE", "INDICES"])]
    m = dict(zip(inst["tradingsymbol"], inst["instrument_token"]))
    out, missing = {}, []
    for s in symbols:
        (out.__setitem__(s, int(m[s])) if s in m else missing.append(s))
    if missing:
        print("Not found on NSE (renamed/delisted?):", ", ".join(missing))
    return out


def fetch_symbol(kite, symbol, token, start):
    f = data.sym_file(symbol)
    old = None
    if f.exists():
        old = pd.read_parquet(f)
        start = (pd.to_datetime(old.index.max()).date() + dt.timedelta(days=1))
    end = dt.date.today()
    frames = []
    d = start
    while d <= end:
        e = min(d + dt.timedelta(days=CHUNK_DAYS - 1), end)
        for attempt in range(4):
            try:
                rows = kite.historical_data(token, d, e, "minute", continuous=False, oi=False)
                break
            except Exception as ex:
                if attempt == 3:
                    raise
                print(f"    retry {symbol} {d}: {ex}")
                time.sleep(2 * (attempt + 1))
        if rows:
            frames.append(pd.DataFrame(rows))
        d = e + dt.timedelta(days=1)
        time.sleep(PAUSE)
    if not frames:
        print(f"  {symbol}: up to date")
        return
    new = pd.concat(frames)
    new["date"] = pd.to_datetime(new["date"])
    if new["date"].dt.tz is not None:
        new["date"] = new["date"].dt.tz_convert("Asia/Kolkata").dt.tz_localize(None)
    new = new.set_index("date")[["open", "high", "low", "close", "volume"]]
    allx = pd.concat([old, new]) if old is not None else new
    allx = allx[~allx.index.duplicated(keep="last")].sort_index()
    f.parent.mkdir(parents=True, exist_ok=True)
    allx.to_parquet(f)
    print(f"  {symbol}: +{len(new):,} bars, total {len(allx):,} ({allx.index.min().date()} -> {allx.index.max().date()})")


def fetch(symbols, start=None):
    start = pd.to_datetime(start or config.FETCH_START).date()
    kite = _kite()
    symbols = [config.INDEX_SYMBOL, config.BANK_INDEX_SYMBOL] + [s for s in symbols if s not in
                                                                  (config.INDEX_SYMBOL, config.BANK_INDEX_SYMBOL)]
    toks = _tokens(kite, symbols)
    for i, (s, t) in enumerate(toks.items()):
        print(f"[{i+1}/{len(toks)}] {s}")
        fetch_symbol(kite, s, t, start)
