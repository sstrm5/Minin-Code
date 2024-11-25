from ninja import Schema

class TestFilters(Schema):
    search: str | None = None


class QuestionFilters(Schema):
    search: str | None = None


class AnswerFilters(Schema):
    search: str | None = None
    