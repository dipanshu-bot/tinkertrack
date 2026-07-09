from sqlalchemy.orm import Session

from app.models.resource import Resource
from app.schemas.resource import ResourceCreate, ResourceUpdate


def create_resource(db: Session, resource: ResourceCreate):
    db_resource = Resource(**resource.model_dump())
    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)
    return db_resource


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
