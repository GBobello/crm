from sqlalchemy.orm import Session
from app.models.permission import Permission

DEFAULT_PERMISSIONS = [
    "view_lawyer",
    "create_lawyer",
    "update_lawyer",
    "delete_lawyer",
    "view_customer",
    "create_customer",
    "update_customer",
    "delete_customer",
    "view_position",
    "create_position",
    "update_position",
    "delete_position",
]


def create_default_permissions(db: Session):
    for perm in DEFAULT_PERMISSIONS:
        exists = db.query(Permission).filter(Permission.name == perm).first()
        if not exists:
            db.add(Permission(name=perm))

        db.commit()
