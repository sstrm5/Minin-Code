from abc import ABC, abstractmethod

from core.apps.customers.entities import CustomerEntity
from django.core.mail import send_mail

from core.apps.events.entities import Event as EventEntity
from core.apps.events.models import Event
from core.project.settings import local as settings


class BaseSenderService(ABC):
    @abstractmethod
    def send_code(self, customer: CustomerEntity, code: str) -> None:
        ...


class DummySenderService(BaseSenderService):
    def send_code(self, customer: CustomerEntity, code: str) -> None:
        print(f'Code to user: {customer}, sent: {code}')


class MailSenderService(BaseSenderService):
    def send_code(self, customer: CustomerEntity, code: str) -> None:
        subject = 'Код подтверждения'
        message = f"""Здравствуйте, {customer.first_name}! Ваш одноразовый код: {
            code}\nЕсли вы получили код по ошибке, просто проигнорируйте его."""
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [customer.email]
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
        )

    def send_event_notification(self, customer, event: EventEntity) -> None:
        subject = 'Запись на мероприятие'
        message = f"""Здравствуйте, {customer.first_name}! Вы записались на мероприятие {
            event.title}, которое пройдет по адресу {event.address}. Дата и время проведения по МСК: {event.start_time}."""
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [customer.email]
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
        )

    # Присылает уведомление администратору о новом участнике в мероприятии
    def send_orginizer_notification(self, customer, event: EventEntity) -> None:
        subject = 'Новый участник в мероприятии'
        message = f"""Уважаемый организатор, новый участник зарегистрирован в мероприятии {
            event.title}. Данные участника: {customer.first_name} {customer.last_name}, {customer.email}."""
        from_email = settings.EMAIL_HOST_USER
        event = Event.objects.get(id=event.id)
        recipient_list = [event.organizer.email]
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
        )
