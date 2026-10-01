from typing import Annotated

from pydantic import BaseModel, Field

from fastapi import APIRouter, Depends, Query, status

from models.user import User
from services.post_service import (
    add_post,
    edit_post,
    fetch_post_by_id,
    list_posts,
    fetch_post_by_title,
)
from schemas.post_schemas import (
    PostCreate,
    PostPublic,
    PostUpdate,
)
from database import SessionDep
from services.user_service import get_current_active_user


class SearchParams(BaseModel):
    title: str
    offset: int = Field(default=0, ge=0)
    limit: int = Field(default=10, le=10)


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
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(le=10)] = 10,
):
    return list_posts(
        session,
        offset,
        limit,
    )


@router.get(
    "/search",
    response_model=list[PostPublic],
    status_code=status.HTTP_200_OK,
)
def get_post_by_title(
    search_query: Annotated[SearchParams, Query()],
    session: SessionDep,
):
    return fetch_post_by_title(
        search_query.title,
        search_query.offset,
        search_query.limit,
        session,
    )


@router.get(
    "/{id}",
    response_model=PostPublic,
    status_code=status.HTTP_200_OK,
)
def get_post_by_id(id: int, session: SessionDep):
    return fetch_post_by_id(id, session)


@router.patch(
    "/posts/{id}",
    response_model=PostPublic,
    status_code=status.HTTP_200_OK,
)
def update_post(id: int, values: PostUpdate, session: SessionDep):
    to_dict = values.model_dump(exclude_unset=True)
    return edit_post(id, to_dict, session)
