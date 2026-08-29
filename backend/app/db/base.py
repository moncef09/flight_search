from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import settings

engine = create_engine(settings.database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """Base class every SQLAlchemy model inherits from."""


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency: yields a DB session for the duration of one request,
    then always closes it - even if the request handler raises.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
