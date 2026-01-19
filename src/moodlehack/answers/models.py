import datetime
from typing import cast

from django.db import models
from django.urls import reverse
from django.utils.text import format_lazy
from django.utils.translation import gettext_lazy as _


def get_current_month():
    return datetime.datetime.now().month

def get_current_year():
    return datetime.datetime.now().year


class Category(models.Model):
    """Category for organizing answers."""

    name = models.CharField(
        max_length=50,
        db_index=True,
        verbose_name=_("Category"),
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ["name"]


class Period(models.Model):
    period = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Period (deprecated)"),
        help_text=cast(str, _(
            "Deprecated field. Will be removed in future version."
        )),
    )

    def __str__(self):
        if self.period:
            return str(self.period.strftime("%B - %Y"))
        return _("Empty period")

    class Meta:
        verbose_name = _("Period (deprecated)")
        verbose_name_plural = _("Periods (deprecated)")
        ordering = ["-period"]


class Answer(models.Model):
    """Answer to test questions with period reference."""

    # Constants for year range
    MIN_YEAR = 2023
    MAX_YEAR = 2033

    # Month choices with names for display
    MONTH_CHOICES = [
        (1, _("January")),
        (2, _("February")),
        (3, _("March")),
        (4, _("April")),
        (5, _("May")),
        (6, _("June")),
        (7, _("July")),
        (8, _("August")),
        (9, _("September")),
        (10, _("October")),
        (11, _("November")),
        (12, _("December")),
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
        (STATUS_ACTUAL, _("Actual")),
        (STATUS_OUTDATED, _("Outdated")),
        (STATUS_DRAFT, _("Draft")),
        (STATUS_REVIEW, _("Under review")),
        (STATUS_UNKNOWN, _("Unknown")),
    ]

    # Model fields
    question = models.TextField(
        unique=True,
        verbose_name=_("Question"),
    )

    answer = models.TextField(
        verbose_name=_("Answer"),
    )

    url = models.URLField(
        null=True,
        blank=True,
        verbose_name=_("Source"),
    )

    tag = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name=_("Tag"),
    )

    # Month field with current month as default
    month = models.IntegerField(
        verbose_name=_("Month"),
        choices=MONTH_CHOICES,
        default=get_current_month,
        help_text=cast(str, _("Answer month (new system)")),
    )

    # Year field with current year as default
    year = models.IntegerField(
        verbose_name=_("Year"),
        choices=YEAR_CHOICES,
        default=get_current_year,
        help_text=cast(str, format_lazy(
            _("Year in range {min}-{max} (new system)"),
            min=MIN_YEAR,
            max=MAX_YEAR
        )),
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_ACTUAL,
        verbose_name=_("Status"),
        help_text=cast(str, _("Answer relevance")),
    )

    create = models.DateTimeField(
        _("Created"),
        auto_now_add=True,
    )

    update = models.DateTimeField(
        _("Updated"),
        auto_now=True,
    )

    category = models.ForeignKey(
        "Category",
        on_delete=models.PROTECT,
        verbose_name=_("Category"),
    )

    #! DEPRECATED: Old period field for backward compatibility
    period = models.ForeignKey(
        "Period",
        on_delete=models.PROTECT,
        verbose_name=_("Period (deprecated)"),
        help_text=cast(str, _(
            "Deprecated field. Will be removed in future version."
        )),
        null=True,
        blank=True,
    )

    #! DEPRECATED: Old actual field for backward compatibility
    actual = models.BooleanField(
        _("Actual (deprecated)"),
        default=True,
        null=True,
        blank=True,
        help_text=cast(str, _(
            "Deprecated field. Will be removed in future version."
        )),
    )

    def get_absolute_url(self):
        return reverse("answers:answer", kwargs={"pk": self.pk})

    @property
    def period_display(self):
        """Display as 'January 2026'."""
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
        verbose_name = _("Answer")
        verbose_name_plural = _("Answers")
        ordering = ["-year", "-month", "update"]
