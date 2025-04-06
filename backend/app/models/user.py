from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.models.position import Position


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    type = Column(String, nullable=False)
    position_id = Column(
        Integer, ForeignKey("positions.id", name="fk_user_position_id")
    )

    position = relationship("Position", backref="users")

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
