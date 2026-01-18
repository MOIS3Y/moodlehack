"""
Django application configuration for the 'serve' module.

This module registers the 'serve' application within the Django project.
The 'serve' app is responsible for managing the ASGI/Uvicorn server
infrastructure and static/media file routing via Starlette.
"""

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ServeConfig(AppConfig):
    name = "moodlehack.serve"
    verbose_name = _("Serve")
