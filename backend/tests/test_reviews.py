from datetime import datetime, timedelta

from app.models.booking import Purchase, Ticket
from tests.factories import make_customer, make_flight, make_staff


def _auth_header(client, db, email="jane@nyu.edu", password="password123"):
    make_customer(db, email=email, password=password)
    login = client.post("/auth/login/customer", json={"username": email, "password": password})
    return {"Authorization": f"Bearer {login.json()['access_token']}"}


def _staff_auth_header(client, db, username="agent1", password="password123", airline_name="Delta"):
    make_staff(db, airline_name=airline_name, username=username, password=password)
    login = client.post("/auth/login/staff", json={"username": username, "password": password})
    return {"Authorization": f"Bearer {login.json()['access_token']}"}


def _book_past_flight(db, email="jane@nyu.edu"):
    flight = make_flight(db, num_seats=10, base_price=150.00, departs_in_days=-5)
    ticket = Ticket(
        ticket_id="TKT-PAST",
        sold_price=150.00,
        airline_name=flight.airline_name,
        flight_no=flight.flight_no,
        departure_date_and_time=flight.departure_date_and_time,
    )
    db.add(ticket)
    db.flush()
    db.add(Purchase(ticket_id=ticket.ticket_id, email=email, date_and_time=datetime.utcnow()))
    db.commit()
    return flight


def test_submit_review_for_taken_flight_succeeds(client, db):
    headers = _auth_header(client, db)
    flight = _book_past_flight(db)

    response = client.post(
        "/reviews",
        json={
            "airline_name": flight.airline_name,
            "flight_no": flight.flight_no,
            "departure_date_and_time": flight.departure_date_and_time.isoformat(),
            "rate": 5,
            "comment": "Great flight!",
        },
        headers=headers,
    )
    assert response.status_code == 201


def test_cannot_review_flight_never_taken(client, db):
    headers = _auth_header(client, db)
    flight = make_flight(db, departs_in_days=-5)

    response = client.post(
        "/reviews",
        json={
            "airline_name": flight.airline_name,
            "flight_no": flight.flight_no,
            "departure_date_and_time": flight.departure_date_and_time.isoformat(),
            "rate": 5,
        },
        headers=headers,
    )
    assert response.status_code == 403


def test_cannot_review_same_flight_twice(client, db):
    headers = _auth_header(client, db)
    flight = _book_past_flight(db)
    payload = {
        "airline_name": flight.airline_name,
        "flight_no": flight.flight_no,
        "departure_date_and_time": flight.departure_date_and_time.isoformat(),
        "rate": 5,
    }

    first = client.post("/reviews", json=payload, headers=headers)
    second = client.post("/reviews", json=payload, headers=headers)

    assert first.status_code == 201
    assert second.status_code == 409


def test_ratable_flights_excludes_already_reviewed(client, db):
    headers = _auth_header(client, db)
    flight = _book_past_flight(db)

    before = client.get("/reviews/ratable", headers=headers).json()
    assert len(before) == 1

    client.post(
        "/reviews",
        json={
            "airline_name": flight.airline_name,
            "flight_no": flight.flight_no,
            "departure_date_and_time": flight.departure_date_and_time.isoformat(),
            "rate": 4,
        },
        headers=headers,
    )

    after = client.get("/reviews/ratable", headers=headers).json()
    assert after == []


def test_staff_summary_returns_average_ratings_and_reviews(client, db):
    # Regression test: average_ratings_for_airline returns raw SQLAlchemy Row
    # tuples (a query() of individual columns, not full ORM objects) - without
    # converting those to a Pydantic model first, FastAPI's JSON encoder fails
    # with a 500 on this endpoint. Caught manually while building the staff
    # dashboard; this pins the fix (see services/review_service.py).
    cust_headers = _auth_header(client, db)
    flight = _book_past_flight(db)
    client.post(
        "/reviews",
        json={
            "airline_name": flight.airline_name,
            "flight_no": flight.flight_no,
            "departure_date_and_time": flight.departure_date_and_time.isoformat(),
            "rate": 5,
            "comment": "Great flight",
        },
        headers=cust_headers,
    )

    staff_headers = _staff_auth_header(client, db, airline_name=flight.airline_name)
    response = client.get("/reviews/staff/summary", headers=staff_headers)

    assert response.status_code == 200
    body = response.json()
    assert body["average_ratings"] == [
        {
            "flight_no": flight.flight_no,
            "departure_date_and_time": flight.departure_date_and_time.isoformat(),
            "avg_rating": 5.0,
        }
    ]
    assert len(body["reviews"]) == 1
    assert body["reviews"][0]["rate"] == 5
