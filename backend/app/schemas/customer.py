from typing import Optional
from datetime import date
from pydantic import BaseModel, field_validator
from app.utils.validate_document import validate_document
from app.utils.validate_phone import validate_phone
from app.models.enums.civil_status import CivilStatus
from app.models.enums.state import State


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

    @field_validator("document")
    @classmethod
    def validate_document(cls, value):
        if not validate_document(value):
            raise ValueError("Documento inválido.")
        return value

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value):
        if not validate_phone(value):
            raise ValueError("Telefone inválido.")
        return value

    @field_validator("civil_status")
    @classmethod
    def validate_civil_status(cls, value):
        if value is None:
            return value

        try:
            return CivilStatus(value)
        except:
            raise ValueError("Estado civil inválido.")

    @field_validator("state")
    @classmethod
    def validate_state(cls, value):
        if value is None:
            return value

        try:
            return State(value)
        except:
            raise ValueError("UF inválido.")


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

    @field_validator("document")
    @classmethod
    def validate_document(cls, value):
        if value is None:
            return value

        if not validate_document(value):
            raise ValueError("Documento inválido.")
        return value

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value):
        if value is None:
            return value

        if not validate_phone(value):
            raise ValueError("Telefone inválido.")
        return value

    @field_validator("civil_status")
    @classmethod
    def validate_civil_status(cls, value):
        if value is None:
            return value

        try:
            return CivilStatus(value)
        except:
            raise ValueError("Estado civil inválido.")

    @field_validator("state")
    @classmethod
    def validate_state(cls, value):
        if value is None:
            return value

        try:
            return State(value)
        except:
            raise ValueError("UF inválido.")


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
