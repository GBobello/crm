import enum
from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from app.models.user import User


class State(str, enum.Enum):
    AC = "AC"
    AL = "AL"
    AP = "AP"
    AM = "AM"
    BA = "BA"
    CE = "CE"
    DF = "DF"
    ES = "ES"
    GO = "GO"
    MA = "MA"
    MT = "MT"
    MS = "MS"
    MG = "MG"
    PA = "PA"
    PB = "PB"
    PR = "PR"
    PE = "PE"
    PI = "PI"
    RJ = "RJ"
    RN = "RN"
    RS = "RS"
    RO = "RO"
    RR = "RR"
    SC = "SC"
    SP = "SP"
    SE = "SE"
    TO = "TO"


class CivilStatus(str, enum.Enum):
    SOLTEIRO = "SOLTEIRO"
    CASADO = "CASADO"
    DIVORCIADO = "DIVORCIADO"
    VIUVO = "VIUVO"
    SEPARADO_JUDICIALMENTE = "SEPARADO_JUDICIALMENTE"
    UNIAO_ESTAVEL = "UNIAO_ESTAVEL"
    OUTRO = "OUTRO"


class Lawyer(User):
    __tablename__ = "lawyers"

    id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    name = Column(String(200), nullable=False)
    email = Column(String(200), nullable=False)
    document = Column(String(14), nullable=False)
    phone = Column(String(15), nullable=False)
    civil_status = Column(Enum(CivilStatus))
    address = Column(String(200))
    city = Column(String(100))
    state = Column(Enum(State))
    zip_code = Column(String(10))
    country = Column(String(200))
    photo_url = Column(String)

    oab = Column(String, nullable=False)
    oab_state = Column(Enum(State), nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "lawyer",
    }

    def __str__(self):
        return f"Lawyer(id={self.id}, oab={self.oab})"
