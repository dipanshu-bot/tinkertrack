from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database.base import Base


class Borrow(Base):
    __tablename__ = "borrows"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    resource_id = Column(Integer, ForeignKey("resources.id"))

    quantity = Column(Integer, nullable=False)

    borrowed_at = Column(DateTime, default=datetime.utcnow)

    returned_at = Column(DateTime, nullable=True)

    user = relationship("User")
    resource = relationship("Resource")
