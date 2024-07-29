from api.schemas.base_db_schema import BaseDBSchema
from api.services.auth import AuthService
from pydantic import BaseModel, field_serializer


class UserCreate(BaseModel):
    name: str
    email: str
    password: str

    @field_serializer("password")
    def hash_password(self, password: str) -> str:
        return AuthService.get_password_hash(password)


class UserOut(BaseDBSchema):
    name: str
    email: str


class UserInDB(UserOut):
    hashed_password: str
