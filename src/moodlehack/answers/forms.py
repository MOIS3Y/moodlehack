from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Div, Field, Layout, Row, Submit
from django import forms
from django.urls import reverse_lazy

from .models import Answer


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = [
            "question",
            "answer",
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

        # Define buttons based on whether the object already exists
        if not self.instance.pk:
            # Buttons for CreateView
            submit_buttons = Div(
                Submit(
                    "save_and_add",
                    "Сохранить и добавить следующий",
                    css_class="btn btn-primary me-2",
                ),
                Submit("submit", "Сохранить", css_class="btn btn-primary"),
                css_class="d-flex justify-content-end",
            )
        else:
            # Button for UpdateView
            submit_buttons = Div(
                Submit("submit", "Сохранить", css_class="btn btn-primary"),
                css_class="d-flex justify-content-end",
            )

        self.helper.layout = Layout(
            Div(
                Field(
                    "question",
                    rows="3",
                    placeholder="Введите вопрос...",
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
                placeholder="Введите ответ...",
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
                    Field("tag", placeholder="тег", css_class="form-control"),
                    css_class="col-md-4",
                ),
                css_class="g-3 mb-4",
            ),
            submit_buttons,
        )
