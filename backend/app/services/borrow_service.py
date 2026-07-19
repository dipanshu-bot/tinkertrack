from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.borrow import Borrow
from app.models.resource import Resource
from app.models.user import User
from datetime import datetime
from sqlalchemy import func


def get_all_borrow_history(db: Session):
    return db.query(Borrow).order_by(Borrow.borrowed_at.desc()).all()


def borrow_resource(
    db: Session,
    resource_id: int,
    quantity: int,
    current_user: User,
):
    # Find the resource
    resource = db.query(Resource).filter(Resource.id == resource_id).first()

    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")

    # Check quantity
    if quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be greater than 0")

    # Check availability
    if resource.available_quantity < quantity:
        raise HTTPException(status_code=400, detail="Not enough quantity available")

    # Reduce available quantity
    resource.available_quantity -= quantity

    # Create borrow record
    borrow = Borrow(
        user_id=current_user.id,
        resource_id=resource.id,
        quantity=quantity,
    )

    db.add(borrow)
    db.commit()
    db.refresh(borrow)

    return borrow


def return_resource(
    db: Session,
    borrow_id: int,
    current_user: User,
):
    borrow = db.query(Borrow).filter(Borrow.id == borrow_id).first()

    if not borrow:
        raise HTTPException(
            status_code=404,
            detail="Borrow record not found",
        )

    if borrow.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You can only return your own borrowed resources",
        )

    if borrow.returned_at is not None:
        raise HTTPException(
            status_code=400,
            detail="Resource already returned",
        )

    resource = db.query(Resource).filter(Resource.id == borrow.resource_id).first()

    resource.available_quantity += borrow.quantity

    borrow.returned_at = datetime.utcnow()

    db.commit()
    db.refresh(borrow)

    return borrow


def get_my_borrows(db, current_user):
    return (
        db.query(Borrow)
        .filter(Borrow.user_id == current_user.id)
        .order_by(Borrow.borrowed_at.desc())
        .all()
    )


def get_all_borrows(db: Session):
    return db.query(Borrow).order_by(Borrow.borrowed_at.desc()).all()


def get_resource_statistics(db):
    total_resources = db.query(Resource).count()

    total_quantity = db.query(func.sum(Resource.quantity)).scalar() or 0

    available = db.query(func.sum(Resource.available_quantity)).scalar() or 0

    return {
        "total_resources": total_resources,
        "total_quantity": total_quantity,
        "available": available,
        "borrowed": total_quantity - available,
    }


def get_active_borrows(db: Session):
    return db.query(Borrow).filter(Borrow.returned_at.is_(None)).all()


def get_returned_borrows(db: Session):
    return db.query(Borrow).filter(Borrow.returned_at.is_not(None)).all()
