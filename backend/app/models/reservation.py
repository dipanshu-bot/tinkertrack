from datetime import datetime

from sqlalchemy import (
    Integer,
    DateTime,
    ForeignKey,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.database.base import Base


class Reservation(Base):
    __tablename__ = "reservations"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    resource_id: Mapped[int] = mapped_column(
        ForeignKey("resources.id")
    )

    start_time: Mapped[datetime]

    end_time: Mapped[datetime]

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )