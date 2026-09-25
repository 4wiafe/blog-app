from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from schemas.token_schemas import Token
from services.auth_service import authenticate_user, create_access_token
from database import SessionDep
from config import settings

router = APIRouter(
    tags=["authentication"],
    responses={404: {"description": "Not found"}},
)


@router.post("/token", response_model=Token, status_code=status.HTTP_200_OK)
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDep,
):

    # Authenticate user and create access token
    user = authenticate_user(form_data.username, form_data.password, session)

    expire = timedelta(minutes=settings.access_token_expire_minutes)
    data = {"sub": user.username}
    access_token = create_access_token(data, expire)

    return Token(access_token=access_token, token_type="bearer")
