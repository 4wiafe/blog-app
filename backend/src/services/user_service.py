from typing import Annotated


from config import settings
from schemas.token_schemas import TokenData
from schemas.user_schemas import UserPublic, UserCreate
from crud.user_crud import get_user_by_email, add_user
from crud import user_crud
from database import SessionDep
from utils.helpers import get_password_hash
from models.user import User

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt import InvalidTokenError

oauth2_schema = OAuth2PasswordBearer(tokenUrl="token")


# Fetch username
def get_user_by_username(username: str, session: SessionDep) -> User | None:
    return user_crud.get_user_by_username(username, session)


def register_user(user: UserCreate, session: SessionDep) -> UserPublic:

    # Throw error if password mismatches
    if user.password != user.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Password does not match",
        )

    # Throw error if email exist
    user_email = get_user_by_email(user.email, session)

    if user_email is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exist",
        )

    # Throw error if username exist
    username = get_user_by_username(user.username, session)

    if username is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already in use",
        )

    # Create and add a user
    hashed_password = get_password_hash(user.password)

    user_data = User(
        full_name=user.full_name,
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
    )

    added_user = add_user(user_data, session)

    return UserPublic(
        id=added_user.id,  # type: ignore
        full_name=added_user.full_name,
        username=added_user.username,
    )


def get_current_user(
    session: SessionDep, token: Annotated[str, Depends(oauth2_schema)]
) -> UserPublic:
    # Error message
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Decode token
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )
        username = payload.get("sub")

        if username is None:
            raise credentials_exception

        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception

    # Return a user
    user = get_user_by_username(token_data.username, session)  # type: ignore

    if user is None:
        raise credentials_exception

    return UserPublic(
        id=user.id,  # type: ignore
        full_name=user.full_name,
        username=user.username,
    )
