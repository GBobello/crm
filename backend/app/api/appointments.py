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
    if not permission.is_superuser and permission.id != appointment.user_id:
        raise HTTPException(
            status_code=403,
            detail="Você não tem permissão para criar agendamentos para outros usuários.",
        )

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
    if permission.is_superuser:
        appointments = db.query(Appointment).all()
    else:
        appointments = (
            db.query(Appointment).filter(Appointment.user_id == permission.id).all()
        )
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

    if permission.is_superuser or appointment.user_id == permission.id:
        return appointment
    else:
        raise HTTPException(
            status_code=403,
            detail="Você não tem permissão para acessar este agendamento.",
        )


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

    if permission.is_superuser or appointment_to_update.user_id == permission.id:
        for field, value in appointment.model_dump(exclude_unset=True).items():
            setattr(appointment_to_update, field, value)
            db.commit()
            db.refresh(appointment_to_update)
            return appointment_to_update
    else:
        raise HTTPException(
            status_code=403,
            detail="Você não tem permissão para atualizar este agendamento.",
        )


@router.delete("/{appointment_id}")
def delete_appointment(
    appointment_id: int,
    permission=Depends(require_permission(DefaultPermissions.DELETE_APPOINTMENT.value)),
    db: Session = Depends(get_db),
):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")

    if permission.is_superuser or appointment.user_id == permission.id:
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
    else:
        raise HTTPException(
            status_code=403,
            detail="Você não tem permissão para deletar este agendamento.",
        )


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

    if permission.is_superuser or all(
        appointment.user_id == permission.id for appointment in appointments
    ):
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
    else:
        raise HTTPException(
            status_code=403,
            detail="Você não tem permissão para deletar estes agendamentos.",
        )


@router.put("/{appointment_id}/start", response_model=AppointmentResponse)
def start_appointment(
    appointment_id: int,
    permission=Depends(require_permission(DefaultPermissions.UPDATE_APPOINTMENT.value)),
    db: Session = Depends(get_db),
):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")

    if permission.is_superuser or appointment_id == permission.id:
        appointment = transition_status(
            db, appointment, AppointmentStatus.EM_ANDAMENTO, permission.id
        )
        db.commit()
        return appointment
    else:
        raise HTTPException(
            status_code=403,
            detail="Você não tem permissão para iniciar este agendamento.",
        )


@router.put("/{appointment_id}/pause", response_model=AppointmentResponse)
def pause_appointment(
    appointment_id: int,
    permission=Depends(require_permission(DefaultPermissions.UPDATE_APPOINTMENT.value)),
    db: Session = Depends(get_db),
):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")

    if permission.is_superuser or appointment_id == permission.id:
        appointment = transition_status(
            db, appointment, AppointmentStatus.PAUSADO, permission.id
        )
        db.commit()
        return appointment
    else:
        raise HTTPException(
            status_code=403,
            detail="Você não tem permissão para pausar este agendamento.",
        )


@router.put("/{appointment_id}/resume", response_model=AppointmentResponse)
def resume_appointment(
    appointment_id: int,
    permission=Depends(require_permission(DefaultPermissions.UPDATE_APPOINTMENT.value)),
    db: Session = Depends(get_db),
):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()

    if not appointment:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")

    if permission.is_superuser or appointment_id == permission.id:
        appointment = transition_status(
            db, appointment, AppointmentStatus.EM_ANDAMENTO, permission.id
        )
        db.commit()
        return appointment
    else:
        raise HTTPException(
            status_code=403,
            detail="Você não tem permissão para retomar este agendamento.",
        )


@router.put("/{appointment_id}/finish", response_model=AppointmentResponse)
def finish_appointment(
    appointment_id: int,
    permission=Depends(require_permission(DefaultPermissions.UPDATE_APPOINTMENT.value)),
    db: Session = Depends(get_db),
):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")

    if permission.is_superuser or appointment_id == permission.id:
        appointment = transition_status(
            db, appointment, AppointmentStatus.CONCLUIDO, permission.id
        )
        db.commit()
        return appointment
    else:
        raise HTTPException(
            status_code=403,
            detail="Você não tem permissão para finalizar este agendamento.",
        )


@router.put("/{appointment_id}/cancel", response_model=AppointmentResponse)
def cancel_appointment(
    appointment_id: int,
    permission=Depends(require_permission(DefaultPermissions.UPDATE_APPOINTMENT.value)),
    db: Session = Depends(get_db),
):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")

    if permission.is_superuser or appointment_id == permission.id:
        appointment = transition_status(
            db, appointment, AppointmentStatus.CANCELADO, permission.id
        )
        db.commit()
        return appointment
    else:
        raise HTTPException(
            status_code=403,
            detail="Você não tem permissão para cancelar esse agendamento.",
        )
