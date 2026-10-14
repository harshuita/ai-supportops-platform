from datetime import datetime

from sqlalchemy import String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(50), default="support_agent")


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)

    orders: Mapped[list["Order"]] = relationship(
        back_populates="customer"
    )

    tickets: Mapped[list["Ticket"]] = relationship(
        back_populates="customer"
    )


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))

    product_name: Mapped[str] = mapped_column(String(255))
    quantity: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(
        String(50),
        default="pending"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    customer: Mapped["Customer"] = relationship(
        back_populates="orders"
    )

    tickets: Mapped[list["Ticket"]] = relationship(
        back_populates="order"
    )


class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))
    order_id: Mapped[int | None] = mapped_column(
        ForeignKey("orders.id"),
        nullable=True
    )

    subject: Mapped[str] = mapped_column(String(255))
    message: Mapped[str] = mapped_column(String(2000))
    status: Mapped[str] = mapped_column(
        String(50),
        default="open"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    customer: Mapped["Customer"] = relationship(
        back_populates="tickets"
    )

    order: Mapped["Order | None"] = relationship(
        back_populates="tickets"
    )