# Generated by Django 3.2.5 on 2021-09-26 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20210926_1733'),
    ]

    operations = [
        migrations.AddField(
            model_name='childmodel',
            name='statusNet',
            field=models.BooleanField(default=True, verbose_name='Подключение к интернету'),
        ),
    ]
