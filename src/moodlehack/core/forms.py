"""Shared native Django field styling for the public Tabler interface."""

from typing import cast, override

from django import forms


class TablerBoundField(forms.BoundField):
    """Style widgets without replacing Django's validation attributes."""

    @override
    def build_widget_attrs(
        self,
        attrs: dict[str, str | bool],
        widget: forms.Widget | None = None,
    ) -> dict[str, str | bool]:
        widget = widget or cast(forms.Widget, self.field.widget)
        attrs = super().build_widget_attrs(attrs, widget)
        if widget.is_hidden:
            return attrs

        if isinstance(widget, forms.CheckboxInput):
            style = "form-check-input"
        elif isinstance(widget, forms.Select):
            style = "form-select"
        else:
            style = "form-control"

        classes = [
            str(cast(object, widget.attrs.get("class", ""))),
            str(attrs.get("class", "")),
        ]
        classes.append(style)
        if self.errors:
            classes.append("is-invalid")
        attrs["class"] = " ".join(filter(None, classes))
        return attrs
