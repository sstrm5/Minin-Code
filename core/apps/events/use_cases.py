from dataclasses import dataclass

from core.api.v1.events.schemas import AddEventSchema
from core.apps.customers.services.customers import ORMCustomerService
from core.apps.events.services import ORMEventsService


@dataclass
class AddEventUseCase:
    customer_service: ORMCustomerService
    event_service: ORMEventsService

    def execute(self, token: str, schema: AddEventSchema) -> str:
        customer = self.customer_service.get_by_token(token=token)
        if not customer or customer.role not in ['admin', 'organization']:
            raise ValueError('Invalid token')

        event = self.event_service.create_event(
            title=schema.title, description=schema.description, address=schema.address, customer=customer)
        return event
