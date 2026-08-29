from datetime import date

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.airline import Airplane, Airport
from app.repositories.admin_repo import AirplaneRepository, AirportRepository, ReportRepository
from app.repositories.booking_repo import BookingRepository
from app.schemas.staff_admin import AirplaneCreate, AirportCreate, SalesReport


class AdminService:
    def __init__(self, db: Session):
        self.db = db
        self.airports = AirportRepository(db)
        self.airplanes = AirplaneRepository(db)
        self.reports = ReportRepository(db)
        self.bookings = BookingRepository(db)

    def add_airport(self, payload: AirportCreate) -> Airport:
        if self.airports.get(payload.airport_id):
            raise HTTPException(status.HTTP_409_CONFLICT, "Airport ID already exists")
        return self.airports.create(Airport(**payload.model_dump()))

    def add_airplane(self, airline_name: str, payload: AirplaneCreate) -> Airplane:
        if self.airplanes.exists(payload.id):
            raise HTTPException(status.HTTP_409_CONFLICT, "Airplane ID already exists")
        airplane = Airplane(airline_name=airline_name, **payload.model_dump())
        return self.airplanes.create(airplane)

    def airplanes_for_airline(self, airline_name: str) -> list[Airplane]:
        return self.airplanes.for_airline(airline_name)

    def sales_report(self, airline: str, start_date: date, end_date: date) -> SalesReport:
        total = self.reports.total_sales(airline, start_date, end_date)
        monthly = [{"month": m, "tickets_sold": c} for m, c in self.reports.monthly_sales(airline)]
        return SalesReport(total_tickets=total, monthly_sales=monthly)

    def passengers_for_flight(self, airline: str, flight_no: str, departure):
        return self.bookings.passengers_for_flight(airline, flight_no, departure)
