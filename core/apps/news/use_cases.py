from dataclasses import dataclass

from core.apps.customers.models import Customer
from core.apps.customers.services.customers import ORMCustomerService
from core.apps.news.services import ORMNewsService


@dataclass
class AddNewsUseCase:
    customer_service: ORMCustomerService
    news_service: ORMNewsService

    def execute(
            self,
            token: str,
            title: str,
            text: str,
            additional_text: str,
            # image,
    ):
        customer = self.customer_service.get_by_token(token)
        if customer is None or customer.role != 'organization':
            raise ValueError('Invalid token or role')
        customer = Customer.from_entity(customer)
        # file_path = self.news_service.add_picture_to_news(image)
        # , image=file_path,
        news = self.news_service.create_news(
            title=title, text=text, additional_text=additional_text, customer=customer)
        return news
