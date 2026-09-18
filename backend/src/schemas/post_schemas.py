from pydantic import BaseModel, Field

from datetime import datetime


class PostBase(BaseModel):
    title: str = Field(min_length=3, max_length=30)
    description: str | None = None
    content: str


class PostCreate(PostBase):
    pass


class PostInDB(PostBase):
    id: int
    created_at: datetime
    edited: bool
    author_id: int


class PostPublic(PostBase):
    id: int
    author_id: int


class PostUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    content: str | None = None
