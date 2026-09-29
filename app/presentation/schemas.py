from pydantic import BaseModel
from qiskit import QuantumCircuit


class QubitDto(BaseModel):
    id: str
    owner: str


class CreateSystemRequest(BaseModel):
    qubits: list[QubitDto]


class CreateSystemResponse(BaseModel):
    system_id: str
    qubits: list[QubitDto]

class TransferQubitRequest(BaseModel):
    new_owner: str

class CreateJobRequest(BaseModel):
    caller: str
    circuit: str
    qubit_mapping: dict[int, str]
    shots: int