from typing import Optional
from pydantic import BaseModel


class LawyerCreate(BaseModel):
    username: str
    password: str
    name: str
    email: str
    document: str
    phone: str
    civil_status: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    country: Optional[str] = None
    oab: str
    oab_state: str


class LawyerUpdate(BaseModel):
    password: str
    name: str
    email: str
    document: str
    phone: str
    civil_status: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    country: Optional[str] = None
    is_active: Optional[bool] = True
    oab: str
    oab_state: str


class LawyerResponse(BaseModel):
    id: int
    username: str
    name: str
    email: str
    document: str
    phone: str
    civil_status: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    country: Optional[str] = None
    photo_url: Optional[str] = None
    oab: str
    oab_state: str

    class Config:
        orm_mode = True
