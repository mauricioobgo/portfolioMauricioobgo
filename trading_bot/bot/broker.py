"""Broker interface. Implement this protocol to plug in a different broker."""

from __future__ import annotations

from typing import Protocol

from bot.models import Candle, Position


class BrokerClient(Protocol):
    def connect(self) -> None: ...

    def get_candles(self, symbol: str, period_minutes: int, bars: int) -> list[Candle]: ...

    def get_equity(self) -> float: ...

    def get_open_positions(self) -> dict[str, Position]: ...

    def market_buy(self, symbol: str, volume: float, stop_loss: float) -> str: ...

    def close_position(self, position: Position) -> str: ...
