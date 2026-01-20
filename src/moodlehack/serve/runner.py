"""
Uvicorn server runner for application.

This module provides the main entry point for running the production server
using Uvicorn with configuration loaded from application settings.
"""

import uvicorn
from django.conf import settings


def runserver() -> None:
    """Run Uvicorn server with application settings"""
    uvicorn.run(
        app="moodlehack.serve.asgi:application",
        **settings.UVICORN
    )
