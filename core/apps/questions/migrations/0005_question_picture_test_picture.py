# Generated by Django 5.1.2 on 2024-10-28 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0004_attempt'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='questions/questions_pictures', verbose_name='Изображение вопроса'),
        ),
        migrations.AddField(
            model_name='test',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='questions/tests_pictures', verbose_name='Изображение теста'),
        ),
    ]
