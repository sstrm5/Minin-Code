from core.apps.customers.entities import CustomerEntity
from core.apps.customers.models import Customer
from core.apps.events.models import Event


class ORMEventsService:
    def get_events_list(self):
        items = Event.objects.filter(
            is_visible=True).order_by('-created_at')
        return [item.to_entity() for item in items]

    def get_event(self, event_id: int):
        item = Event.objects.get(id=event_id)
        return item.to_entity()

    def create_event(self, title, description, address, customer: CustomerEntity):
        event = Event.objects.create(
            title=title, description=description, address=address, organizer=Customer.from_entity(customer))
        return event.to_entity()

    def sign_event(self, event_id, customer: CustomerEntity):
        event = Event.objects.get(id=event_id)
        customer = Customer.objects.get(id=customer.id)
        if customer in event.participants.all():
            raise ValueError('Customer already signed to this event')
        if event.participants.count() >= event.max_participants:
            raise ValueError('There are no available places in this event')
        event.participants.add(customer)
        return True
