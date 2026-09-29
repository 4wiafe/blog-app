from typing import Annotated

from fastapi import APIRouter, Depends, status, Query

from models.user import User
from schemas.post_schemas import PostPublic
from schemas.user_schemas import UserCreate, UserPublic, UserUpdate
from services.post_service import fetch_posts_by_author
from services.user_service import (
    delete_user,
    get_current_active_user,
    get_user_by_username,
    register_user,
    update_user,
)
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


@router.get("/users/{username}", response_model=UserPublic)
def read_user_by_username(username: str, session: SessionDep):
    user = get_user_by_username(username, session)
    return user


@router.patch(
    "/users/me", response_model=UserPublic, status_code=status.HTTP_201_CREATED
)
def edit_user(
    values: Annotated[UserUpdate, Query()],
    session: SessionDep,
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    values_copy = values.model_copy()
    to_dict = values_copy.model_dump(exclude_unset=True)
    user_id = current_user.id
    assert user_id is not None

    updated_user = update_user(user_id, to_dict, session)

    return updated_user


@router.delete("/users/me", status_code=status.HTTP_204_NO_CONTENT)
def remove_user(
    session: SessionDep,
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    user_id = current_user.id
    assert user_id is not None
    deleted_user = delete_user(user_id, session)

    return deleted_user


@router.get(
    "/users/{username}/posts",
    response_model=list[PostPublic],
    status_code=status.HTTP_200_OK,
)
def get_user_posts(
    username: str,
    session: SessionDep,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(le=10)] = 10,
):
    return fetch_posts_by_author(
        username,
        offset,
        limit,
        session,
    )
