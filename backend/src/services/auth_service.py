from services.user_service import get_user_by_username
from database import SessionDep
from schemas.user_schemas import UserPublic
from utils.helpers import verify_password, DUMMY_HASH
from config import settings

from fastapi import HTTPException, status
import jwt

from datetime import datetime, timedelta, timezone


def authenticate_user(username: str, password: str, session: SessionDep) -> UserPublic:

    # Check user credentials
    user = get_user_by_username(username, session)

    if not user:
        verify_password(password, DUMMY_HASH)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return UserPublic(
        id=user.id,  # type: ignore
        full_name=user.full_name,
        username=user.username,
    )


def create_access_token(data: dict, expires_delta: timedelta) -> str:
    # Copy user data and create expire time
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta

    # Encode the data
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.algorithm
    )

    return encoded_jwt
