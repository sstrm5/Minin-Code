from ninja import Schema, File


class CreateNewsSchema(Schema):
    title: str
    text: str
    additional_text: str
