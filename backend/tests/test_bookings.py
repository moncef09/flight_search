from datetime import datetime, timedelta

from app.models.booking import Purchase, Ticket
from tests.factories import make_customer, make_flight


def _auth_header(client, db, email="jane@nyu.edu", password="password123"):
    make_customer(db, email=email, password=password)
    login = client.post("/auth/login/customer", json={"username": email, "password": password})
    token = login.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_quote_returns_base_price_when_flight_mostly_empty(client, db):
    headers = _auth_header(client, db)
    flight = make_flight(db, num_seats=10, base_price=200.00)

    response = client.get(
        "/bookings/quote",
        params={
            "airline_name": flight.airline_name,
            "flight_no": flight.flight_no,
            "departure_date_and_time": flight.departure_date_and_time.isoformat(),
        },
        headers=headers,
    )
    assert response.status_code == 200
    assert response.json()["sold_price"] == 200.00


def test_quote_applies_surcharge_past_60_percent_capacity(client, db):
    headers = _auth_header(client, db)
    flight = make_flight(db, num_seats=5, base_price=100.00)
    filler_email = "filler@nyu.edu"
    make_customer(db, email=filler_email, password="password123")

    # Sell 3 of 5 seats (60%) directly via the DB to simulate prior bookings.
    for i in range(3):
        ticket = Ticket(
            ticket_id=f"TKT{i}",
            sold_price=100.00,
            airline_name=flight.airline_name,
            flight_no=flight.flight_no,
            departure_date_and_time=flight.departure_date_and_time,
        )
        db.add(ticket)
        db.flush()
        db.add(Purchase(ticket_id=ticket.ticket_id, email=filler_email, date_and_time=datetime.utcnow()))
    db.commit()

    response = client.get(
        "/bookings/quote",
        params={
            "airline_name": flight.airline_name,
            "flight_no": flight.flight_no,
            "departure_date_and_time": flight.departure_date_and_time.isoformat(),
        },
        headers=headers,
    )
    assert response.status_code == 200
    # 20% surcharge on top of the $100 base price.
    assert response.json()["sold_price"] == 120.00


def test_quote_rejects_fully_booked_flight(client, db):
    headers = _auth_header(client, db)
    flight = make_flight(db, num_seats=1, base_price=100.00)
    filler_email = "filler@nyu.edu"
    make_customer(db, email=filler_email, password="password123")

    ticket = Ticket(
        ticket_id="TKT0",
        sold_price=100.00,
        airline_name=flight.airline_name,
        flight_no=flight.flight_no,
        departure_date_and_time=flight.departure_date_and_time,
    )
    db.add(ticket)
    db.flush()
    db.add(Purchase(ticket_id=ticket.ticket_id, email=filler_email, date_and_time=datetime.utcnow()))
    db.commit()

    response = client.get(
        "/bookings/quote",
        params={
            "airline_name": flight.airline_name,
            "flight_no": flight.flight_no,
            "departure_date_and_time": flight.departure_date_and_time.isoformat(),
        },
        headers=headers,
    )
    assert response.status_code == 409


def test_full_booking_flow_creates_ticket(client, db):
    headers = _auth_header(client, db)
    flight = make_flight(db, num_seats=10, base_price=150.00)

    response = client.post(
        "/bookings/pay",
        json={
            "airline_name": flight.airline_name,
            "flight_no": flight.flight_no,
            "departure_date_and_time": flight.departure_date_and_time.isoformat(),
            "sold_price": 150.00,
            "card_type": "visa",
            "card_num": "4111111111111111",
            "name_on_card": "Jane Doe",
            "card_expiry_date": (datetime.utcnow() + timedelta(days=365)).isoformat(),
        },
        headers=headers,
    )
    assert response.status_code == 201
    body = response.json()
    assert body["ticket_id"].startswith("TKT")
    assert body["sold_price"] == 150.00

    my_bookings = client.get("/bookings/me", headers=headers).json()
    assert len(my_bookings["upcoming"]) == 1


def test_booking_rejects_expired_card(client, db):
    headers = _auth_header(client, db)
    flight = make_flight(db, num_seats=10, base_price=150.00)

    response = client.post(
        "/bookings/pay",
        json={
            "airline_name": flight.airline_name,
            "flight_no": flight.flight_no,
            "departure_date_and_time": flight.departure_date_and_time.isoformat(),
            "sold_price": 150.00,
            "card_type": "visa",
            "card_num": "4111111111111111",
            "name_on_card": "Jane Doe",
            "card_expiry_date": (datetime.utcnow() - timedelta(days=1)).isoformat(),
        },
        headers=headers,
    )
    assert response.status_code == 422


def test_cancel_within_24_hours_is_rejected(client, db):
    headers = _auth_header(client, db)
    flight = make_flight(db, num_seats=10, base_price=150.00, departs_in_days=0)
    # force departure to ~2 hours from now so it's inside the 24h cutoff
    flight.departure_date_and_time = datetime.utcnow() + timedelta(hours=2)
    db.commit()

    ticket = Ticket(
        ticket_id="TKT99",
        sold_price=150.00,
        airline_name=flight.airline_name,
        flight_no=flight.flight_no,
        departure_date_and_time=flight.departure_date_and_time,
    )
    db.add(ticket)
    db.flush()
    db.add(Purchase(ticket_id=ticket.ticket_id, email="jane@nyu.edu", date_and_time=datetime.utcnow()))
    db.commit()

    response = client.post("/bookings/TKT99/cancel", headers=headers)
    assert response.status_code == 422


def test_cancel_more_than_24_hours_out_succeeds(client, db):
    headers = _auth_header(client, db)
    flight = make_flight(db, num_seats=10, base_price=150.00, departs_in_days=5)

    ticket = Ticket(
        ticket_id="TKT98",
        sold_price=150.00,
        airline_name=flight.airline_name,
        flight_no=flight.flight_no,
        departure_date_and_time=flight.departure_date_and_time,
    )
    db.add(ticket)
    db.flush()
    db.add(Purchase(ticket_id=ticket.ticket_id, email="jane@nyu.edu", date_and_time=datetime.utcnow()))
    db.commit()

    response = client.post("/bookings/TKT98/cancel", headers=headers)
    assert response.status_code == 200


def test_cannot_cancel_someone_elses_ticket(client, db):
    headers = _auth_header(client, db, email="jane@nyu.edu")
    make_customer(db, email="other@nyu.edu", password="password123")
    flight = make_flight(db, num_seats=10, base_price=150.00, departs_in_days=5)

    ticket = Ticket(
        ticket_id="TKT97",
        sold_price=150.00,
        airline_name=flight.airline_name,
        flight_no=flight.flight_no,
        departure_date_and_time=flight.departure_date_and_time,
    )
    db.add(ticket)
    db.flush()
    db.add(Purchase(ticket_id=ticket.ticket_id, email="other@nyu.edu", date_and_time=datetime.utcnow()))
    db.commit()

    response = client.post("/bookings/TKT97/cancel", headers=headers)
    assert response.status_code == 404
