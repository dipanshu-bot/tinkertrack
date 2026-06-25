from fastapi import FastAPI

app = FastAPI(
    title="TinkerTrack",
    description="Shared Resource Management System",
    version="1.0.0",
)


@app.get("/")
def home():
    return {"message": "Welcome to TinkerTrack"}


@app.get("/health")
def health():
    return {"status": "healthy"}
