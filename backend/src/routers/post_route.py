from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from models.user import User
from services.post_service import (
    add_post,
    fetch_post_by_id,
    list_posts,
)
from schemas.post_schemas import PostCreate, PostPublic
from database import SessionDep
from services.user_service import get_current_active_user

router = APIRouter(
    prefix="/posts",
    tags=["posts"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "",
    response_model=PostPublic,
    status_code=status.HTTP_201_CREATED,
)
def create_post(
    post: Annotated[PostCreate, Query()],
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: SessionDep,
):
    added_post = add_post(post, current_user, session)
    return added_post


@router.get(
    "",
    response_model=list[PostPublic],
    status_code=status.HTTP_200_OK,
)
def get_posts(
    session: SessionDep,
    offset: int = 0,
    limit: int = 10,
):
    return list_posts(session, offset, limit)


@router.get(
    "/{id}",
    response_model=PostPublic,
    status_code=status.HTTP_200_OK,
)
def get_post_by_id(id: int, session: SessionDep):
    return fetch_post_by_id(id, session)
