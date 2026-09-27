from crud.post_crud import create_post
from database import SessionDep
from models.user import User
from models.post import Post
from schemas.post_schemas import PostCreate, PostPublic
from schemas.user_schemas import UserPublic


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
        author=UserPublic(
            id=current_user.id,  # type: ignore
            full_name=current_user.full_name,
            username=current_user.username,
        ),
    )
