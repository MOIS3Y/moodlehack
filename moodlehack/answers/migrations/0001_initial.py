# Generated by Django 4.2.2 on 2023-06-29 13:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=50, verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Period',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('period', models.DateField(verbose_name='Период')),
            ],
            options={
                'verbose_name': 'Период',
                'verbose_name_plural': 'Периоды',
                'ordering': ['period'],
            },
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField(unique=True, verbose_name='Вопрос')),
                ('answer', models.TextField(verbose_name='Ответ')),
                ('url', models.URLField(blank=True, null=True, verbose_name='Источник')),
                ('tag', models.CharField(blank=True, max_length=50, null=True, verbose_name='Тег')),
                ('actual', models.BooleanField(default=True, verbose_name='Актуален')),
                ('create', models.DateTimeField(auto_now_add=True)),
                ('update', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='answers.category', verbose_name='Категория')),
                ('period', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='answers.period', verbose_name='Период')),
            ],
            options={
                'verbose_name': 'Ответы',
                'verbose_name_plural': 'Ответы',
                'ordering': ['update', 'period'],
            },
        ),
    ]
