"""Compatibility module for Reflex app discovery.

Reflex resolves app modules as `<app_name>.<app_name>` based on `rxconfig.py`.
This module re-exports the canonical `app` instance from `portfolio_app.app`.
"""

from .app import app

__all__ = ["app"]
