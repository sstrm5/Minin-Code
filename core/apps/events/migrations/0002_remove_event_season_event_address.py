# Generated by Django 5.1.3 on 2024-11-28 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='season',
        ),
        migrations.AddField(
            model_name='event',
            name='address',
            field=models.CharField(blank=True, help_text='Например, улица Интернациональная, дом 123, корпус 4, строение 5', max_length=255, null=True),
        ),
    ]
