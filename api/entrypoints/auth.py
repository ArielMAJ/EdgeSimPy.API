from typing import Annotated, Union

from api.database.models.users import User
from api.exceptions.http_exceptions import CredentialsException
from api.schemas.auth import Token
from api.services.auth import AuthService
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user: Union[User, None] = await AuthService.authenticate_user(
        form_data.username, form_data.password
    )
    if not user:
        raise CredentialsException()
    access_token, expires_at = AuthService.create_access_token(data={"sub": user.email})
    return Token(access_token=access_token, token_type="bearer", expires_at=expires_at)
