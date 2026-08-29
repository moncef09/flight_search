from fastapi import APIRouter

from app.deps import DbSession
from app.schemas.auth import CustomerRegister, LoginRequest, StaffRegister, TokenResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register/customer", status_code=201)
def register_customer(payload: CustomerRegister, db: DbSession):
    AuthService(db).register_customer(payload)
    return {"message": "Registered successfully"}


@router.post("/register/staff", status_code=201)
def register_staff(payload: StaffRegister, db: DbSession):
    AuthService(db).register_staff(payload)
    return {"message": "Registered successfully"}


@router.post("/login/customer", response_model=TokenResponse)
def login_customer(payload: LoginRequest, db: DbSession):
    return AuthService(db).login_customer(payload.username, payload.password)


@router.post("/login/staff", response_model=TokenResponse)
def login_staff(payload: LoginRequest, db: DbSession):
    return AuthService(db).login_staff(payload.username, payload.password)
