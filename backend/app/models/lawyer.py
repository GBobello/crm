from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from app.models.user import User
from app.models.enums.state import State
from app.models.enums.civil_status import CivilStatus


class Lawyer(User):
    __tablename__ = "lawyers"

    id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    name = Column(String(200), nullable=False)
    email = Column(String(200), nullable=False)
    document = Column(String(14), nullable=False)
    phone = Column(String(15), nullable=False)
    civil_status = Column(Enum(CivilStatus))
    address = Column(String(200))
    city = Column(String(100))
    state = Column(Enum(State))
    zip_code = Column(String(10))
    country = Column(String(200))
    photo_url = Column(String)

    oab = Column(String, nullable=False)
    oab_state = Column(Enum(State), nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "lawyer",
    }

    def __str__(self):
        return f"Lawyer(id={self.id}, oab={self.name})"
