# Generated by Django 3.2.5 on 2022-01-11 12:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_alter_childmodel_image'),
        ('catalog', '0011_blockmodel_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='filemodel',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.usermodel'),
        ),
        migrations.CreateModel(
            name='AccessModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('read', models.BooleanField(default=False, verbose_name='Чтение')),
                ('write', models.BooleanField(default=False, verbose_name='Запись')),
                ('file', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.filemodel')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.usermodel')),
            ],
            options={
                'verbose_name': 'Права',
                'verbose_name_plural': 'Права',
            },
        ),
    ]