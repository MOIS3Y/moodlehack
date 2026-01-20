"""
Serve package for running the application with Uvicorn.

This package provides the production server setup for app,
combining Django ASGI application with Starlette ASGI server and
static file serving.
"""

from .runner import runserver

__all__ = ["runserver"]
