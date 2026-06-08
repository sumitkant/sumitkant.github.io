---
name: tradingview-data
description: >
  Fetch market data from TradingView via WebSocket for any ticker — Indian equities,
  NSE/BSE stocks, crypto, forex, indices, and commodities. Pulls OHLCV
  (Open, High, Low, Close, Volume) candlestick/bar data, intraday tick data, raw
  market data, fundamental/financial data (valuation ratios, margins, analyst
  estimates, price targets, earnings history, balance-sheet & cash-flow statement
  fields), and per-symbol news flow. Use this skill whenever the user wants to pull
  historical bars, intraday data, company fundamentals, financial statements,
  analyst recommendations/price targets, earnings data, or news headlines from
  TradingView. Triggers include: "fetch OHLCV from TradingView", "get candlestick
  data", "download historical data", "pull intraday data", "get market data for
  [ticker]", "fetch NSE/BSE data", "get price history", "get fundamentals for
  [ticker]", "fetch financials", "get P/E / margins / market cap", "analyst price
  target", "earnings history", "get TradingView news" — even if the user just says
  "get me some stock data" without naming TradingView explicitly.
---

# TradingView Data Skill

Fetches market data from TradingView for any supported symbol. Covers three data
families:

1. **OHLCV bars** — candlestick/bar series (equities, crypto, forex, indices, commodities).
2. **Fundamentals** — valuation ratios, margins, returns, analyst estimates, price
   targets, earnings history, and full statement fields (~900 fields available).
3. **News** — per-symbol headline flow.

The OHLCV and fundamentals functions both run over TradingView's WebSocket API
(`wss://data.tradingview.com/socket.io/websocket`). News uses a plain REST endpoint.

All functions live in `scripts/tvwebsocket.py` (the OHLCV code is also inlined below
as a standalone template).

---

## Dependencies

Install before first use:
```bash
pip install websocket-client pandas requests
```

`requests` is only needed for fundamentals auth-token derivation and for news; OHLCV
fetching needs just `websocket-client` and `pandas`.

---

## Core Concepts

### Session Architecture
TradingView uses two parallel sessions per connection:
- **Quote session** (`qs_...`): real-time price fields (lp, volume, etc.) — also carries fundamentals.
- **Chart session** (`cs_...`): OHLCV bar series data.

Both are established over a single WebSocket to `wss://data.tradingview.com/socket.io/websocket`.

### Message Protocol
All messages follow the pattern: `~m~{length}~m~{json_payload}`

```python
def prepend_header(st):
    return "~m~" + str(len(st)) + "~m~" + st
```

Server frames also include heartbeats (`~h~...`) which must be echoed back to keep
the connection alive during a fundamentals fetch.

### Resolution Codes
| Code | Meaning        |
|------|---------------|
| `1`  | 1 minute       |
| `5`  | 5 minutes      |
| `15` | 15 minutes     |
| `30` | 30 minutes     |
| `60` | 1 hour         |
| `D`  | Daily          |
| `W`  | Weekly         |
| `M`  | Monthly        |

### Ticker Formats
| Market   | Format Example          |
|----------|------------------------|
| NSE      | `NSE:RELIANCE`         |
| BSE      | `BSE:500325`           |
| NASDAQ   | `NASDAQ:AAPL`          |
| Crypto   | `BINANCE:BTCUSDT`      |
| Index    | `NSE:NIFTY`            |
| Forex    | `FX:EURUSD`            |

---

## OHLCV: Three Fetch Functions

### 1. `search_data` — Equities with Market Hours Filter
Use for **NSE/BSE stocks**. Filters bars to 9:15 AM–3:30 PM IST automatically.

```python
df = search_data(ticker="NSE:RELIANCE", resolution="15", bars=500)
```

**Returns DataFrame columns:** `epochtime, open, high, low, close, volume, datetime, time`

**When to use:** Indian equity intraday analysis, backtesting NSE/BSE strategies.

---

### 2. `fetch_raw_data` — Equities, No Time Filter
Use when you need **all bars** including pre/post-market or for non-Indian markets.

```python
df = fetch_raw_data(ticker="NASDAQ:AAPL", resolution="D", bars=365)
```

**Returns DataFrame columns:** `epochtime, open, high, low, close, volume, datetime, time`

**When to use:** Multi-market data, daily/weekly timeframes, crypto 24/7 data.

---

### 3. `search_nonstock_data` — Non-Equity Instruments
Use for **indices, forex, crypto, commodities** — instruments that don't have a volume column in the standard 5-field schema.

