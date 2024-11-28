from datetime import datetime
from ninja import Schema
from core.apps.events.entities import Event as EventEntity


class EventListOutSchema(Schema):
    id: int
    title: str
    description: str
    address: str | None
    picture: str | None
    organizer_name: str | None
    is_visible: bool

    def from_entity(entity: EventEntity) -> 'EventListOutSchema':
        return EventListOutSchema(
            id=entity.id,
            title=entity.title,
            description=entity.description,
            address=entity.address,
            picture=entity.picture,
            is_visible=entity.is_visible,
            organizer_name=entity.organizer_name,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )


class AddEventSchema(Schema):
    title: str
    description: str
    address: str | None
