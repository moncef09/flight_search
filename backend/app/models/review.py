from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, ForeignKeyConstraint, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Review(Base):
    __tablename__ = "review"
    __table_args__ = (
        ForeignKeyConstraint(
            ["airline_name", "flight_no", "departure_date_and_time"],
            ["flight.airline_name", "flight.flight_no", "flight.departure_date_and_time"],
        ),
    )

    email: Mapped[str] = mapped_column(String(100), ForeignKey("customer.email"), primary_key=True)
    airline_name: Mapped[str] = mapped_column(String(50), primary_key=True)
    flight_no: Mapped[str] = mapped_column(String(20), primary_key=True)
    departure_date_and_time: Mapped[datetime] = mapped_column(DateTime, primary_key=True)
    rate: Mapped[int] = mapped_column(Integer, nullable=False)
    comment: Mapped[str | None] = mapped_column(Text)
