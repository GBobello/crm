from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.db.session import get_db
from app.core.security import require_permission
from app.models.enums.default_permissions import DefaultPermissions
from app.models.appointment import Appointment
from app.models.appointment_status_history import AppointmentStatusHistory
from app.models.user import User
from app.models.enums.appointment_status import AppointmentStatus
from app.schemas.appointment import (
    AppointmentCreate,
    AppointmentUpdate,
    AppointmentResponse,
)
from app.services.appointment_status import transition_status

router = APIRouter()


@router.post("/", response_model=AppointmentResponse)
def create_appointment(
    appointment: AppointmentCreate,
    permission=Depends(require_permission(DefaultPermissions.CREATE_APPOINTMENT.value)),
    db: Session = Depends(get_db),
):
    new_appointment = Appointment(
        title=appointment.title,
        description=appointment.description,
        customer_id=appointment.customer_id,
        user_id=appointment.user_id,
    )

    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)

    return new_appointment


@router.get("/", response_model=List[AppointmentResponse])
def get_appointments(
    permission=Depends(require_permission(DefaultPermissions.VIEW_APPOINTMENT.value)),
    db: Session = Depends(get_db),
):
    appointments = db.query(Appointment).all()
    return appointments


@router.get("/{appointment_id}", response_model=AppointmentResponse)
def get_appointment(
    appointment_id: int,
    permission=Depends(require_permission(DefaultPermissions.VIEW_APPOINTMENT.value)),
    db: Session = Depends(get_db),
):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()

    if not appointment:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")

    return appointment


@router.put("/{appointment_id}", response_model=AppointmentResponse)
def update_appointment(
    appointment_id: int,
    appointment: AppointmentUpdate,
    permission=Depends(require_permission(DefaultPermissions.UPDATE_APPOINTMENT.value)),
    db: Session = Depends(get_db),
):
    appointment_to_update = (
        db.query(Appointment).filter(Appointment.id == appointment_id).first()
    )
    if not appointment_to_update:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")
    for field, value in appointment.model_dump(exclude_unset=True).items():
        setattr(appointment_to_update, field, value)

    db.commit()
    db.refresh(appointment_to_update)
    return appointment_to_update


@router.delete("/{appointment_id}")
def delete_appointment(
    appointment_id: int,
    permission=Depends(require_permission(DefaultPermissions.DELETE_APPOINTMENT.value)),
    db: Session = Depends(get_db),
):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")

    appointment_status_history = (
        db.query(AppointmentStatusHistory)
        .filter(AppointmentStatusHistory.appointment_id == appointment_id)
        .all()
    )

    for history in appointment_status_history:
        db.delete(history)
        db.commit()

    db.delete(appointment)
    db.commit()

    return {"message": "Agendamento deletado com sucesso"}


@router.delete("/list/delete")
def delete_appointments(
    appointment_ids: List[int],
    permission=Depends(require_permission(DefaultPermissions.DELETE_APPOINTMENT.value)),
    db: Session = Depends(get_db),
):
    appointments = (
        db.query(Appointment).filter(Appointment.id.in_(appointment_ids)).all()
    )
    if not appointments:
        raise HTTPException(status_code=404, detail="Agendamentos não encontrados")

    appointment_status_history = (
        db.query(AppointmentStatusHistory)
        .filter(AppointmentStatusHistory.appointment_id.in_(appointment_ids))
        .all()
    )
    for history in appointment_status_history:
        db.delete(history)
        db.commit()

    for appointment in appointments:
        db.delete(appointment)
        db.commit()

    return {"message": "Agendamentos deletados com sucesso"}


@router.put("/{appointment_id}/start", response_model=AppointmentResponse)
def start_appointment(
    appointment_id: int,
    permission=Depends(require_permission(DefaultPermissions.UPDATE_APPOINTMENT.value)),
    db: Session = Depends(get_db),
):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")

    user_id = db.query(User).filter(User.username == permission.username).first().id

    appointment = transition_status(
        db, appointment, AppointmentStatus.EM_ANDAMENTO, user_id
    )
    db.commit()
    return appointment


@router.put("/{appointment_id}/pause", response_model=AppointmentResponse)
def pause_appointment(
    appointment_id: int,
    permission=Depends(require_permission(DefaultPermissions.UPDATE_APPOINTMENT.value)),
    db: Session = Depends(get_db),
):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")

    user_id = db.query(User).filter(User.username == permission.username).first().id

    appointment = transition_status(db, appointment, AppointmentStatus.PAUSADO, user_id)
    db.commit()
    return appointment


@router.put("/{appointment_id}/resume", response_model=AppointmentResponse)
def resume_appointment(
    appointment_id: int,
    permission=Depends(require_permission(DefaultPermissions.UPDATE_APPOINTMENT.value)),
    db: Session = Depends(get_db),
):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()

    if not appointment:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")

    user_id = db.query(User).filter(User.username == permission.username).first().id
    appointment = transition_status(
        db, appointment, AppointmentStatus.EM_ANDAMENTO, user_id
    )
    db.commit()
    return appointment


@router.put("/{appointment_id}/finish", response_model=AppointmentResponse)
def finish_appointment(
    appointment_id: int,
    permission=Depends(require_permission(DefaultPermissions.UPDATE_APPOINTMENT.value)),
    db: Session = Depends(get_db),
):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")

    user_id = db.query(User).filter(User.username == permission.username).first().id
    appointment = transition_status(
        db, appointment, AppointmentStatus.CONCLUIDO, user_id
    )
    db.commit()
    return appointment


@router.put("/{appointment_id}/cancel", response_model=AppointmentResponse)
def cancel_appointment(
    appointment_id: int,
    permission=Depends(require_permission(DefaultPermissions.UPDATE_APPOINTMENT.value)),
    db: Session = Depends(get_db),
):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")

    user_id = db.query(User).filter(User.username == permission.username).first().id
    appointment = transition_status(
        db, appointment, AppointmentStatus.CANCELADO, user_id
    )
    db.commit()
    return appointment
