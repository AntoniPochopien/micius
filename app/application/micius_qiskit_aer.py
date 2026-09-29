from qiskit import QuantumCircuit

from app.domain.job import Job
from app.domain.quantum_system import QuantumSystem


class MiciusQiskitAer:
    """Executes jobs in submit order against a shared joint statevector.

    Unitaries evolve the system state in place. Measurements collapse it and
    return counts keyed by caller. Ownership is enforced per instruction.
    """

    def execute(
        self,
        jobs: list[Job],
        quantum_system: QuantumSystem,
    ) -> dict[str, dict[str, int]]:
        results: dict[str, dict[str, int]] = {}

        for job in jobs:
            results.setdefault(job.caller, {})
            job_counts = self._execute_job(job, quantum_system)
            for bitstring, count in job_counts.items():
                results[job.caller][bitstring] = (
                    results[job.caller].get(bitstring, 0) + count
                )

        return results

    def _execute_job(self, job: Job, system: QuantumSystem) -> dict[str, int]:
        owned = self._owned_circuit_to_system(job, system)
        if len(owned) == 0:
            return {}

        unitary = QuantumCircuit(len(system.qubits))
        # (system_qubit_index, clbit_index | None)
        measures: list[tuple[int, int | None]] = []

        for instruction in job.circuit.data:
            circuit_indexes = [
                job.circuit.find_bit(qubit).index for qubit in instruction.qubits
            ]
            if len(circuit_indexes) == 0:
                continue
            if any(index not in owned for index in circuit_indexes):
                continue

            system_indexes = [owned[index] for index in circuit_indexes]
            operation = instruction.operation

            if operation.name == "measure":
                clbit_index = None
                if len(instruction.clbits) > 0:
                    clbit_index = job.circuit.find_bit(instruction.clbits[0]).index
                measures.append((system_indexes[0], clbit_index))
                continue

            if operation.name in ("barrier", "delay", "reset"):
                continue

            unitary.append(operation, system_indexes)

        if len(unitary.data) > 0:
            system.state = system.state.evolve(unitary)

        if len(measures) == 0:
            return {}

        measures_sorted = sorted(
            measures,
            key=lambda item: item[1] if item[1] is not None else 0,
        )
        qargs = [system_index for system_index, _ in measures_sorted]
        shots = max(job.shots, 1)

        if shots == 1:
            bitstring, system.state = system.state.measure(qargs)
            return {str(bitstring): 1}

        pre_measure = system.state.copy()
        sampled = pre_measure.sample_counts(shots, qargs=qargs)
        _, system.state = pre_measure.measure(qargs)
        return {str(bitstring): int(count) for bitstring, count in sampled.items()}

    def _owned_circuit_to_system(
        self,
        job: Job,
        system: QuantumSystem,
    ) -> dict[int, int]:
        owned: dict[int, int] = {}

        for circuit_index, qubit_id in job.owned_qubits_mapping.items():
            system_index = system.qubit_index(qubit_id)
            if system_index is None:
                continue
            owned[int(circuit_index)] = system_index

        return owned
