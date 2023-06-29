from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Period, Answer


# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


class PeriodAdmin(admin.ModelAdmin):
    list_display = ('id', 'period')
    search_fields = ('period',)


@admin.display(description="Click URL")
class AnswerAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'question', 'answer', 'source', 'actual', 'period', 'category'
    )
    # list_display_links = ()
    search_fields = ('question', 'answer')
    list_filter = ('category', 'period')

    def source(self, obj):
        return format_html(
            "<a href='{url}' target='_blank'>{url}</a>", url=obj.url
        )


admin.site.register(Category, CategoryAdmin)
admin.site.register(Period, PeriodAdmin)
admin.site.register(Answer, AnswerAdmin)

admin.site.site_title = 'Akvolabean'
admin.site.site_header = 'AKVOLABEAN'
