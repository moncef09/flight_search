from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Session, aliased

from app.models.airline import Airplane, Airport
from app.models.booking import Purchase, Ticket
from app.models.flight import Flight


class BookingRepository:
    def __init__(self, db: Session):
        self.db = db

    def tickets_sold_for_flight(self, airline: str, flight_no: str, departure: datetime) -> int:
        return (
            self.db.query(func.count(Ticket.ticket_id))
            .filter(
                Ticket.airline_name == airline,
                Ticket.flight_no == flight_no,
                Ticket.departure_date_and_time == departure,
            )
            .scalar()
            or 0
        )

    def airplane_capacity(self, airline_name: str, airplane_id: str) -> int | None:
        airplane = self.db.get(Airplane, (airline_name, airplane_id))
        return airplane.num_seats if airplane else None

    def total_ticket_count(self) -> int:
        return self.db.query(func.count(Ticket.ticket_id)).scalar() or 0

    def create_ticket_and_purchase(self, ticket: Ticket, email: str) -> Ticket:
        self.db.add(ticket)
        self.db.flush()  # ticket_id must exist before Purchase FK references it
        self.db.add(Purchase(ticket_id=ticket.ticket_id, email=email, date_and_time=datetime.utcnow()))
        self.db.commit()
        self.db.refresh(ticket)
        return ticket

    def get_ticket_with_flight(self, ticket_id: str):
        dep = aliased(Airport)
        arr = aliased(Airport)
        return (
            self.db.query(Ticket, Flight, dep.name.label("departure_airport"), arr.name.label("arrival_airport"))
            .join(
                Flight,
                (Ticket.airline_name == Flight.airline_name)
                & (Ticket.flight_no == Flight.flight_no)
                & (Ticket.departure_date_and_time == Flight.departure_date_and_time),
            )
            .join(dep, Flight.departure_airport_id == dep.airport_id)
            .join(arr, Flight.arrival_airport_id == arr.airport_id)
            .filter(Ticket.ticket_id == ticket_id)
            .first()
        )

    def tickets_for_customer(self, email: str):
        dep = aliased(Airport)
        arr = aliased(Airport)
        return (
            self.db.query(Ticket, Flight, dep.name.label("departure_airport"), arr.name.label("arrival_airport"))
            .join(Purchase, Purchase.ticket_id == Ticket.ticket_id)
            .join(
                Flight,
                (Ticket.airline_name == Flight.airline_name)
                & (Ticket.flight_no == Flight.flight_no)
                & (Ticket.departure_date_and_time == Flight.departure_date_and_time),
            )
            .join(dep, Flight.departure_airport_id == dep.airport_id)
            .join(arr, Flight.arrival_airport_id == arr.airport_id)
            .filter(Purchase.email == email)
            .order_by(Ticket.departure_date_and_time)
            .all()
        )

    def find_owned_ticket(self, ticket_id: str, email: str) -> Ticket | None:
        owns = (
            self.db.query(Purchase)
            .filter(Purchase.ticket_id == ticket_id, Purchase.email == email)
            .first()
        )
        if not owns:
            return None
        return self.db.get(Ticket, ticket_id)

    def cancel(self, ticket_id: str, email: str) -> None:
        self.db.query(Purchase).filter(
            Purchase.ticket_id == ticket_id, Purchase.email == email
        ).delete()
        self.db.query(Ticket).filter(Ticket.ticket_id == ticket_id).delete()
        self.db.commit()

    def passengers_for_flight(self, airline: str, flight_no: str, departure: datetime):
        from app.models.customer import Customer

        return (
            self.db.query(Customer.name, Customer.passport_number)
            .join(Purchase, Purchase.email == Customer.email)
            .join(Ticket, Ticket.ticket_id == Purchase.ticket_id)
            .filter(
                Ticket.airline_name == airline,
                Ticket.flight_no == flight_no,
                Ticket.departure_date_and_time == departure,
            )
            .all()
        )
