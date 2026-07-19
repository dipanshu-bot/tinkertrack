from datetime import datetime

from pydantic import BaseModel, Field


class ReservationCreate(BaseModel):
    resource_id: int = Field(..., gt=0)
    start_time: datetime
    end_time: datetime


class ReservationUpdate(BaseModel):
    start_time: datetime
    end_time: datetime


class ReservationResponse(BaseModel):
    id: int
    user_id: int
    resource_id: int
    start_time: datetime
    end_time: datetime
    created_at: datetime

    model_config = {"from_attributes": True}