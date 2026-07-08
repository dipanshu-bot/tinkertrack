from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.core.oauth2 import oauth2_scheme
from app.core.security import verify_access_token
from app.models.user import User


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):

    payload = verify_access_token(token)

    email = payload.get("sub")

    user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    return user