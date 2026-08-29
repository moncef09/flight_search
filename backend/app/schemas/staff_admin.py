from pydantic import BaseModel, Field


class AirportCreate(BaseModel):
    airport_id: str
    name: str
    city: str
    country: str


class AirportOut(AirportCreate):
    model_config = {"from_attributes": True}


class AirplaneCreate(BaseModel):
    id: str
    num_seats: int = Field(gt=0)
    manufacturing_co: str


class AirplaneOut(AirplaneCreate):
    airline_name: str

    model_config = {"from_attributes": True}


class SalesReport(BaseModel):
    total_tickets: int
    monthly_sales: list[dict]


class PassengerOut(BaseModel):
    name: str
    passport_number: str | None = None
