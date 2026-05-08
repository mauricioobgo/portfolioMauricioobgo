from __future__ import annotations

import argparse
from pathlib import Path

from portfolio_app.services.content import FRONTEND_CONTENT_PATH, write_frontend_content


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build the generated Flet portfolio content asset from YAML and JSON sources."
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=FRONTEND_CONTENT_PATH,
        help="Output path for the generated Flet content payload.",
    )
    args = parser.parse_args()
    write_frontend_content(output_path=args.out)


if __name__ == "__main__":
    main()
