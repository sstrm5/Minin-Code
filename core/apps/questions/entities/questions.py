from dataclasses import dataclass
from datetime import datetime


@dataclass
class Question:
    id: int
    test_id: int
    title: str
    # dict of answer_index: answer_text pairs
    answers: list[dict[str, str]]
    answers_dict: dict[str, bool]
    description: str
    subject: str
    weight: int
    picture: str
    created_at: datetime
    updated_at: datetime


@dataclass
class Test:
    id: int
    title: str
    description: str
    subject: str
    work_time: int
    question_count: int
    picture: str
    created_at: datetime
    updated_at: datetime
