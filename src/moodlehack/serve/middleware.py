"""
ASGI Middleware configuration for the Starlette server.

This module defines a list of Starlette middleware classes that wrap the
entire application. These run before the request reaches the Django
application layer.

Key components:
    - TrustedHostMiddleware: Prevents HTTP Host Header attacks by validating
      the Host header against the Django ALLOWED_HOSTS setting.
"""

from django.conf import settings
from starlette.middleware import Middleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

middleware = [
    Middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.ALLOWED_HOSTS,
    ),
]
