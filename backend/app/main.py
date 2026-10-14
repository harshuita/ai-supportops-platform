from fastapi import FastAPI, Depends

from app.core.database import engine, Base
from app.models.models import User, Customer, Order, Ticket
from app.api.auth import router as auth_router
from app.core.dependencies import get_current_user, require_role
from app.api.customers import router as customer_router
from app.api.orders import router as orders_router
from app.api.tickets import router as tickets_router
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI SupportOps")

app.include_router(auth_router)
app.include_router(customer_router)
app.include_router(orders_router)
app.include_router(tickets_router)
@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/me")
def get_me(user=Depends(get_current_user)):
    return user


@app.get("/admin-test")
def admin_test(user=Depends(require_role("admin"))):
    return {
        "message": "You are an admin",
        "user": user
    }