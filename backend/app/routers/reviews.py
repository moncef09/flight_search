from fastapi import APIRouter

from app.deps import CurrentCustomer, CurrentStaff, DbSession
from app.schemas.review import RatableFlightOut, ReviewCreate, StaffReviewSummary
from app.services.review_service import ReviewService

router = APIRouter(prefix="/reviews", tags=["reviews"])


@router.get("/ratable", response_model=list[RatableFlightOut])
def ratable_flights(db: DbSession, customer: CurrentCustomer):
    return ReviewService(db).ratable_flights_for(customer.username)


@router.post("", status_code=201)
def submit_review(payload: ReviewCreate, db: DbSession, customer: CurrentCustomer):
    ReviewService(db).submit(customer.username, payload)
    return {"message": "Thank you for your rating!"}


@router.get("/staff/summary", tags=["staff"], response_model=StaffReviewSummary)
def staff_review_summary(db: DbSession, staff: CurrentStaff):
    return ReviewService(db).staff_summary(staff.airline)
