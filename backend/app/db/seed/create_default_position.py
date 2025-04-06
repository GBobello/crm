from sqlalchemy.orm import Session
from app.models.position import Position
from app.models.permission import Permission


def create_default_position(db: Session):
    exists = db.query(Position).filter(Position.name == "MASTER").first()
    if not exists:
        permissions = db.query(Permission).all()
        db.add(Position(name="MASTER", permissions=permissions))
        db.commit()

    position = db.query(Position).filter(Position.name == "MASTER").first()

    return position.id
