from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.core.security import get_current_user, require_admin
from app.models.user import User

from app.schemas.borrow import BorrowResponse

from app.services.dashboard_service import (
    get_my_borrows,
    get_dashboard_stats,
)

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get("/my-borrows", response_model=list[BorrowResponse])
def my_borrows(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_my_borrows(db, current_user)


@router.get("/stats", summary="Get dashboard statistics")
def dashboard_stats(
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    return get_dashboard_stats(db)
