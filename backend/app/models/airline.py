from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Airline(Base):
    __tablename__ = "airline"

    name: Mapped[str] = mapped_column(String(50), primary_key=True)


class Airport(Base):
    __tablename__ = "airport"

    airport_id: Mapped[str] = mapped_column(String(10), primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    city: Mapped[str] = mapped_column(String(50), nullable=False)
    country: Mapped[str] = mapped_column(String(50), nullable=False)


class Airplane(Base):
    __tablename__ = "airplane"

    airline_name: Mapped[str] = mapped_column(
        String(50), ForeignKey("airline.name"), primary_key=True
    )
    id: Mapped[str] = mapped_column(String(20), primary_key=True)
    num_seats: Mapped[int] = mapped_column(Integer, nullable=False)
    manufacturing_co: Mapped[str | None] = mapped_column(String(50))
