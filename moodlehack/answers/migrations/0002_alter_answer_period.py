# Generated by Django 4.2.2 on 2023-06-28 07:37

from django.db import migrations
import month.models


class Migration(migrations.Migration):

    dependencies = [
        ('answers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='period',
            field=month.models.MonthField(help_text='some help...', verbose_name='Month Value'),
        ),
    ]