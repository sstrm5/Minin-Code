from dataclasses import dataclass

from core.api.v1.events.schemas import AddEventSchema
from core.apps.customers.services.customers import ORMCustomerService
from core.apps.customers.services.senders import MailSenderService
from core.apps.events.services import ORMEventsAdminService, ORMEventsService


@dataclass
class AddEventUseCase:
    customer_service: ORMCustomerService
    event_service: ORMEventsService

    def execute(self, token: str, schema: AddEventSchema, file) -> str:
        customer = self.customer_service.get_by_token(token=token)
        if not customer or customer.role not in ['admin', 'organization']:
            raise ValueError(
                f'User must be logged-in as organization, not {customer.role}'
            )
        file_path = self.event_service.add_picture_to_event(file)
        event = self.event_service.create_event(
            title=schema.title, description=schema.description, address=schema.address, customer=customer, file_path=file_path)
        return event


@dataclass
class SignUseCase:
    customer_service: ORMCustomerService
    event_service: ORMEventsService
    sender_service: MailSenderService

    def execute(self, token: str, event_id: int):
        customer = self.customer_service.get_by_token(token=token)
        if not customer or customer.role not in ('user',):
            raise ValueError(
                f'User must be logged-in as user, not {customer.role}')

        customer_was_edded_to_event = self.event_service.sign_event(
            event_id=event_id, customer=customer)

        event = self.event_service.get_event(event_id=event_id)

        if customer_was_edded_to_event:
            self.sender_service.send_event_notification(
                customer=customer,
                event=event
            )
            self.sender_service.send_orginizer_notification(
                event=event,
                customer=customer,
            )


@dataclass
class GetEventsAdminUseCase:
    event_service: ORMEventsAdminService
    customer_service: ORMCustomerService

    def execute(self, token: str):
        customer = self.customer_service.get_by_token(token=token)
        if not customer or customer.role not in ['admin']:
            raise ValueError(
                f'User must be logged-in as admin, not {customer.role}'
            )
        events = self.event_service.get_events_list()
        return events


@dataclass
class PublishEventAdminUseCase:
    event_admin_service: ORMEventsAdminService
    event_service: ORMEventsService
    customer_service: ORMCustomerService

    def execute(self, token: str, event_id: int):
        customer = self.customer_service.get_by_token(token=token)
        if not customer or customer.role not in ['admin']:
            raise ValueError(
                f'User must be logged-in as admin, not {customer.role}'
            )
        event = self.event_admin_service.publish_event(event_id=event_id)
        return event


@dataclass
class UnpublishEventAdminUseCase:
    event_admin_service: ORMEventsAdminService
    event_service: ORMEventsService
    customer_service: ORMCustomerService

    def execute(self, token: str, event_id: int):
        customer = self.customer_service.get_by_token(token=token)
        if not customer or customer.role not in ['admin']:
            raise ValueError(
                f'User must be logged-in as admin, not {customer.role}'
            )
        event = self.event_admin_service.unpublish_event(event_id=event_id)
        return event
