from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from datetime import datetime
from app.db.base import Base
from app.models.enums.appointment_status import AppointmentStatus


class AppointmentStatusHistory(Base):
    __tablename__ = "appointment_status_history"

    id = Column(Integer, primary_key=True, index=True)
    appointment_id = Column(Integer, ForeignKey("appointments.id"), nullable=False)
    status = Column(Enum(AppointmentStatus), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    changed_by = Column(Integer, ForeignKey("users.id"), nullable=False)
