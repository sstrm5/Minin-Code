from dataclasses import dataclass

from core.apps.customers.models import Customer
from core.apps.customers.services.customers import ORMCustomerService
from core.apps.news.services import ORMNewsAdminService, ORMNewsService


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
            file,
    ):
        customer = self.customer_service.get_by_token(token)
        if customer is None or customer.role != 'organization':
            raise ValueError('Invalid token or role')
        customer = Customer.from_entity(customer)
        file_path = self.news_service.add_picture_to_news(file)
        news = self.news_service.create_news(
            title=title, text=text, additional_text=additional_text, customer=customer, file_path=file_path)
        return news


@dataclass
class GetNewsAdminUseCase:
    news_admin_service: ORMNewsAdminService
    customer_service: ORMCustomerService

    def execute(self, token: str):
        customer = self.customer_service.get_by_token(token)
        if not customer or customer.role not in ['admin']:
            raise ValueError(
                f'User must be logged-in as admin, not {customer.role}'
            )
        news = self.news_admin_service.get_news()
        return news


@dataclass
class PublishNewsAdminUseCase:
    news_admin_service: ORMNewsAdminService
    customer_service: ORMCustomerService

    def execute(self, token: str, news_id: int):
        customer = self.customer_service.get_by_token(token)
        if not customer or customer.role not in ['admin']:
            raise ValueError(
                f'User must be logged-in as admin, not {customer.role}'
            )
        news = self.news_admin_service.publish_news(news_id)
        return news


@dataclass
class UnpublishNewsAdminUseCase:
    news_admin_service: ORMNewsAdminService
    customer_service: ORMCustomerService

    def execute(self, token: str, news_id: int):
        customer = self.customer_service.get_by_token(token)
        if not customer or customer.role not in ['admin']:
            raise ValueError(
                f'User must be logged-in as admin, not {customer.role}'
            )
        news = self.news_admin_service.unpublish_news(news_id)
        return news
