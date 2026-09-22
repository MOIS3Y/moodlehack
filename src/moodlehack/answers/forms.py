"""Native Django forms for creating and editing answers."""

from typing import TYPE_CHECKING

from django import forms
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from moodlehack.core.forms import TablerBoundField

from .models import Answer

if TYPE_CHECKING:
    AnswerModelForm = forms.ModelForm[Answer]
else:
    AnswerModelForm = forms.ModelForm


class AnswerForm(AnswerModelForm):
    """Validate answers and provide widgets for the shared field template."""

    bound_field_class: type[forms.BoundField] | None = TablerBoundField

    class Meta:
        model: type[Answer] = Answer
        fields: list[str] = [
            "question",
            "answer",
            "note",
            "category",
            "status",
            "month",
            "year",
            "url",
            "tag",
        ]
        widgets: dict[str, forms.Widget] = {
            "question": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": _("Enter question..."),
                    "hx-post": reverse_lazy("answers:check_question"),
                    "hx-trigger": "keyup changed delay:500ms",
                    "hx-target": "next .validation-container",
                    "aria-describedby": "id_question_error",
                }
            ),
            "answer": forms.Textarea(
                attrs={"rows": 10, "placeholder": _("Enter answer...")}
            ),
            "note": forms.Textarea(
                attrs={"rows": 3, "placeholder": _("Enter optional note...")}
            ),
            "url": forms.URLInput(
                attrs={"placeholder": "https://example.com"}
            ),
            "tag": forms.TextInput(attrs={"placeholder": _("tag")}),
        }
