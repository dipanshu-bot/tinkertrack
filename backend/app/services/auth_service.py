from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import hash_password
from app.core.security import verify_password, create_access_token
from app.schemas.user import UserLogin


def register_user(db: Session, user: UserCreate):

    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        return None

    new_user = User(
        name=user.name,
        email=user.email,
        hashed_password=hash_password(user.password),
        role="user",
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def login_user(db: Session, user: UserLogin):

    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user:
        return None

    if not verify_password(user.password, db_user.hashed_password):
        return None

    access_token = create_access_token(
        data={"sub": db_user.email, "role": db_user.role}
    )

    return {"access_token": access_token, "token_type": "bearer"}
