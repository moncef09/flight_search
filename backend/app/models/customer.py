from datetime import date

from sqlalchemy import Date, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Customer(Base):
    __tablename__ = "customer"

    email: Mapped[str] = mapped_column(String(50), primary_key=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)  # bcrypt hash
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    building_num: Mapped[str | None] = mapped_column(String(20))
    street: Mapped[str | None] = mapped_column(String(100))
    city: Mapped[str | None] = mapped_column(String(50))
    state: Mapped[str | None] = mapped_column(String(50))
    phone_num: Mapped[str | None] = mapped_column(String(10))
    passport_number: Mapped[str | None] = mapped_column(String(50))
    passport_expiration: Mapped[date | None] = mapped_column(Date)
    passport_country: Mapped[str | None] = mapped_column(String(50))
    date_of_birth: Mapped[date | None] = mapped_column(Date)
