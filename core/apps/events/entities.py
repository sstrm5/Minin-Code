from dataclasses import dataclass


@dataclass
class Event:
    id: int
    title: str
    description: str
    address: list
    picture: str | None
    is_visible: bool
    organizer_name: str | None
    created_at: str
    updated_at: str
