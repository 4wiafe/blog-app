from pydantic import BaseModel, Field, EmailStr


class UserBase(BaseModel):
    full_name: str = Field(min_length=4, max_length=50)
    username: str = Field(min_length=4, max_length=30)


class UserCreate(UserBase):
    email: EmailStr
    password: str


class UserInDB(UserBase):
    id: int
    email: EmailStr
    hashed_password: str
    is_active: bool


class UserPublic(UserBase):
    id: int