```python
df = search_nonstock_data(ticker="NSE:NIFTY", resolution="60", bars=200)
```

**Returns:** Same schema as above, but `volume` is set to `0`.

**When to use:** Index data (NIFTY, SENSEX), forex pairs, crypto indices.

---

## Fundamentals

Fetches the same fundamental/financial data the TradingView "financials-overview"
page shows: valuation ratios, margins, returns, per-share metrics, analyst
recommendations and price targets, earnings/revenue history, and full balance-sheet,
income-statement, and cash-flow statement fields across multiple periods
(`_fq`, `_fy`, `_ttm`, `_fh`, history variants `_fq_h`, etc.).

### ⚠️ Authentication is required for real data
The full fundamentals set is **gated behind a logged-in TradingView token**. With the
default `unauthorized_user_token` you get almost nothing back. You must supply your
own session, in one of two ways:

1. **Pass cookies** as `sessionid` (and the newer `sessionid_sign`) — the token is
   derived automatically.
2. **Pass a pre-derived `auth_token`** obtained from `get_auth_token(...)`.

**How to get the cookies:** in your browser, open DevTools → Application → Cookies →
`https://www.tradingview.com`, and copy the `sessionid` and `sessionid_sign` values.

Cookies can also be read from environment variables `TV_SESSIONID` and
`TV_SESSIONID_SIGN`, which several helpers fall back to automatically.

```bash
# PowerShell
$env:TV_SESSIONID="..."; $env:TV_SESSIONID_SIGN="..."

# bash
export TV_SESSIONID="..."; export TV_SESSIONID_SIGN="..."
```

### Functions

#### `get_auth_token(sessionid, sessionid_sign=None)`
Derives the WebSocket auth token from your logged-in cookies. Returns the token
string, or `None` if it can't be found (caller should then fall back to
`"unauthorized_user_token"`).

```python
token = get_auth_token(SESSIONID, SESSIONID_SIGN)  # -> "eyJ..." or None
```

#### `fetch_fundamentals(ticker, auth_token="unauthorized_user_token", sessionid=None, sessionid_sign=None, timeout=20, fields=None, verbose=False, debug=False)`
Opens a quote session, subscribes to `ticker`, merges every `qsd` frame the server
pushes, and returns a **dict of all fundamental fields**. Waits for the
`quote_completed` signal (or `timeout`). If `auth_token` is left at the default but
`sessionid` is provided, the token is derived automatically.

The returned dict also carries two meta keys:
- `_symbol` — the requested ticker
- `_complete` — `True` if the `quote_completed` frame arrived

```python
data = fetch_fundamentals("NASDAQ:AAPL", sessionid=SESSIONID, sessionid_sign=SESSIONID_SIGN)
print(data["price_earnings_ttm"], data["market_cap_basic"], data["recommendation_mark"])
```

By default it requests `FUNDAMENTAL_FIELDS` (≈900 fields). Pass a smaller `fields`
list to request only what you need.

#### `summarize_fundamentals(data)`
Reduces a full record to a tidy **one-row dict** of strategy-relevant fields
(`CORE_FIELDS`), and computes a couple of derived metrics:
- `target_upside_pct` — implied upside from `lp` to `price_target_average`
- `last_eps_surprise_pct` / `last_eps_period` — from the most recent reported quarter in `earnings_fq_h`

```python
row = summarize_fundamentals(data)
# {'symbol': 'NASDAQ:AAPL', 'sector': ..., 'price_earnings_ttm': ..., 'target_upside_pct': ...}
```

#### `fundamentals_to_csv(data, path)`
Writes the **full record** to a one-row CSV. Any list/dict values (e.g. earnings
history) are JSON-encoded so the CSV stays flat. Returns the path.

```python
fundamentals_to_csv(data, "AAPL_fundamentals.csv")
```

#### `fetch_many_fundamentals(tickers, auth_token="unauthorized_user_token", sessionid=None, sessionid_sign=None, timeout=20, summary=True, sleep=0.3)`
Fetches fundamentals for a list of symbols sequentially and returns a single
DataFrame. `summary=True` returns the tidy one-row-per-symbol view; `summary=False`
returns the full records. Failures are captured as a `_error` column rather than
raising. `sleep` adds a delay between symbols to avoid rate-limiting.

```python
df = fetch_many_fundamentals(
    ["NASDAQ:AAPL", "NASDAQ:MSFT", "NYSE:KO"],
    sessionid=SESSIONID, sessionid_sign=SESSIONID_SIGN,
)
```

