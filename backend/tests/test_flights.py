from tests.factories import make_flight


def test_search_finds_matching_flight(client, db):
    make_flight(db, flight_no="DL100")

    response = client.get(
        "/flights/search",
        params={"source": "JFK", "destination": "LAX", "departure_date": _departure_date(db)},
    )
    assert response.status_code == 200
    body = response.json()
    assert len(body["departure_flights"]) == 1
    assert body["departure_flights"][0]["flight_no"] == "DL100"


def test_search_by_city_name_also_matches(client, db):
    make_flight(db, flight_no="DL100")

    response = client.get(
        "/flights/search",
        params={
            "source": "New York",
            "destination": "Los Angeles",
            "departure_date": _departure_date(db),
        },
    )
    assert len(response.json()["departure_flights"]) == 1


def test_search_no_match_returns_empty_list(client, db):
    make_flight(db, flight_no="DL100")

    response = client.get(
        "/flights/search",
        params={"source": "JFK", "destination": "ORD", "departure_date": _departure_date(db)},
    )
    assert response.json()["departure_flights"] == []


def _departure_date(db) -> str:
    from datetime import datetime, timedelta

    return (datetime.utcnow() + timedelta(days=5)).strftime("%Y-%m-%d")
