from datetime import datetime

from pydantic import BaseModel, Field


class BookingRequest(BaseModel):
    airline_name: str
    flight_no: str
    departure_date_and_time: datetime


class BookingQuote(BaseModel):
    """Returned before payment so the client can show the price before charging."""

    airline_name: str
    flight_no: str
    departure_date_and_time: datetime
    arrival_date_and_time: datetime
    departure_airport: str
    arrival_airport: str
    base_price: float
    sold_price: float
    capacity_percentage: float


class PaymentRequest(BaseModel):
    airline_name: str
    flight_no: str
    departure_date_and_time: datetime
    sold_price: float = Field(gt=0)
    card_type: str
    card_num: str = Field(pattern=r"^\d+$")
    name_on_card: str
    card_expiry_date: datetime


class TicketOut(BaseModel):
    ticket_id: str
    sold_price: float
    airline_name: str
    flight_no: str
    departure_date_and_time: datetime
    arrival_date_and_time: datetime
    departure_airport: str
    arrival_airport: str
    status: str | None = None

    model_config = {"from_attributes": True}


class CancelRequest(BaseModel):
    ticket_id: str
