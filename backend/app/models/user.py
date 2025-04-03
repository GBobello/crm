from sqlalchemy import Column, Integer, String, Boolean
from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    type = Column(String, nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "user",
        "polymorphic_on": type,
        "with_polymorphic": "*",
    }

    def __str__(self):
        return (
            f"User(id={self.id}, username={self.username},"
            + " hashed_password={self.hashed_password})"
        )
