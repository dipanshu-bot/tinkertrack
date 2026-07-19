from pydantic import BaseModel, Field, model_validator
from datetime import datetime


class ResourceBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: str = Field(..., max_length=300)
    category: str = Field(..., min_length=2)
    quantity: int = Field(..., ge=0)
    available_quantity: int = Field(..., ge=0)

    @model_validator(mode="after")
    def validate_quantities(self):
        if self.quantity <= 0:
            raise ValueError("Quantity must be greater than 0")

        if self.available_quantity < 0:
            raise ValueError("Available quantity cannot be negative")

        if self.available_quantity > self.quantity:
            raise ValueError("Available quantity cannot be greater than total quantity")

        return self


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
