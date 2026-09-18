from __future__ import annotations
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, func, ForeignKey

from ..database import Base

from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int | None] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(30), index=True, nullable=False)
    description: Mapped[str | None] = mapped_column(default=None, nullable=True)
    content: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    edited: Mapped[bool] = mapped_column(default=False, nullable=False)
    author_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )

    user: Mapped[User] = relationship(back_populates="posts")
