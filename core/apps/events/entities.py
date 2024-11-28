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
    conditions: list
    participants: list
    start_time: str
    max_participants: str
    created_at: str
    updated_at: str


@dataclass
class Condition:
    id: int
    text: str
    is_visible: bool
    created_at: str
    updated_at: str
