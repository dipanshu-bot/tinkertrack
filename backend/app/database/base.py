from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# Import all models here
from app.models.user import User
from app.models.resource import Resource
from app.models.borrow import Borrow
from app.models.reservation import Reservation
