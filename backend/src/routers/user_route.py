from typing import Annotated

from fastapi import APIRouter, Depends, status

from models.user import User
from schemas.user_schemas import UserCreate, UserPublic
from services.user_service import get_current_active_user, register_user
from database import SessionDep

router = APIRouter(tags=["users"])


@router.post(
    "/register",
    response_model=UserPublic,
    status_code=status.HTTP_201_CREATED,
)
def add_new_user(user: UserCreate, session: SessionDep):
    registered_user = register_user(user, session)
    return registered_user


@router.get(
    "/users/me",
    response_model=UserPublic,
    status_code=status.HTTP_200_OK,
)
def read_active_user(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user
