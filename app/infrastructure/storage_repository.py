import uuid

from app.domain.qubit import Qubit
from app.domain.quantum_system import QuantumSystem
from app.domain.session import Session


class StorageRepository:
    def __init__(self):
        #TODO: Use a database instead of a dictionary
        self.storage: dict[str, Session] = {}

    def create_session(self) -> Session:
        session_id = str(uuid.uuid4())
        session = Session(session_id)
        self.storage[session_id] = session
        return session

    def get_session(self, session_id: str) -> Session | None:
        return self.storage.get(session_id)

    def create_quantum_system(self, session_id: str, qubits: list[Qubit]) -> QuantumSystem | None:
        session = self.get_session(session_id)
        if session is None:
            return None

        system_id = str(uuid.uuid4())
        system = QuantumSystem(system_id, qubits)
        session.systems.append(system)
        return system
    
    def get_quantum_system(self, session_id: str, system_id: str) -> QuantumSystem | None:
        session = self.get_session(session_id)
        if session is None:
            return None
        for system in session.systems:
            if system.id == system_id:
                return system
        return None

    def transfer_qubit(self, session_id: str, qubit_id: str, new_owner: str) -> Qubit | None:
        session = self.get_session(session_id)
        if session is None:
            return None
        for system in session.systems:
            for qubit in system.qubits:
                if qubit.id == qubit_id:
                    qubit.owner = new_owner
                    return qubit
        return None