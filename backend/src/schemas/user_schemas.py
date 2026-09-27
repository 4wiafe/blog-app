from pydantic import BaseModel, Field, EmailStr


class UserBase(BaseModel):
    full_name: str = Field(min_length=4, max_length=50)
    username: str = Field(min_length=4, max_length=30)


class UserCreate(UserBase):
    email: EmailStr
    password: str = Field(min_length=8)
    confirm_password: str = Field(min_length=8)


class UserInDB(UserBase):
    id: int
    email: EmailStr
    hashed_password: str
    is_active: bool


class UserPublic(UserBase):
    id: int


class UserUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=4, max_length=50)
    username: str | None = Field(default=None, min_length=4, max_length=30)
    email: EmailStr | None = None
    password: str | None = Field(default=None, min_length=8)
    is_active: bool | None = Field(default=None, min_length=8)
