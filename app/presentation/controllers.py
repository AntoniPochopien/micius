import base64
import io
import uuid

from fastapi import APIRouter, HTTPException
from qiskit import qpy

from app.application.micius import Micius
from app.domain.exceptions import QubitOwnershipError, SystemNotFoundError
from app.domain.job import Job
from app.domain.qubit import Qubit
from app.infrastructure.storage_repository import StorageRepository
from app.presentation.schemas import CreateJobRequest, CreateSystemRequest, CreateSystemResponse, QubitDto, TransferQubitRequest

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

@router.post("/sessions/{session_id}/systems/{quantum_system_id}/jobs")
def create_job(session_id: str, quantum_system_id: str, request: CreateJobRequest):
    circuit_bytes = base64.b64decode(request.circuit)
    buffer = io.BytesIO(circuit_bytes)
    circuits = qpy.load(buffer)
    circuit = circuits[0] if isinstance(circuits, list) else circuits

    try:
        return micius.create_job(
            session_id,
            Job(
                id=uuid.uuid4().hex,
                quantum_system_id=quantum_system_id,
                caller=request.caller,
                circuit=circuit,
                qubit_mapping=request.qubit_mapping,
                shots=request.shots,
            ),
        )
    except SystemNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except QubitOwnershipError as e:
        raise HTTPException(status_code=403, detail=str(e)) from e