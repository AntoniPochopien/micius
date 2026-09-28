from app.infrastructure.storage_repository import StorageRepository
from main import app
from fastapi import Request
from app.application.micius import Micius

micius = Micius(StorageRepository())

@app.get("/health")
def read_root():
    return {"status": "System is healthy"}

@app.post("/session")
def create_session(request: Request):
    sessions_id = micius.create_session()
    return {"session_id": sessions_id}

@app.get("/session/{session_id}")
def get_session(session_id: str):
    return micius.get_session(session_id)