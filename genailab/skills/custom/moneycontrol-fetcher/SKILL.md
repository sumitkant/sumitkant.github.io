---
name: moneycontrol-fetcher
description: >
  Fetches historical OHLCV (Open, High, Low, Close, Volume) price data from MoneyControl's
  price API for Indian stock market tickers. Use this skill whenever the user wants to
  download, fetch, scrape, or collect historical stock price data from MoneyControl, even
  if they just say "get stock data", "download price history", or "fetch OHLCV data for
  NSE/BSE stocks". Also triggers for requests involving MoneyControl symbols, bulk ticker
  downloads, intraday/1-minute candle data, or saving stock data to .pkl or .csv files.
  Always use this skill when multiprocessing or parallel fetching of MoneyControl data is
  involved.
---

# MoneyControl Historical Data Fetcher

Fetches 1-minute OHLCV candle data from MoneyControl's chart API for one or many Indian
stock tickers, with parallel execution and polite rate-limiting.

---

## API Details

**Endpoint:**
```
https://priceapi.moneycontrol.com/techCharts/techChartController/history
  ?symbol={symbol}
  &resolution={resolution}    # 1 = 1-minute bars
  &from={unix_timestamp}
  &to={unix_timestamp}
```

**Response JSON keys:** `s` (status), `t` (time), `o` (open), `h` (high), `l` (low),
`c` (close), `v` (volume)

**Symbol format:** MoneyControl uses its own internal symbol codes.  
If the user provides NSE/BSE tickers in the format `NSE:RELIANCE` or `BSE:500325`,
strip the exchange prefix and replace underscores with hyphens:
```python
ticks = [x.split(':')[1].replace('_', '-') for x in ticker_list]
```

**Timezone:** API returns UTC timestamps; add +5:30 to get IST.

---

## Core Workflow

### 1. Set date range and resolution
```python
from datetime import datetime, timedelta

start_time = int((datetime.now() - timedelta(days=600)).timestamp())  # last ~600 days
end_time   = int(datetime.now().timestamp())
resolution = 1  # 1-minute bars; use 5, 15, 30, 60, D, W, M for other resolutions
```

### 2. Single-ticker fetch function
```python
import requests, pandas as pd
from time import sleep
from random import randint

def money_control_fetch(symbol: str) -> pd.DataFrame | None:
    """
    Fetches OHLCV data for one MoneyControl symbol.
    Returns a DataFrame or None on failure.
    Saves a .pkl file as a side-effect.
    """
    sleep(randint(100, 500) / 100)          # polite random delay: 1–5 seconds

    headers = {
        'User-Agent': (
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/50.0.2661.102 Safari/537.36'
        )
    }
    url = (
        f'https://priceapi.moneycontrol.com/techCharts/techChartController/history'
        f'?symbol={symbol}&resolution={resolution}&from={start_time}&to={end_time}'
    )

    try:
        resp = requests.get(url, headers=headers, timeout=30)
        resp.raise_for_status()

        df = pd.DataFrame(resp.json())
        df.drop('s', axis=1, inplace=True)
        df.columns = ['time', 'open', 'high', 'low', 'close', 'volume']
        df['datetime'] = pd.to_datetime(df['time'], unit='s') + timedelta(hours=5.5)
        df['ticker']   = symbol
        df = df[['ticker', 'datetime', 'open', 'high', 'low', 'close', 'volume']]
        df = df.astype({
            'open': 'float32', 'high': 'float32',
            'low':  'float32', 'close': 'float32',
            'volume': 'uint32'
        })

        df.to_pickle(f'{symbol}.pkl')
        print(f'{datetime.now():%Y-%m-%d %H:%M:%S} > FETCHED {symbol}; {len(df)} rows')
        return df

    except Exception as e:
        print(f'{datetime.now():%Y-%m-%d %H:%M:%S} > SKIPPED {symbol} — {e}')
        return None
```

