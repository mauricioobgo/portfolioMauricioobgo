from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class Signal(Enum):
    BUY = "buy"
    SELL = "sell"
    HOLD = "hold"


@dataclass(frozen=True)
class Candle:
    ts: int  # unix milliseconds
    open: float
    high: float
    low: float
    close: float
    volume: float = 0.0


@dataclass
class Position:
    symbol: str
    volume: float
    open_price: float
    stop_loss: float
    opened_ts: int
    order_id: int | None = None


@dataclass
class Trade:
    symbol: str
    volume: float
    open_price: float
    close_price: float
    opened_ts: int
    closed_ts: int
    reason: str

    @property
    def pnl(self) -> float:
        return (self.close_price - self.open_price) * self.volume

    @property
    def return_pct(self) -> float:
        if self.open_price == 0:
            return 0.0
        return (self.close_price - self.open_price) / self.open_price


@dataclass
class BacktestResult:
    initial_equity: float
    final_equity: float
    trades: list[Trade] = field(default_factory=list)
    equity_curve: list[float] = field(default_factory=list)

    @property
    def total_return(self) -> float:
        if self.initial_equity == 0:
            return 0.0
        return (self.final_equity - self.initial_equity) / self.initial_equity

    @property
    def max_drawdown(self) -> float:
        peak = float("-inf")
        max_dd = 0.0
        for value in self.equity_curve:
            peak = max(peak, value)
            if peak > 0:
                max_dd = max(max_dd, (peak - value) / peak)
        return max_dd

    @property
    def win_rate(self) -> float:
        if not self.trades:
            return 0.0
        wins = sum(1 for trade in self.trades if trade.pnl > 0)
        return wins / len(self.trades)
