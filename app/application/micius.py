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
    
    def get_quantum_system(self, session_id: str, system_id: str) -> QuantumSystem | None:
        return self.storage_repository.get_quantum_system(session_id, system_id)
    
    def transfer_qubit(self, session_id: str, qubit_id: str, new_owner: str) -> Qubit | None:
        session = self.get_session(session_id)
        if session is None:
            return None
        _qubit: Qubit | None = None
        for system in session.systems:
            for qubit in system.qubits:
                if qubit.id == qubit_id:
                    qubit.owner = new_owner
                    _qubit = qubit
                    break
        if _qubit is None:
            return None
        return self.storage_repository.transfer_qubit(session_id, _qubit.id, new_owner)
