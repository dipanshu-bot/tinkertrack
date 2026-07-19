from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db

from app.schemas.borrow import BorrowCreate, BorrowResponse

from app.services.borrow_service import (
    borrow_resource,
    get_all_borrow_history,
    get_returned_borrows,
)

from app.core.security import get_current_user, require_admin

from app.models.user import User
from app.services.borrow_service import (
    borrow_resource,
    return_resource,
    get_my_borrows,
    get_all_borrows,
    get_active_borrows,
)

router = APIRouter(
    prefix="/borrow",
    tags=["Borrow"],
)


@router.get("/my", response_model=list[BorrowResponse])
def my_borrow_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_my_borrows(
        db=db,
        current_user=current_user,
    )


@router.get("/all", response_model=list[BorrowResponse])
def all_borrow_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    return get_all_borrows(db)


@router.post("/", response_model=BorrowResponse, summary="Borrow a resource")
def borrow(
    request: BorrowCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return borrow_resource(
        db=db,
        resource_id=request.resource_id,
        quantity=request.quantity,
        current_user=current_user,
    )


@router.put(
    "/return/{borrow_id}",
    response_model=BorrowResponse,
    summary="Return a borrowed resource",
)
def return_borrowed_resource(
    borrow_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return return_resource(
        db=db,
        borrow_id=borrow_id,
        current_user=current_user,
    )


@router.get("/history", response_model=list[BorrowResponse])
def borrow_history(
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    return get_all_borrow_history(db)


@router.get(
    "/active", response_model=list[BorrowResponse], summary="View active borrow records"
)
def active_borrows(
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    return get_active_borrows(db)


@router.get("/returned", response_model=list[BorrowResponse])
def returned_borrows(
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    return get_returned_borrows(db)
