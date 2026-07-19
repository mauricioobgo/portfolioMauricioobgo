# Trading Bot (long-only stocks, XTB)

A small, dependency-free Python trading bot that opens **bull (long) positions on
stocks** using a trend-following strategy, with an [XTB xAPI](https://developers.xstore.pro/documentation)
connector. Built safety-first:

| Mode | Broker | Money at risk |
|---|---|---|
| `backtest` | none (offline) | none |
| `run` (default) | XTB **demo**, dry-run | none — orders are only logged |
| `run --execute` | XTB **demo** | none — demo account balance |
| `run --mode real --execute --i-understand-the-risks` | XTB real | **REAL MONEY** — also requires typing a confirmation |

> ⚠️ **This is not financial advice.** Automated strategies can and do lose
> money. Past (and backtested) performance does not predict future results.
> Run on a demo account for weeks before even considering real mode, start
> tiny, and never trade money you cannot afford to lose.

## Strategy

Long-only trend following on daily candles:

- **Enter** when SMA20 > SMA50, price above SMA20, and RSI(14) < 70.
- **Exit** when SMA20 falls back below SMA50, or the protective stop is hit.
- **Stop-loss** placed 2×ATR(14) below entry, sent with the order.

Risk management (enforced before every order):

- Position sized so a stop-out loses ~**1% of equity**, capped at
  equity/5 notional per position.
- Max **5 open positions**.
- **Daily kill switch**: after −3% on the day, no new positions are opened.

All parameters live in `bot/config.py`.

## Setup

Requires Python 3.11+. No third-party packages.

1. Create an XTB **demo** account (free) and note your user id + password.
2. Configure credentials:

   ```bash
   cd trading_bot
   cp .env.example .env   # then edit .env — never commit it
   ```

3. Backtest first (offline, no credentials needed):

   ```bash
   python -m bot backtest              # synthetic data demo
   python -m bot backtest --bars 1000
   ```

4. Dry-run against your demo account (reads data, logs intended orders):

   ```bash
   python -m bot run --once
   ```

5. Let it place demo orders:

   ```bash
   python -m bot run --execute
   ```

## Configuration

Environment variables (or `.env`):

| Variable | Meaning |
|---|---|
| `XTB_USER_ID` | your XTB account id |
| `XTB_PASSWORD` | your XTB password |
| `XTB_MODE` | `demo` (default) or `real` |
| `BOT_WATCHLIST` | comma-separated symbols, e.g. `AAPL.US,MSFT.US` |

Symbol names must match XTB's catalogue (check the xStation platform or the
`getAllSymbols` API call — US stocks are usually `TICKER.US`).

## Tests

```bash
cd trading_bot
python -m pytest tests -q
```

## Notes & caveats

- The xAPI connector was written against the public xStation5 docs but could
  not be integration-tested from the development sandbox. **Verify every flow
  on demo first** and treat the official docs as the source of truth.
- Depending on your XTB account type, stock instruments may be real equities or
  CFDs, and `volume` may be shares or lots — confirm with `getSymbol`
  (`lotMin`, `lotStep`, `contractSize`) before executing.
- Markets have hours; a daily-candle strategy only needs to run once per day
  (a cron job calling `python -m bot run --once --execute` after the US close
  is a reasonable setup).
- If you ever move brokers, only `bot/xtb.py` needs replacing — strategy, risk
  and backtesting are broker-agnostic (Alpaca has a friendly REST API with
  first-class paper trading if you want an alternative).
- This folder is self-contained and unrelated to the portfolio site. Consider
  moving it to its own **private** repository.
