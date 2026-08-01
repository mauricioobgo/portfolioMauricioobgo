from __future__ import annotations

import json
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bot.alpaca import AlpacaClient, AlpacaError
from bot.models import Position


class FakeTransport:
    """Records requests and replays canned JSON responses per URL substring."""

    def __init__(self, responses: dict[str, object]) -> None:
        self._responses = responses
        self.requests: list[urllib.request.Request] = []

    def __call__(self, request: urllib.request.Request, timeout: float) -> bytes:
        self.requests.append(request)
        for fragment, payload in self._responses.items():
            if fragment in request.full_url:
                return json.dumps(payload).encode("utf-8")
        raise AssertionError(f"unexpected request: {request.full_url}")


def _client(responses: dict[str, object]) -> tuple[AlpacaClient, FakeTransport]:
    transport = FakeTransport(responses)
    client = AlpacaClient("key", "secret", mode="paper", transport=transport)
    return client, transport


def test_connect_sends_auth_headers_to_paper_host() -> None:
    client, transport = _client({"/v2/account": {"equity": "10000"}})
    client.connect()
    request = transport.requests[0]
    assert request.full_url.startswith("https://paper-api.alpaca.markets")
    assert request.get_header("Apca-api-key-id") == "key"
    assert request.get_header("Apca-api-secret-key") == "secret"


def test_connect_requires_credentials() -> None:
    client = AlpacaClient("", "", transport=FakeTransport({}))
    try:
        client.connect()
        raise AssertionError("expected AlpacaError for missing credentials")
    except AlpacaError:
        pass


def test_get_candles_parses_bars_and_daily_timeframe() -> None:
    bars = {
        "bars": [
            {"t": "2024-01-02T05:00:00Z", "o": 100, "h": 102, "l": 99, "c": 101, "v": 5000},
            {"t": "2024-01-03T05:00:00Z", "o": 101, "h": 103, "l": 100, "c": 102, "v": 6000},
        ]
    }
    client, transport = _client({"/v2/stocks/AAPL/bars": bars})
    candles = client.get_candles("AAPL", 1440, 10)
    assert "timeframe=1Day" in transport.requests[0].full_url
    assert "data.alpaca.markets" in transport.requests[0].full_url
    assert len(candles) == 2
    assert candles[0].open == 100 and candles[0].close == 101
    assert candles[1].ts > candles[0].ts > 0


def test_market_buy_sends_oto_order_with_stop() -> None:
    client, transport = _client({"/v2/orders": {"id": "abc-123"}})
    order_id = client.market_buy("MSFT", volume=7, stop_loss=311.456)
    assert order_id == "abc-123"
    request = transport.requests[0]
    assert request.method == "POST"
    body = json.loads(request.data.decode("utf-8"))
    assert body["symbol"] == "MSFT"
    assert body["side"] == "buy"
    assert body["qty"] == "7"
    assert body["order_class"] == "oto"
    assert body["stop_loss"]["stop_price"] == "311.46"


def test_positions_filters_to_long_only() -> None:
    records = [
        {"symbol": "AAPL", "qty": "10", "avg_entry_price": "180.5", "side": "long"},
        {"symbol": "TSLA", "qty": "3", "avg_entry_price": "200.0", "side": "short"},
    ]
    client, _ = _client({"/v2/positions": records})
    positions = client.get_open_positions()
    assert set(positions) == {"AAPL"}
    assert positions["AAPL"].volume == 10
    assert positions["AAPL"].open_price == 180.5


def test_close_position_uses_delete() -> None:
    client, transport = _client({"/v2/positions/AAPL": {"id": "close-1"}})
    position = Position(symbol="AAPL", volume=10, open_price=180.0, stop_loss=0, opened_ts=0)
    assert client.close_position(position) == "close-1"
    assert transport.requests[0].method == "DELETE"


def test_intraday_timeframes() -> None:
    client, _ = _client({})
    assert client._timeframe(1440) == "1Day"
    assert client._timeframe(60) == "1Hour"
    assert client._timeframe(15) == "15Min"
