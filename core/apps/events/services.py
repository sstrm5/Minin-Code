import os
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

    def create_event(self, title, description, address, customer: CustomerEntity, file_path):
        event = Event.objects.create(
            title=title, description=description, address=address, organizer=Customer.from_entity(customer), picture=file_path)
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

    def add_picture_to_event(self, file):
        if not os.path.exists("media/events"):
            os.makedirs("media/events")
        file_path = f"events/{file.name}"
        with open("media/" + file_path, "wb") as f:
            for chunk in file.chunks():
                f.write(chunk)
        return file_path


class ORMEventsAdminService:
    def get_events_list(self):
        items = Event.objects.all().order_by('is_visible', '-created_at')
        return [item.to_entity() for item in items]

    def publish_event(self, event_id: int):
        event = Event.objects.get(id=event_id)
        event.is_visible = True
        event.save()
        return event.to_entity()

    def unpublish_event(self, event_id: int):
        event = Event.objects.get(id=event_id)
        event.is_visible = False
        event.save()
        return event.to_entity()
