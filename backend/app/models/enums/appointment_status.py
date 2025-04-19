from enum import Enum

class AppointmentStatus(Enum):
    PENDENTE="pendente"
    EM_ANDAMENTO="em_andamento"
    PAUSADO="pausado"
    CONCLUIDO="concluido"
    CANCELADO="cancelado"
