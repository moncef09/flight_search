from tests.factories import make_customer


def test_register_customer(client):
    response = client.post(
        "/auth/register/customer",
        json={
            "email": "new@nyu.edu",
            "password": "password123",
            "name": "New User",
            "building_num": "1",
            "street": "Main St",
            "city": "NYC",
            "state": "NY",
            "phone_num": "1234567890",
            "passport_number": "P1",
            "passport_expiration": "2030-01-01",
            "passport_country": "USA",
            "date_of_birth": "2000-01-01",
        },
    )
    assert response.status_code == 201


def test_register_customer_duplicate_email_rejected(client, db):
    make_customer(db, email="dupe@nyu.edu")

    response = client.post(
        "/auth/register/customer",
        json={
            "email": "dupe@nyu.edu",
            "password": "password123",
            "name": "New User",
            "building_num": "1",
            "street": "Main St",
            "city": "NYC",
            "state": "NY",
            "phone_num": "1234567890",
            "passport_number": "P1",
            "passport_expiration": "2030-01-01",
            "passport_country": "USA",
            "date_of_birth": "2000-01-01",
        },
    )
    assert response.status_code == 409


def test_login_success_returns_jwt(client, db):
    make_customer(db, email="jane@nyu.edu", password="password123")

    response = client.post(
        "/auth/login/customer", json={"username": "jane@nyu.edu", "password": "password123"}
    )
    assert response.status_code == 200
    body = response.json()
    assert body["user_type"] == "customer"
    assert body["access_token"]


def test_login_wrong_password_rejected(client, db):
    make_customer(db, email="jane@nyu.edu", password="password123")

    response = client.post(
        "/auth/login/customer", json={"username": "jane@nyu.edu", "password": "wrong-password"}
    )
    assert response.status_code == 401


def test_protected_route_requires_token(client):
    response = client.get("/bookings/me")
    assert response.status_code == 401


def test_protected_route_rejects_staff_token_on_customer_route(client, db):
    from tests.factories import make_staff

    make_staff(db, username="agent1", password="password123")
    login = client.post(
        "/auth/login/staff", json={"username": "agent1", "password": "password123"}
    )
    token = login.json()["access_token"]

    response = client.get("/bookings/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403
