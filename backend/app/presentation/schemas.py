from pydantic import BaseModel


class QubitDto(BaseModel):
    id: str
    owner: str


class JobSummaryDto(BaseModel):
    id: str
    caller: str
    has_measure: bool


class SessionResponse(BaseModel):
    id: str
    qubits: list[QubitDto] = []
    jobs: list[JobSummaryDto] = []
    executed: bool = False


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
