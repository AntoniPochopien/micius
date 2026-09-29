from qiskit.quantum_info import Statevector

from app.domain.qubit import Qubit


class QuantumSystem:
    def __init__(self, id: str, qubits: list[Qubit]):
        self.id = id
        self.qubits = qubits
        self.state = Statevector.from_label("0" * len(qubits)) if qubits else Statevector.from_label("0")

    def qubit_index(self, qubit_id: str) -> int | None:
        for index, qubit in enumerate(self.qubits):
            if qubit.id == qubit_id:
                return index
        return None
