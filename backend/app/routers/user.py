from fastapi import APIRouter, Depends

from app.database.auth_dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/")
def get_users():
    return {"message": "Users API Working"}


@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
