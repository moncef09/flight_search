from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.db.base import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login/customer", auto_error=False)


class CurrentUser:
    def __init__(self, username: str, user_type: str, airline: str | None = None):
        self.username = username
        self.user_type = user_type
        self.airline = airline


def get_current_user(token: Annotated[str | None, Depends(oauth2_scheme)]) -> CurrentUser:
    credentials_error = HTTPException(
        status.HTTP_401_UNAUTHORIZED,
        "Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not token:
        raise credentials_error

    payload = decode_access_token(token)
    if not payload or "sub" not in payload:
        raise credentials_error

    return CurrentUser(
        username=payload["sub"], user_type=payload.get("user_type", ""), airline=payload.get("airline")
    )


def require_customer(user: Annotated[CurrentUser, Depends(get_current_user)]) -> CurrentUser:
    if user.user_type != "customer":
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Customer account required")
    return user


def require_staff(user: Annotated[CurrentUser, Depends(get_current_user)]) -> CurrentUser:
    if user.user_type != "staff":
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Staff account required")
    return user


DbSession = Annotated[Session, Depends(get_db)]
CurrentCustomer = Annotated[CurrentUser, Depends(require_customer)]
CurrentStaff = Annotated[CurrentUser, Depends(require_staff)]
