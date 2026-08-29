from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Session, aliased

from app.models.airline import Airport
from app.models.booking import Purchase, Ticket
from app.models.flight import Flight
from app.models.review import Review


class ReviewRepository:
    def __init__(self, db: Session):
        self.db = db

    def ratable_flights(self, email: str):
        dep = aliased(Airport)
        arr = aliased(Airport)
        return (
            self.db.query(Flight, dep.name.label("departure_airport"), arr.name.label("arrival_airport"))
            .select_from(Purchase)
            .filter(Purchase.email == email)
            .join(Ticket, Ticket.ticket_id == Purchase.ticket_id)
            .join(
                Flight,
                (Ticket.airline_name == Flight.airline_name)
                & (Ticket.flight_no == Flight.flight_no)
                & (Ticket.departure_date_and_time == Flight.departure_date_and_time),
            )
            .join(dep, Flight.departure_airport_id == dep.airport_id)
            .join(arr, Flight.arrival_airport_id == arr.airport_id)
            .outerjoin(
                Review,
                (Review.email == email)
                & (Review.airline_name == Flight.airline_name)
                & (Review.flight_no == Flight.flight_no)
                & (Review.departure_date_and_time == Flight.departure_date_and_time),
            )
            .filter(
                Flight.arrival_date_and_time < datetime.utcnow(),
                Review.email.is_(None),
            )
            .distinct()
            .order_by(Flight.departure_date_and_time.desc())
            .all()
        )

    def has_purchased(self, email: str, airline: str, flight_no: str, departure: datetime) -> bool:
        return (
            self.db.query(Purchase)
            .join(Ticket, Ticket.ticket_id == Purchase.ticket_id)
            .filter(
                Purchase.email == email,
                Ticket.airline_name == airline,
                Ticket.flight_no == flight_no,
                Ticket.departure_date_and_time == departure,
            )
            .first()
            is not None
        )

    def already_reviewed(self, email: str, airline: str, flight_no: str, departure: datetime) -> bool:
        return self.db.get(Review, (email, airline, flight_no, departure)) is not None

    def create(self, review: Review) -> Review:
        self.db.add(review)
        self.db.commit()
        self.db.refresh(review)
        return review

    def average_ratings_for_airline(self, airline: str):
        return (
            self.db.query(
                Review.flight_no,
                Review.departure_date_and_time,
                func.avg(Review.rate).label("avg_rating"),
            )
            .filter(Review.airline_name == airline)
            .group_by(Review.flight_no, Review.departure_date_and_time)
            .order_by(func.avg(Review.rate).desc())
            .all()
        )

    def reviews_for_airline(self, airline: str) -> list[Review]:
        return (
            self.db.query(Review)
            .filter(Review.airline_name == airline)
            .order_by(Review.flight_no, Review.departure_date_and_time, Review.rate.desc())
            .all()
        )