### Field Sets
- `ALL_FIELDS` / `FUNDAMENTAL_FIELDS` — the full ≈900-field capture set, built by
  expanding every statement stem (`_STATEMENT_STEMS`) across every period suffix
  (`_STATEMENT_SUFFIXES`: `""`, `_fq`, `_fy`, `_ttm`, `_fh`, `_current`, and the
  `_*_h` history variants) and unioning with the curated `_QUOTE_FIELDS`
  (identity, price/quote, performance/momentum, size/shares, valuation,
  profitability, per-share/growth, analyst estimates, earnings calendar, dividends).
  TradingView silently ignores any field it doesn't recognise, so an over-broad
  request is safe.
- `CORE_FIELDS` — the curated subset used by `summarize_fundamentals` (sector,
  market cap, recent performance, P/E, EPS, margins, ROE, recommendation counts,
  price targets, estimates, popularity).

### Batch fetching with multiprocessing
For large universes, run fundamentals fetches in a process pool. Resolve the auth
token **once** in the parent and share it with every worker (see
`fetch_all_fundamentals.py`):

```python
import os
from time import sleep
from random import randint
from datetime import datetime
from multiprocessing import Pool

from scripts.tvwebsocket import fetch_fundamentals, fundamentals_to_csv, get_auth_token

SESSIONID = os.environ.get("TV_SESSIONID")
SESSIONID_SIGN = os.environ.get("TV_SESSIONID_SIGN")
_TOKEN = "unauthorized_user_token"

def _init_worker(token):
    global _TOKEN
    _TOKEN = token

def get_fundamentals(ticker):
    try:
        sleep(randint(100, 300) / 100)              # jitter to avoid rate limits
        data = fetch_fundamentals(ticker, auth_token=_TOKEN, timeout=20)
        if len([k for k in data if not k.startswith("_")]) == 0:
            raise RuntimeError("no fields returned (auth/symbol?)")
        fundamentals_to_csv(data, f"{ticker.split(':')[1]}_fundamentals.csv")
        sleep(randint(100, 300) / 100)
    except Exception as e:
        print(f"{datetime.now():%Y-%m-%d %H:%M:%S} > SKIPPED {ticker} due to {e}")

if __name__ == "__main__":
    ticker_list = ["NASDAQ:SNDK", "NASDAQ:MU", "NYSE:STX"]   # fill this in
    token = get_auth_token(SESSIONID, SESSIONID_SIGN) if SESSIONID else "unauthorized_user_token"
    with Pool(12, initializer=_init_worker, initargs=(token,)) as p:
        p.map(get_fundamentals, ticker_list)
```

---

## News

TradingView's news flow is a plain REST/JSON endpoint (not the WebSocket). These
helpers request the per-symbol news list and flatten every field to a DataFrame/CSV.
The list endpoint returns headline metadata; each row carries a `storyPath`/link you
can follow for the full article body. Cookies (`sessionid`, `sessionid_sign`) are
optional and fall back to the `TV_SESSIONID*` env vars.

#### `fetch_news(ticker, lang="en_IN", region="in", sessionid=None, sessionid_sign=None, client="screener", streaming=True, user_prostatus="non_pro", timeout=20, as_dataframe=True)`
Returns a flattened DataFrame (default) or the raw list of dicts. Use `region="us"`
/ `lang="en"` for the US site. A readable timestamp column (`*_dt`) is added when a
published/created epoch is present.

```python
df = fetch_news("NASDAQ:AAPL", region="us", lang="en")
```

#### `news_to_csv(ticker, path=None, **kwargs)`
Fetches news and writes all fields to CSV. Defaults the path to
`{SYMBOL}_news.csv`. Returns the path.

#### `fetch_many_news(tickers, sessionid=None, sessionid_sign=None, lang="en_IN", region="in", timeout=20)`
Fetches news for many symbols and concatenates into one DataFrame (a `_symbol`
column identifies each).

---

## Full Working Template (OHLCV)

