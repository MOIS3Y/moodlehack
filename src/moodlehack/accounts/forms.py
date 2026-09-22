"""Authentication forms styled with the shared Tabler field renderer."""

from django.contrib.auth.forms import AuthenticationForm
from django.forms import BoundField

from moodlehack.core.forms import TablerBoundField


class LoginForm(AuthenticationForm):
    """Keep Django authentication and validation with Tabler widgets."""

    bound_field_class: type[BoundField] | None = TablerBoundField
