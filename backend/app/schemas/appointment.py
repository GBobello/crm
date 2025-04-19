from typing import Optional
from pydantic import BaseModel, field_validator
from datetime import datetime

class AppointmentCreate(BaseModel):
    title: str
    description: Optional[str] = None
    customer_id: Optional[int] = None
    user_id: int

class AppointmentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    customer_id: Optional[int] = None
    user_id: Optional[int] = None

class AppointmentResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: str
    customer_id: Optional[int] = None
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
