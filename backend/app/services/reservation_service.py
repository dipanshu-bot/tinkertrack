from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import and_, or_

from app.models.resource import Resource
from app.models.reservation import Reservation
from app.models.user import User


def create_reservation(
    db: Session,
    resource_id: int,
    start_time,
    end_time,
    current_user: User,
):

    if start_time >= end_time:
        raise HTTPException(
            status_code=400,
            detail="End time must be after start time",
        )

    resource = db.query(Resource).filter(Resource.id == resource_id).first()

    if not resource:
        raise HTTPException(
            status_code=404,
            detail="Resource not found",
        )

    conflict = (
        db.query(Reservation)
        .filter(
            Reservation.resource_id == resource_id,
            or_(
                and_(
                    Reservation.start_time <= start_time,
                    Reservation.end_time > start_time,
                ),
                and_(
                    Reservation.start_time < end_time,
                    Reservation.end_time >= end_time,
                ),
                and_(
                    Reservation.start_time >= start_time,
                    Reservation.end_time <= end_time,
                ),
            ),
        )
        .first()
    )

    if conflict:
        raise HTTPException(
            status_code=400,
            detail="Resource already reserved for this time slot",
        )

    reservation = Reservation(
        user_id=current_user.id,
        resource_id=resource_id,
        start_time=start_time,
        end_time=end_time,
    )

    db.add(reservation)
    db.commit()
    db.refresh(reservation)

    return reservation


def get_my_reservations(
    db: Session,
    current_user: User,
):
    return (
        db.query(Reservation)
        .filter(Reservation.user_id == current_user.id)
        .order_by(Reservation.start_time)
        .all()
    )


from sqlalchemy import and_, or_
from fastapi import HTTPException


def update_reservation(
    db: Session,
    reservation_id: int,
    start_time,
    end_time,
    current_user: User,
):
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()

    if not reservation:
        raise HTTPException(
            status_code=404,
            detail="Reservation not found",
        )

    if reservation.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You can only update your own reservations",
        )

    if start_time >= end_time:
        raise HTTPException(
            status_code=400,
            detail="End time must be after start time",
        )

    conflict = (
        db.query(Reservation)
        .filter(
            Reservation.resource_id == reservation.resource_id,
            Reservation.id != reservation.id,
            or_(
                and_(
                    Reservation.start_time <= start_time,
                    Reservation.end_time > start_time,
                ),
                and_(
                    Reservation.start_time < end_time,
                    Reservation.end_time >= end_time,
                ),
                and_(
                    Reservation.start_time >= start_time,
                    Reservation.end_time <= end_time,
                ),
            ),
        )
        .first()
    )

    if conflict:
        raise HTTPException(
            status_code=400,
            detail="Time slot already reserved",
        )

    reservation.start_time = start_time
    reservation.end_time = end_time

    db.commit()
    db.refresh(reservation)

    return reservation


def cancel_reservation(
    db: Session,
    reservation_id: int,
    current_user: User,
):
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()

    if not reservation:
        raise HTTPException(
            status_code=404,
            detail="Reservation not found",
        )

    if reservation.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You can only cancel your own reservations",
        )

    db.delete(reservation)
    db.commit()

    return {"message": "Reservation cancelled successfully"}
