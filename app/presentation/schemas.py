from pydantic import BaseModel


class QubitDto(BaseModel):
    id: str
    owner: str


class CreateSystemRequest(BaseModel):
    qubits: list[QubitDto]


class CreateSystemResponse(BaseModel):
    system_id: str
    qubits: list[QubitDto]
