from datetime import datetime

from pydantic import BaseModel, Field


class ReviewCreate(BaseModel):
    airline_name: str
    flight_no: str
    departure_date_and_time: datetime
    rate: int = Field(ge=1, le=5)
    comment: str | None = None


class ReviewOut(BaseModel):
    email: str
    airline_name: str
    flight_no: str
    departure_date_and_time: datetime
    rate: int
    comment: str | None = None

    model_config = {"from_attributes": True}


class RatableFlightOut(BaseModel):
    airline_name: str
    flight_no: str
    departure_date_and_time: datetime
    arrival_date_and_time: datetime
    departure_airport: str
    arrival_airport: str


class AverageRatingOut(BaseModel):
    flight_no: str
    departure_date_and_time: datetime
    avg_rating: float


class StaffReviewSummary(BaseModel):
    average_ratings: list[AverageRatingOut]
    reviews: list[ReviewOut]
