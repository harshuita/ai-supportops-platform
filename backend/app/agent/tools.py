from sqlalchemy.orm import Session
from app.rag.retrieval import search_documents
from app.models.models import Order,Ticket


def get_order_details(order_id: int, db: Session) -> dict:
    order = db.query(Order).filter(
        Order.id == order_id
    ).first()

    if not order:
        return {"error": f"Order {order_id} not found"}

    return {
        "id": order.id,
        "customer_id": order.customer_id,
        "product_name": order.product_name,
        "quantity": order.quantity,
        "status": order.status,
        "created_at": order.created_at.isoformat()
    }
def get_ticket_details(ticket_id: int, db: Session) -> dict:
    ticket = db.query(Ticket).filter(
        Ticket.id == ticket_id
    ).first()

    if not ticket:
        return {"error": f"Ticket {ticket_id} not found"}

    return {
        "id": ticket.id,
        "customer_id": ticket.customer_id,
        "order_id": ticket.order_id,
        "subject": ticket.subject,
        "message": ticket.message,
        "status": ticket.status,
        "created_at": ticket.created_at.isoformat()
    }
def search_support_knowledge(query: str) -> dict:
    results = search_documents(query, top_k=2)

    if not results:
        return {"error": "No support documents available"}

    return {
        "results": [
            {
                "source": result["source"],
                "text": result["text"],
                "score": round(result["score"], 3)
            }
            for result in results
        ]
    }