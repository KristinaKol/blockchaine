# Generated by Django 3.2.5 on 2021-09-30 00:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_childmodel_statusnet'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermodel',
            name='email',
            field=models.CharField(blank=True, max_length=100, verbose_name='Почта'),
        ),
        migrations.AddField(
            model_name='usermodel',
            name='login',
            field=models.CharField(blank=True, max_length=100, verbose_name='Логин'),
        ),
        migrations.AddField(
            model_name='usermodel',
            name='password',
            field=models.CharField(default='', max_length=100, verbose_name='Пароль'),
        ),
        migrations.AddField(
            model_name='usermodel',
            name='phone',
            field=models.CharField(blank=True, max_length=100, verbose_name='Номер телефона'),
        ),
        migrations.AddField(
            model_name='usermodel',
            name='token',
            field=models.CharField(blank=True, max_length=100, verbose_name='Токен'),
        ),
    ]