from datetime import datetime
from typing import Union

from pydantic import BaseModel, field_serializer


class Token(BaseModel):
    access_token: str
    token_type: str
    expires_at: datetime

    @field_serializer("expires_at")
    def serialize_expires_at(self, value: datetime):
        return value.strftime("%d-%m-%Y %H:%M:%S")


class TokenData(BaseModel):
    email: Union[str, None] = None