### 3. Bulk parallel fetch
```python
from multiprocessing import Pool

# Convert ticker list if needed (e.g. ["NSE:RELIANCE", "NSE:TCS"])
ticks = [x.split(':')[1].replace('_', '-') for x in ticker_list]

with Pool(12) as p:          # tune worker count to your CPU/network
    results = p.map(money_control_fetch, ticks)

# Combine all into one DataFrame (drop None entries for failed tickers)
all_data = pd.concat([r for r in results if r is not None], ignore_index=True)
```

---

## Output

| Column   | dtype    | Description                        |
|----------|----------|------------------------------------|
| ticker   | object   | MoneyControl symbol string         |
| datetime | datetime | Candle open time in IST (UTC+5:30) |
| open     | float32  | Open price                         |
| high     | float32  | High price                         |
| low      | float32  | Low price                          |
| close    | float32  | Close price                        |
| volume   | uint32   | Volume                             |

Each ticker is also saved as `{symbol}.pkl` in the current working directory.  
To save as CSV instead, replace `df.to_pickle(...)` with:
```python
df.to_csv(f'{symbol}.csv', index=False)
```

---

## Tuning & Edge Cases

| Concern | Guidance |
|---|---|
| **Rate limiting / blocks** | Increase sleep range, e.g. `randint(200, 800)/100`. If still blocked, reduce pool size. |
| **Empty response** | API returns `{"s":"no_data"}` — the `drop('s')` will succeed but the DataFrame will be empty. Add `if df.empty: return None` after the drop. |
| **Symbol not found** | MoneyControl silently returns `no_data`. Pre-validate symbols against MoneyControl's search API if needed. |
| **Large date ranges** | For >2 years of 1-min data, split into 6-month windows and concatenate to avoid hitting response size limits. |
| **Non-trading rows** | The API already filters to market hours; no extra filtering needed. |
| **Pool size** | `12` workers is a good default. On low-core machines, use `os.cpu_count()` instead. |
| **Windows multiprocessing** | Wrap the `Pool` call in `if __name__ == '__main__':` when running as a script on Windows. |

---

## Minimal Complete Example

```python
import os, requests, pandas as pd
from datetime import datetime, timedelta
from time import sleep
from random import randint
from multiprocessing import Pool

START = int((datetime.now() - timedelta(days=600)).timestamp())
END   = int(datetime.now().timestamp())
RES   = 1

HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/50.0.2661.102 Safari/537.36'
    )
}

def fetch(symbol):
    sleep(randint(100, 500) / 100)
    url = (
        f'https://priceapi.moneycontrol.com/techCharts/techChartController/history'
        f'?symbol={symbol}&resolution={RES}&from={START}&to={END}'
    )
    try:
        r = requests.get(url, headers=HEADERS, timeout=30)
        r.raise_for_status()
        df = pd.DataFrame(r.json()).drop('s', axis=1)
        df.columns = ['time', 'open', 'high', 'low', 'close', 'volume']
        df['datetime'] = pd.to_datetime(df['time'], unit='s') + timedelta(hours=5.5)
        df['ticker'] = symbol
        df = df[['ticker', 'datetime', 'open', 'high', 'low', 'close', 'volume']]
        df = df.astype({'open':'float32','high':'float32','low':'float32',
                        'close':'float32','volume':'uint32'})
        df.to_pickle(f'{symbol}.pkl')
        print(f'{datetime.now():%H:%M:%S} {symbol}: {len(df)} rows')
        return df
    except Exception as e:
        print(f'{datetime.now():%H:%M:%S} {symbol}: ERROR {e}')
        return None

if __name__ == '__main__':
    ticker_list = ['NSE:RELIANCE', 'NSE:TCS', 'NSE:INFY']   # your list here
    ticks = [x.split(':')[1].replace('_', '-') for x in ticker_list]
    with Pool(min(12, os.cpu_count())) as p:
        dfs = p.map(fetch, ticks)
    combined = pd.concat([d for d in dfs if d is not None], ignore_index=True)
    combined.to_pickle('all_tickers.pkl')
    print(f'Done — {len(combined):,} rows across {combined.ticker.nunique()} tickers')
```