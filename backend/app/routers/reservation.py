from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.core.security import get_current_user
from app.models.user import User

from app.schemas.reservation import (
    ReservationCreate,
    ReservationUpdate,
    ReservationResponse,
)

from app.services.reservation_service import (
    create_reservation,
    get_my_reservations,
    update_reservation,
    cancel_reservation,
)

router = APIRouter(
    prefix="/reservations",
    tags=["Reservations"],
)


@router.post(
    "/",
    response_model=ReservationResponse,
    summary="Create a reservation",
)
def reserve_resource(
    request: ReservationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_reservation(
        db=db,
        resource_id=request.resource_id,
        start_time=request.start_time,
        end_time=request.end_time,
        current_user=current_user,
    )


@router.get(
    "/my",
    response_model=list[ReservationResponse],
    summary="View my reservations",
)
def my_reservations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_my_reservations(
        db,
        current_user,
    )


@router.put(
    "/{reservation_id}",
    response_model=ReservationResponse,
    summary="Update reservation",
)
def update(
    reservation_id: int,
    request: ReservationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_reservation(
        db=db,
        reservation_id=reservation_id,
        start_time=request.start_time,
        end_time=request.end_time,
        current_user=current_user,
    )


@router.delete(
    "/{reservation_id}",
    summary="Cancel reservation",
)
def delete(
    reservation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return cancel_reservation(
        db=db,
        reservation_id=reservation_id,
        current_user=current_user,
    )


@router.delete(
    "/{reservation_id}",
    summary="Cancel reservation",
)
def delete(
    reservation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return cancel_reservation(
        db=db,
        reservation_id=reservation_id,
        current_user=current_user,
    )
