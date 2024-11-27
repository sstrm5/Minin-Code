# Generated by Django 5.1 on 2024-10-09 13:50

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='token',
            new_name='access_token',
        ),
        migrations.AddField(
            model_name='customer',
            name='expires_in',
            field=models.BigIntegerField(default=0, verbose_name='Время до истечения access token'),
        ),
        migrations.AddField(
            model_name='customer',
            name='refresh_expires_in',
            field=models.BigIntegerField(default=0, verbose_name='Время до истечения refresh token'),
        ),
        migrations.AddField(
            model_name='customer',
            name='refresh_token',
            field=models.CharField(default=uuid.uuid4, max_length=255, verbose_name='Токен для обновления access token'),
        ),
    ]
