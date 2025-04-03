from sqlalchemy.orm import Session
from app.db.base import Base
from app.db.session import engine, SessionLocal
from app.models.user import User
from app.core.security import generate_hashed_password


def init_db():
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()
    user = db.query(User).filter(User.username == "admin").first()
    if not user:
        novo_user = User(
            username="admin", hashed_password=generate_hashed_password("admin")
        )
        db.add(novo_user)
        db.commit()
        print("Usuário admin criado")
    db.close()
