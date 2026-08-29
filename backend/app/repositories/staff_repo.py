from sqlalchemy.orm import Session

from app.models.staff import AirlineStaff, StaffEmail, StaffPhone


class StaffRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_username(self, username: str) -> AirlineStaff | None:
        return self.db.get(AirlineStaff, username)

    def create(self, staff: AirlineStaff, phone_numbers: list[str], emails: list[str]) -> AirlineStaff:
        self.db.add(staff)
        for phone in set(phone_numbers):
            self.db.add(StaffPhone(username=staff.username, phone_num=phone))
        for email in set(emails):
            self.db.add(StaffEmail(username=staff.username, email=email))
        self.db.commit()
        self.db.refresh(staff)
        return staff
