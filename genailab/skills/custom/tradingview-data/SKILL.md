---
name: tradingview-data
description: >
  Fetch OHLCV (Open, High, Low, Close, Volume) market data from TradingView via WebSocket
  for any ticker — Indian equities, NSE/BSE stocks, crypto, forex, indices, and commodities.
  Use this skill whenever the user wants to pull historical candlestick/bar data, intraday
  tick data, or raw market data from TradingView. Triggers include: "fetch OHLCV from
  TradingView", "get candlestick data", "download historical data", "pull intraday data",
  "get market data for [ticker]", "fetch NSE/BSE data", "get price history", or any request
  to collect financial time series data from TradingView — even if the user just says
  "get me some stock data" without naming TradingView explicitly.
---

# TradingView Data Skill

Fetches market data (OHLCV bars) from TradingView's WebSocket API for any supported symbol.
Works for equities (NSE, BSE, NYSE, NASDAQ), crypto, forex, indices, and commodities.

---

## Dependencies

Install before first use:
```bash
pip install websocket-client pandas
```

---

## Core Concepts

### Session Architecture
TradingView uses two parallel sessions per connection:
- **Quote session** (`qs_...`): real-time price fields (lp, volume, etc.)
- **Chart session** (`cs_...`): OHLCV bar series data

Both are established over a single WebSocket to `wss://data.tradingview.com/socket.io/websocket`.

### Message Protocol
All messages follow the pattern: `~m~{length}~m~{json_payload}`

```python
def prepend_header(st):
    return "~m~" + str(len(st)) + "~m~" + st
```

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

## Three Fetch Functions

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

## Full Working Template

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

### Pattern 5: Save to CSV
```python
df = search_data("NSE:INFY", "15", 300)
df.to_csv("infy_15min.csv", index=False)
print(f"Fetched {len(df)} bars")
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

**Empty DataFrame returned:**
- Ticker format wrong — always use `EXCHANGE:SYMBOL` format (e.g., `NSE:TCS`, not just `TCS`)
- `bars` value too large — try reducing to 100–300
- WebSocket timeout — retry; TradingView sometimes rate-limits rapid connections

**`websocket` module not found:**
```bash
pip install websocket-client
```

**`KeyError: 's1'`:**
- The symbol may not exist or is delisted on TradingView
- Try the symbol in TradingView's web UI first to confirm it's valid

**Time offset looks wrong:**
- The `+timedelta(hours=5.5)` converts UTC → IST. Remove or adjust for other timezones.