from typing import Optional
from pydantic import BaseModel, field_validator
from app.utils.validate_document import validate_document
from app.utils.validate_phone import validate_phone
from app.models.enums.civil_status import CivilStatus
from app.models.enums.state import State
from app.schemas.position import PositionResponse


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
    position_id: Optional[int] = None

    @field_validator("position_id")
    @classmethod
    def validate_position(cls, value):
        if value is not None and value <= 0:
            raise ValueError("O id do Cargo deve ser um número positivo.")
        return value

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

    @field_validator("oab_state")
    @classmethod
    def validate_oab_state(cls, value):
        if value is None:
            return value

        try:
            return State(value)
        except:
            raise ValueError("OAB UF inválido.")


class LawyerUpdate(BaseModel):
    password: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    document: Optional[str] = None
    phone: Optional[str] = None
    civil_status: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    country: Optional[str] = None
    is_active: Optional[bool] = True
    oab: Optional[str] = None
    oab_state: Optional[str] = None
    position_id: Optional[int] = None

    @field_validator("position_id")
    @classmethod
    def validate_position(cls, value):
        if value is not None and value <= 0:
            raise ValueError("O id do Cargo deve ser um número positivo.")
        return value

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

    @field_validator("oab_state")
    @classmethod
    def validate_oab_state(cls, value):
        if value is None:
            return value

        try:
            return State(value)
        except:
            raise ValueError("OAB UF inválido.")


class LawyerResponse(BaseModel):
    id: int
    username: str
    name: str
    email: str
    document: str
    phone: str
    civil_status: Optional[str] = None
    is_active: bool
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    country: Optional[str] = None
    photo_url: Optional[str] = None
    oab: str
    oab_state: str
    position_id: Optional[int] = None

    class Config:
        orm_mode = True
