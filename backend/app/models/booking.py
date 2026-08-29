from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, ForeignKeyConstraint, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Ticket(Base):
    __tablename__ = "ticket"
    __table_args__ = (
        ForeignKeyConstraint(
            ["airline_name", "flight_no", "departure_date_and_time"],
            ["flight.airline_name", "flight.flight_no", "flight.departure_date_and_time"],
        ),
    )

    ticket_id: Mapped[str] = mapped_column(String(20), primary_key=True)
    sold_price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    card_type: Mapped[str | None] = mapped_column(String(20))
    card_num: Mapped[str | None] = mapped_column(String(20))
    name_on_card: Mapped[str | None] = mapped_column(String(50))
    card_expiry_date: Mapped[date | None] = mapped_column(Date)

    airline_name: Mapped[str] = mapped_column(String(50))
    flight_no: Mapped[str] = mapped_column(String(20))
    departure_date_and_time: Mapped[datetime] = mapped_column(DateTime)


class Purchase(Base):
    __tablename__ = "purchases"

    ticket_id: Mapped[str] = mapped_column(
        String(20), ForeignKey("ticket.ticket_id"), primary_key=True
    )
    email: Mapped[str] = mapped_column(String(50), ForeignKey("customer.email"), primary_key=True)
    date_and_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
