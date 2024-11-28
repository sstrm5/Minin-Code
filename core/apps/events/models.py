from django.db import models
from core.apps.common.models import TimedBaseModel
from core.apps.customers.models import Customer
from core.apps.events.entities import Event as EventEntity

# Create your models here.


class Event(TimedBaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    address = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text='Например, улица Интернациональная, дом 123, корпус 4, строение 5'
    )
    picture = models.ImageField(
        upload_to='events/pictures',
        blank=True,
        null=True,
    )
    is_visible = models.BooleanField(default=True)
    organizer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='organized_events',
        verbose_name='Организатор',
        null=True,
        blank=True,
    )

    def to_entity(self):
        return EventEntity(
            id=self.id,
            title=self.title,
            description=self.description,
            address=self.address,
            picture=self.picture.url if self.picture else None,
            is_visible=self.is_visible,
            organizer_name=self.organizer.organization_name if self.organizer else 'Не указан',
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    class Meta:
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'

    def __str__(self) -> str:
        return self.title
