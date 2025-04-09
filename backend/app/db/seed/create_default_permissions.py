from sqlalchemy.orm import Session
from app.models.permission import Permission
from app.models.enums.default_permissions import DefaultPermissions


def create_default_permissions(db: Session):
    for perm in DefaultPermissions:
        exists = db.query(Permission).filter(Permission.name == perm.value).first()
        if not exists:
            db.add(Permission(name=perm.value))

        db.commit()
