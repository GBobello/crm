from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.custumer import Customer
from app.schemas.customer import CustomerCreate, CustomerUpdate, CustomerResponse
from app.core.security import verify_session
from app.utils.validate_document import validate_document
from app.utils.validate_phone import validate_phone
from app.db.session import get_db

router = APIRouter()


@router.post("/", response_model=CustomerResponse)
def create_customer(
    customer: CustomerCreate,
    user=Depends(verify_session),
    db: Session = Depends(get_db),
):
    existing = db.query(Customer).filter(Customer.document == customer.document).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Cliente com o mesmo documento já existe.",
        )
    if not validate_document(customer.document):
        raise HTTPException(
            status_code=400,
            detail="Documento inválido.",
        )
    if not validate_phone(customer.phone):
        raise HTTPException(
            status_code=400,
            detail="Telefone inválido.",
        )

    new_customer = Customer(
        name=customer.name,
        document=customer.document,
        email=customer.email,
        phone=customer.phone,
        born_date=customer.born_date,
        civil_status=customer.civil_status,
        address=customer.address,
        city=customer.city,
        state=customer.state,
        zip_code=customer.zip_code,
        country=customer.country,
    )

    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)

    return new_customer


@router.put("/{customer_id}", response_model=CustomerResponse)
def update_customer(
    customer_id: int,
    customer: CustomerUpdate,
    user=Depends(verify_session),
    db: Session = Depends(get_db),
):
    customer_to_update = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer_to_update:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    if not validate_document(customer.document):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Documento inválido.",
        )

    if not validate_phone(customer.phone):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Telefone inválido.",
        )

    customer_to_update.name = customer.name
    customer_to_update.document = customer.document
    customer_to_update.email = customer.email
    customer_to_update.phone = customer.phone
    customer_to_update.born_date = customer.born_date
    customer_to_update.civil_status = customer.civil_status
    customer_to_update.address = customer.address
    customer_to_update.city = customer.city
    customer_to_update.state = customer.state
    customer_to_update.zip_code = customer.zip_code
    customer_to_update.country = customer.country

    db.commit()
    db.refresh(customer_to_update)

    return customer_to_update


@router.get("/", response_model=list[CustomerResponse])
def get_customers(user=Depends(verify_session), db: Session = Depends(get_db)):
    customers = db.query(Customer).all()
    return customers


@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer(
    customer_id: int, user=Depends(verify_session), db: Session = Depends(get_db)
):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return customer


@router.delete("/{customer_id}")
def delete_customer(
    customer_id: int, user=Depends(verify_session), db: Session = Depends(get_db)
):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()

    if not customer:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    db.delete(customer)
    db.commit()

    return {"message": "Cliente deletado com sucesso."}


@router.delete("/list/delete")
def delete_customer_list(
    customer_ids: list[int], user=Depends(verify_session), db: Session = Depends(get_db)
):
    customers = db.query(Customer).filter(Customer.id.in_(customer_ids)).all()
    for customer in customers:
        db.delete(customer)
        db.commit()
    return {"message": "Clientes deletados com sucesso."}
