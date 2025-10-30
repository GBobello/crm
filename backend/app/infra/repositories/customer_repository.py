from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.custumer import Customer
from app.infra.repositories.base_repository import BaseRepository
from app.schemas.customer import CustomerCreate, CustomerUpdate


class CustomerRepository(BaseRepository[Customer]):
    def __init__(self):
        super().__init__(Customer)

    def get_by_document(self, db: Session, document: str) -> Optional[Customer]:
        return db.query(Customer).filter(Customer.document == document).first()

    def create_customer(self, db: Session, customer: CustomerCreate) -> Customer:
        db_customer = Customer(
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
        return self.create(db, db_customer)

    def update_customer(
        self, db: Session, customer_id: int, customer: CustomerUpdate
    ) -> Optional[Customer]:
        db_customer = self.get_by_id(db, customer_id)
        if not db_customer:
            return None

        update_data = customer.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_customer, field, value)

        db.commit()
        db.refresh(db_customer)
        return db_customer

    def delete_multiple(self, db: Session, customer_ids: List[int]) -> bool:
        customers = db.query(Customer).filter(Customer.id.in_(customer_ids)).all()
        for customer in customers:
            db.delete(customer)
        db.commit()
        return True
