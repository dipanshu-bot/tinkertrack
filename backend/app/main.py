from fastapi import FastAPI
from sqlalchemy import text

from app.database.database import engine

app = FastAPI(title="TinkerTrack", version="1.0")


@app.get("/")
def home():
    return {"message": "Welcome to TinkerTrack"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/db-check")
def db_check():

    try:

        with engine.connect() as connection:

            connection.execute(text("SELECT 1"))

        return {"database": "Connected Successfully"}

    except Exception as e:

        return {"database": "Connection Failed", "error": str(e)}
