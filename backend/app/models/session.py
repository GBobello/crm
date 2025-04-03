import uuid
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from app.db.base import Base


class Session(Base):
    __tablename__ = "sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    username = Column(String, nullable=False)
    session_token = Column(String, unique=True, index=True, nullable=False)
    ip = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    expires_at = Column(DateTime)

    def __str__(self):
        return (
            f"Session(id={self.id}, user_id={self.user_id}, username={self.username}, "
            + "session_token={self.session_token}, ip={self.ip}, created_at={self.created_at}, "
            + "expires_at={self.expires_at})"
        )
