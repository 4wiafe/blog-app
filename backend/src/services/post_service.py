from crud.post_crud import (
    create_post,
    get_all_posts,
    get_post_by_id,
    get_post_by_title,
    get_posts_by_author,
    update_post,
)
from crud.user_crud import get_user_by_id, get_user_by_username
from database import SessionDep
from models.user import User
from models.post import Post
from schemas.post_schemas import PostCreate, PostPublic
from schemas.user_schemas import UserPublic

from fastapi import HTTPException, status


# Add new post
def add_post(post: PostCreate, current_user: User, session: SessionDep) -> PostPublic:
    created_post = Post(
        title=post.title,
        description=post.description,
        content=post.content,
        author_id=current_user.id,
    )

    added_post = create_post(created_post, session)

    return PostPublic(
        id=added_post.id,  # type: ignore
        title=added_post.title,
        description=added_post.description,
        content=added_post.content,
        edited=added_post.edited,
        author=UserPublic(
            id=current_user.id,  # type: ignore
            full_name=current_user.full_name,
            username=current_user.username,
        ),
    )


# Get all posts
def list_posts(
    session: SessionDep,
    offset: int,
    limit: int,
) -> list[PostPublic]:
    db_posts = get_all_posts(offset, limit, session)
    public_posts = []

    if len(db_posts) == 0:
        return []

    for post in db_posts:
        author = get_user_by_id(post.author_id, session)
        assert author is not None

        public_posts.append(
            PostPublic(
                id=post.id,  # type: ignore
                title=post.title,
                description=post.description,
                content=post.content,
                edited=post.edited,
                author=UserPublic(
                    id=author.id,  # type: ignore
                    full_name=author.full_name,
                    username=author.username,
                ),
            )
        )

    return public_posts


# Get post using post id
def fetch_post_by_id(
    post_id: int,
    session: SessionDep,
) -> PostPublic:

    post = get_post_by_id(post_id, session)

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} not found",
        )

    author = get_user_by_id(post.author_id, session)
    assert author is not None

    return PostPublic(
        id=post.id,  # type: ignore
        title=post.title,
        description=post.description,
        content=post.content,
        edited=post.edited,
        author=UserPublic(
            id=author.id,  # type: ignore
            full_name=author.full_name,
            username=author.username,
        ),
    )


# Get post using the post title
def fetch_post_by_title(
    post_title: str,
    offset: int,
    limit: int,
    session: SessionDep,
) -> list[PostPublic]:
    db_posts = get_post_by_title(post_title, offset, limit, session)
    posts = []

    if len(db_posts) == 0:
        return []

    for post in db_posts:
        author = get_user_by_id(post.author_id, session)
        assert author is not None

        posts.append(
            PostPublic(
                id=post.id,  # type: ignore
                title=post.title,
                description=post.description,
                content=post.content,
                edited=post.edited,
                author=UserPublic(
                    id=author.id,  # type: ignore
                    full_name=author.full_name,
                    username=author.username,
                ),
            )
        )

    return posts


# Get posts created by author
def fetch_posts_by_author(
    username: str,
    offset: int,
    limit: int,
    session: SessionDep,
) -> list[PostPublic]:

    author = get_user_by_username(username, session)

    if not author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with username {username} not found",
        )

    user_posts = get_posts_by_author(
        author.id,  # type: ignore
        offset,
        limit,
        session,
    )

    public_posts = []

    if len(user_posts) == 0:
        return []

    for post in user_posts:
        public_posts.append(
            PostPublic(
                id=post.id,  # type: ignore
                title=post.title,
                description=post.description,
                content=post.content,
                edited=post.edited,
                author=UserPublic(
                    id=author.id,  # type: ignore
                    full_name=author.full_name,
                    username=author.username,
                ),
            )
        )

    return public_posts


# Edite a post
def edit_post(
    post_id: int,
    values: dict[str, str | None | bool],
    session: SessionDep,
) -> PostPublic:

    if not values:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Update values cannot be empty",
        )

    if ("title" in values and values["title"] is None) or (
        "content" in values and values["content"] is None
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Title and content cannot be null",
        )

    values.update({"edited": True})

    updated_post = update_post(
        post_id,
        values,  # type: ignore
        session,
    )

    if not updated_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} not found",
        )

    author = get_user_by_id(updated_post.author_id, session)
    assert author is not None

    return PostPublic(
        id=updated_post.id,  # type: ignore
        title=updated_post.title,
        description=updated_post.description,
        content=updated_post.content,
        edited=updated_post.edited,
        author=UserPublic(
            id=author.id,  # type: ignore
            full_name=author.full_name,
            username=author.username,
        ),
    )
