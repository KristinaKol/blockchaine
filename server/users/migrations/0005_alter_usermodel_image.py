# Generated by Django 3.2.5 on 2021-09-30 00:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20210930_0024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='images/users/', verbose_name='Фото'),
        ),
    ]
