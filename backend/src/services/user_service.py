from schemas.user_schemas import UserPublic, UserCreate
from crud.user_crud import get_user_by_email, add_user
from crud import user_crud
from database import SessionDep
from utils.helpers import get_password_hash
from models.user import User

from fastapi import HTTPException, status


# Fetch username
def get_user_by_username(username: str, session: SessionDep) -> User | None:
    return user_crud.get_user_by_username(username, session)


# Create a new user
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
