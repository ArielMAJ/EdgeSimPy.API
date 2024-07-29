from typing import Union

from api.database.models.model_base import ModelBase
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from typing_extensions import Self


class User(ModelBase):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=False, index=True
    )
    email: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=False, index=True
    )
    password: Mapped[str] = mapped_column(String(255), nullable=False, index=True)

    @classmethod
    async def get_by_email(cls, email: str) -> Union[Self, None]:
        return await cls.get(cls.email == email)
