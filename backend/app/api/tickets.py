
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.models import Customer, Order, Ticket
from app.schemas.ticket import TicketCreate, TicketResponse, TicketStatusUpdate

router = APIRouter(prefix="/tickets", tags=["Tickets"])


@router.post("/", response_model=TicketResponse, status_code=201)
def create_ticket(
    data: TicketCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    customer = db.query(Customer).filter(
        Customer.id == data.customer_id
    ).first()

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    if data.order_id is not None:
        order = db.query(Order).filter(
            Order.id == data.order_id
        ).first()

        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        if order.customer_id != data.customer_id:
            raise HTTPException(
                status_code=400,
                detail="Order does not belong to this customer",
            )

    ticket = Ticket(
        customer_id=data.customer_id,
        order_id=data.order_id,
        subject=data.subject,
        message=data.message,
        status="open",
    )

    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    return ticket


@router.get("/", response_model=list[TicketResponse])
def get_tickets(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return db.query(Ticket).order_by(Ticket.created_at.desc()).all()


@router.get("/{ticket_id}", response_model=TicketResponse)
def get_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    ticket = db.query(Ticket).filter(
        Ticket.id == ticket_id
    ).first()

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return ticket


@router.patch("/{ticket_id}", response_model=TicketResponse)
def update_ticket_status(
    ticket_id: int,
    data: TicketStatusUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    ticket = db.query(Ticket).filter(
        Ticket.id == ticket_id
    ).first()

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    ticket.status = data.status

    db.commit()
    db.refresh(ticket)

    return ticket
