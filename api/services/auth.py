from datetime import datetime, timedelta, timezone
from typing import Annotated, Union

import jwt
from api.config import Config
from api.database.models.users import User
from api.exceptions.http_exceptions import CredentialsException
from api.schemas.auth import TokenData
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


class AuthService:
    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        return pwd_context.hash(password)

    @staticmethod
    async def authenticate_user(username: str, password: str):
        user: Union[User, None] = await User.get_by_email(username)
        if not user:
            return False
        if not AuthService.verify_password(password, user.password):
            return False
        return user

    @staticmethod
    def create_access_token(
        data: dict, expires_delta_in_minutes: Union[int, None] = None
    ):
        to_encode = data.copy()
        expires_at = datetime.now(timezone.utc) + timedelta(
            minutes=expires_delta_in_minutes or Config.AUTH.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode.update({"exp": expires_at})
        encoded_jwt = jwt.encode(
            to_encode, Config.AUTH.SECRET_KEY, algorithm=Config.AUTH.ALGORITHM
        )
        return encoded_jwt, expires_at

    # @staticmethod
    async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
        try:
            payload = jwt.decode(
                token, Config.AUTH.SECRET_KEY, algorithms=[Config.AUTH.ALGORITHM]
            )
            username: Union[str, None] = payload.get("sub")
            if username is None:
                raise CredentialsException()
            token_data = TokenData(email=username)
        except jwt.InvalidTokenError:
            raise CredentialsException()
        user: Union[User, None] = await User.get_by_email(token_data.email)
        if user is None:
            raise CredentialsException()
        return user

    @staticmethod
    async def get_current_active_user(
        current_user: Annotated[User, Depends(get_current_user)],
    ):
        if current_user.deleted_at:
            raise CredentialsException()
        return current_user
