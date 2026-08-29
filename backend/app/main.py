from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routers import auth, bookings, flights, reviews, staff_admin

app = FastAPI(
    title="Flight Search API",
    description="FastAPI backend for the Flight Search app (search, booking, reviews, staff ops).",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(flights.router)
app.include_router(bookings.router)
app.include_router(reviews.router)
app.include_router(staff_admin.router)


@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok"}
