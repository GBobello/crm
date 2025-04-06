from sqlalchemy.orm import Session
from app.db.base import Base
from app.db.session import engine, SessionLocal
from app.db.seed.create_default_permissions import create_default_permissions
from app.db.seed.create_default_position import create_default_position
from app.models.user import User
from app.core.security import generate_hashed_password


def init_db():
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()

    create_default_permissions(db)

    position_id = create_default_position(db)

    user = db.query(User).filter(User.username == "admin").first()
    if not user:
        novo_user = User(
            username="admin",
            hashed_password=generate_hashed_password("admin"),
            position_id=position_id,
        )
        db.add(novo_user)
        db.commit()
        print("Usuário admin criado")

    db.close()
