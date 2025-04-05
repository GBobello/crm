from typing import Optional
from datetime import date
from pydantic import BaseModel


class CustomerCreate(BaseModel):
    name: str
    document: str
    email: str
    phone: str
    born_date: date
    civil_status: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    country: Optional[str] = None


class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    document: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    born_date: Optional[date] = None
    civil_status: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    country: Optional[str] = None


class CustomerResponse(BaseModel):
    id: int
    name: str
    document: str
    email: str
    phone: str
    created_date: date
    born_date: date
    civil_status: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    country: Optional[str] = None

    class Config:
        orm_mode = True
