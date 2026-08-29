from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, ForeignKeyConstraint, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Flight(Base):
    __tablename__ = "flight"
    __table_args__ = (
        ForeignKeyConstraint(
            ["airplane_airline_name", "airplane_id"],
            ["airplane.airline_name", "airplane.id"],
        ),
    )

    airline_name: Mapped[str] = mapped_column(
        String(50), ForeignKey("airline.name"), primary_key=True
    )
    flight_no: Mapped[str] = mapped_column(String(20), primary_key=True)
    departure_date_and_time: Mapped[datetime] = mapped_column(DateTime, primary_key=True)

    departure_airport_id: Mapped[str] = mapped_column(
        String(10), ForeignKey("airport.airport_id"), nullable=False
    )
    arrival_airport_id: Mapped[str] = mapped_column(
        String(10), ForeignKey("airport.airport_id"), nullable=False
    )
    arrival_date_and_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)
    base_price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)

    airplane_airline_name: Mapped[str | None] = mapped_column(String(50))
    airplane_id: Mapped[str | None] = mapped_column(String(20))
