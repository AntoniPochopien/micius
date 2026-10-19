from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

from app.domain.job import Job
from app.domain.quantum_system import QuantumSystem


class MiciusQiskitAer:
    """Executes jobs in submit order against a shared joint statevector.

    Each shot replays the full job queue from |0...0⟩ so multi-party
    measurements stay correlated. Unitaries evolve the state in place within
    a shot; measurements collapse it. Ownership is enforced per instruction.
    """

    def execute(
        self,
        jobs: list[Job],
        quantum_system: QuantumSystem,
    ) -> dict[str, dict[str, int]]:
        shots = 1
        for job in jobs:
            job_shots = max(job.shots, 1)
            if job_shots > shots:
                shots = job_shots
        results: dict[str, dict[str, int]] = {}

        n_qubits = len(quantum_system.qubits)
        ground = (
            Statevector.from_label("0" * n_qubits)
            if n_qubits
            else Statevector.from_label("0")
        )

        for _ in range(shots):
            quantum_system.state = ground.copy()

            for job in jobs:
                results.setdefault(job.caller, {})
                caller_bits, _measured = self._execute_job_shot(job, quantum_system)
                if caller_bits is None:
                    continue
                results[job.caller][caller_bits] = (
                    results[job.caller].get(caller_bits, 0) + 1
                )

        return results

    def _execute_job_shot(
        self,
        job: Job,
        system: QuantumSystem,
    ) -> tuple[str | None, list[tuple[int, str]]]:
        owned = self._owned_circuit_to_system(job, system)
        if len(owned) == 0:
            return None, []

        unitary = QuantumCircuit(len(system.qubits))
        # (system_qubit_index, clbit_index | None)
        measures: list[tuple[int, int | None]] = []

        for instruction in job.circuit.data:
            circuit_indexes = []
            for qubit in instruction.qubits:
                circuit_indexes.append(job.circuit.find_bit(qubit).index)
            if len(circuit_indexes) == 0:
                continue

            all_owned = True
            for index in circuit_indexes:
                if index not in owned:
                    all_owned = False
                    break
            if not all_owned:
                continue

            system_indexes = []
            for index in circuit_indexes:
                system_indexes.append(owned[index])
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
            return None, []

        measures_sorted = sorted(measures, key=_measure_sort_key)
        qargs = []
        for system_index, _ in measures_sorted:
            qargs.append(system_index)
        bitstring, system.state = system.state.measure(qargs)
        bits = str(bitstring)
        # Qiskit bitstrings are little-endian over qargs (qargs[0] = rightmost).
        measured = []
        for offset, system_index in enumerate(qargs):
            measured.append((system_index, bits[len(bits) - 1 - offset]))
        return bits, measured

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


def _measure_sort_key(item: tuple[int, int | None]) -> int:
    clbit_index = item[1]
    if clbit_index is not None:
        return clbit_index
    return 0
