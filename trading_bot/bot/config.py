from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path


DEFAULT_WATCHLIST = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA"]


def load_dotenv(path: Path) -> None:
    """Minimal .env loader (stdlib-only). Existing environment variables win."""
    if not path.is_file():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip("'\"")
        if key and key not in os.environ:
            os.environ[key] = value


@dataclass
class Config:
    # Broker credentials (never hardcode; set via environment or .env).
    alpaca_key_id: str = ""
    alpaca_secret_key: str = ""
    mode: str = "paper"  # paper | live

    # Universe and timeframe.
    watchlist: list[str] = field(default_factory=lambda: list(DEFAULT_WATCHLIST))
    timeframe_minutes: int = 1440  # daily candles
    history_bars: int = 120

    # Strategy parameters (long-only trend following).
    sma_fast: int = 20
    sma_slow: int = 50
    rsi_period: int = 14
    rsi_max: float = 70.0  # do not buy into overbought conditions
    atr_period: int = 14
    atr_stop_multiple: float = 2.0

    # Risk limits.
    risk_per_trade: float = 0.01  # fraction of equity risked per position
    max_open_positions: int = 5
    max_daily_loss: float = 0.03  # kill switch: stop trading after -3% on the day

    # Execution.
    dry_run: bool = True  # log intended orders instead of sending them
    poll_seconds: int = 300

    @classmethod
    def from_env(cls, env_file: Path | None = None) -> "Config":
        if env_file is not None:
            load_dotenv(env_file)
        cfg = cls()
        cfg.alpaca_key_id = os.environ.get("APCA_API_KEY_ID", "")
        cfg.alpaca_secret_key = os.environ.get("APCA_API_SECRET_KEY", "")
        cfg.mode = os.environ.get("BOT_MODE", cfg.mode).lower()
        watchlist = os.environ.get("BOT_WATCHLIST", "")
        if watchlist:
            cfg.watchlist = [item.strip() for item in watchlist.split(",") if item.strip()]
        return cfg

    def validate(self) -> None:
        if self.mode not in {"paper", "live"}:
            raise ValueError(f"mode must be 'paper' or 'live', got {self.mode!r}")
        if not 0 < self.risk_per_trade <= 0.05:
            raise ValueError("risk_per_trade must be in (0, 0.05]")
        if self.sma_fast >= self.sma_slow:
            raise ValueError("sma_fast must be smaller than sma_slow")
        if self.max_open_positions < 1:
            raise ValueError("max_open_positions must be >= 1")
