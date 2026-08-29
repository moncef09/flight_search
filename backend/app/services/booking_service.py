from datetime import datetime, timedelta

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.booking import Ticket
from app.repositories.booking_repo import BookingRepository
from app.repositories.flight_repo import FlightRepository
from app.repositories.admin_repo import AirportRepository
from app.schemas.booking import BookingQuote, PaymentRequest, TicketOut

# Same dynamic pricing rule as the original app: once 60% of seats are sold,
# the price jumps 20% above base price.
CAPACITY_SURCHARGE_THRESHOLD = 60
SURCHARGE_MULTIPLIER = 1.2


class BookingService:
    def __init__(self, db: Session):
        self.db = db
        self.bookings = BookingRepository(db)
        self.flights = FlightRepository(db)
        self.airports = AirportRepository(db)

    def quote(self, airline: str, flight_no: str, departure: datetime) -> BookingQuote:
        flight = self.flights.get(airline, flight_no, departure)
        if not flight or flight.arrival_date_and_time <= datetime.utcnow():
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Flight not available for booking")

        capacity = self.bookings.airplane_capacity(flight.airplane_airline_name, flight.airplane_id)
        if not capacity:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Flight has no assigned airplane")

        tickets_sold = self.bookings.tickets_sold_for_flight(airline, flight_no, departure)
        if tickets_sold >= capacity:
            raise HTTPException(status.HTTP_409_CONFLICT, "Sorry, this flight is fully booked")

        capacity_pct = (tickets_sold / capacity) * 100
        base_price = float(flight.base_price)
        sold_price = round(
            base_price * SURCHARGE_MULTIPLIER if capacity_pct >= CAPACITY_SURCHARGE_THRESHOLD else base_price,
            2,
        )

        dep_airport = self.airports.get(flight.departure_airport_id)
        arr_airport = self.airports.get(flight.arrival_airport_id)

        return BookingQuote(
            airline_name=airline,
            flight_no=flight_no,
            departure_date_and_time=departure,
            arrival_date_and_time=flight.arrival_date_and_time,
            departure_airport=dep_airport.name if dep_airport else flight.departure_airport_id,
            arrival_airport=arr_airport.name if arr_airport else flight.arrival_airport_id,
            base_price=base_price,
            sold_price=sold_price,
            capacity_percentage=capacity_pct,
        )

    def pay_and_book(self, customer_email: str, payload: PaymentRequest) -> Ticket:
        # Re-quote server-side so the client can't tamper with the price it submits.
        fresh_quote = self.quote(payload.airline_name, payload.flight_no, payload.departure_date_and_time)

        if payload.card_expiry_date < datetime.utcnow():
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "Card has expired")

        next_number = self.bookings.total_ticket_count() + 1
        ticket_id = f"TKT{next_number:05d}"

        ticket = Ticket(
            ticket_id=ticket_id,
            sold_price=fresh_quote.sold_price,
            card_type=payload.card_type,
            card_num=payload.card_num,
            name_on_card=payload.name_on_card,
            card_expiry_date=payload.card_expiry_date.date(),
            airline_name=payload.airline_name,
            flight_no=payload.flight_no,
            departure_date_and_time=payload.departure_date_and_time,
        )
        return self.bookings.create_ticket_and_purchase(ticket, customer_email)

    def get_ticket(self, ticket_id: str) -> TicketOut:
        row = self.bookings.get_ticket_with_flight(ticket_id)
        if not row:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Ticket not found")
        ticket, flight, dep_name, arr_name = row
        return TicketOut(
            ticket_id=ticket.ticket_id,
            sold_price=float(ticket.sold_price),
            airline_name=ticket.airline_name,
            flight_no=ticket.flight_no,
            departure_date_and_time=ticket.departure_date_and_time,
            arrival_date_and_time=flight.arrival_date_and_time,
            departure_airport=dep_name,
            arrival_airport=arr_name,
            status=flight.status,
        )

    def list_for_customer(self, email: str) -> tuple[list[TicketOut], list[TicketOut]]:
        rows = self.bookings.tickets_for_customer(email)
        now = datetime.utcnow()
        upcoming, past = [], []
        for ticket, flight, dep_name, arr_name in rows:
            out = TicketOut(
                ticket_id=ticket.ticket_id,
                sold_price=float(ticket.sold_price),
                airline_name=ticket.airline_name,
                flight_no=ticket.flight_no,
                departure_date_and_time=ticket.departure_date_and_time,
                arrival_date_and_time=flight.arrival_date_and_time,
                departure_airport=dep_name,
                arrival_airport=arr_name,
                status=flight.status,
            )
            (upcoming if ticket.departure_date_and_time > now else past).append(out)
        return upcoming, past

    def cancel(self, ticket_id: str, email: str) -> None:
        ticket = self.bookings.find_owned_ticket(ticket_id, email)
        if not ticket:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Ticket not found or not owned by you")

        if ticket.departure_date_and_time - datetime.utcnow() <= timedelta(hours=24):
            raise HTTPException(
                status.HTTP_422_UNPROCESSABLE_ENTITY,
                "Flight cannot be cancelled since it is within 24 hours of departure",
            )

        self.bookings.cancel(ticket_id, email)
