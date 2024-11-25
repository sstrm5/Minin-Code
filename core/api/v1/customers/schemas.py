from ninja import Schema


class CreateAndAuthInSchema(Schema):
    email: str
    first_name: str
    last_name: str


class GetAndAuthInSchema(Schema):
    email: str


class AuthOutSchema(Schema):
    message: str


class TokenOutSchema(Schema):
    access_token: str
    refresh_token: str
    expires_in: int


class TokenInSchema(Schema):
    email: str
    code: str


class RefreshInSchema(Schema):
    refresh_token: str