import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Enum, Date
from app.db.base import Base
from app.models.enums.state import State
from app.models.enums.civil_status import CivilStatus


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    document = Column(String(14), nullable=False)  # Verificar regra, unique=True)
    email = Column(String(255), nullable=False)
    phone = Column(String(15), nullable=False)
    created_date = Column(Date, default=datetime.now())
    born_date = Column(Date, nullable=False)
    civil_status = Column(Enum(CivilStatus))
    address = Column(String(200))
    city = Column(String(100))
    state = Column(Enum(State))
    zip_code = Column(String(10))
    country = Column(String(200))

    def __str__(self):
        return f"Customer(id={self.id}, name={self.name})"
