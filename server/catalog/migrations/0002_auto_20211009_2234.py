# Generated by Django 3.2.5 on 2021-10-09 22:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='foldermodel',
            options={'verbose_name': 'Директория', 'verbose_name_plural': 'Директории'},
        ),
        migrations.AddField(
            model_name='foldermodel',
            name='parent',
            field=models.CharField(default='-1', max_length=300, verbose_name='Раздел'),
        ),
    ]
