from datetime import date

from sqlalchemy import Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class AirlineStaff(Base):
    __tablename__ = "airline_staff"

    username: Mapped[str] = mapped_column(String(50), primary_key=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)  # bcrypt hash
    f_name: Mapped[str] = mapped_column(String(50), nullable=False)
    l_name: Mapped[str] = mapped_column(String(50), nullable=False)
    date_of_birth: Mapped[date | None] = mapped_column(Date)
    airline_name: Mapped[str | None] = mapped_column(String(50), ForeignKey("airline.name"))


class StaffPhone(Base):
    __tablename__ = "phone_num"

    username: Mapped[str] = mapped_column(
        String(50), ForeignKey("airline_staff.username"), primary_key=True
    )
    phone_num: Mapped[str] = mapped_column(String(10), primary_key=True)


class StaffEmail(Base):
    __tablename__ = "email"

    username: Mapped[str] = mapped_column(
        String(50), ForeignKey("airline_staff.username"), primary_key=True
    )
    email: Mapped[str] = mapped_column(String(50), primary_key=True)
