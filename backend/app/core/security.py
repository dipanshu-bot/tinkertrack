from datetime import datetime, timedelta
from jose import jwt
from pwdlib import PasswordHash
from jose import JWTError
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.models.user import User
from fastapi.security import OAuth2PasswordBearer
from app.core.config import (
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


def verify_access_token(token: str):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        return payload

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token"
        )


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    print("=" * 50)
    print("TOKEN RECEIVED:")
    print(token)
    print("=" * 50)

    payload = verify_access_token(token)

    print(payload)

    email = payload.get("sub")

    user = db.query(User).filter(User.email == email).first()

    return user


from app.models.user import User


def require_admin(current_user: User = Depends(get_current_user)):

    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required",
        )

    return current_user
