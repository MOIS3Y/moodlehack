from django.db import models


class Category(models.Model):
    name = models.CharField(
        max_length=50, db_index=True, verbose_name='Категория'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name


class Period(models.Model):
    period = models.DateField(verbose_name='Период')

    class Meta:
        verbose_name = 'Период'
        verbose_name_plural = 'Периоды'
        ordering = ['-period']

    def __str__(self):
        return str(self.period.strftime('%B - %Y'))


class Answer(models.Model):
    question = models.TextField(unique=True, verbose_name='Вопрос')
    answer = models.TextField(verbose_name='Ответ')
    url = models.URLField(null=True, blank=True, verbose_name='Источник')
    tag = models.CharField(
        max_length=50, null=True, blank=True, verbose_name='Тег'
    )
    actual = models.BooleanField(default=True, verbose_name='Актуален')
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(
        'Category', on_delete=models.PROTECT, verbose_name='Категория'
    )
    period = models.ForeignKey(
        'Period', on_delete=models.PROTECT, verbose_name='Период'
    )

    class Meta:
        verbose_name = 'Ответы'
        verbose_name_plural = 'Ответы'
        ordering = ['update', 'period']

    def __str__(self):
        return self.question
