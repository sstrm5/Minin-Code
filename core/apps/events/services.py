from core.apps.customers.entities import CustomerEntity
from core.apps.customers.models import Customer
from core.apps.events.models import Event


class ORMEventsService:
    def get_events_list(self):
        items = Event.objects.filter(
            is_visible=True).order_by('-created_at')
        return [item.to_entity() for item in items]

    def create_event(self, title, description, address, customer: CustomerEntity):
        event = Event.objects.create(
            title=title, description=description, address=address, organizer=Customer.from_entity(customer))
        return event.to_entity()
