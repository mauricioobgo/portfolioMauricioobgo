"""Alpaca Markets connector (REST, stdlib only).

Why Alpaca: a maintained public trading API with first-class paper trading -
paper and live use identical endpoints on different hosts, so the exact code
you validate on paper is what runs live. Docs: https://docs.alpaca.markets

- Trading API (paper): https://paper-api.alpaca.markets
- Trading API (live):  https://api.alpaca.markets
- Market data:         https://data.alpaca.markets  (free IEX feed)

Auth is two headers generated from your dashboard: APCA-API-KEY-ID and
APCA-API-SECRET-KEY. Paper keys only ever work against the paper host.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Callable
from datetime import datetime, timezone
from typing import Any

from bot.models import Candle, Position


TRADING_HOSTS = {
    "paper": "https://paper-api.alpaca.markets",
    "live": "https://api.alpaca.markets",
}
DATA_HOST = "https://data.alpaca.markets"

# Injectable transport so unit tests can stub HTTP without a network.
Transport = Callable[[urllib.request.Request, float], bytes]


def _default_transport(request: urllib.request.Request, timeout: float) -> bytes:
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read()


class AlpacaError(RuntimeError):
    pass


class AlpacaClient:
    """Synchronous Alpaca client covering the surface this bot needs."""

    def __init__(
        self,
        key_id: str,
        secret_key: str,
        mode: str = "paper",
        timeout: float = 15.0,
        transport: Transport = _default_transport,
    ) -> None:
        if mode not in TRADING_HOSTS:
            raise ValueError(f"mode must be one of {sorted(TRADING_HOSTS)}, got {mode!r}")
        self.mode = mode
        self._key_id = key_id
        self._secret_key = secret_key
        self._timeout = timeout
        self._transport = transport

    def connect(self) -> None:
        """Validate credentials by fetching the account."""
        if not self._key_id or not self._secret_key:
            raise AlpacaError("APCA_API_KEY_ID and APCA_API_SECRET_KEY must be set")
        self._request("GET", TRADING_HOSTS[self.mode], "/v2/account")

    # -- market data --------------------------------------------------------

    def get_candles(self, symbol: str, period_minutes: int, bars: int) -> list[Candle]:
        timeframe = self._timeframe(period_minutes)
        query = {"timeframe": timeframe, "limit": str(bars), "feed": "iex", "adjustment": "split"}
        data = self._request(
            "GET", DATA_HOST, f"/v2/stocks/{urllib.parse.quote(symbol)}/bars", query=query
        )
        candles: list[Candle] = []
        for bar in data.get("bars") or []:
            candles.append(
                Candle(
                    ts=_iso_to_ms(bar["t"]),
                    open=float(bar["o"]),
                    high=float(bar["h"]),
                    low=float(bar["l"]),
                    close=float(bar["c"]),
                    volume=float(bar.get("v", 0)),
                )
            )
        return candles[-bars:]

    # -- account state ------------------------------------------------------

    def get_equity(self) -> float:
        data = self._request("GET", TRADING_HOSTS[self.mode], "/v2/account")
        return float(data.get("equity", 0.0))

    def get_open_positions(self) -> dict[str, Position]:
        records = self._request("GET", TRADING_HOSTS[self.mode], "/v2/positions")
        positions: dict[str, Position] = {}
        for record in records or []:
            if record.get("side") != "long":
                continue  # this bot is long-only; ignore anything else
            symbol = record.get("symbol", "")
            positions[symbol] = Position(
                symbol=symbol,
                volume=float(record.get("qty", 0.0)),
                open_price=float(record.get("avg_entry_price", 0.0)),
                stop_loss=0.0,  # stop lives in the attached stop order, not the position
                opened_ts=0,
                order_id=None,
            )
        return positions

    # -- orders (long-only) -------------------------------------------------

    def market_buy(self, symbol: str, volume: float, stop_loss: float) -> str:
        """Market buy with an attached protective stop (one-triggers-other)."""
        payload = {
            "symbol": symbol,
            "qty": str(int(volume)),
            "side": "buy",
            "type": "market",
            "time_in_force": "day",
            "order_class": "oto",
            "stop_loss": {"stop_price": str(round(stop_loss, 2))},
        }
        data = self._request("POST", TRADING_HOSTS[self.mode], "/v2/orders", body=payload)
        return str(data.get("id", ""))

    def close_position(self, position: Position) -> str:
        data = self._request(
            "DELETE",
            TRADING_HOSTS[self.mode],
            f"/v2/positions/{urllib.parse.quote(position.symbol)}",
        )
        if isinstance(data, dict):
            return str(data.get("id", ""))
        return ""

    # -- HTTP plumbing ------------------------------------------------------

    @staticmethod
    def _timeframe(period_minutes: int) -> str:
        if period_minutes >= 1440:
            return "1Day"
        if period_minutes >= 60:
            return f"{period_minutes // 60}Hour"
        return f"{period_minutes}Min"

    def _request(
        self,
        method: str,
        host: str,
        path: str,
        *,
        query: dict[str, str] | None = None,
        body: dict[str, Any] | None = None,
    ) -> Any:
        url = host + path
        if query:
            url += "?" + urllib.parse.urlencode(query)
        request = urllib.request.Request(
            url,
            method=method,
            data=json.dumps(body).encode("utf-8") if body is not None else None,
            headers={
                "APCA-API-KEY-ID": self._key_id,
                "APCA-API-SECRET-KEY": self._secret_key,
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
        )
        try:
            raw = self._transport(request, self._timeout)
        except urllib.error.HTTPError as error:
            detail = ""
            try:
                detail = error.read().decode("utf-8", errors="replace")[:300]
            except Exception:
                pass
            raise AlpacaError(f"{method} {path} failed: HTTP {error.code} {detail}") from error
        except urllib.error.URLError as error:
            raise AlpacaError(f"{method} {path} failed: {error.reason}") from error
        if not raw:
            return {}
        return json.loads(raw.decode("utf-8"))


def _iso_to_ms(timestamp: str) -> int:
    """Convert Alpaca's RFC3339 timestamps (e.g. 2024-01-02T05:00:00Z) to ms."""
    normalized = timestamp.replace("Z", "+00:00")
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return int(parsed.timestamp() * 1000)
