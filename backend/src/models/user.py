from __future__ import annotations
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String

from database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int | None] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    username: Mapped[str] = mapped_column(
        String(30), unique=True, index=True, nullable=False
    )
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)

    posts = relationship(
        "Post",
        back_populates="user",
        passive_deletes=True,
    )
