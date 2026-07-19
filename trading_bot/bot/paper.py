"""In-memory broker used by backtests and paper trading. No real orders ever."""

from __future__ import annotations

from bot.models import Candle, Position, Trade


class PaperBroker:
    def __init__(self, initial_cash: float = 10_000.0) -> None:
        self.cash = initial_cash
        self.positions: dict[str, Position] = {}
        self.trades: list[Trade] = []
        self._last_price: dict[str, float] = {}

    def mark(self, symbol: str, candle: Candle) -> None:
        """Update the latest known price and enforce protective stops intrabar."""
        self._last_price[symbol] = candle.close
        position = self.positions.get(symbol)
        if position is not None and candle.low <= position.stop_loss:
            self._close(symbol, price=position.stop_loss, ts=candle.ts, reason="stop-loss")

    def equity(self) -> float:
        value = self.cash
        for symbol, position in self.positions.items():
            value += position.volume * self._last_price.get(symbol, position.open_price)
        return value

    def market_buy(self, symbol: str, volume: float, stop_loss: float, ts: int) -> Position | None:
        price = self._last_price.get(symbol)
        if price is None or volume <= 0 or symbol in self.positions:
            return None
        cost = price * volume
        if cost > self.cash:
            return None
        self.cash -= cost
        position = Position(
            symbol=symbol, volume=volume, open_price=price, stop_loss=stop_loss, opened_ts=ts
        )
        self.positions[symbol] = position
        return position

    def close_position(self, symbol: str, ts: int, reason: str = "signal") -> Trade | None:
        price = self._last_price.get(symbol)
        if price is None or symbol not in self.positions:
            return None
        return self._close(symbol, price=price, ts=ts, reason=reason)

    def _close(self, symbol: str, *, price: float, ts: int, reason: str) -> Trade:
        position = self.positions.pop(symbol)
        self.cash += price * position.volume
        trade = Trade(
            symbol=symbol,
            volume=position.volume,
            open_price=position.open_price,
            close_price=price,
            opened_ts=position.opened_ts,
            closed_ts=ts,
            reason=reason,
        )
        self.trades.append(trade)
        return trade
