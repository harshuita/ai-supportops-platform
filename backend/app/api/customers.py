from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.models import Customer
from app.schemas.customers import CustomerCreate, CustomerResponse


router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)


@router.post(
    "/",
    response_model=CustomerResponse,
    dependencies=[Depends(get_current_user)]
)
def create_customer(
    data: CustomerCreate,
    db: Session = Depends(get_db)
):
    existing = (
        db.query(Customer)
        .filter(Customer.email == data.email)
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Customer with this email already exists"
        )

    customer = Customer(
        name=data.name,
        email=data.email
    )

    db.add(customer)
    db.commit()
    db.refresh(customer)

    return customer


@router.get(
    "/",
    response_model=list[CustomerResponse],
    dependencies=[Depends(get_current_user)]
)
def get_customers(db: Session = Depends(get_db)):
    return db.query(Customer).all()


@router.get(
    "/{customer_id}",
    response_model=CustomerResponse,
    dependencies=[Depends(get_current_user)]
)
def get_customer(
    customer_id: int,
    db: Session = Depends(get_db)
):
    customer = (
        db.query(Customer)
        .filter(Customer.id == customer_id)
        .first()
    )

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return customer