from pydantic import BaseModel
from typing import List, Optional
from app.schemas.permission import PermissionRead


class PositionBase(BaseModel):
    name: str


class PositionCreate(PositionBase):
    permissions_ids: List[int] = []


class PositionUpdate(BaseModel):
    name: Optional[str] = None
    permissions_ids: Optional[List[int]] = None


class PositionResponse(PositionBase):
    id: int
    permissions: List[PermissionRead]

    class Config:
        from_attributes = True
