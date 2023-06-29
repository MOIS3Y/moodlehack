from django.db import models
from month.models import MonthField


class Answer(models.Model):
    question = models.TextField(unique=True)
    answer = models.TextField()
    url = models.URLField()
    tag = models.CharField(max_length=50)
    actual = models.BooleanField(default=True)
    period = MonthField("Period", help_text="month of testing")
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question
