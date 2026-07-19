from fastapi import FastAPI
from sqlalchemy import text
from fastapi.middleware.cors import CORSMiddleware

from app.database.database import engine
from app.database.base import Base
from app.routers.user import router as user_router
from app.routers.auth import router as auth_router
from app.routers.resource import router as resource_router
from app.routers.borrow import router as borrow_router
from app.routers.dashboard import router as dashboard_router
from app.routers.reservation import router as reservation_router

# Create database tables
# Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TinkerTrack API",
    version="1.0.0",
    description="""
Inventory Management System

Features:

- JWT Authentication
- Role Based Authorization
- Resource Management
- Borrow & Return Resources
- Dashboard Statistics
- Search & Pagination
""",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5173",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(resource_router)
app.include_router(borrow_router)
app.include_router(dashboard_router)
app.include_router(reservation_router)


@app.get("/")
def home():
    return {"message": "Welcome to TinkerTrack"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/db-check")
def database_check():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {"database": "Connected Successfully"}

    except Exception as e:
        return {"database": "Connection Failed", "error": str(e)}
