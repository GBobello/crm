from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.customer import CustomerCreate, CustomerUpdate, CustomerResponse
from app.core.security import require_permission
from app.db.session import get_db
from app.models.enums.default_permissions import DefaultPermissions
from app.infra.repositories.customer_repository import CustomerRepository
from app.core.exceptions import ConflictException, NotFoundException

router = APIRouter()
customer_repository = CustomerRepository()


@router.post("/", response_model=CustomerResponse)
def create_customer(
    customer: CustomerCreate,
    permission=Depends(require_permission(DefaultPermissions.CREATE_CUSTOMER.value)),
    db: Session = Depends(get_db),
):
    if customer_repository.get_by_document(db, customer.document):
        raise ConflictException("Cliente com o mesmo documento já existe.")

    return customer_repository.create_customer(db, customer)


@router.put("/{customer_id}", response_model=CustomerResponse)
def update_customer(
    customer_id: int,
    customer: CustomerUpdate,
    permission=Depends(require_permission(DefaultPermissions.UPDATE_CUSTOMER.value)),
    db: Session = Depends(get_db),
):
    updated_customer = customer_repository.update_customer(db, customer_id, customer)
    if not updated_customer:
        raise NotFoundException("Cliente")
    return updated_customer


@router.get("/", response_model=list[CustomerResponse])
def get_customers(
    permission=Depends(require_permission(DefaultPermissions.VIEW_CUSTOMER.value)),
    db: Session = Depends(get_db),
):
    return customer_repository.get_all(db)


@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer(
    customer_id: int,
    permission=Depends(require_permission(DefaultPermissions.VIEW_CUSTOMER.value)),
    db: Session = Depends(get_db),
):
    customer = customer_repository.get_by_id(db, customer_id)
    if not customer:
        raise NotFoundException("Cliente")
    return customer


@router.delete("/{customer_id}")
def delete_customer(
    customer_id: int,
    permission=Depends(require_permission(DefaultPermissions.DELETE_CUSTOMER.value)),
    db: Session = Depends(get_db),
):
    if not customer_repository.delete(db, customer_id):
        raise NotFoundException("Cliente")
    return {"message": "Cliente deletado com sucesso."}


@router.delete("/list/delete")
def delete_customer_list(
    customer_ids: list[int],
    permission=Depends(require_permission(DefaultPermissions.DELETE_CUSTOMER.value)),
    db: Session = Depends(get_db),
):
    customer_repository.delete_multiple(db, customer_ids)
    return {"message": "Clientes deletados com sucesso."}