```python
import string
import random
import json
import re
import pandas as pd
from datetime import timedelta, time
from websocket import create_connection


# ── Session generators ────────────────────────────────────────────────────────

def generate_session():
    letters = string.ascii_lowercase
    return "qs_" + ''.join(random.choice(letters) for _ in range(12))

def generate_chart_session():
    letters = string.ascii_lowercase
    return "cs_" + ''.join(random.choice(letters) for _ in range(12))


# ── WebSocket message helpers ─────────────────────────────────────────────────

def prepend_header(st):
    return "~m~" + str(len(st)) + "~m~" + st

def construct_message(func, param_list):
    return json.dumps({"m": func, "p": param_list}, separators=(',', ':'))

def send_message(ws, func, args):
    ws.send(prepend_header(construct_message(func, args)))


# ── Connection + session setup ────────────────────────────────────────────────

def new_session():
    headers = json.dumps({'Origin': 'https://data.tradingview.com'})
    ws = create_connection(
        'wss://data.tradingview.com/socket.io/websocket',
        headers=headers
    )
    return ws, generate_session(), generate_chart_session()

def send_subscription(ws, session, chart_session, ticker, resolution, bars):
    send_message(ws, "set_auth_token", ["unauthorized_user_token"])
    send_message(ws, "chart_create_session", [chart_session, ""])
    send_message(ws, "quote_create_session", [session])
    send_message(ws, "quote_set_fields", [
        session, "ch", "chp", "current_session", "description",
        "local_description", "language", "exchange", "fractional",
        "is_tradable", "lp", "lp_time", "minmov", "minmove2",
        "original_name", "pricescale", "pro_name", "short_name",
        "type", "update_mode", "volume", "currency_code", "rchp", "rtc"
    ])
    send_message(ws, "quote_add_symbols", [session, ticker, {"flags": ['force_permission']}])
    send_message(ws, "quote_fast_symbols", [session, ticker])
    send_message(ws, "resolve_symbol", [
        chart_session, "symbol_1",
        '={"symbol":"' + ticker + '","adjustment":"splits","session":"extended"}'
    ])
    send_message(ws, "create_series", [chart_session, "s1", "s1", "symbol_1", resolution, bars])


# ── Data fetch functions ──────────────────────────────────────────────────────

def search_data(ticker, resolution, bars):
    """Equity data with IST market-hours filter (9:15–15:30)."""
    ws, session, chart_session = new_session()
    send_subscription(ws, session, chart_session, ticker, resolution, bars)
    while True:
        try:
            result = ws.recv().split('~')
            for item in result:
                if 'timescale_update' in item:
                    df = pd.DataFrame([x['v'] for x in json.loads(item)['p'][1]['s1']['s']])
                    df.columns = ['epochtime', 'open', 'high', 'low', 'close', 'volume']
                    df['datetime'] = pd.to_datetime(df.epochtime, unit='s') + timedelta(hours=5.5)
                    df['time'] = df.datetime.dt.time
                    df = df[df.time.between(time(9, 15), time(15, 30), inclusive='both')]
                    return df
        except Exception:
            return pd.DataFrame()

def fetch_raw_data(ticker, resolution, bars):
    """All bars, no time filter. Good for daily/weekly or non-Indian markets."""
    ws, session, chart_session = new_session()
    send_subscription(ws, session, chart_session, ticker, resolution, bars)
    while True:
        try:
            result = ws.recv().split('~')
            for item in result:
                if 'timescale_update' in item:
                    df = pd.DataFrame([x['v'] for x in json.loads(item)['p'][1]['s1']['s']])
                    df.columns = ['epochtime', 'open', 'high', 'low', 'close', 'volume']
                    df['datetime'] = pd.to_datetime(df.epochtime, unit='s') + timedelta(hours=5.5)
                    df['time'] = df.datetime.dt.time
                    return df
        except Exception:
            return pd.DataFrame()

def search_nonstock_data(ticker, resolution, bars):
    """Indices, forex, crypto — instruments without a volume column."""
    ws, session, chart_session = new_session()
    send_subscription(ws, session, chart_session, ticker, resolution, bars)
    while True:
        try:
            result = ws.recv().split('~')
            for item in result:
                if 'timescale_update' in item:
                    df = pd.DataFrame([x['v'] for x in json.loads(item)['p'][1]['s1']['s']])
                    df.columns = ['epochtime', 'open', 'high', 'low', 'close']
                    df['volume'] = 0
                    df['datetime'] = pd.to_datetime(df.epochtime, unit='s') + timedelta(hours=5.5)
                    df['time'] = df.datetime.dt.time
                    df.drop_duplicates(inplace=True)
                    return df
        except Exception:
            return pd.DataFrame()
```

> The fundamentals and news functions (`fetch_fundamentals`, `summarize_fundamentals`,
> `fundamentals_to_csv`, `fetch_many_fundamentals`, `get_auth_token`, `fetch_news`,
> `news_to_csv`, `fetch_many_news`) are long (the field lists alone are ≈900 entries)
> and live in `scripts/tvwebsocket.py`. Import them from there rather than inlining.

