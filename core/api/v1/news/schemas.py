from ninja import Schema, File
from django.core.files.uploadedfile import UploadedFile


class CreateNewsSchema(Schema):
    title: str
    text: str
    additional_text: str
    # image: bytes = File(..., description="Image file for the news")

    # class Config:
    #     arbitrary_types_allowed = True
