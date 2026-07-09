from pydantic import BaseModel
from datetime import datetime


class ResourceBase(BaseModel):
    name: str
    description: str
    category: str
    quantity: int
    available_quantity: int


class ResourceCreate(ResourceBase):
    pass


class ResourceUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    category: str | None = None
    quantity: int | None = None
    available_quantity: int | None = None


class ResourceResponse(ResourceBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}
