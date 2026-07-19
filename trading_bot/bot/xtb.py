"""Minimal XTB xAPI client (JSON over SSL socket), stdlib only.

Protocol reference: https://developers.xstore.pro/documentation (xStation5 API).
Demo and real accounts use the same protocol on different ports. All requests
are JSON objects; responses arrive as JSON terminated by a blank line.

IMPORTANT: validate every flow on a DEMO account before considering real mode.
API details (ports, symbol names, volume units) can change - treat the official
documentation as the source of truth.
"""

from __future__ import annotations

import json
import socket
import ssl
import time
from typing import Any

from bot.models import Candle, Position


HOSTS = {
    "demo": ("xapi.xtb.com", 5124),
    "real": ("xapi.xtb.com", 5112),
}

CMD_BUY = 0
TYPE_OPEN = 0
TYPE_CLOSE = 2


class XTBError(RuntimeError):
    pass


class XTBClient:
    """Synchronous xAPI client covering the small surface this bot needs."""

    def __init__(self, mode: str = "demo", timeout: float = 15.0) -> None:
        if mode not in HOSTS:
            raise ValueError(f"mode must be one of {sorted(HOSTS)}, got {mode!r}")
        self.mode = mode
        self._timeout = timeout
        self._sock: ssl.SSLSocket | None = None
        self._session_id: str | None = None

    # -- connection ---------------------------------------------------------

    def connect(self) -> None:
        host, port = HOSTS[self.mode]
        raw = socket.create_connection((host, port), timeout=self._timeout)
        context = ssl.create_default_context()
        self._sock = context.wrap_socket(raw, server_hostname=host)

    def login(self, user_id: str, password: str) -> None:
        if not user_id or not password:
            raise XTBError("XTB_USER_ID and XTB_PASSWORD must be set")
        data = self._command("login", {"userId": user_id, "password": password})
        self._session_id = data.get("streamSessionId")

    def logout(self) -> None:
        if self._sock is not None:
            try:
                self._command("logout", {})
            except Exception:
                pass
            self._sock.close()
            self._sock = None

    def ping(self) -> None:
        self._command("ping", {})

    # -- market data --------------------------------------------------------

    def get_candles(self, symbol: str, period_minutes: int, bars: int) -> list[Candle]:
        """Fetch the most recent ``bars`` candles for ``symbol``.

        xAPI returns ``open`` as an absolute scaled price and close/high/low as
        scaled OFFSETS relative to open; everything divides by 10**digits.
        """
        start_ms = int(time.time() * 1000) - bars * period_minutes * 60_000 * 2
        data = self._command(
            "getChartLastRequest",
            {"info": {"period": period_minutes, "start": start_ms, "symbol": symbol}},
        )
        digits = int(data.get("digits", 2))
        scale = 10**digits
        candles: list[Candle] = []
        for rate in data.get("rateInfos", []):
            open_price = rate["open"] / scale
            candles.append(
                Candle(
                    ts=int(rate["ctm"]),
                    open=open_price,
                    close=open_price + rate["close"] / scale,
                    high=open_price + rate["high"] / scale,
                    low=open_price + rate["low"] / scale,
                    volume=float(rate.get("vol", 0.0)),
                )
            )
        return candles[-bars:]

    def get_symbol(self, symbol: str) -> dict[str, Any]:
        return self._command("getSymbol", {"symbol": symbol})

    # -- account state ------------------------------------------------------

    def get_equity(self) -> float:
        data = self._command("getMarginLevel", {})
        return float(data.get("equity", data.get("balance", 0.0)))

    def get_open_positions(self) -> dict[str, Position]:
        records = self._command("getTrades", {"openedOnly": True})
        positions: dict[str, Position] = {}
        for record in records or []:
            if record.get("cmd") != CMD_BUY or record.get("closed"):
                continue
            symbol = record.get("symbol", "")
            positions[symbol] = Position(
                symbol=symbol,
                volume=float(record.get("volume", 0.0)),
                open_price=float(record.get("open_price", 0.0)),
                stop_loss=float(record.get("sl", 0.0)),
                opened_ts=int(record.get("open_time", 0)),
                order_id=record.get("order"),
            )
        return positions

    # -- orders (long-only) -------------------------------------------------

    def market_buy(self, symbol: str, volume: float, stop_loss: float) -> int:
        info = self.get_symbol(symbol)
        ask = float(info.get("ask", 0.0))
        if ask <= 0:
            raise XTBError(f"no ask price for {symbol}")
        trade_info = {
            "cmd": CMD_BUY,
            "type": TYPE_OPEN,
            "symbol": symbol,
            "volume": volume,
            "price": ask,
            "sl": round(stop_loss, int(info.get("precision", 2))),
            "tp": 0.0,
            "order": 0,
            "expiration": 0,
            "customComment": "trading-bot",
        }
        data = self._command("tradeTransaction", {"tradeTransInfo": trade_info})
        return int(data.get("order", 0))

    def close_position(self, position: Position) -> int:
        info = self.get_symbol(position.symbol)
        bid = float(info.get("bid", 0.0))
        trade_info = {
            "cmd": CMD_BUY,
            "type": TYPE_CLOSE,
            "symbol": position.symbol,
            "volume": position.volume,
            "price": bid,
            "order": position.order_id or 0,
            "sl": 0.0,
            "tp": 0.0,
            "expiration": 0,
            "customComment": "trading-bot",
        }
        data = self._command("tradeTransaction", {"tradeTransInfo": trade_info})
        return int(data.get("order", 0))

    def order_status(self, order_id: int) -> dict[str, Any]:
        return self._command("tradeTransactionStatus", {"order": order_id})

    # -- wire protocol ------------------------------------------------------

    def _command(self, command: str, arguments: dict[str, Any]) -> Any:
        if self._sock is None:
            raise XTBError("not connected - call connect() first")
        payload: dict[str, Any] = {"command": command}
        if arguments:
            payload["arguments"] = arguments
        self._sock.sendall(json.dumps(payload).encode("utf-8"))
        response = self._read_response()
        if not response.get("status", False):
            code = response.get("errorCode", "?")
            descr = response.get("errorDescr", "unknown error")
            raise XTBError(f"{command} failed: [{code}] {descr}")
        return response.get("returnData")

    def _read_response(self) -> dict[str, Any]:
        assert self._sock is not None
        buffer = b""
        deadline = time.monotonic() + self._timeout
        while time.monotonic() < deadline:
            chunk = self._sock.recv(65536)
            if not chunk:
                raise XTBError("connection closed by server")
            buffer += chunk
            text = buffer.decode("utf-8", errors="replace").strip()
            if not text:
                continue
            try:
                return json.loads(text)
            except json.JSONDecodeError:
                continue  # partial message - keep reading
        raise XTBError("timed out waiting for response")
