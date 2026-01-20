from crispy_forms.bootstrap import StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Div, Field, Layout, Row
from django import forms
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from .models import Answer


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = [
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Identify if we are editing an existing record
        instance_id = self.instance.pk if self.instance.pk else ""

        self.helper = FormHelper()
        self.helper.form_id = "answer-form"
        self.helper.form_method = "post"
        self.helper.form_class = "needs-validation"
        self.helper.attrs = {"novalidate": ""}

        # Labels with icons
        icon_save = mark_safe('<i class="bi bi-check-lg me-2"></i>')
        icon_add = mark_safe('<i class="bi bi-plus-circle me-2"></i>')
        icon_continue = mark_safe('<i class="bi bi-arrow-repeat me-2"></i>')

        # Define buttons logic
        if not self.instance.pk:
            # Buttons for CreateView
            submit_buttons = Row(
                Column(
                    StrictButton(
                        icon_add + _("Save and add next"),
                        name="save_and_add",
                        type="submit",
                        css_class="btn btn-success w-100",  # Green
                    ),
                    css_class="col-12 col-lg-auto mb-2 mb-lg-0",
                ),
                Column(
                    StrictButton(
                        icon_continue + _("Save and continue editing"),
                        name="save_and_continue",
                        type="submit",
                        css_class="btn btn-warning w-100",  # Yellow
                    ),
                    css_class="col-12 col-lg-auto mb-2 mb-lg-0",
                ),
                Column(
                    StrictButton(
                        icon_save + _("Save"),
                        name="submit",
                        type="submit",
                        css_class="btn btn-primary w-100",  # Blue
                    ),
                    css_class="col-12 col-lg-auto",
                ),
                css_class="justify-content-lg-end g-lg-2",
            )
        else:
            # Buttons for UpdateView
            submit_buttons = Row(
                Column(
                    StrictButton(
                        icon_continue + _("Save and continue editing"),
                        name="save_and_continue",
                        type="submit",
                        css_class="btn btn-warning w-100",  # Yellow
                    ),
                    css_class="col-12 col-lg-auto mb-2 mb-lg-0",
                ),
                Column(
                    StrictButton(
                        icon_save + _("Save changes"),
                        name="submit",
                        type="submit",
                        css_class="btn btn-primary w-100",  # Blue
                    ),
                    css_class="col-12 col-lg-auto",
                ),
                css_class="justify-content-lg-end g-lg-2",
            )

        self.helper.layout = Layout(
            Div(
                Field(
                    "question",
                    rows="3",
                    placeholder=_("Enter question..."),
                    css_class="mb-1",
                    hx_post=reverse_lazy("answers:check_question"),
                    hx_trigger="keyup changed delay:500ms",
                    hx_target="next .validation-container",
                    hx_vals=f'{{"instance_id": "{instance_id}"}}',
                ),
                Div(css_class="validation-container mb-3"),
            ),
            Field(
                "answer",
                rows="10",
                placeholder=_("Enter answer..."),
                css_class="mb-3 form-control",
            ),
            Field(
                "note",
                rows="3",
                placeholder=_("Enter optional note..."),
                css_class="mb-3 form-control",
            ),
            Row(
                Column(
                    Field("category", css_class="form-select"),
                    css_class="col-md-3",
                ),
                Column(
                    Field("status", css_class="form-select"),
                    css_class="col-md-3",
                ),
                Column(
                    Field("month", css_class="form-select"),
                    css_class="col-md-3",
                ),
                Column(
                    Field("year", css_class="form-select"),
                    css_class="col-md-3",
                ),
                css_class="g-3 mb-3",
            ),
            Row(
                Column(
                    Field(
                        "url",
                        placeholder="https://example.com",
                        css_class="form-control",
                    ),
                    css_class="col-md-8",
                ),
                Column(
                    Field(
                        "tag",
                        placeholder=_("tag"),
                        css_class="form-control"
                    ),
                    css_class="col-md-4",
                ),
                css_class="g-3 mb-4",
            ),
            submit_buttons,
        )
