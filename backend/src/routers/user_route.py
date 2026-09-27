from typing import Annotated

from fastapi import APIRouter, Depends, status, Query

from models.user import User
from schemas.user_schemas import UserCreate, UserPublic, UserUpdate
from services.user_service import get_current_active_user, register_user, update_user
from database import SessionDep

router = APIRouter(
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


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


@router.patch(
    "/users/{user_id}", response_model=UserPublic, status_code=status.HTTP_201_CREATED
)
def edit_user(
    user_id: int, values: Annotated[UserUpdate, Query()], session: SessionDep
):
    values_copy = values.model_copy()
    to_dict = values_copy.model_dump(exclude_unset=True)

    updated_user = update_user(user_id, to_dict, session)

    return updated_user
