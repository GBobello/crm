from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from app.db.base import Base
from app.models.position_permission import position_permissions


class Position(Base):
    __tablename__ = "positions"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    # position_permissions = relationship(
    #     "PositionPermission", backref="position", cascade="all, delete-orphan"
    # )

    permissions = relationship(
        "Permission", secondary=position_permissions, backref="positions"
    )
