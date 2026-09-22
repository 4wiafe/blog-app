from database import SessionDep
from models.user import User
from sqlalchemy import select, update, delete


def add_user(user: User, session: SessionDep) -> User:
    session.add(user)
    session.commit()
    session.refresh(user)

    return user


def get_user_by_id(user_id: int, session: SessionDep) -> User | None:
    statement = select(User).where(User.id == user_id)

    return session.scalar(statement)


def get_user_by_username(username: str, session: SessionDep) -> User | None:
    statement = select(User).where(User.username == username)

    return session.scalar(statement)


def get_user_by_email(email: str, session: SessionDep) -> User | None:
    statement = select(User).where(User.email == email)

    return session.scalar(statement)


def update_user(
    user_id: int, values: dict[str, str | bool], session: SessionDep
) -> User | None:
    statement = update(User).where(User.id == user_id).values(**values).returning(User)
    user = session.scalar(statement)

    if user is None:
        return None

    session.commit()

    return user


def delete_user(user_id: int, session: SessionDep) -> bool:
    statement = delete(User).where(User.id == user_id).returning(User.id)
    deleted_id = session.scalar(statement)

    session.commit()

    return deleted_id is not None
