from sqlalchemy import Table, Column, Integer, ForeignKey
from app.db.base import Base

position_permissions = Table(
    "position_permissions",
    Base.metadata,
    Column("position_id", Integer, ForeignKey("positions.id")),
    Column("permission_id", Integer, ForeignKey("permissions.id")),
)
