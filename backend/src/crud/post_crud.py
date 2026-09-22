from database import SessionDep
from models.post import Post

from sqlalchemy import select, update, delete


def create_post(post: Post, session: SessionDep) -> Post:
    session.add(post)
    session.commit()
    session.refresh(post)

    return post


def get_all_posts(offset: int, limit: int, session: SessionDep) -> list[Post]:
    statement = (
        select(Post).order_by(Post.created_at.desc()).offset(offset).limit(limit)
    )

    return list(session.scalars(statement).all())


def get_posts_by_author(
    author_id: int, offset: int, limit: int, session: SessionDep
) -> list[Post]:
    statement = (
        select(Post)
        .where(Post.author_id == author_id)
        .order_by(Post.created_at.desc())
        .offset(offset)
        .limit(limit)
    )

    return list(session.scalars(statement).all())


def get_post_by_title(
    post_title: str, offset: int, limit: int, session: SessionDep
) -> list[Post]:
    statement = (
        select(Post)
        .where(Post.title.ilike(f"%{post_title}%"))
        .order_by(Post.created_at.desc())
        .offset(offset)
        .limit(limit)
    )

    return list(session.scalars(statement).all())


def update_post(
    post_id: int, values: dict[str, str], session: SessionDep
) -> Post | None:
    statement = update(Post).where(Post.id == post_id).values(**values).returning(Post)
    post = session.scalar(statement)

    if post is None:
        return None

    session.commit()

    return post


def delete_post(post_id: int, session: SessionDep) -> bool:
    statement = delete(Post).where(Post.id == post_id).returning(Post.id)
    deleted_id = session.scalar(statement)

    session.commit()

    return deleted_id is not None
