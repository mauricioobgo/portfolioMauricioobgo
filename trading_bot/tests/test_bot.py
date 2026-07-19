from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bot.backtest import run_backtest, synthetic_candles  # noqa: E402
from bot.config import Config  # noqa: E402
from bot.indicators import atr, rsi, sma  # noqa: E402
from bot.models import Candle, Signal  # noqa: E402
from bot.paper import PaperBroker  # noqa: E402
from bot.risk import RiskManager  # noqa: E402
from bot.strategy import TrendFollowingStrategy  # noqa: E402


def _flat_candles(n: int, price: float = 100.0) -> list[Candle]:
    return [
        Candle(ts=i, open=price, high=price + 1, low=price - 1, close=price, volume=1)
        for i in range(n)
    ]


def _trending_candles(n: int, start: float = 100.0, step: float = 1.0) -> list[Candle]:
    candles = []
    price = start
    for i in range(n):
        close = price + step
        candles.append(
            Candle(ts=i, open=price, high=close + 0.5, low=price - 0.5, close=close, volume=1)
        )
        price = close
    return candles


def _pullback_uptrend(n: int, start: float = 100.0) -> list[Candle]:
    """Rising market with periodic pullbacks, so RSI stays below overbought."""
    candles = []
    price = start
    for i in range(n):
        # Two up bars then one equal down bar: net uptrend, steady-state
        # Wilder RSI ~= 66.7, safely under the 70 overbought filter.
        step = -1.0 if i % 3 == 2 else 1.0
        close = max(1.0, price + step)
        candles.append(
            Candle(
                ts=i,
                open=price,
                high=max(price, close) + 0.4,
                low=min(price, close) - 0.4,
                close=close,
                volume=1,
            )
        )
        price = close
    return candles


def test_sma_and_rsi_basics() -> None:
    assert sma([1, 2, 3, 4, 5], 5) == 3
    assert sma([1, 2, 3], 5) is None
    up_only = list(range(1, 20))
    value = rsi([float(v) for v in up_only], 14)
    assert value is not None and value > 99
    assert rsi([1.0, 2.0], 14) is None


def test_atr_positive_on_moving_market() -> None:
    candles = _trending_candles(30)
    value = atr(candles, 14)
    assert value is not None and value > 0


def test_strategy_buys_in_uptrend_and_sells_in_downtrend() -> None:
    config = Config()
    strategy = TrendFollowingStrategy(config)

    # A monotonic ramp pegs RSI at 100, so the overbought filter blocks entry.
    ramp = _trending_candles(80, step=0.4)
    assert strategy.evaluate(ramp).signal is Signal.HOLD

    # A realistic uptrend with pullbacks produces a BUY with an ATR stop.
    # (121 bars so the series ends on an up bar, with price above the fast SMA.)
    uptrend = _pullback_uptrend(121)
    evaluation = strategy.evaluate(uptrend)
    assert evaluation.signal is Signal.BUY
    assert evaluation.stop_distance is not None and evaluation.stop_distance > 0

    downtrend = _trending_candles(80, start=200.0, step=-1.0)
    evaluation = strategy.evaluate(downtrend)
    assert evaluation.signal is Signal.SELL

    assert strategy.evaluate(_flat_candles(10)).signal is Signal.HOLD


def test_risk_position_sizing_caps_risk_and_notional() -> None:
    config = Config()
    risk = RiskManager(config)
    # 1% of 10k = 100 risk budget; stop 2.0 away -> 50 shares by risk,
    # but notional cap = (10000/5)/100 = 20 shares.
    assert risk.position_size(10_000, price=100.0, stop_distance=2.0) == 20
    # Wide stop: risk budget dominates. 100/10 = 10 shares.
    assert risk.position_size(10_000, price=100.0, stop_distance=10.0) == 10
    assert risk.position_size(10_000, price=0.0, stop_distance=1.0) == 0


def test_kill_switch_halts_after_daily_loss() -> None:
    config = Config()
    risk = RiskManager(config)
    risk.start_of_day(10_000)
    assert risk.check_kill_switch(9_900) is False
    assert risk.can_open(0) is True
    assert risk.check_kill_switch(9_600) is True  # -4% < -3% limit
    assert risk.can_open(0) is False


def test_paper_broker_stop_loss_triggers_intrabar() -> None:
    broker = PaperBroker(10_000)
    broker.mark("X", Candle(ts=1, open=100, high=101, low=99, close=100))
    position = broker.market_buy("X", volume=10, stop_loss=95.0, ts=1)
    assert position is not None
    broker.mark("X", Candle(ts=2, open=100, high=100, low=94, close=96))
    assert "X" not in broker.positions
    assert broker.trades[0].reason == "stop-loss"
    assert broker.trades[0].close_price == 95.0


def test_paper_broker_rejects_overspend_and_duplicates() -> None:
    broker = PaperBroker(1_000)
    broker.mark("X", Candle(ts=1, open=100, high=101, low=99, close=100))
    assert broker.market_buy("X", volume=100, stop_loss=90, ts=1) is None  # too expensive
    assert broker.market_buy("X", volume=5, stop_loss=90, ts=1) is not None
    assert broker.market_buy("X", volume=1, stop_loss=90, ts=1) is None  # already open


def test_backtest_profits_on_strong_uptrend() -> None:
    config = Config()
    candles = _pullback_uptrend(241, start=50.0)
    result = run_backtest(config, {"UP.US": candles}, initial_cash=10_000)
    assert result.trades, "expected at least one trade in a rising market with pullbacks"
    assert result.final_equity > result.initial_equity
    assert 0 <= result.max_drawdown < 1


def test_backtest_runs_on_synthetic_basket() -> None:
    config = Config()
    basket = {f"S{i}.US": synthetic_candles(300, seed=i) for i in range(3)}
    result = run_backtest(config, basket, initial_cash=10_000)
    assert len(result.equity_curve) > 250
    assert result.final_equity > 0


def test_config_validation() -> None:
    config = Config()
    config.validate()
    config.risk_per_trade = 0.5
    try:
        config.validate()
        raise AssertionError("expected ValueError for excessive risk_per_trade")
    except ValueError:
        pass
