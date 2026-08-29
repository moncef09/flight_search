from datetime import date, datetime

from sqlalchemy import or_
from sqlalchemy.orm import Session, aliased

from app.models.airline import Airport
from app.models.flight import Flight


class FlightRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, airline_name: str, flight_no: str, departure: datetime) -> Flight | None:
        return self.db.get(Flight, (airline_name, flight_no, departure))

    def search(self, source: str, destination: str, on_date: date) -> list[Flight]:
        """
        Mirrors the old app's search: `source`/`destination` can be a city,
        airport name, or airport id.
        """
        dep = aliased(Airport)
        arr = aliased(Airport)

        return (
            self.db.query(Flight)
            .join(dep, Flight.departure_airport_id == dep.airport_id)
            .join(arr, Flight.arrival_airport_id == arr.airport_id)
            .filter(
                or_(dep.city == source, dep.name == source, dep.airport_id == source),
                or_(arr.city == destination, arr.name == destination, arr.airport_id == destination),
                Flight.departure_date_and_time >= datetime.combine(on_date, datetime.min.time()),
                Flight.departure_date_and_time < datetime.combine(on_date, datetime.max.time()),
            )
            .all()
        )

    def search_for_staff(
        self,
        airline: str,
        start_date: datetime | None,
        end_date: datetime | None,
        source: str | None,
        destination: str | None,
        status: str | None,
    ) -> list[Flight]:
        query = self.db.query(Flight).filter(Flight.airline_name == airline)
        if start_date:
            query = query.filter(Flight.departure_date_and_time >= start_date)
        if end_date:
            query = query.filter(Flight.departure_date_and_time <= end_date)
        if source:
            query = query.filter(Flight.departure_airport_id == source)
        if destination:
            query = query.filter(Flight.arrival_airport_id == destination)
        if status:
            query = query.filter(Flight.status == status)
        return query.all()

    def upcoming_for_airline(self, airline: str, days: int = 30) -> list[Flight]:
        from datetime import timedelta

        now = datetime.utcnow()
        return (
            self.db.query(Flight)
            .filter(
                Flight.airline_name == airline,
                Flight.departure_date_and_time.between(now, now + timedelta(days=days)),
            )
            .order_by(Flight.departure_date_and_time.asc())
            .all()
        )

    def upsert(self, flight: Flight) -> Flight:
        existing = self.get(flight.airline_name, flight.flight_no, flight.departure_date_and_time)
        if existing:
            existing.departure_airport_id = flight.departure_airport_id
            existing.arrival_airport_id = flight.arrival_airport_id
            existing.arrival_date_and_time = flight.arrival_date_and_time
            existing.status = flight.status
            existing.base_price = flight.base_price
            existing.airplane_airline_name = flight.airplane_airline_name
            existing.airplane_id = flight.airplane_id
            self.db.commit()
            self.db.refresh(existing)
            return existing

        self.db.add(flight)
        self.db.commit()
        self.db.refresh(flight)
        return flight

    def update_status(self, airline: str, flight_no: str, departure: datetime, status: str) -> None:
        flight = self.get(airline, flight_no, departure)
        if flight:
            flight.status = status
            self.db.commit()
