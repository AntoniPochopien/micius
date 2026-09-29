from app.application.micius_qiskit_aer import MiciusQiskitAer
from app.domain.exceptions import SystemNotFoundError
from app.domain.job import Job
from app.domain.qubit import Qubit
from app.domain.quantum_system import QuantumSystem
from app.domain.session import Session
from app.infrastructure.storage_repository import StorageRepository


class Micius:
    def __init__(self, storage_repository: StorageRepository):
        self.storage_repository = storage_repository

    def create_session(self) -> Session:
        return self.storage_repository.create_session()

    def get_session(self, session_id: str) -> Session | None:
        return self.storage_repository.get_session(session_id)

    def create_quantum_system(self, session_id: str, qubits: list[Qubit]) -> QuantumSystem | None:
        return self.storage_repository.create_quantum_system(session_id, qubits)
    
    def get_quantum_system(self, session_id: str, quantum_system_id: str) -> QuantumSystem | None:
        return self.storage_repository.get_quantum_system(session_id, quantum_system_id)
    
    def transfer_qubit(self, session_id: str, qubit_id: str, new_owner: str) -> Qubit | None:
        return self.storage_repository.transfer_qubit(session_id, qubit_id, new_owner)

    def create_job(self, session_id: str, job: Job) -> dict[str, int]:
        system = self.get_quantum_system(session_id, job.quantum_system_id)
        if system is None:
            raise SystemNotFoundError(f"System '{job.quantum_system_id}' not found")
        return MiciusQiskitAer().execute(job, system)