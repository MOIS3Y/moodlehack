"""
URL routing configuration for the Starlette ASGI server.

This module defines the route mappings that combine the Django ASGI application
with static file serving for media and static assets.
"""

from django.conf import settings
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles

from moodlehack.core.asgi import application

# Route ordering matters - static and media mounts must precede the root route
# to prevent Django from handling static file requests.
routes: list[Mount] = [
    Mount(
        path=settings.MEDIA_URL,
        app=StaticFiles(directory=settings.MEDIA_ROOT),
        name="media"
    ),
    Mount(
        path=settings.STATIC_URL,
        app=StaticFiles(directory=settings.STATIC_ROOT),
        name="static"
    ),
    Mount(
        path="/",
        app=application,
        name="app"
    ),
]
