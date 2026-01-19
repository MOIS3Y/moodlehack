from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from .models import Answer, Category, Period


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


# Deprecated it will be removed
class PeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Period
        fields = "__all__"


class AnswerSerializer(serializers.ModelSerializer):
    # Read-only properties from the model
    period_display = serializers.ReadOnlyField()
    quarter = serializers.ReadOnlyField()
    quarter_display = serializers.ReadOnlyField()
    month_display = serializers.ReadOnlyField()
    status_display = serializers.CharField(
        source="get_status_display",
        read_only=True,
    )

    # Standard timestamps
    create = serializers.DateTimeField(read_only=True)
    update = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Answer
        fields = [
            "id",
            "question",
            "answer",
            "note",
            "url",
            "tag",
            "status",
            "month",
            "year",
            "category",
            "period_display",
            "month_display",
            "quarter",
            "quarter_display",
            "status_display",
            "create",
            "update",
            # Deprecated fields
            "period",
            "actual",
        ]

        # Swagger/OpenAPI deprecation notice
        extra_kwargs = {
            "period": {
                "help_text": _("DEPRECATED: Use month and year."),
            },
            "actual": {
                "help_text": _("DEPRECATED: Use status."),
            },
        }

    def get_fields(self):
        """
        Set deprecated flag for OpenAPI schema generator.
        """
        fields = super().get_fields()

        # drf-spectacular recognizes this attribute during schema generation
        if "period" in fields:
            fields["period"].deprecated = True
        if "actual" in fields:
            fields["actual"].deprecated = True

        return fields
