from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.models.customer import Customer
from app.models.staff import AirlineStaff
from app.repositories.customer_repo import CustomerRepository
from app.repositories.staff_repo import StaffRepository
from app.schemas.auth import CustomerRegister, StaffRegister, TokenResponse


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.customers = CustomerRepository(db)
        self.staff = StaffRepository(db)

    def register_customer(self, payload: CustomerRegister) -> Customer:
        if self.customers.get_by_email(payload.email):
            raise HTTPException(status.HTTP_409_CONFLICT, "This user already exists")

        customer = Customer(
            email=payload.email,
            password=hash_password(payload.password),
            name=payload.name,
            building_num=payload.building_num,
            street=payload.street,
            city=payload.city,
            state=payload.state,
            phone_num=payload.phone_num,
            passport_number=payload.passport_number,
            passport_expiration=payload.passport_expiration,
            passport_country=payload.passport_country,
            date_of_birth=payload.date_of_birth,
        )
        return self.customers.create(customer)

    def register_staff(self, payload: StaffRegister) -> AirlineStaff:
        if self.staff.get_by_username(payload.username):
            raise HTTPException(status.HTTP_409_CONFLICT, "This user already exists")

        staff = AirlineStaff(
            username=payload.username,
            password=hash_password(payload.password),
            f_name=payload.f_name,
            l_name=payload.l_name,
            date_of_birth=payload.date_of_birth,
            airline_name=payload.airline_name,
        )
        return self.staff.create(staff, payload.phone_numbers, payload.emails)

    def login_customer(self, email: str, password: str) -> TokenResponse:
        customer = self.customers.get_by_email(email)
        if not customer or not verify_password(password, customer.password):
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid email or password")

        token = create_access_token(subject=customer.email, user_type="customer")
        return TokenResponse(access_token=token, user_type="customer", username=customer.email)

    def login_staff(self, username: str, password: str) -> TokenResponse:
        staff = self.staff.get_by_username(username)
        if not staff or not verify_password(password, staff.password):
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid username or password")

        token = create_access_token(
            subject=staff.username, user_type="staff", extra_claims={"airline": staff.airline_name}
        )
        return TokenResponse(access_token=token, user_type="staff", username=staff.username)
