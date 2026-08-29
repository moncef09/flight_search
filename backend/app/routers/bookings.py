from datetime import datetime

from fastapi import APIRouter

from app.deps import CurrentCustomer, DbSession
from app.schemas.booking import BookingQuote, PaymentRequest, TicketOut
from app.services.booking_service import BookingService

router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.get("/quote", response_model=BookingQuote)
def get_quote(
    db: DbSession,
    customer: CurrentCustomer,
    airline_name: str,
    flight_no: str,
    departure_date_and_time: datetime,
):
    """Dynamic-priced quote shown before payment (mirrors /book_flight in the old app)."""
    return BookingService(db).quote(airline_name, flight_no, departure_date_and_time)


@router.post("/pay", response_model=TicketOut, status_code=201)
def pay(payload: PaymentRequest, db: DbSession, customer: CurrentCustomer):
    ticket = BookingService(db).pay_and_book(customer.username, payload)
    return BookingService(db).get_ticket(ticket.ticket_id)


@router.get("/me")
def my_bookings(db: DbSession, customer: CurrentCustomer):
    upcoming, past = BookingService(db).list_for_customer(customer.username)
    return {"upcoming": upcoming, "past": past}


@router.get("/{ticket_id}", response_model=TicketOut)
def get_ticket(ticket_id: str, db: DbSession, customer: CurrentCustomer):
    return BookingService(db).get_ticket(ticket_id)


@router.post("/{ticket_id}/cancel")
def cancel_booking(ticket_id: str, db: DbSession, customer: CurrentCustomer):
    BookingService(db).cancel(ticket_id, customer.username)
    return {"message": "Flight cancelled successfully. Your payment will be refunded within 7-10 business days."}
