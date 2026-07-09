from datetime import datetime

from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Resource(Base):
    __tablename__ = "resources"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    name: Mapped[str] = mapped_column(String(100), nullable=False)

    description: Mapped[str] = mapped_column(String(500), nullable=False)

    category: Mapped[str] = mapped_column(String(100), nullable=False)

    quantity: Mapped[int] = mapped_column(Integer, default=1)

    available_quantity: Mapped[int] = mapped_column(Integer, default=1)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
