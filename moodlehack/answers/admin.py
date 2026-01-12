from django.contrib import admin
from django.utils.html import format_html

from .models import Answer, Category, Period


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
    ]
    list_display_links = [
        "id",
        "name",
    ]
    search_fields = [
        "name",
    ]


@admin.register(Period)
class PeriodAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "__str__",
        "period",
    ]
    list_display_links = [
        "id",
        "__str__",
    ]
    search_fields = [
        "period",
    ]
    list_filter = [
        "period",
    ]


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "short_question",
        "status",
        "category",
        "month_display",
        "year",
        "source_display",
        "create",
    ]
    list_display_links = [
        "id",
        "short_question",
    ]
    search_fields = [
        "question",
        "answer",
        "tag",
    ]
    list_filter = [
        "status",
        "category",
        "year",
        "month",
        "period",
    ]
    readonly_fields = [
        "create",
        "update",
    ]
    fieldsets = (
        (
            "Основная информация",
            {
                "fields": (
                    "question",
                    "answer",
                    "category",
                    "month",
                    "year",
                    "period",
                ),
            },
        ),
        (
            "Дополнительная информация",
            {
                "fields": (
                    "url",
                    "tag",
                    "status",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Системная информация",
            {
                "fields": (
                    "create",
                    "update",
                ),
                "classes": ("collapse",),
            },
        ),
    )

    @admin.display(description="Вопрос")
    def short_question(self, obj):
        if len(obj.question) > 80:
            return f"{obj.question[:80]}..."
        return obj.question

    @admin.display(description="Месяц")
    def month_display(self, obj):
        return obj.month_display

    @admin.display(description="Источник")
    def source_display(self, obj):
        if obj.url:
            return format_html(
                '<a href="{}" target="_blank">Источник</a>',
                obj.url,
            )
        return "—"

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related("category", "period")


admin.site.site_title = "Akvolabean"
admin.site.site_header = "AKVOLABEAN"
