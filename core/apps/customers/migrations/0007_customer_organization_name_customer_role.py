# Generated by Django 5.1.3 on 2024-11-28 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0006_alter_customer_expires_in_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='organization_name',
            field=models.CharField(blank=True, help_text='Название организации, если пользователь представляет организацию', max_length=255, null=True, verbose_name='Название организации'),
        ),
        migrations.AddField(
            model_name='customer',
            name='role',
            field=models.CharField(choices=[('user', 'Обычный пользователь'), ('admin', 'Администратор'), ('organization', 'Организация')], default='user', help_text='Определяет роль пользователя: обычный пользователь, администратор или организация', max_length=20, verbose_name='Роль пользователя'),
        ),
    ]
