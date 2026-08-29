from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.flight import Flight
from app.repositories.flight_repo import FlightRepository
from app.repositories.admin_repo import AirportRepository
from app.schemas.flight import FlightCreate, FlightOut, FlightSearchResponse


class FlightService:
    def __init__(self, db: Session):
        self.db = db
        self.flights = FlightRepository(db)
        self.airports = AirportRepository(db)

    def _to_out(self, flight: Flight) -> FlightOut:
        dep = self.airports.get(flight.departure_airport_id)
        arr = self.airports.get(flight.arrival_airport_id)
        return FlightOut(
            airline_name=flight.airline_name,
            flight_no=flight.flight_no,
            departure_date_and_time=flight.departure_date_and_time,
            arrival_date_and_time=flight.arrival_date_and_time,
            departure_airport=dep.name if dep else flight.departure_airport_id,
            arrival_airport=arr.name if arr else flight.arrival_airport_id,
            departure_city=dep.city if dep else "",
            arrival_city=arr.city if arr else "",
            base_price=float(flight.base_price),
            status=flight.status,
        )

    def search(self, source: str, destination: str, departure_date: str, return_date: str | None) -> FlightSearchResponse:
        dep_date = datetime.strptime(departure_date, "%Y-%m-%d").date()
        departures = [self._to_out(f) for f in self.flights.search(source, destination, dep_date)]

        returns: list[FlightOut] = []
        if return_date:
            ret_date = datetime.strptime(return_date, "%Y-%m-%d").date()
            returns = [self._to_out(f) for f in self.flights.search(destination, source, ret_date)]

        return FlightSearchResponse(departure_flights=departures, return_flights=returns)

    def staff_search(self, airline: str, start_date, end_date, source, destination, status_filter):
        return self.flights.search_for_staff(airline, start_date, end_date, source, destination, status_filter)

    def upcoming_for_airline(self, airline: str):
        return self.flights.upcoming_for_airline(airline)

    def create_or_update(self, airline: str, payload: FlightCreate) -> Flight:
        if payload.departure_date_and_time >= payload.arrival_date_and_time:
            raise HTTPException(
                status.HTTP_422_UNPROCESSABLE_ENTITY, "Arrival must be after departure"
            )

        flight = Flight(
            airline_name=airline,
            flight_no=payload.flight_no,
            departure_date_and_time=payload.departure_date_and_time,
            departure_airport_id=payload.departure_airport_id,
            arrival_airport_id=payload.arrival_airport_id,
            arrival_date_and_time=payload.arrival_date_and_time,
            status=payload.status,
            base_price=payload.base_price,
            airplane_airline_name=airline,
            airplane_id=payload.airplane_id,
        )
        return self.flights.upsert(flight)

    def update_status(self, airline: str, flight_no: str, departure: datetime, status_value: str) -> None:
        self.flights.update_status(airline, flight_no, departure, status_value)
