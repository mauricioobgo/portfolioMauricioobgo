"""Long-only trend-following strategy.

Entry (bull position): fast SMA above slow SMA, price above the fast SMA, and
RSI below the overbought threshold (avoid chasing blow-off tops).

Exit: fast SMA crosses back below slow SMA. Stop-losses are handled by the
risk layer / broker (ATR-based protective stop set at entry).

The strategy is stateless: the engine decides what to do with a signal based
on whether a position is already open.
"""

from __future__ import annotations

from dataclasses import dataclass

from bot.config import Config
from bot.indicators import atr, rsi, sma
from bot.models import Candle, Signal


@dataclass
class Evaluation:
    signal: Signal
    reason: str
    stop_distance: float | None = None


class TrendFollowingStrategy:
    def __init__(self, config: Config) -> None:
        self._cfg = config

    def min_bars(self) -> int:
        return max(self._cfg.sma_slow, self._cfg.rsi_period + 1, self._cfg.atr_period + 1) + 1

    def evaluate(self, candles: list[Candle]) -> Evaluation:
        if len(candles) < self.min_bars():
            return Evaluation(Signal.HOLD, "not enough history")

        closes = [candle.close for candle in candles]
        fast = sma(closes, self._cfg.sma_fast)
        slow = sma(closes, self._cfg.sma_slow)
        strength = rsi(closes, self._cfg.rsi_period)
        volatility = atr(candles, self._cfg.atr_period)
        if fast is None or slow is None or strength is None or volatility is None:
            return Evaluation(Signal.HOLD, "indicators unavailable")

        price = closes[-1]
        if fast < slow:
            return Evaluation(
                Signal.SELL, f"downtrend: SMA{self._cfg.sma_fast} < SMA{self._cfg.sma_slow}"
            )
        if price > fast and strength < self._cfg.rsi_max:
            stop_distance = volatility * self._cfg.atr_stop_multiple
            return Evaluation(
                Signal.BUY,
                f"uptrend: price>{self._cfg.sma_fast}SMA, RSI={strength:.1f}",
                stop_distance=stop_distance,
            )
        return Evaluation(Signal.HOLD, f"uptrend but no entry (RSI={strength:.1f})")
