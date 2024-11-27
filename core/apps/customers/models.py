import time
from uuid import uuid4
from django.db import models

from core.apps.common.models import TimedBaseModel
from core.apps.customers.entities import CustomerEntity


class Customer(TimedBaseModel):
    def get_expires_in():
        return int(time.time()) + 3600

    def get_refresh_expires_in():
        return int(time.time()) + 1209600

    email = models.CharField(
        verbose_name='Почта пользователя',
        unique=True,
        help_text='Уникальный почта каждого пользователя',
    )

    first_name = models.CharField(
        verbose_name='Имя',
        max_length=50,
        null=True,
    )

    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=50,
        null=True,
    )

    access_token = models.CharField(
        verbose_name='Токен авторизации',
        default=uuid4,
        max_length=255,
    )

    refresh_token = models.CharField(
        verbose_name='Токен для обновления access token',
        default=uuid4,
        max_length=255,
    )

    expires_in = models.BigIntegerField(
        verbose_name='Время до истечения access token',
        default=get_expires_in,
    )

    refresh_expires_in = models.BigIntegerField(
        verbose_name='Время до истечения refresh token',
        default=get_refresh_expires_in,
    )

    def __str__(self) -> str:
        return self.email

    def to_entity(self) -> CustomerEntity:
        return CustomerEntity(
            id=self.pk,
            email=self.email,
            first_name=self.first_name,
            last_name=self.last_name,
            created_at=self.created_at,
        )

    @classmethod
    def from_entity(cls, entity: CustomerEntity) -> 'Customer':
        return cls(
            id=entity.id,
            email=entity.email,
            first_name=entity.first_name,
            last_name=entity.last_name,
            created_at=entity.created_at,
        )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
