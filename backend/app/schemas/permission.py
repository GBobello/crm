from pydantic import BaseModel


class PermissionRead(BaseModel):
    id: int
    name: str
    description: str | None = None

    class Config:
        from_attributes = True
