"""Long-only stock trading bot with an XTB (xAPI) connector.

Safety model:
- ``backtest`` and ``paper`` modes never touch a broker.
- ``run --mode demo`` trades only on an XTB *demo* account.
- ``run --mode real`` requires an explicit flag plus an interactive confirmation.
"""

__all__ = ["__version__"]

__version__ = "0.1.0"
