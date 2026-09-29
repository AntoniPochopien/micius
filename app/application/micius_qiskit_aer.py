from qiskit_aer import AerSimulator

from app.domain.exceptions import QubitOwnershipError
from app.domain.job import Job
from app.domain.quantum_system import QuantumSystem


class MiciusQiskitAer:
    def execute(self, job: Job, quantum_system: QuantumSystem) -> dict[str, int]:
        qubits_by_id = {qubit.id: qubit for qubit in quantum_system.qubits}
        for qubit_id in job.qubit_mapping.values():
            qubit = qubits_by_id.get(qubit_id)
            if qubit is None:
                raise QubitOwnershipError(f"Qubit '{qubit_id}' not found in quantum system")
            if qubit.owner != job.caller:
                raise QubitOwnershipError(
                    f"Caller '{job.caller}' does not own qubit '{qubit_id}' (owner: '{qubit.owner}')"
                )

        backend = AerSimulator()
        result = backend.run(job.circuit, shots=job.shots).result()

        return result.get_counts()
