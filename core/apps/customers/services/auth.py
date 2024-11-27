from abc import ABC, abstractmethod
from dataclasses import dataclass

from core.apps.customers.services.codes import BaseCodeService
from core.apps.customers.services.customers import BaseCustomerService
from core.apps.customers.services.senders import BaseSenderService


@dataclass(eq=False)
class BaseAuthService(ABC):
    customer_service: BaseCustomerService
    codes_service: BaseCodeService
    sender_service: BaseSenderService

    @abstractmethod
    def get_and_authorize(self, email: str):
        ...


    @abstractmethod
    def create_and_authorize(self, email: str, first_name: str, last_name: str):
        ...


    @abstractmethod
    def confirm(self, email:str, code: str):
        ...


class AuthService(BaseAuthService):
    def get_and_authorize(self, email: str):
        customer = self.customer_service.get(email=email)
        if not customer:
            raise ValueError(f'No customer found with email: {email}')
        code = self.codes_service.generate_code(customer=customer)
        self.sender_service.send_code(customer=customer, code=code)
    

    def create_and_authorize(self, email: str, first_name: str, last_name: str):
        customer = self.customer_service.get_or_create(email=email, first_name=first_name, last_name=last_name)
        code = self.codes_service.generate_code(customer=customer)
        self.sender_service.send_code(customer=customer, code=code)

    
    def confirm(self, email: str, code: str):
        customer = self.customer_service.get(email=email)
        self.codes_service.validate_code(code=code, customer=customer)
        access_token, refresh_token, expires_in = self.customer_service.generate_token(customer=customer)

        return access_token, refresh_token, expires_in