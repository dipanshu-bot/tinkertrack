from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.resource import Resource
from app.models.borrow import Borrow


def get_my_borrows(db: Session, current_user: User):
    return db.query(Borrow).filter(Borrow.user_id == current_user.id).all()


def get_dashboard_stats(db: Session):

    total_users = db.query(User).count()

    total_resources = db.query(Resource).count()

    total_borrow_records = db.query(Borrow).count()

    active_borrows = db.query(Borrow).filter(Borrow.returned_at == None).count()

    returned_borrows = db.query(Borrow).filter(Borrow.returned_at != None).count()

    available_items = db.query(func.sum(Resource.available_quantity)).scalar() or 0

    total_items = db.query(func.sum(Resource.quantity)).scalar() or 0

    borrowed_items = total_items - available_items

    return {
        "total_users": total_users,
        "total_resources": total_resources,
        "total_borrow_records": total_borrow_records,
        "active_borrows": active_borrows,
        "returned_borrows": returned_borrows,
        "available_items": available_items,
        "borrowed_items": borrowed_items,
    }
