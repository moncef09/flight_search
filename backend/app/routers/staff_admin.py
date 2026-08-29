from datetime import date, datetime

from fastapi import APIRouter

from app.deps import CurrentStaff, DbSession
from app.schemas.staff_admin import (
    AirplaneCreate,
    AirplaneOut,
    AirportCreate,
    AirportOut,
    PassengerOut,
    SalesReport,
)
from app.services.admin_service import AdminService

router = APIRouter(prefix="/staff", tags=["staff"])


@router.post("/airports", status_code=201, response_model=AirportOut)
def add_airport(payload: AirportCreate, db: DbSession, staff: CurrentStaff):
    return AdminService(db).add_airport(payload)


@router.post("/airplanes", status_code=201, response_model=AirplaneOut)
def add_airplane(payload: AirplaneCreate, db: DbSession, staff: CurrentStaff):
    return AdminService(db).add_airplane(staff.airline, payload)


@router.get("/airplanes", response_model=list[AirplaneOut])
def list_airplanes(db: DbSession, staff: CurrentStaff):
    return AdminService(db).airplanes_for_airline(staff.airline)


@router.get("/reports", response_model=SalesReport)
def sales_report(
    db: DbSession,
    staff: CurrentStaff,
    start_date: date = date(1900, 1, 1),
    end_date: date = date(2100, 1, 1),
):
    return AdminService(db).sales_report(staff.airline, start_date, end_date)


@router.get("/flights/{flight_no}/passengers", response_model=list[PassengerOut])
def flight_passengers(flight_no: str, departure: datetime, db: DbSession, staff: CurrentStaff):
    rows = AdminService(db).passengers_for_flight(staff.airline, flight_no, departure)
    return [{"name": name, "passport_number": passport} for name, passport in rows]
