from django.conf import settings

# Pre-fetch at module level to avoid getattr on every request
_SITE_CACHE = getattr(settings, "SITE", {})

def site_context(request):
    """
    Expose site-wide branding settings to all templates.
    Uses module-level cache to stay efficient.
    """
    return {
        "SITE": _SITE_CACHE
    }
