from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.database.dependencies import get_db
from app.schemas.user import UserCreate, UserResponse
from app.services.auth_service import register_user
from app.schemas.user import UserLogin, Token
from app.services.auth_service import login_user
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):

    new_user = register_user(db, user)

    if new_user is None:
        raise HTTPException(status_code=400, detail="Email already registered")

    return new_user


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):

    user = UserLogin(
        email=form_data.username,
        password=form_data.password,
    )

    token = login_user(db, user)

    if token is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    return token


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
