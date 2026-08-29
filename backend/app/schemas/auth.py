from datetime import date

from pydantic import BaseModel, EmailStr, Field


class CustomerRegister(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
    name: str
    building_num: str
    street: str
    city: str
    state: str
    phone_num: str
    passport_number: str
    passport_expiration: date
    passport_country: str
    date_of_birth: date


class StaffRegister(BaseModel):
    username: str
    password: str = Field(min_length=6)
    f_name: str
    l_name: str
    date_of_birth: date
    airline_name: str
    phone_numbers: list[str] = []
    emails: list[EmailStr] = []


class LoginRequest(BaseModel):
    username: str  # email for customers, username for staff
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_type: str
    username: str


class CustomerOut(BaseModel):
    email: str
    name: str
    city: str | None = None

    model_config = {"from_attributes": True}


class StaffOut(BaseModel):
    username: str
    f_name: str
    l_name: str
    airline_name: str | None = None

    model_config = {"from_attributes": True}
