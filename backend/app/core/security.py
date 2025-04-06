from datetime import datetime, timedelta
from jose import jwt, JWTError, ExpiredSignatureError
from fastapi import Request, HTTPException, Depends
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.models.session import Session as SessionModel
from app.models.user import User
from app.models.position import Position
from app.db.session import get_db
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def require_permission(permission_name: str):
    def permission_checker(
        session: dict = Depends(verify_session),
        db: Session = Depends(get_db),
    ):
        user = db.query(User).filter(User.username == session.get("sub")).first()
        if not user.position_id:
            raise HTTPException(
                status_code=403,
                detail="Usuário não possui cargo definido.",
            )

        position = db.query(Position).filter(Position.id == user.position_id).first()

        if not position:
            raise HTTPException(status_code=404, detail="Cargo não encontrado.")

        permission_names = {perm.name for perm in position.permissions}
        if permission_name not in permission_names:
            raise HTTPException(status_code=403, detail="Permissão negada.")

        return user

    return permission_checker


def verify_session(request: Request, db: Session = Depends(get_db)):
    try:
        token = request.cookies.get("session_token")
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
        username = payload.get("sub")
    except AttributeError:
        raise HTTPException(status_code=401, detail="Token ausente")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

    sessao = (
        db.query(SessionModel)
        .filter(SessionModel.username == username, SessionModel.session_token == token)
        .first()
    )

    if not sessao:
        raise HTTPException(status_code=401, detail="Sessão inválida")
    if sessao.expires_at < datetime.now():
        raise HTTPException(status_code=401, detail="Sessão expirada")
    if sessao.ip != request.client.host:
        raise HTTPException(status_code=401, detail="IP inválido")

    return payload


def create_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return {
        "access_token": jwt.encode(
            to_encode, settings.secret_key, algorithm=settings.algorithm
        ),
        "expires_at": expire,
    }


def verify_token_cookie(request: Request):
    token = request.cookies.get("session_token")
    if not token:
        raise HTTPException(status_code=401, detail="Token ausente")
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
        return payload
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")


def verify_password(password, hashed_password):
    return pwd_context.verify(password, hashed_password)


def generate_hashed_password(password):
    return pwd_context.hash(password)
