from fastapi import APIRouter, HTTPException

from app.application.micius import Micius
from app.domain.qubit import Qubit
from app.infrastructure.storage_repository import StorageRepository
from app.presentation.schemas import CreateSystemRequest, CreateSystemResponse, QubitDto, TransferQubitRequest

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
    session = micius.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


@router.post("/sessions/{session_id}/systems", response_model=CreateSystemResponse)
def create_quantum_system(session_id: str, request: CreateSystemRequest):
    qubits = [Qubit(id=q.id, owner=q.owner) for q in request.qubits]
    system = micius.create_quantum_system(session_id, qubits)
    if system is None:
        raise HTTPException(status_code=404, detail="Session not found")

    return CreateSystemResponse(
        system_id=system.id,
        qubits=[QubitDto(id=q.id, owner=q.owner) for q in system.qubits],
    )


@router.get("/sessions/{session_id}/systems/{system_id}")
def get_quantum_system(session_id: str, system_id: str):
    system = micius.get_quantum_system(session_id, system_id)
    if system is None:
        raise HTTPException(status_code=404, detail="System not found")
    return system

@router.post("/sessions/{session_id}/qubits/{qubit_id}/transfer")
def transfer_qubit(session_id: str, qubit_id: str, request: TransferQubitRequest):
    qubit = micius.transfer_qubit(session_id, qubit_id, request.new_owner)
    if qubit is None:
        raise HTTPException(status_code=404, detail="Qubit not found")
    return qubit