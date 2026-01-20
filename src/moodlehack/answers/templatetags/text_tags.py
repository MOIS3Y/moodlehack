import markdown
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name="markdown")
def markdown_format(text):
    """
    Converts markdown text to safe HTML.
    - 'extra': complex structures like tables, code blocks.
    - 'nl2br': treats single newlines as <br>.
    - 'sane_lists': makes lists behavior more predictable.
    """
    if not text:
            return ""

    md_extensions = [
        'extra',
        'nl2br',
        'sane_lists',
        'toc',
    ]

    html_content = markdown.markdown(text, extensions=md_extensions)
    return mark_safe(html_content)
