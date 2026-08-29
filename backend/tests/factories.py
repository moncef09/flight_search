"""Small helpers for building test fixtures - the layered architecture means
tests can insert model objects directly instead of going through the API."""
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.airline import Airline, Airplane, Airport
from app.models.customer import Customer
from app.models.flight import Flight
from app.models.staff import AirlineStaff


def make_customer(db: Session, email="jane@nyu.edu", password="password123") -> Customer:
    customer = Customer(
        email=email,
        password=hash_password(password),
        name="Jane Doe",
        building_num="10",
        street="Main St",
        city="New York",
        state="NY",
        phone_num="1234567890",
        passport_number="P1",
        passport_expiration="2030-01-01",
        passport_country="USA",
        date_of_birth="1995-01-01",
    )
    db.add(customer)
    db.commit()
    return customer


def make_staff(db: Session, airline_name="Delta", username="agent1", password="password123") -> AirlineStaff:
    db.merge(Airline(name=airline_name))
    staff = AirlineStaff(
        username=username,
        password=hash_password(password),
        f_name="Sam",
        l_name="Staffer",
        date_of_birth="1990-01-01",
        airline_name=airline_name,
    )
    db.add(staff)
    db.commit()
    return staff


def make_flight(
    db: Session,
    airline_name="Delta",
    flight_no="DL100",
    num_seats=2,
    departs_in_days=5,
    base_price=200.00,
) -> Flight:
    db.merge(Airline(name=airline_name))
    db.merge(Airport(airport_id="JFK", name="JFK Airport", city="New York", country="USA"))
    db.merge(Airport(airport_id="LAX", name="LAX Airport", city="Los Angeles", country="USA"))
    db.merge(Airplane(airline_name=airline_name, id="AC1", num_seats=num_seats, manufacturing_co="Boeing"))
    db.commit()

    departure = datetime.utcnow() + timedelta(days=departs_in_days)
    flight = Flight(
        airline_name=airline_name,
        flight_no=flight_no,
        departure_date_and_time=departure,
        departure_airport_id="JFK",
        arrival_airport_id="LAX",
        arrival_date_and_time=departure + timedelta(hours=6),
        status="on-time",
        base_price=base_price,
        airplane_airline_name=airline_name,
        airplane_id="AC1",
    )
    db.add(flight)
    db.commit()
    return flight
