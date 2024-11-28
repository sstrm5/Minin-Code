from dataclasses import dataclass


@dataclass
class News:
    id: int
    title: str
    image: str
    text: str
    additional_text: str
    is_published: bool
    created_at: str
    updated_at: str
