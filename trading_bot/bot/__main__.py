"""CLI entrypoint.

Usage (from the trading_bot/ directory):

    python -m bot backtest                # synthetic-data backtest (no network)
    python -m bot backtest --file c.json  # backtest candles from a JSON file
    python -m bot run                     # demo account, dry-run (logs only)
    python -m bot run --execute           # demo account, real demo orders
    python -m bot run --mode real --execute --i-understand-the-risks
                                          # real money - requires typed confirmation
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

from bot.backtest import format_report, run_backtest, synthetic_candles
from bot.config import Config
from bot.engine import TradingEngine
from bot.models import Candle
from bot.xtb import XTBClient


def _load_candles_file(path: Path) -> dict[str, list[Candle]]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    result: dict[str, list[Candle]] = {}
    for symbol, rows in raw.items():
        result[symbol] = [Candle(**row) for row in rows]
    return result


def cmd_backtest(args: argparse.Namespace) -> int:
    config = Config.from_env(env_file=Path(args.env))
    if args.file:
        candles_by_symbol = _load_candles_file(Path(args.file))
    else:
        candles_by_symbol = {
            symbol: synthetic_candles(args.bars, seed=index + 1)
            for index, symbol in enumerate(config.watchlist)
        }
        print(f"(no --file given: using synthetic data, {args.bars} bars per symbol)\n")
    result = run_backtest(config, candles_by_symbol, initial_cash=args.cash)
    print(format_report(result))
    return 0


def cmd_run(args: argparse.Namespace) -> int:
    config = Config.from_env(env_file=Path(args.env))
    config.mode = args.mode
    config.dry_run = not args.execute
    config.validate()

    if config.mode == "real":
        if not args.i_understand_the_risks:
            print("Refusing to run in real mode without --i-understand-the-risks.")
            return 2
        answer = input(
            "You are about to trade with REAL MONEY. Automated strategies can lose "
            "money quickly.\nType 'trade real money' to continue: "
        )
        if answer.strip().lower() != "trade real money":
            print("Aborted.")
            return 2

    client = XTBClient(mode=config.mode)
    client.connect()
    client.login(config.xtb_user_id, config.xtb_password)
    engine = TradingEngine(config, client)
    try:
        if args.once:
            engine.run_once()
        else:
            engine.run_forever()
    except KeyboardInterrupt:
        print("stopped by user")
    finally:
        client.logout()
    return 0


def main(argv: list[str] | None = None) -> int:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    parser = argparse.ArgumentParser(prog="bot", description="Long-only stock trading bot")
    parser.add_argument("--env", default=".env", help="path to .env file (default: .env)")
    sub = parser.add_subparsers(dest="command", required=True)

    p_backtest = sub.add_parser("backtest", help="run a backtest (no broker, no network)")
    p_backtest.add_argument("--file", help="JSON file: {symbol: [candle, ...]}")
    p_backtest.add_argument("--bars", type=int, default=500, help="synthetic bars per symbol")
    p_backtest.add_argument("--cash", type=float, default=10_000.0, help="starting cash")
    p_backtest.set_defaults(func=cmd_backtest)

    p_run = sub.add_parser("run", help="run against XTB (demo by default, dry-run by default)")
    p_run.add_argument("--mode", choices=["demo", "real"], default="demo")
    p_run.add_argument("--execute", action="store_true", help="actually send orders")
    p_run.add_argument("--once", action="store_true", help="single cycle instead of a loop")
    p_run.add_argument("--i-understand-the-risks", action="store_true")
    p_run.set_defaults(func=cmd_run)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
