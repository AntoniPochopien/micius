from app.domain.qubit import Qubit


class QuantumSystem:
    def __init__(self, id: str, qubits: list[Qubit]):
        self.id = id
        self.qubits = qubits
