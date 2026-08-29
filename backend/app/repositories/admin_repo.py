from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.airline import Airplane, Airport
from app.models.booking import Purchase, Ticket


class AirportRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, airport_id: str) -> Airport | None:
        return self.db.get(Airport, airport_id)

    def create(self, airport: Airport) -> Airport:
        self.db.add(airport)
        self.db.commit()
        self.db.refresh(airport)
        return airport


class AirplaneRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, airline_name: str, airplane_id: str) -> Airplane | None:
        return self.db.get(Airplane, (airline_name, airplane_id))

    def exists(self, airplane_id: str) -> bool:
        return self.db.query(Airplane).filter(Airplane.id == airplane_id).first() is not None

    def create(self, airplane: Airplane) -> Airplane:
        self.db.add(airplane)
        self.db.commit()
        self.db.refresh(airplane)
        return airplane

    def for_airline(self, airline_name: str) -> list[Airplane]:
        return self.db.query(Airplane).filter(Airplane.airline_name == airline_name).all()


class ReportRepository:
    def __init__(self, db: Session):
        self.db = db

    def total_sales(self, airline: str, start_date, end_date) -> int:
        return (
            self.db.query(func.count(Purchase.ticket_id))
            .join(Ticket, Ticket.ticket_id == Purchase.ticket_id)
            .filter(
                Ticket.airline_name == airline,
                Purchase.date_and_time.between(start_date, end_date),
            )
            .scalar()
            or 0
        )

    def monthly_sales(self, airline: str) -> list[tuple[str, int]]:
        month = func.to_char(Purchase.date_and_time, "YYYY-MM")
        return (
            self.db.query(month.label("month"), func.count(Purchase.ticket_id).label("tickets_sold"))
            .join(Ticket, Ticket.ticket_id == Purchase.ticket_id)
            .filter(Ticket.airline_name == airline)
            .group_by(month)
            .order_by(month)
            .all()
        )
