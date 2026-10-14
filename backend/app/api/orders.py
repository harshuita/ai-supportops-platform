from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.models import Customer, Order
from app.schemas.order import OrderCreate, OrderResponse,OrderStatusUpdate

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

@router.get("/", response_model=list[OrderResponse])
def get_orders(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return db.query(Order).all()

@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    order = db.query(Order).filter(
        Order.id == order_id
    ).first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return order

@router.post(
    "/",
    response_model=OrderResponse,
    status_code=201
)
def create_order(
    data: OrderCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    customer = db.query(Customer).filter(
        Customer.id == data.customer_id
    ).first()

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    order = Order(
        customer_id=data.customer_id,
        product_name=data.product_name,
        quantity=data.quantity,
        status="created"
    )

    db.add(order)
    db.commit()
    db.refresh(order)

    return order


@router.patch("/{order_id}", response_model=OrderResponse)
def update_order_status(
    order_id: int,
    data: OrderStatusUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    order = db.query(Order).filter(
        Order.id == order_id
    ).first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    order.status = data.status

    db.commit()
    db.refresh(order)

    return order
