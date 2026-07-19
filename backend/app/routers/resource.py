from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.services import resource_service
from app.database.dependencies import get_db
from app.schemas.resource import (
    ResourceCreate,
    ResourceUpdate,
    ResourceResponse,
)
from app.services.resource_service import (
    create_resource as create_resource_service,
    get_all_resources,
    get_low_stock_resources,
    get_resource,
    get_resource_statistics,
    update_resource,
    delete_resource,
    get_resources,
    get_available_resources,
)
from app.models.user import User

from app.core.security import (
    get_current_user,
    require_admin,
)

router = APIRouter(
    prefix="/resources",
    tags=["Resources"],
)


@router.get("/", response_model=list[ResourceResponse])
def read_resources(
    category: str | None = None,
    search: str | None = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return resource_service.get_resources(
        db,
        category=category,
        search=search,
        skip=skip,
        limit=limit,
    )


@router.post(
    "/",
    response_model=ResourceResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Resource",
)
def create_resource(
    resource: ResourceCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    return create_resource_service(db, resource)


@router.get("/available", response_model=list[ResourceResponse])
def available_resources(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_available_resources(db)


@router.get("/low-stock", response_model=list[ResourceResponse])
def low_stock(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    return get_low_stock_resources(db)


@router.get("/statistics")
def resource_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    return get_resource_statistics(db)


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
