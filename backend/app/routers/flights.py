from datetime import datetime

from fastapi import APIRouter

from app.deps import CurrentStaff, DbSession
from app.schemas.flight import FlightCreate, FlightSearchResponse, FlightStatusUpdate, StaffFlightOut
from app.services.flight_service import FlightService

router = APIRouter(prefix="/flights", tags=["flights"])


@router.get("/search", response_model=FlightSearchResponse)
def search_flights(
    db: DbSession,
    source: str,
    destination: str,
    departure_date: str,
    return_date: str | None = None,
):
    """Public flight search - no auth required, mirrors the old /search_flights form."""
    return FlightService(db).search(source, destination, departure_date, return_date)


@router.get("/staff", tags=["staff"], response_model=list[StaffFlightOut])
def staff_search_flights(
    db: DbSession,
    staff: CurrentStaff,
    start_date: datetime | None = None,
    end_date: datetime | None = None,
    source: str | None = None,
    destination: str | None = None,
    status: str | None = None,
):
    return FlightService(db).staff_search(staff.airline, start_date, end_date, source, destination, status)


@router.get("/staff/upcoming", tags=["staff"], response_model=list[StaffFlightOut])
def upcoming_flights(db: DbSession, staff: CurrentStaff):
    return FlightService(db).upcoming_for_airline(staff.airline)


@router.post("/staff", status_code=201, tags=["staff"], response_model=StaffFlightOut)
def create_or_update_flight(payload: FlightCreate, db: DbSession, staff: CurrentStaff):
    return FlightService(db).create_or_update(staff.airline, payload)


@router.patch("/staff/status", tags=["staff"])
def update_flight_status(payload: FlightStatusUpdate, db: DbSession, staff: CurrentStaff):
    FlightService(db).update_status(
        staff.airline, payload.flight_no, payload.departure_date_and_time, payload.status
    )
    return {"message": "Status updated"}
