from pydantic import BaseModel
from datetime import datetime


class BorrowCreate(BaseModel):
    resource_id: int
    quantity: int


class BorrowResponse(BaseModel):
    id: int
    user_id: int
    resource_id: int
    quantity: int
    borrowed_at: datetime
    returned_at: datetime | None

    model_config = {"from_attributes": True}
