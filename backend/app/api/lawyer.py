import os
import platform
import shutil
from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.models.lawyer import Lawyer
from app.models.position import Position
from app.schemas.lawyer import LawyerCreate, LawyerUpdate, LawyerResponse
from app.core.security import (
    generate_hashed_password,
    require_permission,
)
from app.core.config import settings
from app.models.enums.default_permissions import DefaultPermissions

router = APIRouter()


@router.post("/", response_model=LawyerResponse)
def create_lawyer(
    lawyer: LawyerCreate,
    permission=Depends(require_permission(DefaultPermissions.CREATE_LAWYER.value)),
    db: Session = Depends(get_db),
):
    if not permission.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="Você não tem permissão para criar advogados.",
        )

    existing = db.query(User).filter(User.username == lawyer.username).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Username já existe.",
        )

    if lawyer.position_id is not None:
        position = db.query(Position).get(lawyer.position_id)
        if not position:
            raise HTTPException(status_code=404, detail="Cargo não encontrado")

    new_lawyer = Lawyer(
        username=lawyer.username,
        hashed_password=generate_hashed_password(lawyer.password),
        name=lawyer.name,
        email=lawyer.email,
        document=lawyer.document,
        phone=lawyer.phone,
        civil_status=lawyer.civil_status,
        address=lawyer.address,
        city=lawyer.city,
        state=lawyer.state,
        zip_code=lawyer.zip_code,
        country=lawyer.country,
        oab=lawyer.oab,
        oab_state=lawyer.oab_state,
        position_id=lawyer.position_id,
    )

    db.add(new_lawyer)
    db.commit()
    db.refresh(new_lawyer)

    return new_lawyer


@router.put("/{lawyer_id}", response_model=LawyerResponse)
def update_lawyer(
    lawyer_id: int,
    lawyer: LawyerUpdate,
    permission=Depends(require_permission(DefaultPermissions.UPDATE_LAWYER.value)),
    db: Session = Depends(get_db),
):
    if not permission.is_superuser and permission.id != lawyer_id:
        raise HTTPException(status_code=403, detail="Acesso negado")

    lawyer_to_update = db.query(Lawyer).filter(Lawyer.id == lawyer_id).first()
    if not lawyer_to_update:
        raise HTTPException(status_code=404, detail="Advogado não encontrado")

    if lawyer.position_id is not None:
        position = db.query(Position).get(lawyer.position_id)
        if not position:
            raise HTTPException(status_code=404, detail="Cargo não encontrado")

    for field, value in lawyer.model_dump(exclude_unset=True).items():
        setattr(lawyer_to_update, field, value)

    db.commit()
    db.refresh(lawyer_to_update)

    return lawyer_to_update


@router.get("/", response_model=list[LawyerResponse])
def get_lawyers(
    permission=Depends(require_permission(DefaultPermissions.VIEW_LAWYER.value)),
    db: Session = Depends(get_db),
):
    if permission.is_superuser:
        lawyers = db.query(Lawyer).order_by(Lawyer.id).all()
    else:
        lawyers = db.query(Lawyer).filter(Lawyer.id == permission.id).all()
    return lawyers


@router.get("/{lawyer_id}", response_model=LawyerResponse)
def get_lawyer(
    lawyer_id: int,
    permission=Depends(require_permission(DefaultPermissions.VIEW_LAWYER.value)),
    db: Session = Depends(get_db),
):
    if not permission.is_superuser and permission.id != lawyer_id:
        raise HTTPException(status_code=403, detail="Acesso negado")

    lawyer = db.query(Lawyer).filter(Lawyer.id == lawyer_id).first()
    if not lawyer:
        raise HTTPException(status_code=404, detail="Advogado não encontrado")
    return lawyer


@router.delete("/{lawyer_id}")
def delete_lawyer(
    lawyer_id: int,
    permission=Depends(require_permission(DefaultPermissions.DELETE_LAWYER.value)),
    db: Session = Depends(get_db),
):
    if not permission.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="Você não tem permissão para deletar advogados.",
        )

    lawyer = db.query(Lawyer).filter(Lawyer.id == lawyer_id).first()
    if not lawyer:
        raise HTTPException(status_code=404, detail="Advogado não encontrado")

    if lawyer.photo_url and os.path.exists(lawyer.photo_url):
        os.remove(lawyer.photo_url)

    db.delete(lawyer)
    db.commit()
    return {"message": "Advogado deletado com sucesso."}


@router.post("/{lawyer_id}/upload_profile_picture")
def upload_profile_picture(
    lawyer_id: int,
    file: UploadFile = File(...),
    permission=Depends(require_permission(DefaultPermissions.UPDATE_LAWYER.value)),
    db: Session = Depends(get_db),
):
    if not permission.is_superuser and permission.id != lawyer_id:
        raise HTTPException(status_code=403, detail="Acesso negado")

    lawyer = db.query(Lawyer).filter(Lawyer.id == lawyer_id).first()
    if not lawyer:
        raise HTTPException(status_code=404, detail="Advogado não encontrado")

    ext = os.path.splitext(file.filename)[1]
    filename = f"{uuid4().hex}{ext}"
    if platform.system() == "Windows":
        if not os.path.exists(settings.upload_folder_win):
            os.makedirs(settings.upload_folder_win)
        filepath = os.path.join(settings.upload_folder_win, filename)
    else:
        if not os.path.exists(settings.upload_folder_linux):
            os.makedirs(settings.upload_folder_linux)
        filepath = os.path.join(settings.upload_folder_linux, filename)

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    lawyer.photo_url = filepath
    db.commit()
    db.refresh(lawyer)

    return {"message": "Foto de perfil atualizada com sucesso."}


@router.put("/list/active")
def activate_lawyer_list(
    lawyer_ids: list[int],
    permission=Depends(require_permission(DefaultPermissions.UPDATE_LAWYER.value)),
    db: Session = Depends(get_db),
):
    if not permission.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="Você não tem permissão para ativar advogados.",
        )

    lawyers = db.query(Lawyer).filter(Lawyer.id.in_(lawyer_ids)).all()
    for lawyer in lawyers:
        lawyer.is_active = True
        db.commit()
    return {"message": "Advogados ativados com sucesso."}


@router.delete("/list/delete")
def delete_lawyer_list(
    lawyer_ids: list[int],
    permission=Depends(require_permission(DefaultPermissions.DELETE_LAWYER.value)),
    db: Session = Depends(get_db),
):
    if not permission.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="Você não tem permissão para deletar advogados.",
        )

    lawyers = db.query(Lawyer).filter(Lawyer.id.in_(lawyer_ids)).all()
    for lawyer in lawyers:
        if lawyer.photo_url and os.path.exists(lawyer.photo_url):
            os.remove(lawyer.photo_url)
        db.delete(lawyer)
        db.commit()
    return {"message": "Advogados deletados com sucesso."}
