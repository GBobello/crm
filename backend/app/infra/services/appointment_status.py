from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.appointment import Appointment
from app.models.appointment_status_history import AppointmentStatusHistory
from app.models.enums.appointment_status import AppointmentStatus
from datetime import datetime

VALID_TRANSITIONS = {
    AppointmentStatus.PENDENTE: [
        AppointmentStatus.EM_ANDAMENTO,
        AppointmentStatus.CANCELADO,
    ],
    AppointmentStatus.EM_ANDAMENTO: [
        AppointmentStatus.PAUSADO,
        AppointmentStatus.CONCLUIDO,
        AppointmentStatus.CANCELADO,
    ],
    AppointmentStatus.PAUSADO: [
        AppointmentStatus.EM_ANDAMENTO,
        AppointmentStatus.CANCELADO,
    ],
}


def transition_status(
    db: Session,
    appointment: Appointment,
    new_status: AppointmentStatus,
    user_id: int = None,
):
    current_status = appointment.status

    if current_status == new_status:
        return appointment

    allowed = VALID_TRANSITIONS.get(current_status, [])
    if new_status not in allowed:
        raise HTTPException(
            status_code=400,
            detail=f"Transição inválida de {current_status.value} para {new_status.value}",
        )

    # Atualiza status atual

    appointment.status = new_status
    appointment.updated_at = datetime.now()

    if new_status == AppointmentStatus.PAUSADO:
        appointment.paused_at = datetime.now()
    elif new_status == AppointmentStatus.CONCLUIDO:
        appointment.finished_at = datetime.now()
    elif new_status == AppointmentStatus.CANCELADO:
        appointment.cancelled_at = datetime.now()
    elif (
        new_status == AppointmentStatus.EM_ANDAMENTO
        and current_status == AppointmentStatus.PAUSADO
    ):
        appointment.resumed_at = datetime.now()

    # Cria histórico
    history = AppointmentStatusHistory(
        appointment_id=appointment.id,
        status=new_status,
        changed_by=user_id,
    )
    db.add(history)
    db.commit()
    db.refresh(appointment)

    return appointment
