"""Live trading engine: polls candles, evaluates signals, manages positions.

Long-only by design. In dry-run mode (the default) every order is logged but
never sent, which is the recommended first step even on a paper account.
"""

from __future__ import annotations

import logging
import time

from bot.broker import BrokerClient
from bot.config import Config
from bot.models import Signal
from bot.risk import RiskManager
from bot.strategy import TrendFollowingStrategy

log = logging.getLogger("trading_bot")


class TradingEngine:
    def __init__(self, config: Config, client: BrokerClient) -> None:
        config.validate()
        self._cfg = config
        self._client = client
        self._strategy = TrendFollowingStrategy(config)
        self._risk = RiskManager(config)

    def run_once(self) -> None:
        equity = self._client.get_equity()
        if self._risk.check_kill_switch(equity):
            log.warning("kill switch active: daily loss limit reached, no new trades today")
        positions = self._client.get_open_positions()
        log.info("equity=%.2f open_positions=%d", equity, len(positions))

        for symbol in self._cfg.watchlist:
            try:
                self._process_symbol(symbol, equity, positions)
            except Exception as error:  # noqa: BLE001 - one symbol/cycle must not kill the loop
                log.error("%s: %s", symbol, error)

    def _process_symbol(self, symbol: str, equity: float, positions: dict) -> None:
        candles = self._client.get_candles(
            symbol, self._cfg.timeframe_minutes, self._cfg.history_bars
        )
        evaluation = self._strategy.evaluate(candles)
        has_position = symbol in positions
        log.info("%s: %s (%s)", symbol, evaluation.signal.value, evaluation.reason)

        if evaluation.signal is Signal.SELL and has_position:
            self._execute_close(positions[symbol])
        elif evaluation.signal is Signal.BUY and not has_position:
            if not self._risk.can_open(len(positions)):
                log.info("%s: buy signal skipped (risk limits)", symbol)
                return
            price = candles[-1].close
            stop_distance = evaluation.stop_distance or 0.0
            volume = self._risk.position_size(equity, price, stop_distance)
            if volume <= 0:
                log.info("%s: buy signal skipped (position size 0)", symbol)
                return
            self._execute_buy(symbol, volume, price - stop_distance)

    def _execute_buy(self, symbol: str, volume: float, stop_loss: float) -> None:
        if self._cfg.dry_run:
            log.info("[dry-run] BUY %s volume=%g sl=%.2f", symbol, volume, stop_loss)
            return
        order_id = self._client.market_buy(symbol, volume, stop_loss)
        log.info("BUY sent %s volume=%g sl=%.2f order=%s", symbol, volume, stop_loss, order_id)

    def _execute_close(self, position) -> None:
        if self._cfg.dry_run:
            log.info("[dry-run] CLOSE %s volume=%g", position.symbol, position.volume)
            return
        order_id = self._client.close_position(position)
        log.info("CLOSE sent %s volume=%g order=%s", position.symbol, position.volume, order_id)

    def run_forever(self) -> None:
        log.info(
            "engine started: mode=%s dry_run=%s watchlist=%s",
            self._cfg.mode,
            self._cfg.dry_run,
            ",".join(self._cfg.watchlist),
        )
        while True:
            try:
                self.run_once()
            except Exception as error:  # noqa: BLE001 - one symbol/cycle must not kill the loop
                log.error("cycle failed: %s", error)
            time.sleep(self._cfg.poll_seconds)
