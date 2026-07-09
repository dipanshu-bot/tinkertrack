from fastapi import FastAPI
from sqlalchemy import text

from app.database.database import engine
from app.database.base import Base
from app.routers.user import router as user_router
from app.routers.auth import router as auth_router
from app.routers.resource import router as resource_router

# Create database tables
# Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TinkerTrack",
    description="Shared Resource Management System",
    version="1.0.0",
)

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(resource_router)


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
