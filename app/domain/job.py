from qiskit import QuantumCircuit


class Job:
    def __init__(
        self,
        id: str,
        caller: str,
        circuit: QuantumCircuit,
        qubit_mapping: dict[int, str],
        shots: int,
    ):
        self.id = id
        self.caller = caller
        self.circuit = circuit
        self.qubit_mapping = qubit_mapping
        self.shots = shots
