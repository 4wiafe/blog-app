from fastapi import APIRouter, status

from schemas.user_schemas import UserCreate, UserPublic
from services.user_service import register_user
from database import SessionDep

router = APIRouter()


@router.post(
    "/register",
    tags=["users"],
    response_model=UserPublic,
    status_code=status.HTTP_201_CREATED,
)
def add_new_user(user: UserCreate, session: SessionDep):
    registered_user = register_user(user, session)
    return registered_user
