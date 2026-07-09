from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.schemas.resource import (
    ResourceCreate,
    ResourceUpdate,
    ResourceResponse,
)
from app.services.resource_service import (
    create_resource,
    get_all_resources,
    get_resource,
    update_resource,
    delete_resource,
)
from app.core.security import (
    get_current_user,
    require_admin,
)

router = APIRouter(
    prefix="/resources",
    tags=["Resources"],
)


@router.post("/", response_model=ResourceResponse)
def create(
    resource: ResourceCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    return create_resource(db, resource)


@router.get("/", response_model=list[ResourceResponse])
def read_all(db: Session = Depends(get_db)):
    return get_all_resources(db)


@router.get("/{resource_id}", response_model=ResourceResponse)
def read_one(resource_id: int, db: Session = Depends(get_db)):
    resource = get_resource(db, resource_id)

    if resource is None:
        raise HTTPException(status_code=404, detail="Resource not found")

    return resource


@router.put("/{resource_id}", response_model=ResourceResponse)
def update(
    resource_id: int,
    resource: ResourceUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    updated = update_resource(db, resource_id, resource)

    if updated is None:
        raise HTTPException(status_code=404, detail="Resource not found")

    return updated


@router.delete("/{resource_id}")
def delete(
    resource_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    deleted = delete_resource(db, resource_id)

    if deleted is None:
        raise HTTPException(status_code=404, detail="Resource not found")

    return {"message": "Resource deleted successfully"}
