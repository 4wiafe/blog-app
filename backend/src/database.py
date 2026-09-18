from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import create_engine


from config import settings


class Base(DeclarativeBase):
    pass


engine = create_engine(settings.database_url)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


def get_session():
    with SessionLocal() as session:
        yield session
