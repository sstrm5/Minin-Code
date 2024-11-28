from django.db import models
from core.apps.common.models import TimedBaseModel
from core.apps.customers.models import Customer
from core.apps.events.entities import Condition as ConditionEntity, Event as EventEntity

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
    conditions = models.ManyToManyField(
        'Condition',
        verbose_name='Условия проведения',
        blank=True,
        related_name='events',
    )
    participants = models.ManyToManyField(
        Customer,
        verbose_name='Участники',
        blank=True,
        related_name='added_participants',
    )
    start_time = models.CharField(
        max_length=50,
        verbose_name='Дата и время начала проведения',
        blank=True,
        null=True,
    )
    max_participants = models.PositiveIntegerField(
        verbose_name='Максимальное количество участников',
        blank=True,
        null=True,
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
            conditions=[condition.to_entity()
                        for condition in self.conditions.all()],
            participants=[participant.to_entity()
                          for participant in self.participants.all()],
            start_time=self.start_time,
            max_participants=self.max_participants,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    class Meta:
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'

    def __str__(self) -> str:
        return self.title


class Condition(TimedBaseModel):
    text = models.CharField(max_length=255)
    is_visible = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.text

    class Meta:
        verbose_name = 'Условие'
        verbose_name_plural = 'Условия'

    def to_entity(self):
        return ConditionEntity(
            id=self.id,
            text=self.text,
            is_visible=self.is_visible,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
