from qiskit import QuantumCircuit


class Job:
    def __init__(
        self,
        id: str,
        caller: str,
        circuit: QuantumCircuit,
        qubit_mapping: dict[int, str],
        shots: int,
        owned_qubits_mapping: dict[int, str] | None = None,
    ):
        self.id = id
        self.caller = caller
        self.circuit = circuit
        self.qubit_mapping = qubit_mapping
        self.shots = shots
        self.owned_qubits_mapping = (
            owned_qubits_mapping if owned_qubits_mapping is not None else dict(qubit_mapping)
        )
