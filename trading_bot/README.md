# Trading Bot (long-only stocks, Alpaca)

A small, dependency-free Python trading bot that opens **bull (long) positions on
stocks** using a trend-following strategy, connected to
[Alpaca Markets](https://alpaca.markets) — chosen because it has a maintained
public trading API with **first-class paper trading** (paper and live use the
same endpoints on different hosts, so what you validate on paper is exactly what
runs live).

> **Why not XTB?** XTB discontinued its investment-automation API for retail
> clients ([their help center](https://www.xtb.com/int/help-center/our-platforms-6-4/does-xtb-offer-investment-automation-tools-4)),
> so there is no supported way to automate an XTB account. The broker layer here
> is pluggable (`bot/broker.py`), so another connector can be added if that
> changes.

| Mode | Broker | Money at risk |
|---|---|---|
| `backtest` | none (offline) | none |
| `run` (default) | Alpaca **paper**, dry-run | none — orders are only logged |
| `run --execute` | Alpaca **paper** | none — simulated paper balance |
| `run --mode live --execute --i-understand-the-risks` | Alpaca live | **REAL MONEY** — also requires typing a confirmation |

> ⚠️ **This is not financial advice.** Automated strategies can and do lose
> money. Past (and backtested) performance does not predict future results.
> Run on paper for weeks before even considering live mode, start tiny, and
> never trade money you cannot afford to lose.

## Strategy

Long-only trend following on daily candles:

- **Enter** when SMA20 > SMA50, price above SMA20, and RSI(14) < 70.
- **Exit** when SMA20 falls back below SMA50, or the protective stop is hit.
- **Stop-loss** placed 2×ATR(14) below entry, attached to the buy order
  (Alpaca one-triggers-other order class).

Risk management (enforced before every order):

- Position sized so a stop-out loses ~**1% of equity**, capped at
  equity/5 notional per position.
- Max **5 open positions**.
- **Daily kill switch**: after −3% on the day, no new positions are opened.

All parameters live in `bot/config.py`.

## Setup

Requires Python 3.11+. No third-party packages.

1. Create a free Alpaca account at https://alpaca.markets and generate
   **paper trading** API keys from the dashboard (paper keys are separate from
   live keys and only work against the paper host).
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

4. Dry-run against your paper account (reads data, logs intended orders):

   ```bash
   python -m bot run --once
   ```

5. Let it place paper orders:

   ```bash
   python -m bot run --execute
   ```

## Configuration

Environment variables (or `.env`):

| Variable | Meaning |
|---|---|
| `APCA_API_KEY_ID` | Alpaca API key id |
| `APCA_API_SECRET_KEY` | Alpaca API secret |
| `BOT_MODE` | `paper` (default) or `live` |
| `BOT_WATCHLIST` | comma-separated tickers, e.g. `AAPL,MSFT,NVDA` |

Market data uses Alpaca's free IEX feed; symbols are plain US tickers.

## Tests

```bash
cd trading_bot
python -m pytest tests -q
```

The Alpaca connector is unit-tested against a fake HTTP transport (no network),
covering auth headers, candle parsing, order payloads, and error handling.

## Notes & caveats

- Markets have hours; a daily-candle strategy only needs to run once per day
  (a cron job calling `python -m bot run --once --execute` after the US close
  is a reasonable setup).
- Alpaca availability varies by country for **live** accounts; paper trading is
  available regardless. Check their onboarding for your jurisdiction.
- This folder is self-contained and unrelated to the portfolio site. Consider
  moving it to its own **private** repository.
