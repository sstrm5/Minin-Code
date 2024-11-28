from django.db import models
from core.apps.common.models import TimedBaseModel
from core.apps.customers.models import Customer
from core.apps.news.entities import News as NewsEntity

# Create your models here.


class News(TimedBaseModel):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='news',
        blank=True,
        null=True,
    )
    text = models.TextField(
        verbose_name='Текст новости',
        help_text='Максимальное количество символов: 5000',
        max_length=5000,
    )
    additional_text = models.TextField(
        verbose_name='Дополнительный текст',
        help_text='Максимальное количество символов: 2000',
        max_length=2000,
        blank=True,
        null=True,
    )
    author = models.ForeignKey(
        Customer,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='news',
        blank=True,
        null=True,
    )
    is_published = models.BooleanField(
        verbose_name='Опубликовано',
        default=True,
    )

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def to_entity(self):
        return NewsEntity(
            id=self.pk,
            title=self.title,
            image=self.image.url if self.image else '',
            text=self.text,
            additional_text=self.additional_text,
            is_published=self.is_published,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
