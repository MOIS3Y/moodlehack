"""
Lifespan event handlers for application.

This module contains all startup and shutdown logic for the ASGI application.
"""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from starlette.applications import Starlette


@asynccontextmanager
async def lifespan(app: Starlette) -> AsyncIterator[None]:
    """Main lifespan handler."""

    # add actions below before app run:

    # .................................
    yield
    # .................................

    # add actions below after app stop:
