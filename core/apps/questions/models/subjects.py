from django.db import models

from core.apps.common.models import TimedBaseModel


class Subject(TimedBaseModel):
    subject = models.CharField(
        verbose_name='Тема',
        max_length=255,
    )
    is_visible = models.BooleanField(
        verbose_name='Виден ли тема в списке',
        default=True,
    )

    class Meta:
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'

    def __str__(self) -> str:
        return self.subject