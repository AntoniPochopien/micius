from fastapi import APIRouter

from app.application.micius import Micius
from app.infrastructure.storage_repository import StorageRepository

router = APIRouter()
micius = Micius(StorageRepository())


@router.get("/health")
def read_root():
    return {"status": "System is healthy"}


@router.post("/session")
def create_session():
    session = micius.create_session()
    return session


@router.get("/session/{session_id}")
def get_session(session_id: str):
    return micius.get_session(session_id)
