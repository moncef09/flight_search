from datetime import datetime

from pydantic import BaseModel, Field


class FlightSearchQuery(BaseModel):
    source: str
    destination: str
    departure_date: str  # YYYY-MM-DD
    return_date: str | None = None


class FlightOut(BaseModel):
    airline_name: str
    flight_no: str
    departure_date_and_time: datetime
    arrival_date_and_time: datetime
    departure_airport: str
    arrival_airport: str
    departure_city: str
    arrival_city: str
    base_price: float
    status: str

    model_config = {"from_attributes": True}


class FlightSearchResponse(BaseModel):
    departure_flights: list[FlightOut]
    return_flights: list[FlightOut] = []


class FlightCreate(BaseModel):
    flight_no: str
    departure_date_and_time: datetime
    departure_airport_id: str
    arrival_airport_id: str
    arrival_date_and_time: datetime
    status: str = "on-time"
    base_price: float = Field(gt=0)
    airplane_id: str


class FlightStatusUpdate(BaseModel):
    flight_no: str
    departure_date_and_time: datetime
    status: str


class StaffFlightOut(BaseModel):
    """Raw flight row for staff screens - no airport-name joins, unlike FlightOut."""

    airline_name: str
    flight_no: str
    departure_date_and_time: datetime
    arrival_date_and_time: datetime
    departure_airport_id: str
    arrival_airport_id: str
    status: str
    base_price: float
    airplane_airline_name: str | None = None
    airplane_id: str | None = None

    model_config = {"from_attributes": True}
