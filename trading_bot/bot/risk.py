"""Risk management: position sizing, exposure limits, and a daily kill switch."""

from __future__ import annotations

import math

from bot.config import Config


class RiskManager:
    def __init__(self, config: Config) -> None:
        self._cfg = config
        self._day_start_equity: float | None = None
        self.halted = False

    def start_of_day(self, equity: float) -> None:
        self._day_start_equity = equity
        self.halted = False

    def check_kill_switch(self, equity: float) -> bool:
        """Return True (and halt trading) once the daily loss limit is breached."""
        if self._day_start_equity is None:
            self._day_start_equity = equity
        if self._day_start_equity > 0:
            daily_return = (equity - self._day_start_equity) / self._day_start_equity
            if daily_return <= -self._cfg.max_daily_loss:
                self.halted = True
        return self.halted

    def can_open(self, open_position_count: int) -> bool:
        return not self.halted and open_position_count < self._cfg.max_open_positions

    def position_size(self, equity: float, price: float, stop_distance: float) -> float:
        """Shares to buy so that hitting the stop loses ~risk_per_trade of equity.

        Also caps notional exposure per position at equity / max_open_positions so a
        tight stop can never produce an outsized position.
        """
        if equity <= 0 or price <= 0 or stop_distance <= 0:
            return 0.0
        risk_budget = equity * self._cfg.risk_per_trade
        shares_by_risk = risk_budget / stop_distance
        shares_by_notional = (equity / self._cfg.max_open_positions) / price
        shares = math.floor(min(shares_by_risk, shares_by_notional))
        return float(max(shares, 0))
