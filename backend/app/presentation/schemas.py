from pydantic import BaseModel


class QubitDto(BaseModel):
    id: str
    owner: str


class CreateQuantumSystemRequest(BaseModel):
    qubits: list[QubitDto]


class CreateSystemResponse(BaseModel):
    qubits: list[QubitDto]


class TransferQubitRequest(BaseModel):
    new_owner: str


class CreateJobRequest(BaseModel):
    caller: str
    circuit: str
    qubit_mapping: dict[int, str]
    shots: int


class CreateJobResponse(BaseModel):
    id: str
    caller: str
    qubit_mapping: dict[int, str]
    shots: int


class ExecuteResponse(BaseModel):
    results: dict[str, dict[str, int]]