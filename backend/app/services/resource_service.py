from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.resource import Resource
from app.schemas.resource import ResourceCreate, ResourceUpdate
from sqlalchemy import func


from fastapi import HTTPException


def create_resource(db: Session, resource: ResourceCreate):

    if resource.quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be greater than 0")

    if resource.available_quantity < 0:
        raise HTTPException(
            status_code=400, detail="Available quantity cannot be negative"
        )

    if resource.available_quantity > resource.quantity:
        raise HTTPException(
            status_code=400,
            detail="Available quantity cannot be greater than total quantity",
        )

    new_resource = Resource(**resource.model_dump())

    db.add(new_resource)
    db.commit()
    db.refresh(new_resource)

    return new_resource


def get_all_resources(db: Session):
    return db.query(Resource).all()


def get_resource(db: Session, resource_id: int):
    return db.query(Resource).filter(Resource.id == resource_id).first()


def update_resource(db: Session, resource_id: int, resource: ResourceUpdate):
    db_resource = get_resource(db, resource_id)

    if not db_resource:
        return None

    for key, value in resource.model_dump(exclude_unset=True).items():
        setattr(db_resource, key, value)

    db.commit()
    db.refresh(db_resource)

    return db_resource


def delete_resource(db: Session, resource_id: int):
    db_resource = get_resource(db, resource_id)

    if not db_resource:
        return None

    db.delete(db_resource)
    db.commit()

    return db_resource


def get_resources(
    db: Session,
    category: str | None = None,
    search: str | None = None,
    skip: int = 0,
    limit: int = 10,
):
    query = db.query(Resource)

    if category:
        query = query.filter(Resource.category == category)

    if search:
        query = query.filter(
            or_(
                Resource.name.ilike(f"%{search}%"),
                Resource.description.ilike(f"%{search}%"),
            )
        )

    return query.offset(skip).limit(limit).all()


def get_available_resources(db):
    return db.query(Resource).filter(Resource.available_quantity > 0).all()


def get_low_stock_resources(db):
    return db.query(Resource).filter(Resource.available_quantity < 5).all()


def get_resource_statistics(db):
    total_resources = db.query(Resource).count()

    total_quantity = db.query(func.sum(Resource.quantity)).scalar() or 0

    available = db.query(func.sum(Resource.available_quantity)).scalar() or 0

    return {
        "total_resources": total_resources,
        "available": available,
        "borrowed": total_quantity - available,
    }
