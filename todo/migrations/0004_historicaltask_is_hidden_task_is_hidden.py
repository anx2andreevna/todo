# Generated by Django 4.2.7 on 2024-03-03 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0003_historicaltask'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicaltask',
            name='is_hidden',
            field=models.BooleanField(default=False, verbose_name='Скрыт'),
        ),
        migrations.AddField(
            model_name='task',
            name='is_hidden',
            field=models.BooleanField(default=False, verbose_name='Скрыт'),
        ),
    ]
