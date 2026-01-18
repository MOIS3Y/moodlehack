"""ASGI application factory for app."""

from starlette.applications import Starlette


def get_asgi_application() -> Starlette:
    """Get or create ASGI application instance."""
    import django
    from django.apps import apps
    from django.conf import settings

    from .lifespan import lifespan
    from .middleware import middleware
    from .routes import routes

    if not apps.ready:
        django.setup(set_prefix=False)

    return Starlette(
        debug=settings.DEBUG,
        routes=routes,
        middleware=middleware,
        lifespan=lifespan
    )

application = get_asgi_application()
