from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

from app.domain.job import Job
from app.domain.quantum_system import QuantumSystem


class MiciusQiskitAer:
    def execute(self, jobs: list[Job], quantum_system: QuantumSystem) -> dict[str, int]:
        qubits_by_id = {}
        for qubit in quantum_system.qubits:
            qubits_by_id[qubit.id] = qubit

        simulator = AerSimulator()
        counts = {}

        for job in jobs:
            caller_qubit_indexes = set()

            for i in job.qubit_mapping:
                qubit_id = job.qubit_mapping[i]
                qubit = qubits_by_id.get(qubit_id)

                if qubit is None:
                    continue
                if qubit.owner != job.caller:
                    continue

                caller_qubit_indexes.add(i)

            if len(caller_qubit_indexes) == 0:
                continue

            circuit = self._circuit_for_caller_qubits(job.circuit, caller_qubit_indexes)
            result = simulator.run(circuit, shots=job.shots).result()
            job_counts = result.get_counts()

            for bitstring in job_counts:
                count = job_counts[bitstring]
                if bitstring in counts:
                    counts[bitstring] = counts[bitstring] + count
                else:
                    counts[bitstring] = count

        return counts

    def _circuit_for_caller_qubits(
        self,
        circuit: QuantumCircuit,
        caller_qubit_indexes: set[int],
    ) -> QuantumCircuit:
        filtered = QuantumCircuit(circuit.num_qubits, circuit.num_clbits)

        for instruction in circuit.data:
            qubit_indexes = []
            for qubit in instruction.qubits:
                index = circuit.find_bit(qubit).index
                qubit_indexes.append(index)

            if len(qubit_indexes) == 0:
                continue

            uses_only_caller_qubits = True
            for index in qubit_indexes:
                if index not in caller_qubit_indexes:
                    uses_only_caller_qubits = False
                    break

            if uses_only_caller_qubits:
                filtered.append(instruction)

        return filtered
