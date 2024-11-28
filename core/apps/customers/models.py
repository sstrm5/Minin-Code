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

    ROLE_CHOICES = [
        ('user', 'Обычный пользователь'),
        ('admin', 'Администратор'),
        ('organization', 'Организация'),
    ]

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

    role = models.CharField(
        verbose_name='Роль пользователя',
        max_length=20,
        choices=ROLE_CHOICES,
        default='user',
        help_text='Определяет роль пользователя: обычный пользователь, администратор или организация',
    )

    organization_name = models.CharField(
        verbose_name='Название организации',
        max_length=255,
        null=True,
        blank=True,
        help_text='Название организации, если пользователь представляет организацию',
    )

    def __str__(self) -> str:
        return self.email if self.role in ('admin', 'user') else self.organization_name

    def to_entity(self) -> CustomerEntity:
        return CustomerEntity(
            id=self.pk,
            email=self.email,
            first_name=self.first_name,
            last_name=self.last_name,
            created_at=self.created_at,
            role=self.role,
            organization_name=self.organization_name,
        )

    @classmethod
    def from_entity(cls, entity: CustomerEntity) -> 'Customer':
        return cls(
            id=entity.id,
            email=entity.email,
            first_name=entity.first_name,
            last_name=entity.last_name,
            role=entity.role,
            created_at=entity.created_at,
        )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
