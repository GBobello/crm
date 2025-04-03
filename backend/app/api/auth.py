from datetime import timedelta
from fastapi import APIRouter, HTTPException, Form, Response, Depends, Request
from sqlalchemy.orm import Session
from app.core.security import create_token, verify_session, verify_password
from app.db.session import get_db
from app.models.session import Session as SessionModel
from app.models.user import User

router = APIRouter()


@router.post("/login")
def login(
    request: Request,
    response: Response,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    token = create_token({"sub": user.username}, timedelta(days=30))

    sessao = SessionModel(
        user_id=user.id,
        username=user.username,
        session_token=token["access_token"],
        ip=request.client.host,
        expires_at=token["expires_at"],
    )
    db.add(sessao)
    db.commit()

    response.set_cookie(
        key="session_token",
        value=token["access_token"],
        httponly=True,
        max_age=3600,
        samesite="Lax",
    )
    return token


@router.post("/logout")
def logout(
    request: Request,
    response: Response,
    user=Depends(verify_session),
    db: Session = Depends(get_db),
):
    token = request.cookies.get("session_token")

    sessao = db.query(SessionModel).filter(SessionModel.session_token == token).first()
    if not sessao:
        raise HTTPException(status_code=401, detail="Sessão inválida")
    db.delete(sessao)
    db.commit()

    response.delete_cookie(key="session_token")

    return {"mensagem": "Logout realizado com sucesso"}


@router.get("/protegido")
def protegido(user=Depends(verify_session)):
    return {"mensagem": f"Olá, {user['sub']}! Você está autenticado."}
