"""
Import every model here so Alembic's autogenerate can discover them all
through `Base.metadata` (see alembic/env.py).
"""
from app.models.airline import Airline, Airplane, Airport  # noqa: F401
from app.models.booking import Purchase, Ticket  # noqa: F401
from app.models.customer import Customer  # noqa: F401
from app.models.flight import Flight  # noqa: F401
from app.models.review import Review  # noqa: F401
from app.models.staff import AirlineStaff, StaffEmail, StaffPhone  # noqa: F401
