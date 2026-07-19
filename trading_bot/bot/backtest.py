"""Walk-forward backtester over historical candles (one symbol or a basket)."""

from __future__ import annotations

import random

from bot.config import Config
from bot.models import BacktestResult, Candle, Signal
from bot.paper import PaperBroker
from bot.risk import RiskManager
from bot.strategy import TrendFollowingStrategy


def synthetic_candles(
    bars: int,
    *,
    seed: int = 7,
    start_price: float = 100.0,
    drift: float = 0.0004,
    volatility: float = 0.015,
) -> list[Candle]:
    """Deterministic geometric random walk, for demos and tests only."""
    rng = random.Random(seed)
    candles: list[Candle] = []
    price = start_price
    ts = 1_700_000_000_000
    for i in range(bars):
        change = rng.gauss(drift, volatility)
        open_price = price
        close = max(0.01, open_price * (1 + change))
        high = max(open_price, close) * (1 + abs(rng.gauss(0, volatility / 3)))
        low = min(open_price, close) * (1 - abs(rng.gauss(0, volatility / 3)))
        candles.append(
            Candle(
                ts=ts + i * 86_400_000,
                open=round(open_price, 4),
                high=round(high, 4),
                low=round(low, 4),
                close=round(close, 4),
                volume=1_000,
            )
        )
        price = close
    return candles


def run_backtest(
    config: Config,
    candles_by_symbol: dict[str, list[Candle]],
    initial_cash: float = 10_000.0,
) -> BacktestResult:
    strategy = TrendFollowingStrategy(config)
    risk = RiskManager(config)
    broker = PaperBroker(initial_cash)
    result = BacktestResult(initial_equity=initial_cash, final_equity=initial_cash)

    total_bars = min(len(candles) for candles in candles_by_symbol.values())
    warmup = strategy.min_bars()
    if total_bars <= warmup:
        raise ValueError(f"Need more than {warmup} bars per symbol, got {total_bars}")

    for bar in range(total_bars):
        for symbol, candles in candles_by_symbol.items():
            broker.mark(symbol, candles[bar])
        if bar < warmup:
            result.equity_curve.append(broker.equity())
            continue

        for symbol, candles in candles_by_symbol.items():
            window = candles[: bar + 1]
            evaluation = strategy.evaluate(window)
            ts = candles[bar].ts
            has_position = symbol in broker.positions

            if evaluation.signal is Signal.SELL and has_position:
                broker.close_position(symbol, ts=ts, reason="trend-exit")
            elif evaluation.signal is Signal.BUY and not has_position:
                equity = broker.equity()
                if risk.check_kill_switch(equity) or not risk.can_open(len(broker.positions)):
                    continue
                stop_distance = evaluation.stop_distance or 0.0
                price = candles[bar].close
                volume = risk.position_size(equity, price, stop_distance)
                if volume > 0:
                    broker.market_buy(symbol, volume, stop_loss=price - stop_distance, ts=ts)

        result.equity_curve.append(broker.equity())

    for symbol in list(broker.positions):
        last = candles_by_symbol[symbol][total_bars - 1]
        broker.close_position(symbol, ts=last.ts, reason="end-of-backtest")

    result.trades = broker.trades
    result.final_equity = broker.equity()
    result.equity_curve.append(result.final_equity)
    return result


def format_report(result: BacktestResult) -> str:
    lines = [
        "=== Backtest report ===",
        f"initial equity : {result.initial_equity:,.2f}",
        f"final equity   : {result.final_equity:,.2f}",
        f"total return   : {result.total_return * 100:+.2f}%",
        f"max drawdown   : {result.max_drawdown * 100:.2f}%",
        f"trades         : {len(result.trades)}",
        f"win rate       : {result.win_rate * 100:.1f}%",
    ]
    for trade in result.trades[-10:]:
        lines.append(
            f"  {trade.symbol:<10} vol={trade.volume:<8g} "
            f"{trade.open_price:.2f} -> {trade.close_price:.2f} "
            f"pnl={trade.pnl:+.2f} ({trade.reason})"
        )
    return "\n".join(lines)
