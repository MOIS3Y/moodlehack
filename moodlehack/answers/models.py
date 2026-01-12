import datetime

from django.db import models
from django.urls import reverse


def get_current_month():
    return datetime.datetime.now().month

def get_current_year():
    return datetime.datetime.now().year


class Category(models.Model):
    """Category for organizing answers."""

    name = models.CharField(
        max_length=50,
        db_index=True,
        verbose_name="Категория",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]


class Period(models.Model):
    period = models.DateField(
        verbose_name="Период (deprecated)",
        help_text="Устаревшее поле. Будет удалено в будущей версии.",
        null=True,
        blank=True,
    )

    def __str__(self):
        if self.period:
            return str(self.period.strftime("%B - %Y"))
        return "Пустой период"

    class Meta:
        verbose_name = "Период (deprecated)"
        verbose_name_plural = "Периоды (deprecated)"
        ordering = ["-period"]


class Answer(models.Model):
    """Answer to test questions with period reference."""

    # Constants for year range
    MIN_YEAR = 2023
    MAX_YEAR = 2033

    # Month choices with Russian names for display
    MONTH_CHOICES = [
        (1, "Январь"),
        (2, "Февраль"),
        (3, "Март"),
        (4, "Апрель"),
        (5, "Май"),
        (6, "Июнь"),
        (7, "Июль"),
        (8, "Август"),
        (9, "Сентябрь"),
        (10, "Октябрь"),
        (11, "Ноябрь"),
        (12, "Декабрь"),
    ]

    # Year choices - simple list comprehension
    YEAR_CHOICES = [
        (year, str(year)) for year in range(MIN_YEAR, MAX_YEAR + 1)
    ]

    # Status choices (short and clear)
    STATUS_ACTUAL = "actual"
    STATUS_OUTDATED = "outdated"
    STATUS_DRAFT = "draft"
    STATUS_REVIEW = "review"
    STATUS_UNKNOWN = "unknown"

    STATUS_CHOICES = [
        (STATUS_ACTUAL, "Актуален"),
        (STATUS_OUTDATED, "Устарел"),
        (STATUS_DRAFT, "Черновик"),
        (STATUS_REVIEW, "На проверке"),
        (STATUS_UNKNOWN, "Неизвестно"),
    ]

    # Model fields
    question = models.TextField(
        unique=True,
        verbose_name="Вопрос",
    )

    answer = models.TextField(
        verbose_name="Ответ",
    )

    url = models.URLField(
        null=True,
        blank=True,
        verbose_name="Источник",
    )

    tag = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Тег",
    )

    # Month field with current month as default
    month = models.IntegerField(
        verbose_name="Месяц",
        choices=MONTH_CHOICES,
        default=get_current_month,
        help_text="Месяц ответа (новая система)",
    )

    # Year field with current year as default
    year = models.IntegerField(
        verbose_name="Год",
        choices=YEAR_CHOICES,
        default=get_current_year,
        help_text=f"Год в диапазоне {MIN_YEAR}-{MAX_YEAR} (новая система)",
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_ACTUAL,
        verbose_name="Статус",
        help_text="Актуальность ответа",
    )

    create = models.DateTimeField(
        "Создан",
        auto_now_add=True,
    )

    update = models.DateTimeField(
        "Обновлен",
        auto_now=True,
    )

    category = models.ForeignKey(
        "Category",
        on_delete=models.PROTECT,
        verbose_name="Категория",
    )

    #! DEPRECATED: Old period field for backward compatibility
    period = models.ForeignKey(
        "Period",
        on_delete=models.PROTECT,
        verbose_name="Период (deprecated)",
        help_text="Устаревшее поле. Будет удалено в будущей версии.",
        null=True,
        blank=True,
    )

    #! DEPRECATED: Old actual field for backward compatibility
    actual = models.BooleanField(
        "Актуален (deprecated)",
        default=True,
        null=True,
        blank=True,
        help_text="Устаревшее поле. Будет удалено в будущей версии.",
    )

    def get_absolute_url(self):
        return reverse("answers:answer", kwargs={"pk": self.pk})

    @property
    def period_display(self):
        """Display as 'Январь 2026'."""
        month_name = dict(self.MONTH_CHOICES)[self.month]
        return f"{month_name} {self.year}"

    @property
    def period_code(self):
        """Numeric code for sorting (e.g., 202601 for January 2026)."""
        return self.year * 100 + self.month

    @property
    def quarter(self):
        """Calculate quarter (1-4) based on month."""
        return (self.month - 1) // 3 + 1

    @property
    def quarter_display(self):
        """Display quarter in format '2026 Q1'."""
        return f"{self.year} Q{self.quarter}"

    @property
    def is_actual(self):
        """Property for backward compatibility."""
        return self.status == self.STATUS_ACTUAL

    @property
    def month_display(self):
        """Display month name."""
        return dict(self.MONTH_CHOICES)[self.month]

    @property
    def status_color(self):
        """
        Returns simple color name for flexibility.
        """
        color_map = {
            self.STATUS_ACTUAL: "success",
            self.STATUS_OUTDATED: "secondary",
            self.STATUS_DRAFT: "info",
            self.STATUS_REVIEW: "warning",
            self.STATUS_UNKNOWN: "dark",
        }
        return color_map.get(self.status, "secondary")

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"
        ordering = ["-year", "-month", "update"]
