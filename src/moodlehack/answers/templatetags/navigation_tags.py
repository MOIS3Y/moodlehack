from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def update_query_params(context, **kwargs):
    """
    Updates the current URL query parameters with the provided arguments.

    If a parameter's value is None or an empty string,
    it is removed from the URL.
    This ensures clean URLs without redundant or empty keys.
    """
    request = context.get("request")
    if not request:
        return ""

    params = request.GET.copy()

    for key, value in kwargs.items():
        if value is not None and value != "":
            params[key] = value
        else:
            # Safely remove the key to prevent empty params like '?page='
            params.pop(key, None)

    # Return the encoded query string prefixed with '?'
    return f"?{params.urlencode()}"
