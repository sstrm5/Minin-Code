from abc import ABC, abstractmethod

from core.apps.customers.entities import CustomerEntity
from django.core.mail import send_mail

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
        message = f'Здравствуйте, {customer.first_name}! Ваш одноразовый код: {code}\nЕсли вы получили код по ошибке, просто проигнорируйте его.'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [customer.email]
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
        )
