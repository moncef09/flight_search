from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.review import Review
from app.repositories.review_repo import ReviewRepository
from app.repositories.admin_repo import AirportRepository
from app.schemas.review import AverageRatingOut, RatableFlightOut, ReviewCreate, StaffReviewSummary


class ReviewService:
    def __init__(self, db: Session):
        self.db = db
        self.reviews = ReviewRepository(db)
        self.airports = AirportRepository(db)

    def ratable_flights_for(self, email: str) -> list[RatableFlightOut]:
        rows = self.reviews.ratable_flights(email)
        out = []
        for flight, dep_name, arr_name in rows:
            out.append(
                RatableFlightOut(
                    airline_name=flight.airline_name,
                    flight_no=flight.flight_no,
                    departure_date_and_time=flight.departure_date_and_time,
                    arrival_date_and_time=flight.arrival_date_and_time,
                    departure_airport=dep_name,
                    arrival_airport=arr_name,
                )
            )
        return out

    def submit(self, email: str, payload: ReviewCreate) -> Review:
        if not self.reviews.has_purchased(
            email, payload.airline_name, payload.flight_no, payload.departure_date_and_time
        ):
            raise HTTPException(status.HTTP_403_FORBIDDEN, "You can only rate flights you have taken")

        if self.reviews.already_reviewed(
            email, payload.airline_name, payload.flight_no, payload.departure_date_and_time
        ):
            raise HTTPException(status.HTTP_409_CONFLICT, "You have already rated this flight")

        review = Review(
            email=email,
            airline_name=payload.airline_name,
            flight_no=payload.flight_no,
            departure_date_and_time=payload.departure_date_and_time,
            rate=payload.rate,
            comment=payload.comment,
        )
        return self.reviews.create(review)

    def staff_summary(self, airline: str) -> StaffReviewSummary:
        # average_ratings_for_airline returns raw SQLAlchemy Row tuples (from a
        # query(...) of individual columns, not a full ORM model) - FastAPI's
        # JSON encoder can't serialize those directly, so convert to named
        # Pydantic objects here rather than leaking a raw Row out of the API.
        averages = [
            AverageRatingOut(flight_no=row.flight_no, departure_date_and_time=row.departure_date_and_time, avg_rating=float(row.avg_rating))
            for row in self.reviews.average_ratings_for_airline(airline)
        ]
        return StaffReviewSummary(
            average_ratings=averages,
            reviews=self.reviews.reviews_for_airline(airline),
        )
