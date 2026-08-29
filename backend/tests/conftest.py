"""
Shared pytest fixtures.

Strategy: point SQLAlchemy at a dedicated `flights_test` Postgres database,
create all tables once for the whole test session. Service-layer code commits
mid-request (e.g. booking a flight touches Ticket then Purchase), so a simple
"wrap the test in one transaction and roll it back" pattern doesn't work here -
instead every table is truncated after each test for a clean slate.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

import app.models  # noqa: F401  (registers all models on Base.metadata)
from app.db.base import Base, get_db
from app.main import app

TEST_DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/flights_test"


@pytest.fixture(scope="session")
def engine():
    engine = create_engine(TEST_DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture()
def db(engine):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()

    yield session

    session.close()
    with engine.begin() as connection:
        table_names = ", ".join(t.name for t in reversed(Base.metadata.sorted_tables))
        connection.execute(text(f"TRUNCATE TABLE {table_names} RESTART IDENTITY CASCADE"))


@pytest.fixture()
def client(db):
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