---

## Usage Patterns

### Pattern 1: Intraday NSE equity
```python
df = search_data("NSE:RELIANCE", resolution="5", bars=500)
print(df.head())
```

### Pattern 2: Daily OHLCV for US stock
```python
df = fetch_raw_data("NASDAQ:AAPL", resolution="D", bars=252)
df.to_csv("aapl_daily.csv", index=False)
```

### Pattern 3: NIFTY 50 index (no volume)
```python
df = search_nonstock_data("NSE:NIFTY", resolution="60", bars=300)
```

### Pattern 4: Crypto (24/7, no market hours)
```python
df = fetch_raw_data("BINANCE:BTCUSDT", resolution="60", bars=500)
```

### Pattern 5: Save OHLCV to CSV
```python
df = search_data("NSE:INFY", "15", 300)
df.to_csv("infy_15min.csv", index=False)
print(f"Fetched {len(df)} bars")
```

### Pattern 6: Single-symbol fundamentals (authenticated)
```python
from scripts.tvwebsocket import fetch_fundamentals, summarize_fundamentals, fundamentals_to_csv

data = fetch_fundamentals("NASDAQ:AAPL",
                          sessionid=SESSIONID, sessionid_sign=SESSIONID_SIGN)
print(summarize_fundamentals(data))
fundamentals_to_csv(data, "AAPL_fundamentals.csv")
```

### Pattern 7: Fundamentals for a universe → one DataFrame
```python
from scripts.tvwebsocket import fetch_many_fundamentals

df = fetch_many_fundamentals(["NASDAQ:AAPL", "NASDAQ:MSFT", "NYSE:KO"],
                             sessionid=SESSIONID, sessionid_sign=SESSIONID_SIGN)
df.to_csv("fundamentals_summary.csv", index=False)
```

### Pattern 8: Combine price + fundamentals for a screen
```python
ohlcv = fetch_raw_data("NASDAQ:AAPL", "D", 252)
fund  = summarize_fundamentals(
    fetch_fundamentals("NASDAQ:AAPL", sessionid=SESSIONID, sessionid_sign=SESSIONID_SIGN)
)
# e.g. join 1y return from ohlcv with P/E and price-target upside from fund
```

### Pattern 9: News for a symbol
```python
from scripts.tvwebsocket import news_to_csv
news_to_csv("NASDAQ:AAPL", region="us", lang="en")   # -> AAPL_news.csv
```

---

## Bugs Fixed from Original Source

| Original Bug | Fix Applied |
|---|---|
| `datetime.fromtimestamp(...)` — missing `datetime.datetime` | Used `pd.to_datetime(..., unit='s')` instead |
| `return item` before `search_tu = False` — loop never exits | Removed dead code; `return` exits immediately |
| Session/function naming mixed snake_case and camelCase | Normalized to snake_case |
| No empty DataFrame fallback on exception | Returns `pd.DataFrame()` instead of `''` |

---

## Troubleshooting

**Empty DataFrame returned (OHLCV):**
- Ticker format wrong — always use `EXCHANGE:SYMBOL` format (e.g., `NSE:TCS`, not just `TCS`)
- `bars` value too large — try reducing to 100–300
- WebSocket timeout — retry; TradingView sometimes rate-limits rapid connections

**Fundamentals come back empty / only a few fields:**
- Almost always an **auth** problem. `unauthorized_user_token` returns next to
  nothing — supply `sessionid` (+ `sessionid_sign`) or a token from `get_auth_token`.
- Confirm `get_auth_token(...)` returns a non-`None` token; if `None`, your cookies
  are stale — re-copy them from DevTools while logged in.
- Run `fetch_fundamentals(..., debug=True)` to print every message type and any
  `critical_error` / `protocol_error` frame the server sends.
- The fetch needs `_complete=True` and `len(data) > 3` to stop early; on a slow
  connection raise `timeout`.

**`KeyError: 's1'`:**
- The symbol may not exist or is delisted on TradingView
- Try the symbol in TradingView's web UI first to confirm it's valid

**News request returns nothing:**
- Match `region`/`lang` to the symbol's market (`us`/`en` for US names,
  `in`/`en_IN` for Indian names).
- Some symbols simply have no recent news flow.

**`websocket` / `requests` module not found:**
```bash
pip install websocket-client pandas requests
```

**Time offset looks wrong:**
- The `+timedelta(hours=5.5)` converts UTC → IST. Remove or adjust for other timezones.
