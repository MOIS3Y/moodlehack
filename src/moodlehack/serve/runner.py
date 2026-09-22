"""
Uvicorn server runner for application.

This module provides the main entry point for running the production server
using Uvicorn with configuration loaded from application settings.
"""

from collections.abc import Callable
from typing import cast

import uvicorn
from django.conf import settings


def runserver() -> None:
    """Run Uvicorn with options validated by the dynamic settings model."""
    options = cast(dict[str, object], settings.UVICORN)
    # The runtime-derived schema validates this dynamic keyword interface.
    start = cast(Callable[..., None], uvicorn.run)
    start(
        app="moodlehack.serve.asgi:application",
        **options,
    )
